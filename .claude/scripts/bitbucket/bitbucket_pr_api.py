# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "atlassian-python-api>=3.41.0",
#   "python-dotenv>=1.0.0",
#   "click>=8.0.0",
#   "requests>=2.28.0",
# ]
# ///

"""
Bitbucket Pull Request Creation Script

This script handles pull request creation as part of the hybrid Bitbucket API + MCP integration.
It manages branch creation, git operations, PR creation, and reviewer assignment.

Usage:
    uv run bitbucket_pr_api.py create-pr [destination] [ticket] [options]
    
Examples:
    uv run bitbucket_pr_api.py create-pr main 123 --reviewers user1,user2
    uv run bitbucket_pr_api.py create-pr development 456 --draft
"""

import os
import sys
import json
import logging
import subprocess
import re
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime

import click

# Import utilities from the same directory
sys.path.append(str(Path(__file__).parent))
try:
    from bitbucket_utils import (
        BitbucketClient, create_bitbucket_client, get_workspace_and_repo,
        format_error_message, output_json, output_error, setup_logging,
        BitbucketError, BitbucketAuthError, GitRemoteInfo, parse_git_remote
    )
except ImportError as e:
    print(f"Error importing utilities: {e}", file=sys.stderr)
    print("Ensure bitbucket_utils.py is in the same directory", file=sys.stderr)
    sys.exit(1)


@dataclass
class PRCreationResult:
    """Result of PR creation operation."""
    success: bool
    pr_id: Optional[int] = None
    pr_url: Optional[str] = None
    branch_name: Optional[str] = None
    reviewers_added: Optional[List[str]] = None
    error_message: Optional[str] = None
    is_production: bool = False


@dataclass 
class GitStatus:
    """Current git repository status."""
    current_branch: str
    staged_files: List[str]
    unstaged_files: List[str]
    untracked_files: List[str]
    has_changes: bool
    recent_commits: List[str]


class GitOperationError(Exception):
    """Git operation specific errors."""
    pass


def run_git_command(command: List[str], check: bool = True) -> subprocess.CompletedProcess:
    """
    Run a git command safely.
    
    Args:
        command: Git command as list of strings
        check: Whether to check return code
        
    Returns:
        CompletedProcess result
        
    Raises:
        GitOperationError: If git command fails
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=check,
            cwd=Path.cwd()
        )
        return result
    except subprocess.CalledProcessError as e:
        raise GitOperationError(f"Git command failed: {' '.join(command)}\nError: {e.stderr}")
    except FileNotFoundError:
        raise GitOperationError("Git not found. Please ensure git is installed and in PATH.")


def get_git_status() -> GitStatus:
    """
    Get comprehensive git repository status.
    
    Returns:
        GitStatus with current repository state
        
    Raises:
        GitOperationError: If git operations fail
    """
    logger = logging.getLogger("bitbucket_api")
    
    # Get current branch
    result = run_git_command(["git", "branch", "--show-current"])
    current_branch = result.stdout.strip()
    
    # Get git status (porcelain format for parsing)
    result = run_git_command(["git", "status", "--porcelain"])
    status_lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
    
    staged_files = []
    unstaged_files = []
    untracked_files = []
    
    for line in status_lines:
        if not line.strip():
            continue
            
        status_code = line[:2]
        filename = line[3:].strip()
        
        # First character: staged status, second character: unstaged status
        if status_code[0] in 'MADRC':  # Modified, Added, Deleted, Renamed, Copied
            staged_files.append(filename)
        if status_code[1] in 'MD':  # Modified, Deleted
            unstaged_files.append(filename)
        if status_code[0] == '?' and status_code[1] == '?':  # Untracked
            untracked_files.append(filename)
    
    # Get recent commits (for PR description)
    result = run_git_command(["git", "log", "--oneline", "-5"])
    recent_commits = result.stdout.strip().split('\n') if result.stdout.strip() else []
    
    has_changes = bool(staged_files or unstaged_files or untracked_files)
    
    logger.debug(f"Git status - Branch: {current_branch}, Changes: {has_changes}")
    
    return GitStatus(
        current_branch=current_branch,
        staged_files=staged_files,
        unstaged_files=unstaged_files,
        untracked_files=untracked_files,
        has_changes=has_changes,
        recent_commits=recent_commits
    )


def create_branch_name(destination_branch: str, ticket_number: str) -> str:
    """
    Create branch name following naming convention.
    
    Args:
        destination_branch: Target branch name
        ticket_number: Ticket/issue number
        
    Returns:
        Branch name in format: {destination}-{ticket}
    """
    # Sanitize inputs
    destination_clean = re.sub(r'[^a-zA-Z0-9-_]', '-', destination_branch)
    ticket_clean = re.sub(r'[^a-zA-Z0-9-_]', '-', ticket_number)
    
    branch_name = f"{destination_clean}-{ticket_clean}"
    
    # Ensure branch name is valid (no consecutive dashes, no leading/trailing dashes)
    branch_name = re.sub(r'-+', '-', branch_name)
    branch_name = branch_name.strip('-')
    
    return branch_name


def create_and_checkout_branch(branch_name: str) -> bool:
    """
    Create and checkout a new branch.
    
    Args:
        branch_name: Name of the branch to create
        
    Returns:
        True if successful, False otherwise
        
    Raises:
        GitOperationError: If git operations fail
    """
    logger = logging.getLogger("bitbucket_api")
    
    # Check if branch already exists
    try:
        run_git_command(["git", "rev-parse", "--verify", branch_name], check=False)
        logger.info(f"Branch {branch_name} already exists, checking out")
        run_git_command(["git", "checkout", branch_name])
        return True
    except GitOperationError:
        pass  # Branch doesn't exist, create it
    
    logger.info(f"Creating and checking out new branch: {branch_name}")
    
    # Create and checkout new branch
    run_git_command(["git", "checkout", "-b", branch_name])
    
    logger.info(f"Successfully created and checked out branch: {branch_name}")
    return True


def push_branch_to_remote(branch_name: str) -> bool:
    """
    Push branch to remote with upstream tracking.
    
    Args:
        branch_name: Name of the branch to push
        
    Returns:
        True if successful, False otherwise
        
    Raises:
        GitOperationError: If git operations fail
    """
    logger = logging.getLogger("bitbucket_api")
    
    logger.info(f"Pushing branch {branch_name} to remote")
    
    # Push with upstream tracking
    run_git_command(["git", "push", "--set-upstream", "origin", branch_name])
    
    logger.info(f"Successfully pushed branch: {branch_name}")
    return True


def parse_reviewers(reviewers_input: Optional[str]) -> List[str]:
    """
    Parse reviewer list from command input.
    
    Args:
        reviewers_input: Comma-separated list of reviewers (may include @mentions)
        
    Returns:
        List of cleaned reviewer usernames
    """
    if not reviewers_input:
        return []
    
    reviewers = []
    for reviewer in reviewers_input.split(','):
        reviewer = reviewer.strip()
        # Remove @ mention if present
        if reviewer.startswith('@'):
            reviewer = reviewer[1:]
        
        if reviewer:  # Only add non-empty reviewers
            reviewers.append(reviewer)
    
    return reviewers


def generate_pr_description(git_status: GitStatus, ticket_number: str) -> str:
    """
    Generate PR description from git status and ticket information.
    
    Args:
        git_status: Current git repository status
        ticket_number: Associated ticket number
        
    Returns:
        Formatted PR description
    """
    description_parts = [
        f"## Changes for Ticket {ticket_number}",
        "",
    ]
    
    # Add changes summary if available
    if git_status.has_changes or git_status.staged_files:
        description_parts.extend([
            "### Files Changed:",
            ""
        ])
        
        all_changed_files = set(git_status.staged_files + git_status.unstaged_files)
        for file in sorted(all_changed_files):
            description_parts.append(f"- `{file}`")
        
        description_parts.append("")
    
    # Add recent commits
    if git_status.recent_commits:
        description_parts.extend([
            "### Recent Commits:",
            ""
        ])
        
        for commit in git_status.recent_commits[:3]:  # Show last 3 commits
            description_parts.append(f"- {commit}")
        
        description_parts.append("")
    
    description_parts.extend([
        "### Review Checklist:",
        "- [ ] Code follows project standards",
        "- [ ] Tests are included and passing",
        "- [ ] Documentation is updated if needed",
        "- [ ] No breaking changes without discussion",
        "",
        f"**Ticket Reference:** {ticket_number}"
    ])
    
    return "\n".join(description_parts)


def is_production_branch(branch_name: str) -> bool:
    """
    Determine if a branch is considered a production branch.
    
    Args:
        branch_name: Branch name to check
        
    Returns:
        True if it's a production branch
    """
    production_branches = {
        'main', 'master', 'production', 'release',
        'prod', 'live', 'stable'
    }
    
    return branch_name.lower().strip() in production_branches


def create_pull_request_with_client(
    client: BitbucketClient,
    workspace: str,
    repository: str,
    source_branch: str,
    destination_branch: str,
    title: str,
    description: str,
    reviewers: List[str]
) -> Dict[str, Any]:
    """
    Create pull request using Bitbucket client.
    
    Args:
        client: Configured BitbucketClient
        workspace: Bitbucket workspace name
        repository: Repository name
        source_branch: Source branch name
        destination_branch: Destination branch name
        title: PR title
        description: PR description
        reviewers: List of reviewer usernames
        
    Returns:
        PR creation result dictionary
    """
    logger = logging.getLogger("bitbucket_api")
    
    logger.info(f"Creating PR: {source_branch} -> {destination_branch}")
    logger.info(f"Title: {title}")
    if reviewers:
        logger.info(f"Reviewers: {', '.join(reviewers)}")
    
    try:
        pr_result = client.create_pull_request(
            workspace=workspace,
            repo_slug=repository,
            source_branch=source_branch,
            destination_branch=destination_branch,
            title=title,
            description=description,
            reviewers=reviewers
        )
        
        return pr_result
        
    except Exception as e:
        logger.error(f"Failed to create PR: {e}")
        raise


@click.group()
def cli():
    """Bitbucket PR creation utilities."""
    pass


@cli.command("create-pr")
@click.argument("destination_branch")
@click.argument("ticket_number") 
@click.option("--reviewers", help="Comma-separated list of reviewer usernames")
@click.option("--draft", is_flag=True, help="Create as draft PR")
@click.option("--title", help="Custom PR title")
@click.option("--no-push", is_flag=True, help="Skip pushing branch to remote")
def create_pr_command(
    destination_branch: str,
    ticket_number: str,
    reviewers: Optional[str] = None,
    draft: bool = False,
    title: Optional[str] = None,
    no_push: bool = False
):
    """
    Create a pull request with branch management.
    
    DESTINATION_BRANCH: Target branch for the PR (e.g., 'main', 'development')
    TICKET_NUMBER: Ticket/issue number for branch naming
    """
    logger = setup_logging()
    
    try:
        # Get git status
        git_status = get_git_status()
        logger.info(f"Current branch: {git_status.current_branch}")
        
        # Create branch name
        branch_name = create_branch_name(destination_branch, ticket_number)
        logger.info(f"Target branch name: {branch_name}")
        
        # Get workspace and repository info
        workspace, repository = get_workspace_and_repo()
        logger.info(f"Working with {workspace}/{repository}")
        
        # Create and checkout branch if not current
        if git_status.current_branch != branch_name:
            create_and_checkout_branch(branch_name)
        else:
            logger.info(f"Already on target branch: {branch_name}")
        
        # Push branch to remote unless disabled
        if not no_push:
            push_branch_to_remote(branch_name)
        
        # Parse reviewers
        reviewer_list = parse_reviewers(reviewers)
        
        # Generate PR title and description
        pr_title = title or f"{repository} {branch_name}: {ticket_number}"
        pr_description = generate_pr_description(git_status, ticket_number)
        
        # Create Bitbucket client and PR
        client = create_bitbucket_client()
        pr_result = create_pull_request_with_client(
            client=client,
            workspace=workspace,
            repository=repository,
            source_branch=branch_name,
            destination_branch=destination_branch,
            title=pr_title,
            description=pr_description,
            reviewers=reviewer_list
        )
        
        # Extract PR information
        pr_id = pr_result.get('id')
        pr_url = pr_result.get('links', {}).get('html', {}).get('href', '')
        
        # Determine if this is a production branch
        is_prod = is_production_branch(destination_branch)
        
        # Output success result
        result = PRCreationResult(
            success=True,
            pr_id=pr_id,
            pr_url=pr_url,
            branch_name=branch_name,
            reviewers_added=reviewer_list,
            is_production=is_prod
        )
        
        output_json({
            "success": True,
            "pr": {
                "id": pr_id,
                "url": pr_url,
                "title": pr_title,
                "source_branch": branch_name,
                "destination_branch": destination_branch,
                "reviewers": reviewer_list,
                "is_draft": draft,
                "is_production": is_prod
            },
            "git": {
                "branch_created": branch_name,
                "pushed_to_remote": not no_push,
                "has_changes": git_status.has_changes
            },
            "next_steps": [
                f"✅ Pull request created: {pr_url}",
                f"🔄 Branch pushed: {branch_name}",
                "📋 Code review ticket will be created by command if production branch" if is_prod else None,
                f"👥 Reviewers notified: {', '.join(reviewer_list)}" if reviewer_list else None
            ]
        })
        
    except GitOperationError as e:
        output_error(f"Git operation failed: {e}", "create_pr")
        sys.exit(1)
    except BitbucketError as e:
        output_error(format_error_message(e, "PR creation"), "create_pr")
        sys.exit(1)
    except Exception as e:
        output_error(f"Unexpected error: {e}", "create_pr")
        sys.exit(1)


@cli.command("check-branch")
@click.argument("destination_branch")
@click.argument("ticket_number")
def check_branch_command(destination_branch: str, ticket_number: str):
    """Check if target branch name would conflict."""
    try:
        branch_name = create_branch_name(destination_branch, ticket_number)
        git_status = get_git_status()
        
        # Check if branch exists
        try:
            run_git_command(["git", "rev-parse", "--verify", branch_name], check=False)
            branch_exists = True
        except GitOperationError:
            branch_exists = False
        
        output_json({
            "success": True,
            "branch_name": branch_name,
            "current_branch": git_status.current_branch,
            "branch_exists": branch_exists,
            "same_as_current": git_status.current_branch == branch_name,
            "has_local_changes": git_status.has_changes
        })
        
    except Exception as e:
        output_error(f"Branch check failed: {e}", "check_branch")
        sys.exit(1)


if __name__ == "__main__":
    cli()
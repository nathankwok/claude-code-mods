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
Bitbucket Pull Request Status Monitoring Script

This script handles PR status checking as part of the hybrid Bitbucket API + MCP integration.
It retrieves PR information, review status, comments, and formats output for display.

Usage:
    uv run pr_status_api.py check-status [options]
    uv run pr_status_api.py list-prs [options]
    
Examples:
    uv run pr_status_api.py check-status --pr-id 123 --comments
    uv run pr_status_api.py list-prs --all-states
"""

import os
import sys
import json
import logging
import subprocess
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict

import click

# Import utilities from the same directory
sys.path.append(str(Path(__file__).parent))
try:
    from bitbucket_utils import (
        BitbucketClient, create_bitbucket_client, get_workspace_and_repo,
        format_error_message, output_json, output_error, setup_logging,
        BitbucketError, parse_git_remote
    )
except ImportError as e:
    print(f"Error importing utilities: {e}", file=sys.stderr)
    print("Ensure bitbucket_utils.py is in the same directory", file=sys.stderr)
    sys.exit(1)


@dataclass
class ReviewStatus:
    """Status of PR reviews."""
    total_reviewers: int
    approved: List[str]
    changes_requested: List[str]
    pending: List[str]
    approval_count: int
    
    @property
    def is_approved(self) -> bool:
        """Check if PR has sufficient approvals."""
        return self.approval_count > 0 and len(self.changes_requested) == 0
    
    @property
    def summary(self) -> str:
        """Get review summary string."""
        if self.total_reviewers == 0:
            return "No reviewers"
        
        parts = []
        if self.approved:
            parts.append(f"✅ {len(self.approved)}")
        if self.changes_requested:
            parts.append(f"❌ {len(self.changes_requested)}")
        if self.pending:
            parts.append(f"⏳ {len(self.pending)}")
            
        return f"{' '.join(parts)} ({self.approval_count}/{self.total_reviewers})"


@dataclass
class PRSummary:
    """Summary of a pull request."""
    id: int
    title: str
    state: str
    author: str
    source_branch: str
    destination_branch: str
    created_on: str
    updated_on: str
    url: str
    review_status: Optional[ReviewStatus] = None
    comment_count: int = 0
    commit_count: int = 0


def get_current_branch() -> Optional[str]:
    """
    Get the current git branch.
    
    Returns:
        Current branch name or None if not in a git repository
    """
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def list_repository_prs(
    client: BitbucketClient,
    workspace: str,
    repository: str,
    state: str = "OPEN",
    limit: int = 25
) -> List[Dict[str, Any]]:
    """
    List pull requests for a repository.
    
    Args:
        client: Bitbucket client
        workspace: Workspace name
        repository: Repository name
        state: PR state filter (OPEN, MERGED, DECLINED, SUPERSEDED, or ALL)
        limit: Maximum number of PRs to retrieve
        
    Returns:
        List of PR dictionaries
    """
    logger = logging.getLogger("bitbucket_api")
    
    # Handle "ALL" state by not filtering
    if state.upper() == "ALL":
        state = None
        logger.info(f"Listing all PRs for {workspace}/{repository}")
    else:
        logger.info(f"Listing {state} PRs for {workspace}/{repository}")
    
    try:
        prs = client.list_pull_requests(
            workspace=workspace,
            repo_slug=repository,
            state=state,
            limit=limit
        )
        
        logger.info(f"Found {len(prs)} pull requests")
        return prs
        
    except Exception as e:
        logger.error(f"Failed to list PRs: {e}")
        raise


def get_detailed_pr_info(
    client: BitbucketClient,
    workspace: str,
    repository: str,
    pr_id: int
) -> Dict[str, Any]:
    """
    Get detailed information about a specific PR.
    
    Args:
        client: Bitbucket client
        workspace: Workspace name
        repository: Repository name
        pr_id: Pull request ID
        
    Returns:
        Detailed PR information
    """
    logger = logging.getLogger("bitbucket_api")
    logger.info(f"Getting detailed info for PR #{pr_id}")
    
    try:
        # Get PR details
        pr_data = client._client.get_pull_request(workspace, repository, pr_id)
        
        # Get participants (reviewers) information
        if 'participants' in pr_data:
            pr_data['reviewers'] = [
                p for p in pr_data['participants'] 
                if p.get('role') == 'REVIEWER'
            ]
        
        return pr_data
        
    except Exception as e:
        logger.error(f"Failed to get PR details: {e}")
        raise


def get_pr_comments(
    client: BitbucketClient,
    workspace: str,
    repository: str,
    pr_id: int
) -> List[Dict[str, Any]]:
    """
    Get comments for a pull request.
    
    Args:
        client: Bitbucket client
        workspace: Workspace name
        repository: Repository name
        pr_id: Pull request ID
        
    Returns:
        List of comment dictionaries
    """
    logger = logging.getLogger("bitbucket_api")
    logger.info(f"Getting comments for PR #{pr_id}")
    
    try:
        # Get PR comments
        comments_response = client._client.get_pull_request_comments(
            workspace, repository, pr_id
        )
        
        if isinstance(comments_response, dict) and 'values' in comments_response:
            comments = comments_response['values']
        else:
            comments = comments_response if isinstance(comments_response, list) else []
        
        logger.info(f"Found {len(comments)} comments")
        return comments
        
    except Exception as e:
        logger.error(f"Failed to get PR comments: {e}")
        return []


def get_pr_commits(
    client: BitbucketClient,
    workspace: str,
    repository: str,
    pr_id: int
) -> List[Dict[str, Any]]:
    """
    Get commits for a pull request.
    
    Args:
        client: Bitbucket client
        workspace: Workspace name
        repository: Repository name
        pr_id: Pull request ID
        
    Returns:
        List of commit dictionaries
    """
    logger = logging.getLogger("bitbucket_api")
    logger.info(f"Getting commits for PR #{pr_id}")
    
    try:
        # Get PR commits
        commits_response = client._client.get_pull_request_commits(
            workspace, repository, pr_id
        )
        
        if isinstance(commits_response, dict) and 'values' in commits_response:
            commits = commits_response['values']
        else:
            commits = commits_response if isinstance(commits_response, list) else []
        
        logger.info(f"Found {len(commits)} commits")
        return commits
        
    except Exception as e:
        logger.error(f"Failed to get PR commits: {e}")
        return []


def analyze_review_status(pr_data: Dict[str, Any]) -> ReviewStatus:
    """
    Analyze the review status of a pull request.
    
    Args:
        pr_data: Pull request data
        
    Returns:
        ReviewStatus object with analysis
    """
    approved = []
    changes_requested = []
    pending = []
    
    participants = pr_data.get('participants', [])
    reviewers = [p for p in participants if p.get('role') == 'REVIEWER']
    
    for reviewer in reviewers:
        user = reviewer.get('user', {})
        username = user.get('display_name', user.get('nickname', 'Unknown'))
        state = reviewer.get('state', 'pending')
        
        if state == 'approved':
            approved.append(username)
        elif state == 'changes_requested':
            changes_requested.append(username)
        else:
            pending.append(username)
    
    return ReviewStatus(
        total_reviewers=len(reviewers),
        approved=approved,
        changes_requested=changes_requested,
        pending=pending,
        approval_count=len(approved)
    )


def find_current_branch_pr(
    client: BitbucketClient,
    workspace: str,
    repository: str,
    branch: str
) -> Optional[Dict[str, Any]]:
    """
    Find PR associated with the current branch.
    
    Args:
        client: Bitbucket client
        workspace: Workspace name
        repository: Repository name
        branch: Branch name to search for
        
    Returns:
        PR data if found, None otherwise
    """
    logger = logging.getLogger("bitbucket_api")
    logger.info(f"Looking for PR with source branch: {branch}")
    
    try:
        prs = list_repository_prs(client, workspace, repository, "OPEN")
        
        for pr in prs:
            source = pr.get('source', {})
            source_branch = source.get('branch', {}).get('name', '')
            
            if source_branch == branch:
                logger.info(f"Found PR #{pr.get('id')} for branch {branch}")
                return pr
        
        logger.info(f"No PR found for branch {branch}")
        return None
        
    except Exception as e:
        logger.error(f"Failed to find PR for branch: {e}")
        return None


def format_pr_summary(pr_data: Dict[str, Any]) -> PRSummary:
    """
    Format PR data into a summary object.
    
    Args:
        pr_data: Raw PR data from API
        
    Returns:
        PRSummary object
    """
    # Extract basic information
    pr_id = pr_data.get('id', 0)
    title = pr_data.get('title', 'Untitled')
    state = pr_data.get('state', 'UNKNOWN')
    
    # Author information
    author_data = pr_data.get('author', {})
    author = author_data.get('display_name', author_data.get('nickname', 'Unknown'))
    
    # Branch information
    source = pr_data.get('source', {})
    destination = pr_data.get('destination', {})
    source_branch = source.get('branch', {}).get('name', 'unknown')
    dest_branch = destination.get('branch', {}).get('name', 'unknown')
    
    # Timestamps
    created_on = pr_data.get('created_on', '')
    updated_on = pr_data.get('updated_on', '')
    
    # URL
    links = pr_data.get('links', {})
    html_link = links.get('html', {})
    url = html_link.get('href', '')
    
    # Review status
    review_status = analyze_review_status(pr_data)
    
    # Comment count
    comment_count = pr_data.get('comment_count', 0)
    
    return PRSummary(
        id=pr_id,
        title=title,
        state=state,
        author=author,
        source_branch=source_branch,
        destination_branch=dest_branch,
        created_on=created_on,
        updated_on=updated_on,
        url=url,
        review_status=review_status,
        comment_count=comment_count
    )


def format_pr_table(pr_summaries: List[PRSummary]) -> str:
    """
    Format PR list as a table.
    
    Args:
        pr_summaries: List of PR summaries
        
    Returns:
        Formatted table string
    """
    if not pr_summaries:
        return "No pull requests found."
    
    lines = []
    lines.append("┌─────────────────────────────────────────────────────────────────────────────┐")
    
    for pr in pr_summaries:
        # Truncate title if too long
        title = pr.title[:30] + "..." if len(pr.title) > 30 else pr.title.ljust(33)
        
        # Format state
        state_display = pr.state.ljust(9)
        
        # Review status
        review_display = pr.review_status.summary if pr.review_status else "No reviews"
        
        line = f"│ #{str(pr.id).ljust(4)} │ {title} │ {state_display} │ {review_display.ljust(15)} │"
        lines.append(line)
    
    lines.append("└─────────────────────────────────────────────────────────────────────────────┘")
    
    return "\n".join(lines)


def format_pr_details(
    pr_summary: PRSummary,
    comments: Optional[List[Dict[str, Any]]] = None,
    commits: Optional[List[Dict[str, Any]]] = None
) -> str:
    """
    Format detailed PR view.
    
    Args:
        pr_summary: PR summary object
        comments: Optional list of comments
        commits: Optional list of commits
        
    Returns:
        Formatted detail string
    """
    lines = []
    
    # Header
    lines.append(f"PR #{pr_summary.id}: {pr_summary.title}")
    lines.append(f"├── Status: {pr_summary.state}")
    lines.append(f"├── Author: {pr_summary.author}")
    lines.append(f"├── Source: {pr_summary.source_branch} → {pr_summary.destination_branch}")
    
    # Review status
    if pr_summary.review_status:
        lines.append("├── Reviewers:")
        
        for reviewer in pr_summary.review_status.approved:
            lines.append(f"│   ├── ✅ {reviewer} (approved)")
        
        for reviewer in pr_summary.review_status.changes_requested:
            lines.append(f"│   ├── ❌ {reviewer} (requested changes)")
        
        for reviewer in pr_summary.review_status.pending:
            lines.append(f"│   ├── ⏳ {reviewer} (pending)")
        
        if not pr_summary.review_status.total_reviewers:
            lines.append("│   └── No reviewers assigned")
    
    # Comments summary
    if comments is not None:
        resolved = sum(1 for c in comments if c.get('resolved', False))
        active = len(comments) - resolved
        lines.append(f"├── Comments: {len(comments)} total ({resolved} resolved, {active} active)")
    else:
        lines.append(f"├── Comments: {pr_summary.comment_count} total")
    
    # Commits summary
    if commits is not None:
        lines.append(f"├── Commits: {len(commits)} commits")
    
    # URL
    lines.append(f"└── URL: {pr_summary.url}")
    
    return "\n".join(lines)


def format_comment_threads(comments: List[Dict[str, Any]]) -> str:
    """
    Format comment threads for display.
    
    Args:
        comments: List of comment dictionaries
        
    Returns:
        Formatted comment threads
    """
    if not comments:
        return "No comments on this pull request."
    
    lines = ["💬 Comments:"]
    
    # Group comments by parent/thread
    threads = defaultdict(list)
    root_comments = []
    
    for comment in comments:
        parent = comment.get('parent')
        if parent:
            parent_id = parent.get('id')
            threads[parent_id].append(comment)
        else:
            root_comments.append(comment)
    
    # Format root comments and their replies
    for i, comment in enumerate(root_comments):
        user = comment.get('user', {})
        username = user.get('display_name', user.get('nickname', 'Unknown'))
        content = comment.get('content', {}).get('raw', '').strip()
        
        # Truncate long comments
        if len(content) > 100:
            content = content[:97] + "..."
        
        is_last = (i == len(root_comments) - 1)
        prefix = "└──" if is_last else "├──"
        
        lines.append(f"{prefix} {username}")
        lines.append(f"{'    ' if is_last else '│   '}└── \"{content}\"")
        
        # Add replies
        comment_id = comment.get('id')
        if comment_id in threads:
            for reply in threads[comment_id]:
                reply_user = reply.get('user', {})
                reply_username = reply_user.get('display_name', reply_user.get('nickname', 'Unknown'))
                reply_content = reply.get('content', {}).get('raw', '').strip()
                
                if len(reply_content) > 80:
                    reply_content = reply_content[:77] + "..."
                
                lines.append(f"{'    ' if is_last else '│   '}    └── {reply_username}: \"{reply_content}\"")
    
    return "\n".join(lines)


@click.group()
def cli():
    """Bitbucket PR status monitoring utilities."""
    pass


@cli.command("check-status")
@click.option("--pr-id", type=int, help="Specific PR ID to check")
@click.option("--comments", is_flag=True, help="Include comments in output")
@click.option("--all-states", is_flag=True, help="Show all PR states, not just OPEN")
def check_status_command(pr_id: Optional[int], comments: bool, all_states: bool):
    """
    Check PR status with optional details.
    
    If no PR ID is provided, lists all PRs for the repository.
    """
    logger = setup_logging()
    
    try:
        # Get workspace and repository
        workspace, repository = get_workspace_and_repo()
        logger.info(f"Working with {workspace}/{repository}")
        
        # Create Bitbucket client
        client = create_bitbucket_client()
        
        # Get current branch
        current_branch = get_current_branch()
        current_branch_pr = None
        
        if pr_id:
            # Get specific PR details
            logger.info(f"Getting details for PR #{pr_id}")
            
            pr_data = get_detailed_pr_info(client, workspace, repository, pr_id)
            pr_summary = format_pr_summary(pr_data)
            
            # Get comments if requested
            pr_comments = None
            if comments:
                pr_comments = get_pr_comments(client, workspace, repository, pr_id)
            
            # Get commits
            pr_commits = get_pr_commits(client, workspace, repository, pr_id)
            
            # Output detailed view
            output_json({
                "success": True,
                "mode": "detail",
                "pr": {
                    "id": pr_summary.id,
                    "title": pr_summary.title,
                    "state": pr_summary.state,
                    "author": pr_summary.author,
                    "source_branch": pr_summary.source_branch,
                    "destination_branch": pr_summary.destination_branch,
                    "url": pr_summary.url,
                    "review_status": {
                        "approved": pr_summary.review_status.approved,
                        "changes_requested": pr_summary.review_status.changes_requested,
                        "pending": pr_summary.review_status.pending,
                        "summary": pr_summary.review_status.summary
                    } if pr_summary.review_status else None,
                    "comment_count": len(pr_comments) if pr_comments else pr_summary.comment_count,
                    "commit_count": len(pr_commits) if pr_commits else 0
                },
                "formatted_output": format_pr_details(pr_summary, pr_comments, pr_commits),
                "comments": format_comment_threads(pr_comments) if comments and pr_comments else None
            })
            
        else:
            # List all PRs
            state = "ALL" if all_states else "OPEN"
            logger.info(f"Listing {state} PRs")
            
            prs = list_repository_prs(client, workspace, repository, state)
            pr_summaries = [format_pr_summary(pr) for pr in prs]
            
            # Check if current branch has a PR
            if current_branch:
                current_branch_pr = find_current_branch_pr(
                    client, workspace, repository, current_branch
                )
            
            # Output list view
            output_json({
                "success": True,
                "mode": "list",
                "prs": [{
                    "id": pr.id,
                    "title": pr.title,
                    "state": pr.state,
                    "author": pr.author,
                    "source_branch": pr.source_branch,
                    "destination_branch": pr.destination_branch,
                    "url": pr.url,
                    "review_summary": pr.review_status.summary if pr.review_status else "No reviews"
                } for pr in pr_summaries],
                "formatted_output": format_pr_table(pr_summaries),
                "current_branch": current_branch,
                "current_branch_pr": {
                    "id": current_branch_pr.get('id'),
                    "url": current_branch_pr.get('links', {}).get('html', {}).get('href', '')
                } if current_branch_pr else None
            })
            
    except BitbucketError as e:
        output_error(format_error_message(e, "PR status check"), "check_status")
        sys.exit(1)
    except Exception as e:
        output_error(f"Unexpected error: {e}", "check_status")
        sys.exit(1)


@cli.command("list-prs")
@click.option("--state", default="OPEN", help="PR state: OPEN, MERGED, DECLINED, ALL")
@click.option("--limit", default=25, type=int, help="Maximum number of PRs to retrieve")
def list_prs_command(state: str, limit: int):
    """List pull requests for the repository."""
    logger = setup_logging()
    
    try:
        workspace, repository = get_workspace_and_repo()
        client = create_bitbucket_client()
        
        prs = list_repository_prs(client, workspace, repository, state, limit)
        pr_summaries = [format_pr_summary(pr) for pr in prs]
        
        output_json({
            "success": True,
            "repository": f"{workspace}/{repository}",
            "state_filter": state,
            "count": len(pr_summaries),
            "prs": [{
                "id": pr.id,
                "title": pr.title,
                "state": pr.state,
                "url": pr.url
            } for pr in pr_summaries]
        })
        
    except Exception as e:
        output_error(f"Failed to list PRs: {e}", "list_prs")
        sys.exit(1)


if __name__ == "__main__":
    cli()
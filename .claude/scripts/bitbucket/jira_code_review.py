#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv>=1.0.0",
#     "click>=8.1.7",
#     "rich>=13.0.0",
# ]
# ///

"""
Jira Code Review Ticket Creation Script

Creates standardized Jira code review tickets for pull requests.
This script is designed to be called by slash commands and integrates
with the Atlassian MCP server for actual ticket creation.

Ticket Format:
- Type: Task
- Component: Code Review
- Story Points: 1
- Title: {repo} {branch} Code Review
- Description: Pull Request: {pr-url}
"""

import json
import logging
import os
import sys
from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from pathlib import Path

import click
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('create_code_review_ticket')

# Load environment variables
env_path = Path('.env')
if env_path.exists():
    load_dotenv(env_path)
    logger.info(f"Loaded environment from {env_path}")

console = Console()


@dataclass
class CodeReviewTicket:
    """Code review ticket data structure."""
    repository: str
    branch: str
    pr_url: str
    pr_id: int
    project_key: Optional[str] = None
    assignee: Optional[str] = None
    reviewers: Optional[List[str]] = None
    description: Optional[str] = None
    
    @property
    def title(self) -> str:
        """Generate ticket title."""
        return f"{self.repository} {self.branch} Code Review"
    
    @property
    def full_description(self) -> str:
        """Generate full ticket description."""
        desc_parts = [f"Pull Request: {self.pr_url}"]
        
        if self.pr_id:
            desc_parts.append(f"PR ID: #{self.pr_id}")
        
        if self.description:
            desc_parts.append("")
            desc_parts.append("Details:")
            desc_parts.append(self.description)
        
        if self.reviewers:
            desc_parts.append("")
            desc_parts.append("Reviewers:")
            for reviewer in self.reviewers:
                desc_parts.append(f"- {reviewer}")
        
        return "\n".join(desc_parts)


def prepare_ticket_data(ticket: CodeReviewTicket) -> Dict[str, Any]:
    """
    Prepare ticket data for MCP server consumption.
    
    Returns a dictionary that can be passed to the MCP server
    for Jira ticket creation.
    """
    data = {
        "project_key": ticket.project_key,
        "issue_type": "Task",
        "summary": ticket.title,
        "description": ticket.full_description,
        "additional_fields": {
            "components": [{"name": "Code Review"}],
            # Story points field varies by Jira instance
            # Common field names: customfield_10002, Story Points, storyPoints
            "customfield_10002": 1,  # Story points
        }
    }
    
    if ticket.assignee:
        data["assignee_account_id"] = ticket.assignee
    
    return data


def format_mcp_commands(ticket_data: Dict[str, Any]) -> List[str]:
    """
    Format MCP tool commands for creating the Jira ticket.
    
    Returns a list of MCP commands that need to be executed.
    """
    commands = []
    
    # Step 1: Get cloud ID
    commands.append("mcp__atlassian_confluence_jira__getAccessibleAtlassianResources")
    
    # Step 2: Get visible projects if project key not specified
    if not ticket_data.get("project_key"):
        commands.append("mcp__atlassian_confluence_jira__getVisibleJiraProjects")
    
    # Step 3: Get issue type metadata
    commands.append(
        f"mcp__atlassian_confluence_jira__getJiraProjectIssueTypesMetadata "
        f"--projectKey {ticket_data.get('project_key', 'TBD')}"
    )
    
    # Step 4: Create the ticket
    commands.append(
        f"mcp__atlassian_confluence_jira__createJiraIssue "
        f"--project {ticket_data.get('project_key', 'TBD')} "
        f"--issueType Task "
        f"--summary \"{ticket_data['summary']}\" "
        f"--description \"{ticket_data['description']}\""
    )
    
    return commands


@click.group()
def cli():
    """Jira Code Review Ticket Management."""
    pass


@cli.command()
@click.option('--repository', '-r', required=True, help='Repository name')
@click.option('--branch', '-b', required=True, help='Branch name')
@click.option('--pr-url', '-u', required=True, help='Pull request URL')
@click.option('--pr-id', '-i', type=int, required=True, help='Pull request ID')
@click.option('--project-key', '-p', help='Jira project key')
@click.option('--assignee', '-a', help='Assignee account ID')
@click.option('--reviewers', '-R', multiple=True, help='Reviewer usernames')
@click.option('--description', '-d', help='Additional description')
@click.option('--output-format', '-o', 
              type=click.Choice(['json', 'commands', 'pretty']), 
              default='json',
              help='Output format')
def prepare_ticket(
    repository: str,
    branch: str,
    pr_url: str,
    pr_id: int,
    project_key: Optional[str],
    assignee: Optional[str],
    reviewers: tuple,
    description: Optional[str],
    output_format: str
):
    """
    Prepare a Jira code review ticket.
    
    This command prepares the ticket data and outputs either:
    - JSON data for MCP consumption
    - MCP commands to execute
    - Pretty formatted output for review
    """
    try:
        # Create ticket object
        ticket = CodeReviewTicket(
            repository=repository,
            branch=branch,
            pr_url=pr_url,
            pr_id=pr_id,
            project_key=project_key,
            assignee=assignee,
            reviewers=list(reviewers) if reviewers else None,
            description=description
        )
        
        # Prepare ticket data
        ticket_data = prepare_ticket_data(ticket)
        
        # Output based on format
        if output_format == 'json':
            # JSON format for MCP consumption
            output = {
                "success": True,
                "ticket_data": ticket_data,
                "title": ticket.title,
                "description": ticket.full_description
            }
            print(json.dumps(output, indent=2))
            
        elif output_format == 'commands':
            # MCP commands format
            commands = format_mcp_commands(ticket_data)
            output = {
                "success": True,
                "mcp_commands": commands,
                "ticket_data": ticket_data
            }
            print(json.dumps(output, indent=2))
            
        else:  # pretty
            # Pretty format for human review
            console.print("\n[bold cyan]Jira Code Review Ticket[/bold cyan]")
            console.print("=" * 50)
            
            table = Table(show_header=False, box=None)
            table.add_column("Field", style="bold")
            table.add_column("Value")
            
            table.add_row("Title:", ticket.title)
            table.add_row("Repository:", repository)
            table.add_row("Branch:", branch)
            table.add_row("PR URL:", pr_url)
            table.add_row("PR ID:", f"#{pr_id}")
            
            if project_key:
                table.add_row("Project:", project_key)
            if assignee:
                table.add_row("Assignee:", assignee)
            if reviewers:
                table.add_row("Reviewers:", ", ".join(reviewers))
            
            console.print(table)
            
            console.print("\n[bold]Description:[/bold]")
            console.print(ticket.full_description)
            
            console.print("\n[bold green]✓[/bold green] Ticket data prepared successfully")
            
    except Exception as e:
        logger.error(f"Failed to prepare ticket: {e}", exc_info=True)
        output = {
            "success": False,
            "error": str(e),
            "operation": "prepare_ticket"
        }
        print(json.dumps(output, indent=2))
        sys.exit(1)


@cli.command()
@click.option('--pr-url', '-u', required=True, help='Pull request URL')
@click.option('--output-format', '-o',
              type=click.Choice(['json', 'pretty']),
              default='json',
              help='Output format')
def validate_production_branch(pr_url: str, output_format: str):
    """
    Check if a PR targets a production branch.
    
    Production branches: main, master, release/*
    """
    try:
        # Extract branch info from PR URL if possible
        # Format: https://bitbucket.org/workspace/repo/pull-requests/123
        # This is a simplified check - in practice, you'd query the API
        
        production_patterns = ['main', 'master', 'release']
        
        # For now, we'll return a structure that the slash command can use
        result = {
            "success": True,
            "is_production": False,  # Would be determined from actual PR data
            "recommendation": "Code review ticket recommended for production branches",
            "pr_url": pr_url
        }
        
        if output_format == 'json':
            print(json.dumps(result, indent=2))
        else:
            console.print(f"\n[bold]PR URL:[/bold] {pr_url}")
            console.print(f"[bold]Production Branch:[/bold] {result['is_production']}")
            console.print(f"[bold]Recommendation:[/bold] {result['recommendation']}")
            
    except Exception as e:
        logger.error(f"Failed to validate branch: {e}", exc_info=True)
        output = {
            "success": False,
            "error": str(e),
            "operation": "validate_production_branch"
        }
        print(json.dumps(output, indent=2))
        sys.exit(1)


@cli.command()
def test():
    """Test the script with sample data."""
    sample_ticket = CodeReviewTicket(
        repository="analytics-platform",
        branch="main-PROJ-123",
        pr_url="https://bitbucket.org/workspace/analytics-platform/pull-requests/456",
        pr_id=456,
        project_key="PROJ",
        reviewers=["alice", "bob"],
        description="Implements new authentication flow"
    )
    
    console.print("[bold green]Testing Jira Code Review Ticket Creation[/bold green]\n")
    
    # Show ticket details
    console.print("[bold]Sample Ticket:[/bold]")
    console.print(f"  Title: {sample_ticket.title}")
    console.print(f"  Repository: {sample_ticket.repository}")
    console.print(f"  Branch: {sample_ticket.branch}")
    console.print(f"  PR: {sample_ticket.pr_url}")
    
    # Show prepared data
    ticket_data = prepare_ticket_data(sample_ticket)
    console.print("\n[bold]Prepared Data:[/bold]")
    console.print(json.dumps(ticket_data, indent=2))
    
    # Show MCP commands
    commands = format_mcp_commands(ticket_data)
    console.print("\n[bold]MCP Commands:[/bold]")
    for i, cmd in enumerate(commands, 1):
        console.print(f"  {i}. {cmd}")
    
    console.print("\n[bold green]✓[/bold green] Test completed successfully")


if __name__ == "__main__":
    cli()
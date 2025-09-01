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
Bitbucket API Utilities for Claude Code Integration

This module provides utility functions for interacting with the Bitbucket API
as part of the hybrid Bitbucket API + Atlassian MCP integration.

Features:
- Environment configuration loading
- Bitbucket client initialization and management
- Git remote parsing for workspace/repository detection
- Comprehensive error handling with retry logic
- Structured logging configuration
- Response caching for performance optimization
"""

import os
import sys
import json
import logging
import re
import subprocess
import time
from typing import Dict, Optional, Tuple, Any, List
from urllib.parse import urlparse
from pathlib import Path
from dataclasses import dataclass
from functools import wraps

try:
    from dotenv import load_dotenv
    from atlassian import Bitbucket
    import requests
    import click
except ImportError as e:
    print(f"Missing required dependency: {e}", file=sys.stderr)
    print("Please ensure all dependencies are installed", file=sys.stderr)
    sys.exit(1)


@dataclass
class BitbucketConfig:
    """Configuration for Bitbucket API operations."""
    url: str
    username: str
    password: str
    auth_type: str  # "api_token" or "app_password"
    workspace: Optional[str] = None
    timeout: int = 30
    max_retries: int = 3
    retry_backoff_factor: float = 1.0
    cache_enabled: bool = True
    cache_ttl: int = 300
    log_level: str = "INFO"


@dataclass
class GitRemoteInfo:
    """Information parsed from git remote."""
    workspace: str
    repository: str
    url: str
    is_ssh: bool = False


class BitbucketError(Exception):
    """Base exception for Bitbucket API operations."""
    pass


class BitbucketAuthError(BitbucketError):
    """Authentication-related errors."""
    pass


class BitbucketNotFoundError(BitbucketError):
    """Resource not found errors."""
    pass


class BitbucketRateLimitError(BitbucketError):
    """Rate limit exceeded errors."""
    pass


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Set up structured logging for Bitbucket operations.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("bitbucket_api")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Avoid duplicate handlers
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


def load_bitbucket_config() -> BitbucketConfig:
    """
    Load Bitbucket configuration from environment variables.
    Supports API tokens (preferred) with fallback to app passwords.
    
    Returns:
        BitbucketConfig instance with loaded settings
        
    Raises:
        BitbucketError: If required configuration is missing
    """
    # Load environment from .env file if it exists
    env_path = Path.cwd() / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    
    # Required configuration
    url = os.getenv('BITBUCKET_URL', 'https://api.bitbucket.org')
    username = os.getenv('BITBUCKET_USERNAME')
    
    if not username:
        raise BitbucketError(
            "BITBUCKET_USERNAME not found in environment. "
            "Please set in .env file or environment variables."
        )
    
    # Authentication priority: API token > App password
    api_token = os.getenv('BITBUCKET_API_TOKEN')
    app_password = os.getenv('BITBUCKET_APP_PASSWORD')
    
    if api_token:
        password = api_token
        auth_type = "api_token"
    elif app_password:
        password = app_password
        auth_type = "app_password"
    else:
        raise BitbucketError(
            "Neither BITBUCKET_API_TOKEN nor BITBUCKET_APP_PASSWORD found in environment. "
            "Please set one of these in .env file or environment variables.\n"
            "Recommended: Use BITBUCKET_API_TOKEN (generate at: "
            "https://bitbucket.org/account/settings/personal-access-tokens/)"
        )
    
    # Optional configuration with defaults
    config = BitbucketConfig(
        url=url,
        username=username,
        password=password,
        auth_type=auth_type,
        workspace=os.getenv('BITBUCKET_WORKSPACE'),
        timeout=int(os.getenv('REQUEST_TIMEOUT', 30)),
        max_retries=int(os.getenv('MAX_RETRIES', 3)),
        retry_backoff_factor=float(os.getenv('RETRY_BACKOFF_FACTOR', 1.0)),
        cache_enabled=os.getenv('CACHE_ENABLED', 'true').lower() == 'true',
        cache_ttl=int(os.getenv('CACHE_TTL', 300)),
        log_level=os.getenv('LOG_LEVEL', 'INFO')
    )
    
    return config


def parse_git_remote(remote_name: str = "origin") -> Optional[GitRemoteInfo]:
    """
    Parse git remote URL to extract workspace and repository information.
    
    Args:
        remote_name: Name of the git remote (default: "origin")
        
    Returns:
        GitRemoteInfo instance with parsed data, or None if parsing fails
    """
    try:
        # Get the remote URL
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            check=True
        )
        remote_url = result.stdout.strip()
        
        # Parse different URL formats
        # SSH format: git@bitbucket.org:workspace/repo.git
        ssh_match = re.match(r'git@([^:]+):([^/]+)/([^/]+?)(?:\.git)?$', remote_url)
        if ssh_match:
            _, workspace, repository = ssh_match.groups()
            return GitRemoteInfo(
                workspace=workspace,
                repository=repository,
                url=remote_url,
                is_ssh=True
            )
        
        # HTTPS format: https://bitbucket.org/workspace/repo.git
        https_match = re.match(r'https://[^/]+/([^/]+)/([^/]+?)(?:\.git)?$', remote_url)
        if https_match:
            workspace, repository = https_match.groups()
            return GitRemoteInfo(
                workspace=workspace,
                repository=repository,
                url=remote_url,
                is_ssh=False
            )
        
        return None
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def retry_on_error(max_retries: int = 3, backoff_factor: float = 1.0):
    """
    Decorator to retry function calls on specific errors.
    
    Args:
        max_retries: Maximum number of retry attempts
        backoff_factor: Exponential backoff multiplier
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger("bitbucket_api")
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.ConnectionError as e:
                    if attempt == max_retries:
                        raise BitbucketError(f"Connection failed after {max_retries} retries: {e}")
                    
                    wait_time = backoff_factor * (2 ** attempt)
                    logger.warning(f"Connection error, retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429:  # Rate limit
                        if attempt == max_retries:
                            raise BitbucketRateLimitError("Rate limit exceeded")
                        
                        # Try to get retry-after header
                        retry_after = e.response.headers.get('retry-after', '60')
                        wait_time = int(retry_after)
                        logger.warning(f"Rate limit hit, waiting {wait_time}s...")
                        time.sleep(wait_time)
                        
                    elif e.response.status_code == 401:
                        raise BitbucketAuthError("Authentication failed. Check your credentials.")
                    elif e.response.status_code == 404:
                        raise BitbucketNotFoundError("Resource not found")
                    else:
                        if attempt == max_retries:
                            raise BitbucketError(f"HTTP error: {e}")
                        
                        wait_time = backoff_factor * (2 ** attempt)
                        logger.warning(f"HTTP error {e.response.status_code}, retrying in {wait_time}s...")
                        time.sleep(wait_time)
                        
        return wrapper
    return decorator


class BitbucketClient:
    """Enhanced Bitbucket client with error handling and retry logic."""
    
    def __init__(self, config: BitbucketConfig):
        self.config = config
        self.logger = setup_logging(config.log_level)
        
        # Initialize the Atlassian Bitbucket client
        self._client = Bitbucket(
            url=config.url,
            username=config.username,
            password=config.password,
            timeout=config.timeout
        )
        
        # Simple in-memory cache
        self._cache = {} if config.cache_enabled else None
        
        auth_method = "API Token" if config.auth_type == "api_token" else "App Password"
        self.logger.info(f"Initialized Bitbucket client for {config.url} using {auth_method}")
    
    def _get_cache_key(self, method: str, *args, **kwargs) -> str:
        """Generate a cache key for the given method and arguments."""
        return f"{method}:{hash((args, tuple(sorted(kwargs.items()))))}"
    
    def _get_cached(self, cache_key: str) -> Optional[Any]:
        """Get cached response if available and not expired."""
        if not self._cache:
            return None
            
        if cache_key in self._cache:
            cached_time, cached_data = self._cache[cache_key]
            if time.time() - cached_time < self.config.cache_ttl:
                self.logger.debug(f"Cache hit for {cache_key}")
                return cached_data
            else:
                # Remove expired entry
                del self._cache[cache_key]
                
        return None
    
    def _set_cached(self, cache_key: str, data: Any) -> None:
        """Store response in cache."""
        if self._cache is not None:
            self._cache[cache_key] = (time.time(), data)
            self.logger.debug(f"Cached response for {cache_key}")
    
    @retry_on_error()
    def get_repository_info(self, workspace: str, repo_slug: str) -> Dict[str, Any]:
        """Get repository information."""
        cache_key = self._get_cache_key("get_repository_info", workspace, repo_slug)
        cached = self._get_cached(cache_key)
        if cached:
            return cached
            
        self.logger.info(f"Getting repository info for {workspace}/{repo_slug}")
        
        try:
            repo_info = self._client.get_repo(workspace, repo_slug)
            self._set_cached(cache_key, repo_info)
            return repo_info
        except Exception as e:
            self.logger.error(f"Failed to get repository info: {e}")
            raise
    
    @retry_on_error()
    def list_pull_requests(self, workspace: str, repo_slug: str, 
                          state: str = "OPEN", limit: int = 50) -> List[Dict[str, Any]]:
        """List pull requests for a repository."""
        cache_key = self._get_cache_key("list_pull_requests", workspace, repo_slug, state, limit)
        cached = self._get_cached(cache_key)
        if cached:
            return cached
            
        self.logger.info(f"Listing pull requests for {workspace}/{repo_slug} (state={state})")
        
        try:
            # The atlassian-python-api uses get_pull_requests for Server/Data Center
            # For Cloud API, it's different, but we'll try the Server method first
            prs = self._client.get_pull_requests(workspace, repo_slug, state=state, limit=limit)
            if 'values' in prs:
                pr_list = prs['values']
            else:
                pr_list = prs if isinstance(prs, list) else [prs]
                
            self._set_cached(cache_key, pr_list)
            return pr_list
        except Exception as e:
            self.logger.error(f"Failed to list pull requests: {e}")
            raise
    
    @retry_on_error()
    def create_pull_request(self, workspace: str, repo_slug: str, 
                           source_branch: str, destination_branch: str,
                           title: str, description: str = "",
                           reviewers: Optional[List[str]] = None) -> Dict[str, Any]:
        """Create a new pull request."""
        self.logger.info(f"Creating PR: {source_branch} -> {destination_branch} in {workspace}/{repo_slug}")
        
        pr_data = {
            "title": title,
            "description": description,
            "source": {
                "branch": {"name": source_branch}
            },
            "destination": {
                "branch": {"name": destination_branch}
            }
        }
        
        if reviewers:
            pr_data["reviewers"] = [{"uuid": reviewer} for reviewer in reviewers]
        
        try:
            result = self._client.open_pullrequest(
                source_project=workspace,
                source_repo=repo_slug,
                dest_project=workspace,
                dest_repo=repo_slug,
                source_branch=f"refs/heads/{source_branch}",
                destination_branch=f"refs/heads/{destination_branch}",
                title=title,
                description=description
            )
            
            self.logger.info(f"Successfully created PR #{result.get('id', 'unknown')}")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to create pull request: {e}")
            raise


def get_workspace_and_repo() -> Tuple[str, str]:
    """
    Get workspace and repository name from git remote or configuration.
    
    Returns:
        Tuple of (workspace, repository)
        
    Raises:
        BitbucketError: If workspace/repo cannot be determined
    """
    config = load_bitbucket_config()
    
    # Try to get from configuration first
    if config.workspace:
        # Still need repository name from git
        remote_info = parse_git_remote()
        if remote_info:
            return config.workspace, remote_info.repository
        else:
            raise BitbucketError(
                "Could not determine repository name from git remote. "
                "Ensure you're in a git repository with a remote named 'origin'."
            )
    
    # Try to parse from git remote
    remote_info = parse_git_remote()
    if remote_info:
        return remote_info.workspace, remote_info.repository
    
    raise BitbucketError(
        "Could not determine workspace and repository. "
        "Please set BITBUCKET_WORKSPACE in .env or ensure git remote 'origin' is configured."
    )


def create_bitbucket_client() -> BitbucketClient:
    """
    Create and configure a Bitbucket client.
    
    Returns:
        Configured BitbucketClient instance
        
    Raises:
        BitbucketError: If configuration is invalid
    """
    config = load_bitbucket_config()
    return BitbucketClient(config)


def format_error_message(error: Exception, operation: str) -> str:
    """
    Format error message for user display.
    
    Args:
        error: The exception that occurred
        operation: Description of the operation that failed
        
    Returns:
        Formatted error message
    """
    if isinstance(error, BitbucketAuthError):
        return (
            f"Authentication failed during {operation}. "
            "Please check your BITBUCKET_USERNAME and either BITBUCKET_API_TOKEN or BITBUCKET_APP_PASSWORD in .env file."
        )
    elif isinstance(error, BitbucketNotFoundError):
        return f"Resource not found during {operation}. Please check the repository and branch names."
    elif isinstance(error, BitbucketRateLimitError):
        return f"Rate limit exceeded during {operation}. Please wait before retrying."
    else:
        return f"Error during {operation}: {str(error)}"


def output_json(data: Dict[str, Any]) -> None:
    """
    Output JSON data for consumption by slash commands.
    
    Args:
        data: Dictionary to output as JSON
    """
    print(json.dumps(data, indent=2, default=str))


def output_error(error: str, operation: str = "operation") -> None:
    """
    Output error information in JSON format.
    
    Args:
        error: Error message
        operation: Operation that failed
    """
    error_data = {
        "success": False,
        "error": error,
        "operation": operation,
        "timestamp": time.time()
    }
    output_json(error_data)


# CLI command group for testing
@click.group()
def cli():
    """Bitbucket API utilities for Claude Code."""
    pass


@cli.command()
def test_config():
    """Test configuration loading."""
    try:
        config = load_bitbucket_config()
        workspace, repo = get_workspace_and_repo()
        
        output_json({
            "success": True,
            "config": {
                "url": config.url,
                "username": config.username,
                "auth_type": config.auth_type,
                "workspace": workspace,
                "repository": repo,
                "cache_enabled": config.cache_enabled,
                "log_level": config.log_level
            }
        })
    except Exception as e:
        output_error(format_error_message(e, "configuration test"), "test_config")
        sys.exit(1)


@cli.command()
def test_connection():
    """Test Bitbucket API connection."""
    try:
        client = create_bitbucket_client()
        workspace, repo = get_workspace_and_repo()
        
        # Try to get repository info
        repo_info = client.get_repository_info(workspace, repo)
        
        output_json({
            "success": True,
            "repository": {
                "name": repo_info.get("name"),
                "full_name": repo_info.get("full_name"),
                "is_private": repo_info.get("is_private"),
                "created_on": repo_info.get("created_on"),
                "updated_on": repo_info.get("updated_on")
            }
        })
    except Exception as e:
        output_error(format_error_message(e, "connection test"), "test_connection")
        sys.exit(1)


if __name__ == "__main__":
    cli()
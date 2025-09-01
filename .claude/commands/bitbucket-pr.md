---
allowed-tools: Bash(git:*), mcp__bitbucket__bb_add_pr, mcp__bitbucket__bb_ls_repos, mcp__bitbucket__bb_get_repo, mcp__atlassian_confluence_jira__getAccessibleAtlassianResources, mcp__atlassian_confluence_jira__getVisibleJiraProjects, mcp__atlassian_confluence_jira__getJiraProjectIssueTypesMetadata, mcp__atlassian_confluence_jira__createJiraIssue, mcp__atlassian_confluence_jira__lookupJiraAccountId
argument-hint: [destination-branch] [ticket-number] [reviewers...] [--jira-project PROJECT_KEY]
description: Create Bitbucket PR with proper branch naming and automatic Jira code review ticket creation
model: sonnet
---

# Bitbucket Pull Request Creation with Jira Integration

Create a pull request following the standardized workflow with proper branch naming and automatic Jira code review ticket creation for production branches.

## Arguments
- `destination-branch`: Target branch (e.g., "development", "main")  
- `ticket-number`: Ticket/issue number for branch naming
- `reviewers`: Comma-separated list of reviewer usernames (optional)
- `--jira-project`: Jira project key for code review tickets (optional, will auto-detect if not provided)

## Workflow Context

**Branch Naming Convention**: `{destination-branch}-{ticket-number}`
**Example**: For merging to development with ticket 123 → branch name: `development-123`

**Code Review Ticket Format**:
- **Ticket Type**: Task
- **Component**: Code Review  
- **Story Points**: 1
- **Title**: `{repo} {full-branch-name} Code Review`
- **Description**: Link to pull request

## Current Repository State

**Git Status**: !`git status --porcelain`

**Current Branch**: !`git branch --show-current`

**Recent Commits**: !`git log --oneline -5`

**Staged/Unstaged Changes**: !`git diff HEAD`

**Repository Info**: Determine current Bitbucket workspace and repo from git remote

## Your Tasks

1. **Validate Arguments**: 
   - Ensure destination branch and ticket number are provided
   - Parse reviewers list and jira-project flag if provided
   - Extract repository name from git remote

2. **Branch Management**:
   - Create branch with naming convention: `{destination-branch}-{ticket-number}`
   - If branch exists, checkout and ensure it's up to date
   - Push branch to remote with upstream tracking

3. **Create Pull Request**:
   - Use Bitbucket MCP tools to create PR
   - Set appropriate title and description including changes summary
   - Add reviewers if specified
   - Set destination branch correctly
   - Capture PR URL from response

4. **Jira Code Review Ticket Creation**:
   - **For production branches (main/master/release):**
     a. Get Atlassian cloud ID using `getAccessibleAtlassianResources`
     b. Find appropriate Jira project:
        - Use provided `--jira-project` if specified
        - Otherwise, search visible projects and select most appropriate
     c. Get issue type metadata to find "Task" type
     d. Create Jira ticket with exact specifications:
        - **Issue Type**: Task
        - **Component**: Code Review (use `additional_fields` if needed)
        - **Summary**: `{repo-name} {full-branch-name} Code Review`
        - **Description**: `Pull Request: {pr-url}`
        - **Story Points**: 1 (use `additional_fields`)
     e. If reviewers specified, lookup their Jira account IDs and assign
   - **For development branches**: Note that code review is optional

5. **Error Handling**:
   - If Jira ticket creation fails, still report PR success
   - Provide manual ticket creation instructions as fallback
   - Log specific error details for troubleshooting

6. **Output Summary**:
   - ✅ Branch created: `{branch-name}`
   - ✅ Pull Request created: `{pr-url}`
   - ✅ Code Review Ticket created: `{jira-ticket-url}` (for production branches)
   - 📋 Ticket Details: Title, Component, Story Points
   - 📝 Next steps and review assignments

## Success Criteria
- Branch created with correct naming convention
- PR created with proper metadata and reviewers
- Jira code review ticket automatically created for production branches
- Ticket follows exact format specifications
- Clear, actionable output with all relevant URLs
- Graceful error handling with fallback instructions
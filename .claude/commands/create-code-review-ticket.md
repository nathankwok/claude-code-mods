---
allowed-tools: Bash(git:*), mcp__atlassian_confluence_jira__getAccessibleAtlassianResources, mcp__atlassian_confluence_jira__getVisibleJiraProjects, mcp__atlassian_confluence_jira__getJiraProjectIssueTypesMetadata, mcp__atlassian_confluence_jira__createJiraIssue, mcp__atlassian_confluence_jira__lookupJiraAccountId
argument-hint: [pr-url] [branch-name] [--jira-project PROJECT_KEY] [--assignee EMAIL_OR_NAME]
description: Create a Jira code review ticket for an existing pull request
model: sonnet
---

# Create Jira Code Review Ticket

Create a Jira code review ticket for an existing pull request following the standardized format.

## Arguments
- `pr-url`: URL of the pull request (required)
- `branch-name`: Branch name for the ticket title (optional, will be extracted from PR if possible)
- `--jira-project`: Jira project key (optional, will auto-detect if not provided)
- `--assignee`: Email or display name of assignee/reviewer (optional)

## Code Review Ticket Specifications

**Required Format:**
- **Ticket Type**: Task
- **Component**: Code Review
- **Story Points**: 1 (bump up if large refactors)
- **Title**: `{repo} {full-branch-name} Code Review`
- **Description**: Link to pull request

**Example Title**: "analytics-lambda development-123 Code Review"

## Current Repository Context

**Current Repository**: !`basename $(git rev-parse --show-toplevel)`

**Git Remote**: !`git remote get-url origin`

## Your Tasks

1. **Validate Arguments**:
   - Ensure PR URL is provided and valid
   - Parse branch name from arguments or extract from PR URL/title
   - Validate optional jira-project and assignee arguments

2. **Extract Repository Information**:
   - Get repository name from git remote or PR URL
   - If branch-name not provided, attempt to extract from PR URL or title
   - Ensure we have all components for the ticket title format

3. **Jira Setup and Project Discovery**:
   - Get Atlassian cloud ID using `getAccessibleAtlassianResources`
   - Find appropriate Jira project:
     - Use provided `--jira-project` if specified
     - Otherwise, search visible projects and select most appropriate
     - Display available projects if multiple options exist

4. **Issue Type Validation**:
   - Get project issue type metadata to find "Task" type
   - Verify "Task" type exists in the selected project
   - Get any required fields for Task creation

5. **Create Code Review Ticket**:
   - **Issue Type**: Task
   - **Summary**: `{repo-name} {branch-name} Code Review`
   - **Description**: `Pull Request: {pr-url}`
   - **Additional Fields**:
     - Component: "Code Review" (if component field exists)
     - Story Points: 1 (if story points field exists)
   - **Assignee**: Lookup and assign if `--assignee` provided

6. **Error Handling**:
   - Validate Atlassian connectivity
   - Handle missing project or issue type errors
   - Provide clear error messages with troubleshooting steps
   - Suggest manual creation steps if automated creation fails

7. **Output Results**:
   - ✅ **Ticket Created**: `{jira-ticket-url}`
   - 📋 **Details**:
     - Title: `{full-title}`
     - Type: Task
     - Component: Code Review
     - Story Points: 1
     - Assignee: `{assignee}` (if set)
   - 🔗 **Links**:
     - Pull Request: `{pr-url}`
     - Jira Ticket: `{ticket-url}`

## Usage Examples

```bash
# Basic usage with PR URL
/create-code-review-ticket https://bitbucket.org/workspace/repo/pull-requests/123

# With specific branch name and project
/create-code-review-ticket https://bitbucket.org/workspace/repo/pull-requests/123 development-456 --jira-project PROJ

# With assignee
/create-code-review-ticket https://bitbucket.org/workspace/repo/pull-requests/123 --assignee john.doe@company.com
```

## Success Criteria
- Jira ticket created with exact format specifications
- All required fields populated correctly
- Assignee set if specified
- Clear output with ticket and PR links
- Graceful error handling with helpful messages
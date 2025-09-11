---
allowed-tools: Bash(git:*), Bash(uv:*), 
               mcp__atlassian_confluence_jira__getAccessibleAtlassianResources,
               mcp__atlassian_confluence_jira__getVisibleJiraProjects,
               mcp__atlassian_confluence_jira__getJiraProjectIssueTypesMetadata,
               mcp__atlassian_confluence_jira__createJiraIssue,
               mcp__atlassian_confluence_jira__lookupJiraAccountId
argument-hint: [destination-branch] [ticket-number] [reviewers...] [--jira-project PROJECT_KEY] [--no-jira] [--draft]
description: Create Bitbucket PR with hybrid API + MCP Jira integration (API token preferred, app password fallback)
model: claude-sonnet-4-0
---

# Hybrid Bitbucket PR Creation with Jira Integration

Create a pull request using direct Bitbucket API integration (Python) combined with Atlassian MCP server for Jira ticket management.

## Arguments
- `destination-branch`: Target branch (e.g., "main", "development", "release") 
- `ticket-number`: Ticket/issue number for branch naming
- `reviewers`: Comma-separated reviewer usernames (optional, can use @mentions)

## Options
- `--jira-project`: Specify Jira project key for code review ticket (optional)
- `--no-jira`: Skip Jira ticket creation entirely
- `--draft`: Create as draft PR
- `--title`: Custom PR title (optional)

## Authentication & Configuration

**Bitbucket Authentication** (via .env file):
- **Preferred**: `BITBUCKET_API_TOKEN` (recommended)
- **Fallback**: `BITBUCKET_APP_PASSWORD` (deprecated but supported)

**Jira Authentication**: Handled by Atlassian MCP server (no .env needed)

## Current Repository Context

**Git Status**: !`git status --porcelain`
**Current Branch**: !`git branch --show-current`  
**Recent Commits**: !`git log --oneline -3`

## Workflow Execution

### Step 1: Parse and Validate Arguments

```bash
# Parse arguments
DESTINATION_BRANCH="$1"
TICKET_NUMBER="$2"
REVIEWERS="$3"

# Parse options
JIRA_PROJECT=""
NO_JIRA=false
DRAFT=false
CUSTOM_TITLE=""

shift 3  # Remove positional arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --jira-project)
      JIRA_PROJECT="$2"
      shift 2
      ;;
    --no-jira)
      NO_JIRA=true
      shift
      ;;
    --draft)
      DRAFT=true
      shift
      ;;
    --title)
      CUSTOM_TITLE="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validate required arguments
if [[ -z "$DESTINATION_BRANCH" || -z "$TICKET_NUMBER" ]]; then
    echo "❌ Error: destination-branch and ticket-number are required"
    echo "Usage: /bitbucket-pr-api [destination-branch] [ticket-number] [reviewers...] [options]"
    exit 1
fi
```

### Step 2: Bitbucket Operations (Python Script)

Execute PR creation via direct API:

```bash
echo "🔄 Creating pull request via Bitbucket API..."

# Build command arguments
CMD_ARGS=("$DESTINATION_BRANCH" "$TICKET_NUMBER")

if [[ -n "$REVIEWERS" ]]; then
    CMD_ARGS+=(--reviewers "$REVIEWERS")
fi

if [[ "$DRAFT" == "true" ]]; then
    CMD_ARGS+=(--draft)
fi

if [[ -n "$CUSTOM_TITLE" ]]; then
    CMD_ARGS+=(--title "$CUSTOM_TITLE")
fi

# Execute Python script
PR_RESULT=$(uv run .claude/scripts/bitbucket/bitbucket_pr_api.py create-pr "${CMD_ARGS[@]}" 2>&1)
PR_EXIT_CODE=$?

if [[ $PR_EXIT_CODE -ne 0 ]]; then
    echo "❌ Pull request creation failed:"
    echo "$PR_RESULT"
    exit 1
fi

# Parse PR result
PR_URL=$(echo "$PR_RESULT" | jq -r '.pr.url // empty' 2>/dev/null)
PR_ID=$(echo "$PR_RESULT" | jq -r '.pr.id // empty' 2>/dev/null)  
BRANCH_NAME=$(echo "$PR_RESULT" | jq -r '.pr.source_branch // empty' 2>/dev/null)
IS_PRODUCTION=$(echo "$PR_RESULT" | jq -r '.pr.is_production // false' 2>/dev/null)

echo "✅ Pull request created successfully!"
echo "🔗 **PR URL**: $PR_URL"
echo "📋 **PR ID**: #$PR_ID"
echo "🌿 **Branch**: $BRANCH_NAME"
```

### Step 3: Jira Integration (MCP Tools)

For production branches, create code review ticket:

```bash
# Determine if we should create Jira ticket
SHOULD_CREATE_TICKET=false

if [[ "$NO_JIRA" != "true" && "$IS_PRODUCTION" == "true" ]]; then
    SHOULD_CREATE_TICKET=true
fi

if [[ "$SHOULD_CREATE_TICKET" == "true" ]]; then
    echo ""
    echo "🎫 Creating Jira code review ticket for production branch..."
    
    # Extract repository name from git remote
    REPO_NAME=$(basename $(git remote get-url origin) .git 2>/dev/null || echo "repository")
    
    # Jira ticket details
    TICKET_TITLE="$REPO_NAME $BRANCH_NAME Code Review"
    TICKET_DESCRIPTION="Pull Request: $PR_URL"
    
    echo "📝 Ticket Title: $TICKET_TITLE"
    echo "📄 Ticket Description: $TICKET_DESCRIPTION"
```

Execute MCP operations for Jira ticket creation:

1. **Get Atlassian Resources**:
   - Use `mcp__atlassian_confluence_jira__getAccessibleAtlassianResources` to get cloud ID

2. **Discover Jira Project**:
   - If `--jira-project` specified: Use that project
   - Otherwise: Use `mcp__atlassian_confluence_jira__getVisibleJiraProjects` to find appropriate project

3. **Get Issue Type Metadata**:
   - Use `mcp__atlassian_confluence_jira__getJiraProjectIssueTypesMetadata` to find "Task" type

4. **Create Code Review Ticket**:
   - Use `mcp__atlassian_confluence_jira__createJiraIssue` with:
     - **Issue Type**: Task
     - **Summary**: `{repo} {branch-name} Code Review`
     - **Description**: `Pull Request: {pr-url}`
     - **Story Points**: 1 (via additional_fields if available)
     - **Component**: Code Review (via additional_fields if available)

5. **Assign Reviewer** (if specified):
   - Use `mcp__atlassian_confluence_jira__lookupJiraAccountId` to find reviewer
   - Set assignee during ticket creation

### Step 4: Output Summary

```bash
echo ""
echo "🎉 **Pull Request Workflow Complete**"
echo ""
echo "📋 **Summary**:"
echo "  ✅ Branch: $BRANCH_NAME"
echo "  ✅ Pull Request: $PR_URL"
if [[ -n "$JIRA_TICKET_URL" ]]; then
    echo "  ✅ Code Review Ticket: $JIRA_TICKET_URL"
fi
if [[ -n "$REVIEWERS" ]]; then
    echo "  👥 Reviewers: $REVIEWERS"
fi

echo ""
echo "🚀 **Next Steps**:"
echo "  1. Reviewers have been notified"
if [[ "$IS_PRODUCTION" == "true" ]]; then
    echo "  2. Code review ticket created for production branch"
fi
echo "  3. Monitor PR for feedback and approvals"
echo "  4. Merge when approved and CI passes"
```

## Error Handling

### Bitbucket API Errors
- **Authentication**: Clear guidance on API token vs app password setup
- **Repository Access**: Check workspace/repository permissions  
- **Branch Conflicts**: Handle existing branches gracefully
- **Network Issues**: Retry with exponential backoff

### MCP/Jira Errors
- **MCP Unavailable**: Continue with PR creation, note Jira ticket failure
- **Project Not Found**: List available projects for user selection
- **Permission Errors**: Clear permission requirements
- **Field Validation**: Handle missing or invalid Jira fields

### Git Operation Errors
- **Not a Git Repository**: Clear error message with setup instructions
- **Dirty Working Directory**: Guidance on committing or stashing changes
- **Remote Issues**: Help with remote configuration

## Example Usage

```bash
# Basic PR creation
/bitbucket-pr-api main 123

# With reviewers  
/bitbucket-pr-api development 456 @john,@jane

# Production branch with specific Jira project
/bitbucket-pr-api release 789 @team --jira-project PROJ

# Draft PR without Jira ticket
/bitbucket-pr-api feature 321 --draft --no-jira

# Custom title
/bitbucket-pr-api main 555 --title "Critical bug fix for authentication"
```

## Success Criteria

- ✅ Branch created with naming convention: `{destination}-{ticket}`
- ✅ PR created with proper title, description, and metadata
- ✅ Reviewers assigned and notified
- ✅ Jira ticket created automatically for production branches  
- ✅ Clear success/error messages with actionable guidance
- ✅ Graceful handling of MCP server unavailability
- ✅ Support for both API tokens and app passwords
- ✅ Comprehensive error handling with user-friendly messages
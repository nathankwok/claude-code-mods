---
allowed-tools: Bash(git:*), Bash(uv:*),
               mcp__atlassian_confluence_jira__getAccessibleAtlassianResources,
               mcp__atlassian_confluence_jira__getVisibleJiraProjects,
               mcp__atlassian_confluence_jira__getJiraProjectIssueTypesMetadata,
               mcp__atlassian_confluence_jira__createJiraIssue,
               mcp__atlassian_confluence_jira__lookupJiraAccountId
argument-hint: <pr-url> [--project PROJECT_KEY] [--assignee USERNAME] [--branch BRANCH]
description: Create standalone Jira code review ticket for a PR using hybrid approach
model: claude-sonnet-4-0
---

# Jira Code Review Ticket Creation

Create a standardized Jira code review ticket for an existing pull request. This hybrid command uses Python scripts to prepare ticket data and MCP tools for actual Jira integration.

## Arguments
- `pr-url`: Full URL of the pull request (required)
- `--project`: Jira project key (optional, will auto-detect if not provided)
- `--assignee`: Username to assign the ticket to (optional)
- `--branch`: Branch name if not detectable from PR URL (optional)

## Ticket Format
- **Type**: Task
- **Component**: Code Review
- **Story Points**: 1
- **Title**: `{repository} {branch} Code Review`
- **Description**: Pull request URL and details

## Current Context

**Repository**: !`basename $(git remote get-url origin) .git 2>/dev/null || echo "unknown"`
**Current Branch**: !`git branch --show-current`

## Workflow Execution

### Step 1: Parse Arguments and Extract PR Info

```bash
# Parse the PR URL and options
PR_URL="$1"
shift

# Initialize variables
PROJECT_KEY=""
ASSIGNEE=""
BRANCH_NAME=""

# Parse remaining options
while [[ $# -gt 0 ]]; do
  case $1 in
    --project)
      PROJECT_KEY="$2"
      shift 2
      ;;
    --assignee)
      ASSIGNEE="$2"
      shift 2
      ;;
    --branch)
      BRANCH_NAME="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: /jira-code-review <pr-url> [--project KEY] [--assignee USER] [--branch BRANCH]"
      exit 1
      ;;
  esac
done

# Validate PR URL
if [[ -z "$PR_URL" ]]; then
    echo "❌ Error: PR URL is required"
    echo "Usage: /jira-code-review <pr-url> [--project KEY] [--assignee USER] [--branch BRANCH]"
    exit 1
fi

echo "🎫 Creating Jira code review ticket for PR"
echo "   URL: $PR_URL"
```

### Step 2: Extract PR Information

Extract repository, PR ID, and branch from the URL:

```bash
# Parse PR URL to extract info
# Format: https://bitbucket.org/workspace/repository/pull-requests/123
if [[ "$PR_URL" =~ bitbucket\.org/([^/]+)/([^/]+)/pull-requests/([0-9]+) ]]; then
    WORKSPACE="${BASH_REMATCH[1]}"
    REPOSITORY="${BASH_REMATCH[2]}"
    PR_ID="${BASH_REMATCH[3]}"
    echo "   Repository: $REPOSITORY"
    echo "   PR ID: #$PR_ID"
else
    echo "⚠️  Warning: Could not parse PR URL format"
    # Try to get repository from git
    REPOSITORY=$(basename $(git remote get-url origin) .git 2>/dev/null || echo "repository")
    PR_ID="unknown"
fi

# If branch not provided, try to detect from current branch
if [[ -z "$BRANCH_NAME" ]]; then
    BRANCH_NAME=$(git branch --show-current 2>/dev/null || echo "feature-branch")
fi
echo "   Branch: $BRANCH_NAME"
```

### Step 3: Prepare Ticket Data

Use the Python script to prepare ticket data:

```bash
echo ""
echo "📝 Preparing ticket data..."

# Build command arguments
PREPARE_ARGS=(
    "--repository" "$REPOSITORY"
    "--branch" "$BRANCH_NAME"
    "--pr-url" "$PR_URL"
    "--pr-id" "$PR_ID"
    "--output-format" "json"
)

if [[ -n "$PROJECT_KEY" ]]; then
    PREPARE_ARGS+=("--project-key" "$PROJECT_KEY")
fi

# Prepare ticket data
TICKET_DATA=$(uv run .claude/scripts/bitbucket/create_code_review_ticket.py prepare-ticket "${PREPARE_ARGS[@]}" 2>&1)
PREPARE_EXIT=$?

if [[ $PREPARE_EXIT -ne 0 ]]; then
    echo "❌ Failed to prepare ticket data:"
    echo "$TICKET_DATA"
    exit 1
fi

# Extract ticket details
TICKET_TITLE=$(echo "$TICKET_DATA" | jq -r '.title // "Code Review Ticket"')
TICKET_DESC=$(echo "$TICKET_DATA" | jq -r '.description // "Pull request review"')

echo "   Title: $TICKET_TITLE"
```

### Step 4: Get Atlassian Cloud ID (MCP)

```bash
echo ""
echo "🔍 Getting Atlassian cloud resources..."
```

Use MCP to get cloud ID:
- Execute: `mcp__atlassian_confluence_jira__getAccessibleAtlassianResources`
- Extract cloud ID from response
- Store for subsequent operations

### Step 5: Determine Project (MCP)

```bash
if [[ -z "$PROJECT_KEY" ]]; then
    echo "🔍 Finding appropriate Jira project..."
```

Use MCP to find project:
- Execute: `mcp__atlassian_confluence_jira__getVisibleJiraProjects` with cloudId
- Select appropriate project based on permissions
- Extract project key

```bash
else
    echo "   Using specified project: $PROJECT_KEY"
fi
```

### Step 6: Get Issue Type Metadata (MCP)

```bash
echo "📋 Getting issue type metadata..."
```

Use MCP to get issue types:
- Execute: `mcp__atlassian_confluence_jira__getJiraProjectIssueTypesMetadata`
- Find "Task" issue type
- Extract required and optional fields

### Step 7: Lookup Assignee (Optional MCP)

```bash
if [[ -n "$ASSIGNEE" ]]; then
    echo "👤 Looking up assignee account ID..."
```

Use MCP to find user:
- Execute: `mcp__atlassian_confluence_jira__lookupJiraAccountId` with username
- Extract account ID for assignment

```bash
fi
```

### Step 8: Create Jira Ticket (MCP)

```bash
echo ""
echo "🎫 Creating Jira code review ticket..."
```

Use MCP to create ticket:
- Execute: `mcp__atlassian_confluence_jira__createJiraIssue` with:
  - cloudId
  - projectKey
  - issueTypeName: "Task"
  - summary: ticket title
  - description: ticket description with PR URL
  - additional_fields: components, story points
  - assignee_account_id (if provided)

### Step 9: Display Results

```bash
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ **Code Review Ticket Created Successfully**"
echo ""
echo "📋 **Ticket Details**:"
echo "   Project: $PROJECT_KEY"
echo "   Type: Task"
echo "   Component: Code Review"
echo "   Story Points: 1"
echo "   Title: $TICKET_TITLE"
echo ""
echo "🔗 **Links**:"
echo "   Pull Request: $PR_URL"
echo "   Jira Ticket: [URL from MCP response]"

if [[ -n "$ASSIGNEE" ]]; then
    echo ""
    echo "👤 **Assigned to**: $ASSIGNEE"
fi

echo ""
echo "🚀 **Next Steps**:"
echo "   1. Review the pull request"
echo "   2. Update ticket status as review progresses"
echo "   3. Log time spent on review"
echo "   4. Close ticket when PR is merged"
```

## Error Handling

### Python Script Errors
- **Missing dependencies**: Install with `uv pip install`
- **Invalid PR URL**: Check URL format
- **Parse failures**: Provide branch name manually with --branch

### MCP/Jira Errors
- **Authentication**: Ensure Atlassian MCP server is configured
- **Project not found**: Specify with --project flag
- **Permission denied**: Check Jira project permissions
- **Field validation**: Ensure required fields are provided

### Recovery Options
- Manual ticket creation instructions provided on failure
- Ticket data saved for retry
- Clear error messages with resolution steps

## Example Usage

```bash
# Basic usage with PR URL
/jira-code-review https://bitbucket.org/workspace/repo/pull-requests/123

# Specify project and assignee
/jira-code-review https://bitbucket.org/workspace/repo/pull-requests/123 --project PROJ --assignee john.doe

# Provide branch name explicitly
/jira-code-review https://bitbucket.org/workspace/repo/pull-requests/123 --branch feature-auth

# Full options
/jira-code-review https://bitbucket.org/workspace/repo/pull-requests/123 --project PROJ --assignee john.doe --branch main-123
```

## Success Criteria

- ✅ Extract PR information from URL
- ✅ Prepare standardized ticket data
- ✅ Create Jira ticket with correct format
- ✅ Link ticket to pull request
- ✅ Assign to appropriate reviewer
- ✅ Add required components and story points
- ✅ Provide clear success/error feedback
- ✅ Support manual project selection
---
allowed-tools: Bash(git:*), Bash(uv:*),
               mcp__atlassian_confluence_jira__searchJiraIssuesUsingJql,
               mcp__atlassian_confluence_jira__getAccessibleAtlassianResources
argument-hint: [pr-id] [--comments] [--jira] [--all]
description: Check Bitbucket PR status with optional Jira ticket integration (API token preferred)
model: claude-sonnet-4-0
---

# Hybrid PR Status Monitoring with Jira Integration

Check pull request status using direct Bitbucket API integration combined with optional Atlassian MCP server for Jira ticket correlation.

## Arguments
- `pr-id`: Specific PR ID to check (optional - shows list if omitted)

## Options
- `--comments`: Include PR comments in detailed view
- `--jira`: Search for linked Jira tickets (via MCP)
- `--all`: Show all PR states, not just OPEN

## Authentication

**Bitbucket**: Via .env file (API token preferred, app password fallback)
**Jira**: Via Atlassian MCP server

## Current Repository Context

**Current Branch**: !`git branch --show-current`
**Repository**: !`basename $(git remote get-url origin) .git 2>/dev/null || echo "repository"`

## Workflow Execution

### Step 1: Parse Arguments

```bash
# Parse arguments and options
PR_ID="$1"
INCLUDE_COMMENTS=false
CHECK_JIRA=false
SHOW_ALL=false

# Remove PR_ID from arguments if provided
if [[ -n "$PR_ID" && "$PR_ID" =~ ^[0-9]+$ ]]; then
    shift
else
    PR_ID=""
fi

# Parse remaining options
while [[ $# -gt 0 ]]; do
  case $1 in
    --comments)
      INCLUDE_COMMENTS=true
      shift
      ;;
    --jira)
      CHECK_JIRA=true
      shift
      ;;
    --all)
      SHOW_ALL=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: /pr-status-api [pr-id] [--comments] [--jira] [--all]"
      exit 1
      ;;
  esac
done
```

### Step 2: Retrieve PR Status (Python Script)

Execute status check via Bitbucket API:

```bash
echo "🔍 Checking pull request status..."

# Build command arguments
CMD_ARGS=()

if [[ -n "$PR_ID" ]]; then
    CMD_ARGS+=(--pr-id "$PR_ID")
    echo "📋 Retrieving details for PR #$PR_ID"
else
    echo "📋 Listing pull requests for repository"
fi

if [[ "$INCLUDE_COMMENTS" == "true" ]]; then
    CMD_ARGS+=(--comments)
fi

if [[ "$SHOW_ALL" == "true" ]]; then
    CMD_ARGS+=(--all-states)
fi

# Execute Python script
PR_STATUS_RESULT=$(uv run .claude/scripts/bitbucket/pr_status_api.py check-status "${CMD_ARGS[@]}" 2>&1)
PR_EXIT_CODE=$?

if [[ $PR_EXIT_CODE -ne 0 ]]; then
    echo "❌ Failed to retrieve PR status:"
    echo "$PR_STATUS_RESULT"
    exit 1
fi

# Parse results
MODE=$(echo "$PR_STATUS_RESULT" | jq -r '.mode // "unknown"' 2>/dev/null)
SUCCESS=$(echo "$PR_STATUS_RESULT" | jq -r '.success // false' 2>/dev/null)

if [[ "$SUCCESS" != "true" ]]; then
    echo "❌ Error retrieving PR status"
    echo "$PR_STATUS_RESULT" | jq -r '.error // "Unknown error"' 2>/dev/null
    exit 1
fi
```

### Step 3: Display PR Information

Display results based on mode (list vs detail):

```bash
if [[ "$MODE" == "detail" ]]; then
    # Detailed PR view
    echo ""
    echo "$PR_STATUS_RESULT" | jq -r '.formatted_output // "No output available"'
    
    # Show comments if requested
    if [[ "$INCLUDE_COMMENTS" == "true" ]]; then
        COMMENTS_OUTPUT=$(echo "$PR_STATUS_RESULT" | jq -r '.comments // null')
        if [[ "$COMMENTS_OUTPUT" != "null" && -n "$COMMENTS_OUTPUT" ]]; then
            echo ""
            echo "$COMMENTS_OUTPUT"
        fi
    fi
    
    # Extract PR info for Jira search
    PR_URL=$(echo "$PR_STATUS_RESULT" | jq -r '.pr.url // ""')
    SOURCE_BRANCH=$(echo "$PR_STATUS_RESULT" | jq -r '.pr.source_branch // ""')
    
elif [[ "$MODE" == "list" ]]; then
    # List view
    echo ""
    echo "Recent PRs for repository:"
    echo "$PR_STATUS_RESULT" | jq -r '.formatted_output // "No PRs found"'
    
    # Check for current branch PR
    CURRENT_BRANCH=$(echo "$PR_STATUS_RESULT" | jq -r '.current_branch // null')
    CURRENT_PR_ID=$(echo "$PR_STATUS_RESULT" | jq -r '.current_branch_pr.id // null')
    CURRENT_PR_URL=$(echo "$PR_STATUS_RESULT" | jq -r '.current_branch_pr.url // null')
    
    if [[ "$CURRENT_BRANCH" != "null" && "$CURRENT_PR_ID" != "null" ]]; then
        echo ""
        echo "🌿 Current branch: $CURRENT_BRANCH"
        echo "   └── PR #$CURRENT_PR_ID: $CURRENT_PR_URL"
    elif [[ "$CURRENT_BRANCH" != "null" ]]; then
        echo ""
        echo "🌿 Current branch: $CURRENT_BRANCH (no associated PR found)"
    fi
fi
```

### Step 4: Jira Integration (Optional MCP)

Search for related Jira tickets if requested:

```bash
if [[ "$CHECK_JIRA" == "true" ]]; then
    echo ""
    echo "🎫 Searching for related Jira tickets..."
    
    # For detail mode, search for specific PR
    if [[ "$MODE" == "detail" && -n "$PR_URL" ]]; then
        echo "   Searching for tickets containing PR URL..."
        
        # Build JQL query
        JQL_QUERY="description ~ \"$PR_URL\" OR comment ~ \"$PR_URL\""
        
        # If we have branch name, also search for code review tickets
        if [[ -n "$SOURCE_BRANCH" ]]; then
            REPO_NAME=$(basename $(git remote get-url origin) .git 2>/dev/null || echo "repo")
            REVIEW_TITLE="$REPO_NAME $SOURCE_BRANCH Code Review"
            JQL_QUERY="$JQL_QUERY OR summary ~ \"$REVIEW_TITLE\""
        fi
        
        echo "   JQL Query: $JQL_QUERY"
```

Execute MCP search for Jira tickets:

```bash
        # Use MCP to search for tickets (pseudo-code for MCP integration)
        # 1. Get cloud ID
        # 2. Search using JQL
        # 3. Display results
        
        echo "   Note: Execute MCP tools here for Jira search"
        echo "   - mcp__atlassian_confluence_jira__getAccessibleAtlassianResources"
        echo "   - mcp__atlassian_confluence_jira__searchJiraIssuesUsingJql"
    
    elif [[ "$MODE" == "list" ]]; then
        # For list mode, general search for code review tickets
        echo "   Searching for open code review tickets..."
        
        JQL_QUERY="component = \"Code Review\" AND status != Done"
        echo "   JQL Query: $JQL_QUERY"
        
        # Execute MCP search
        echo "   Note: Execute MCP tools here for Jira search"
    fi
fi
```

### Step 5: Summary and Next Steps

```bash
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [[ "$MODE" == "detail" ]]; then
    # Get review status
    REVIEW_SUMMARY=$(echo "$PR_STATUS_RESULT" | jq -r '.pr.review_status.summary // "No reviews"')
    PR_STATE=$(echo "$PR_STATUS_RESULT" | jq -r '.pr.state // "UNKNOWN"')
    
    echo "📊 **Status Summary**:"
    echo "   State: $PR_STATE"
    echo "   Reviews: $REVIEW_SUMMARY"
    
    if [[ "$PR_STATE" == "OPEN" ]]; then
        echo ""
        echo "🚀 **Next Steps**:"
        
        # Check if changes requested
        CHANGES_REQUESTED=$(echo "$PR_STATUS_RESULT" | jq -r '.pr.review_status.changes_requested | length' 2>/dev/null)
        if [[ "$CHANGES_REQUESTED" -gt 0 ]]; then
            echo "   1. Address requested changes from reviewers"
            echo "   2. Push updates to the source branch"
            echo "   3. Request re-review when ready"
        else
            PENDING_COUNT=$(echo "$PR_STATUS_RESULT" | jq -r '.pr.review_status.pending | length' 2>/dev/null)
            if [[ "$PENDING_COUNT" -gt 0 ]]; then
                echo "   1. Wait for pending reviews to complete"
                echo "   2. Address any feedback received"
            else
                echo "   1. PR is approved and ready to merge"
                echo "   2. Ensure CI/CD checks pass"
                echo "   3. Merge when ready"
            fi
        fi
    elif [[ "$PR_STATE" == "MERGED" ]]; then
        echo "   ✅ This PR has been merged"
    elif [[ "$PR_STATE" == "DECLINED" ]]; then
        echo "   ❌ This PR has been declined"
    fi
    
else
    # List mode summary
    OPEN_COUNT=$(echo "$PR_STATUS_RESULT" | jq '[.prs[] | select(.state == "OPEN")] | length' 2>/dev/null)
    TOTAL_COUNT=$(echo "$PR_STATUS_RESULT" | jq '.prs | length' 2>/dev/null)
    
    echo "📊 **Repository Summary**:"
    echo "   Total PRs shown: $TOTAL_COUNT"
    if [[ "$SHOW_ALL" != "true" ]]; then
        echo "   Open PRs: $OPEN_COUNT"
    fi
    
    echo ""
    echo "💡 **Quick Actions**:"
    echo "   • View specific PR: /pr-status-api [pr-id]"
    echo "   • Include comments: /pr-status-api [pr-id] --comments"
    echo "   • Check Jira tickets: /pr-status-api --jira"
    echo "   • Show all states: /pr-status-api --all"
fi
```

## Error Handling

### Bitbucket API Errors
- **Authentication**: Check BITBUCKET_API_TOKEN or BITBUCKET_APP_PASSWORD
- **PR Not Found**: Verify PR ID exists in repository
- **Repository Access**: Ensure proper workspace/repository permissions
- **Rate Limiting**: Wait and retry with exponential backoff

### MCP/Jira Errors  
- **MCP Unavailable**: Show PR info without Jira data
- **Search Failures**: Note issue but continue with PR display
- **No Results**: Indicate no linked Jira tickets found

### Git Context Errors
- **No Repository**: Basic PR lookup without branch context
- **No Remote**: Manual workspace/repository specification needed

## Example Usage

```bash
# List all open PRs
/pr-status-api

# Check specific PR with details
/pr-status-api 123

# Include comments in PR view
/pr-status-api 123 --comments

# Search for linked Jira tickets
/pr-status-api 123 --jira

# Show all PR states
/pr-status-api --all

# Full detailed view with everything
/pr-status-api 123 --comments --jira

# List view with Jira search
/pr-status-api --jira --all
```

## Output Examples

### List View
```
Recent PRs for repository:
┌─────────────────────────────────────────────────────────────────────────────┐
│ #123 │ Feature Implementation        │ OPEN      │ ✅ 2 ⏳ 1 (2/3)      │
│ #122 │ Bug fix for login            │ MERGED    │ ✅ 3 (3/3)           │
│ #121 │ Update documentation         │ DECLINED  │ ❌ 1 ⏳ 1 (0/2)      │
└─────────────────────────────────────────────────────────────────────────────┘

🌿 Current branch: feature/auth-improvements (no associated PR found)
```

### Detailed View
```
PR #123: Feature Implementation
├── Status: OPEN
├── Author: john.doe
├── Source: feature-branch → development
├── Reviewers:
│   ├── ✅ jane.smith (approved)
│   ├── ⏳ bob.jones (pending)
│   └── ❌ alice.wilson (requested changes)
├── Comments: 5 total (3 resolved, 2 active)
├── Commits: 7 commits
└── URL: https://bitbucket.org/workspace/repo/pull-requests/123

💬 Comments:
├── alice.wilson
│   └── "Please add input validation for edge cases"
└── john.doe
    └── "Good point, I'll add that validation"
```

## Success Criteria

- ✅ List PRs with clear status indicators
- ✅ Show detailed PR information with review status
- ✅ Display comment threads in readable format
- ✅ Integrate Jira ticket information when requested
- ✅ Handle all PR states (open, merged, declined)
- ✅ Provide actionable next steps based on PR status
- ✅ Clear error messages with recovery suggestions
- ✅ Support both API tokens and app passwords
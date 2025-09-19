---
allowed-tools: Bash(git:*), mcp__bitbucket, mcp__atlassian_confluence_jira
argument-hint: [pr-id] [--comments] [--jira]
description: Check Bitbucket PR status, reviews, comments, and linked Jira tickets
model: claude-sonnet-4-0
---

# Pull Request Status Check with Jira Integration

Check the status of pull requests in the current repository, including review status, comments, and linked Jira code review tickets.

## Arguments
- `pr-id`: Specific PR ID to check (optional - if not provided, shows recent PRs)
- `--comments`: Include comments in the output (optional)
- `--jira`: Check for linked Jira code review tickets (optional)

## Current Repository Context

**Current Branch**: !`git branch --show-current`

**Repository Remote**: !`git remote get-url origin`

## Your Tasks

1. **Repository Detection**:
   - Extract workspace and repository from git remote URL
   - Validate Bitbucket connectivity

2. **PR Status Check**:
   - If `pr-id` provided: Get detailed status for specific PR
   - If no `pr-id`: List recent open PRs for current repository
   - Show PR details:
     - Title and description
     - Source and destination branches
     - Author and creation date
     - Review status (approved, needs changes, pending)
     - Reviewers and their status

3. **Comments Review** (if `--comments` flag used):
   - Retrieve and display PR comments
   - Show inline code comments with file/line references
   - Organize by comment thread and timestamp

4. **Jira Ticket Lookup** (if `--jira` flag used):
   - Get Atlassian cloud ID using `getAccessibleAtlassianResources`
   - Search for code review tickets using JQL:
     - Search for tickets with PR URL in description
     - Search for tickets with branch name in title
     - Look for "Code Review" component tickets
   - Display linked ticket status and assignee

5. **Branch Relationship**:
   - If current branch matches a PR source branch, highlight that PR
   - Show if current branch has an associated PR

## Output Format

### For Single PR:
```
PR #123: Feature Implementation
├── Status: OPEN
├── Author: john.doe
├── Source: feature-branch → development  
├── Created: 2 days ago
├── Reviewers:
│   ├── ✅ jane.smith (approved)
│   ├── ⏳ bob.jones (pending)
│   └── ❌ alice.wilson (requested changes)
├── Comments: 5 total (3 resolved, 2 active)
└── 🎫 Jira Ticket: PROJ-456 (Code Review) - IN PROGRESS - Assigned: jane.smith
```

### For PR List:
```
Recent PRs for repository:
┌────────────────────────────────────────────────────────────┐
│ #123 | Feature Implementation        | OPEN     | 2d ago    │
│ #122 | Bug fix for login            | MERGED   | 1w ago    │  
│ #121 | Update documentation         | DECLINED | 2w ago    │
└────────────────────────────────────────────────────────────┘
```

## Success Criteria
- Clear PR status overview with all relevant information
- Review status for each reviewer with visual indicators
- Comments organized and readable (if requested)
- Jira ticket status and assignee information (if --jira flag used)
- Branch relationship detection and highlighting
- Actionable insights for next steps
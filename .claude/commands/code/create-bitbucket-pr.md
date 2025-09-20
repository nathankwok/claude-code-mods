---
allowed-tools: Bash(git:*), mcp__bitbucket, mcp__atlassian_confluence_jira
argument-hint: [destination-branch] [jira-project-ticket] [reviewers...] [--force]
description: Create Bitbucket PR following Git Flow with feature branch naming and automatic Jira code review ticket creation
model: claude-sonnet-4-0
---

# Bitbucket Pull Request Creation with Jira Integration

Create a pull request following Git Flow standards with proper feature branch naming, readiness validation, squash merge configuration, and automatic Jira code review ticket creation for production branches.

## Arguments
- `destination-branch`: Target branch (e.g., "main", "development")
- `jira-project-ticket`: Full Jira ticket (e.g., "DATAENG-123") or just ticket number if project can be inferred
- `reviewers`: Comma-separated list of reviewer usernames (optional)
- `--force`: Skip PR readiness validation checks (optional)

## Workflow Context

**Branch Naming Convention**: `feature/<jira-project>-<ticket-number>`
**Example**: For ticket DATAENG-123 → branch name: `feature/DATAENG-123`

## Pull Request Template

The following template must be used for all pull requests' description (from Git Flow documentation):

```markdown
# Summary
<!-- Provide a concise description of the changes in this PR -->

# Related Tickets
<!-- List links to the related ticket(s) -->

# Test Instructions
<!-- Detailed instructions for reviewers to test the feature end-to-end -->

# Notes
<!-- Optional: any additional context, caveats, or references -->
```

## Code Review Ticket Format
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
   - Ensure destination branch and jira ticket are provided
   - Parse Jira project and ticket number from input (e.g., DATAENG-123)
   - Parse reviewers list and --force flag if provided
   - Extract repository name from git remote

2. **PR Readiness Validation** (skip if --force used):
   - Check if there are uncommitted changes
   - Confirm all changes have been tested according to repo-specific guidelines
   - Warn about Git Flow requirement: "Only open PRs when ready for final review"
   - Prompt user to confirm readiness or suggest closing/reopening if changes needed

3. **Branch Management**:
   - If the branch exists, check if git is already on that branch (likely). If not, then checkout the branch and ensure it's up to date with main by merging main to the branch
   - If the branch does not exist, create branch with Git Flow naming: `feature/{jira-project}-{ticket-number}`. Then push branch to remote with upstream tracking

4. **Populate Pull Request Template**:
   - **CRITICAL**: Use the official Git Flow PR template for description (see template above)
   - Auto-populate template sections where possible:
     - Summary: Brief description of changes
     - Related Tickets: Link to Jira ticket from branch name
     - Proof of Functionality: Prompt user for evidence. User might choose to ignore this to do this step manually at a later point in time.
     - Test Instructions: Include basic testing steps
     - Notes: Any additional context
   - **CRITICAL**: Print the populated Pull Request Template. Stop here before continuing to steps 5 and beyond, in order for the user to review the populated Pull Request Template. 
   - **CRITICAL**: Do not continue until the user has given the approval for this populated template to be used. User may have feedback to incorporate.

5. **Create Pull Request using Populated Pull Request Template**:
   - Use the Bitbucket MCP tool to get the repository based on the current project and project root directory. The project root directory is usually the repository name.
   - Use Bitbucket MCP tools to create PR
   - Add reviewers if specified
   - Set destination branch correctly
   - Capture PR URL from response

6. **Jira Code Review Ticket Creation**:
   - **For production branches (main/master/release):**
     a. Get Atlassian cloud ID using `getAccessibleAtlassianResources`
     b. Find appropriate Jira project:
        - Extract project from jira-project-ticket (e.g., DATAENG from DATAENG-123)
        - Default to DATAENG if no project is given
        - Validate project exists in visible projects
     c. Get issue type metadata to find "Task" type
     d. Create Jira ticket with exact specifications:
        - **Issue Type**: Task
        - **Component**: Code Review (use `additional_fields` if needed)
        - **Summary**: `{repo-name} {full-branch-name} Code Review`
        - **Description**: `Pull Request: {pr-url}`
        - **Story Points**: 1 (use `additional_fields`)
     e. If reviewers specified, lookup their Jira account IDs and assign
   - **For development branches**: Note that code review is optional

7. **Error Handling**:
   - If Jira ticket creation fails, still report PR success
   - Provide manual ticket creation instructions as fallback
   - Log specific error details for troubleshooting

8. **Output Summary**:
   - ✅ Branch created: `feature/{jira-project}-{ticket-number}`
   - ✅ Pull Request created: `{pr-url}`
   - ⚙️ Squash merge configured (for main branch PRs)
   - ✅ Code Review Ticket created: `{jira-ticket-url}` (for production branches)
   - 📋 Ticket Details: Title, Component, Story Points
   - 📝 Git Flow reminder: Only close/reopen PR if further changes needed before review
   - 📝 Next steps and review assignments

## Template Requirements

**Required Sections** (must be present in PR description):
- ✅ **Summary**: Concise description of changes. do not look at the git commit message history to create this summary. If a file has been added or changed, you must look at the whole file, as well as the diffs for those files.  
- ✅ **Related Tickets**: Links to Jira tickets
- ✅ **Proof of Functionality**: Evidence that changes work
- ✅ **Test Instructions**: How reviewers can test
- ⚠️ **Notes**: Optional additional context

**Template Auto-Population**:
- Extract Jira ticket from branch name for Related Tickets section
- Generate basic summary from new or changed files and their diffs
- Prompt user for Proof of Functionality and Test Instructions
- Include template comments as guidance

## Success Criteria
- Branch created with Git Flow naming convention: `feature/{jira-project}-{ticket-number}`
- PR readiness validated (unless --force used)
- PR created with **official Git Flow template** properly populated
- All required template sections completed
- Proper metadata, reviewers, and squash merge for main branch
- Jira code review ticket automatically created for production branches
- Ticket follows exact Git Flow format specifications
- User warned about Git Flow PR guidelines (ready for final review)
- Clear, actionable output with all relevant URLs
- Graceful error handling with fallback instructions
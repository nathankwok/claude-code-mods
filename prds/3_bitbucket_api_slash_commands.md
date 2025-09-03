# Product Requirements Document: Hybrid Bitbucket API & Atlassian MCP Integration

## Document Information
- **Version**: 2.0
- **Date**: 2025-08-31
- **Author**: System Architect
- **Status**: Draft - Awaiting Approval

## 1. Executive Summary

This PRD outlines the implementation of three new Claude Code slash commands that use a hybrid approach: direct Bitbucket API integration for repository and pull request operations, while leveraging the existing Atlassian Confluence/Jira MCP server for Jira ticket management. This approach eliminates dependency on the Bitbucket MCP server while maintaining the robust Jira integration already available through MCP.

## 2. Problem Statement

### Current State
- Existing Bitbucket slash commands rely on Bitbucket MCP server integration
- Bitbucket MCP server creates an unnecessary abstraction layer
- Limited visibility into Bitbucket API interactions
- Bitbucket credential management tied to MCP configuration
- Atlassian Confluence/Jira MCP server works well for Jira operations

### Challenges
- Bitbucket MCP server availability and maintenance overhead
- Debugging complexity for Bitbucket operations
- Limited customization of Bitbucket API interaction logic
- Indirect control over Bitbucket authentication and error handling

### Opportunity
Create hybrid integration that provides:
- Direct Bitbucket API control for repository operations
- Continued use of proven Atlassian MCP for Jira operations
- Transparent error handling for Bitbucket operations
- Flexible Bitbucket credential management via environment variables
- Maintains existing Jira integration without changes

## 3. Solution Overview

### Approach
Implement a hybrid solution: Python scripts using the `atlassian-python-api` library for direct Bitbucket API interaction, while continuing to use the Atlassian Confluence/Jira MCP server for all Jira operations.

### Why Hybrid?
- **Best of Both Worlds**: Direct control over Bitbucket operations, proven MCP for Jira
- **Minimal Changes**: Keeps working Jira integration intact
- **Reduced Complexity**: No need to reimplement Jira authentication and API logic
- **Faster Implementation**: Focus only on Bitbucket API integration
- **Maintainability**: Separate concerns between repository and issue tracking

### Key Components
1. **Python Scripts**: UV single-file scripts for Bitbucket operations
2. **MCP Integration**: Existing Atlassian MCP server for Jira operations
3. **Environment Configuration**: Bitbucket credentials in `.env` file
4. **Slash Commands**: New hybrid commands with `-api` suffix
5. **Shared Utilities**: Common functions for Bitbucket operations

### Hybrid Execution Flow
1. User invokes slash command
2. Command determines operation type:
   - **Bitbucket operations** → Python script via UV
   - **Jira operations** → MCP tools directly
3. Results combined and presented to user

## 4. User Stories

### Story 1: Developer Creates Pull Request
**As a** developer  
**I want to** create a pull request using a slash command  
**So that** I can quickly submit code for review without leaving my development environment

**Acceptance Criteria:**
- Command creates branch with proper naming convention
- Pull request is created with title and description
- Reviewers are assigned if specified
- Jira ticket is created for production branches
- Success/failure is clearly communicated

### Story 2: Developer Checks PR Status
**As a** developer  
**I want to** check the status of pull requests  
**So that** I can track review progress and address feedback

**Acceptance Criteria:**
- Command shows PR state and review status
- Reviewer approval/rejection status is visible
- Comments can be retrieved if requested
- Linked Jira tickets are displayed
- Output is formatted for easy reading

### Story 3: Team Lead Creates Code Review Tickets
**As a** team lead  
**I want to** create Jira code review tickets for PRs  
**So that** code reviews are tracked in our sprint planning

**Acceptance Criteria:**
- Command creates properly formatted Jira ticket
- Ticket includes PR link and branch information
- Story points and component are set correctly
- Assignee can be specified
- Ticket URL is returned for reference

## 5. Technical Architecture

### System Design

```
┌─────────────────────────────────────────────────────────┐
│                   Claude Code CLI                        │
├─────────────────────────────────────────────────────────┤
│                   Slash Commands                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ /bitbucket- │  │ /pr-status- │  │ /create-    │    │
│  │ pr-api      │  │ api         │  │ code-review-│    │
│  │             │  │             │  │ ticket-api  │    │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘    │
│         │                 │                 │           │
├─────────┼─────────────────┼─────────────────┼───────────┤
│         ▼                 ▼                 ▼           │
│              Python Scripts + MCP Hybrid                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ bitbucket_  │  │ pr_status_  │  │   Hybrid:   │    │
│  │ pr_api.py   │  │ api.py      │  │ Python +    │    │
│  │ (Python)    │  │ (Python)    │  │ MCP Tools   │    │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘    │
│         │                 │                 │           │
│         └─────────────────┼─────────────────┼───────────┤
│                           ▼                 ▼           │
│           ┌─────────────────┐    ┌──────────────────┐  │
│           │ bitbucket_utils │    │ Atlassian MCP    │  │
│           │      .py         │    │ Server Tools     │  │
│           └────────┬────────┘    └────────┬─────────┘  │
├───────────────────┼───────────────────────┼─────────────┤
│                   ▼                       ▼             │
│         ┌─────────────┐         ┌──────────────┐       │
│         │   .env file  │         │ MCP Config   │       │
│         └──────┬──────┘         └──────┬───────┘       │
│                │                        │               │
├────────────────┼────────────────────────┼───────────────┤
│                ▼                        ▼               │
│                   External Services                      │
│  ┌─────────────────────────────────────────────┐      │
│  │          Bitbucket API v2.0                  │      │
│  │          (Direct via Python)                 │      │
│  └─────────────────────────────────────────────┘      │
│  ┌─────────────────────────────────────────────┐      │
│  │      Atlassian Jira (via MCP Server)         │      │
│  └─────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────┘
```

### Directory Structure

```
claude-code-mods/
├── .env.example                    # Template for environment variables
├── .env                           # Actual credentials (gitignored)
├── .claude/
│   ├── commands/
│   │   ├── bitbucket-pr-api.md       # PR creation command
│   │   ├── pr-status-api.md          # Status check command
│   │   └── create-code-review-ticket-api.md  # Jira ticket command
│   └── scripts/
│       └── bitbucket/
│           ├── bitbucket_utils.py     # Shared Bitbucket utilities
│           ├── bitbucket_pr_api.py    # PR creation logic
│           └── pr_status_api.py       # Status checking logic
└── prds/
    └── 3_bitbucket_api_slash_commands.md  # This document
```

### Technology Stack

| Component | Technology | Justification |
|-----------|------------|---------------|
| Language | Python 3.8+ | Mature ecosystem, excellent API libraries |
| Package Manager | UV | Fast, reliable, single-file script support |
| Bitbucket Library | atlassian-python-api | Well-maintained, comprehensive coverage |
| Jira Integration | Atlassian MCP Server | Existing, proven integration |
| Environment Management | python-dotenv | Standard for environment variables |
| Authentication | Hybrid (API + MCP) | Bitbucket via env vars, Jira via MCP |

## 6. Implementation Phases

### Phase 1: Foundation and Setup
**Duration**: 1 day  
**Dependencies**: None

**Deliverables:**
1. `.env.example` template with Bitbucket variables
2. Directory structure creation
3. `bitbucket_utils.py` with:
   - Environment variable loading for Bitbucket
   - Bitbucket client initialization
   - Git remote parsing
   - Common error handling
   - Logging configuration

**Tasks:**
- [ ] Create `.env.example` with Bitbucket configuration
- [ ] Set up directory structure
- [ ] Implement environment loading utility
- [ ] Create Bitbucket client wrapper
- [ ] Add git remote detection logic
- [ ] Implement error handling framework
- [ ] Set up logging

### Phase 2: Pull Request Creation
**Duration**: 1 day  
**Dependencies**: Phase 1

**Deliverables:**
1. `bitbucket_pr_api.py` script
2. `/bitbucket-pr-api` slash command

**Tasks:**
- [ ] Implement branch creation with naming convention
- [ ] Add git operations (checkout, commit, push)
- [ ] Create PR via Bitbucket API with metadata
- [ ] Implement reviewer assignment
- [ ] Integrate MCP tools for Jira ticket creation
- [ ] Create hybrid slash command definition
- [ ] Test end-to-end workflow

### Phase 3: PR Status Monitoring
**Duration**: 1 day  
**Dependencies**: Phase 1

**Deliverables:**
1. `pr_status_api.py` script
2. `/pr-status-api` slash command

**Tasks:**
- [ ] Implement PR list retrieval
- [ ] Add detailed PR information fetching
- [ ] Create comment retrieval logic
- [ ] Implement review status parsing
- [ ] Add visual formatting for output
- [ ] Create slash command definition
- [ ] Test various PR states

### Phase 4: Hybrid Jira Integration
**Duration**: 1 day  
**Dependencies**: Phase 1

**Deliverables:**
1. `/create-code-review-ticket-api` slash command (MCP-based)
2. `/bitbucket-pr-api` Jira integration (MCP-based)

**Tasks:**
- [ ] Configure MCP tool permissions in commands
- [ ] Implement MCP tool calls for project discovery
- [ ] Add MCP-based issue type metadata retrieval
- [ ] Create ticket via MCP with proper format
- [ ] Implement assignee lookup via MCP
- [ ] Create hybrid slash command definitions
- [ ] Test MCP-Python integration workflow

### Phase 5: Testing and Documentation
**Duration**: 1 day  
**Dependencies**: Phases 2-4

**Deliverables:**
1. Updated README.md
2. Troubleshooting guide
3. Test results documentation

**Tasks:**
- [ ] Perform integration testing
- [ ] Add comprehensive error handling
- [ ] Update README with new commands
- [ ] Create setup instructions
- [ ] Document troubleshooting steps
- [ ] Add usage examples
- [ ] Performance optimization

## 7. API Specifications

### Environment Variables

```bash
# Bitbucket Configuration (Direct API)
BITBUCKET_URL=https://api.bitbucket.org  # or your server URL
BITBUCKET_USERNAME=your_username
BITBUCKET_APP_PASSWORD=your_app_password  # or API token
BITBUCKET_WORKSPACE=your_workspace  # optional, can be detected

# Jira Configuration handled by MCP Server
# No Jira credentials needed in .env file
# Configured via Atlassian MCP server settings

# Optional Configuration
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
CACHE_ENABLED=true  # Enable response caching
CACHE_TTL=300  # Cache TTL in seconds
```

### Command Interfaces

#### `/bitbucket-pr-api`
```bash
/bitbucket-pr-api [destination-branch] [ticket-number] [reviewers] [options]

Arguments:
  destination-branch  Target branch (required)
  ticket-number      Ticket number for branch name (required)
  reviewers          Comma-separated usernames (optional)

Options:
  --jira-project     Jira project key for code review ticket (via MCP)
  --no-jira          Skip Jira ticket creation
  --draft            Create as draft PR

Allowed Tools:
  - Python script for Bitbucket operations
  - MCP tools: mcp__atlassian_confluence_jira__* for Jira operations
```

#### `/pr-status-api`
```bash
/pr-status-api [pr-id] [options]

Arguments:
  pr-id              Specific PR ID (optional, shows list if omitted)

Options:
  --comments         Include PR comments (via Bitbucket API)
  --jira            Check for linked Jira tickets (via MCP)
  --all             Show all PRs (not just open)

Allowed Tools:
  - Python script for Bitbucket operations
  - MCP tools: mcp__atlassian_confluence_jira__searchJiraIssuesUsingJql (if --jira)
```

#### `/create-code-review-ticket-api`
```bash
/create-code-review-ticket-api [pr-url] [options]

Arguments:
  pr-url            Pull request URL (required)

Options:
  --branch-name     Override branch name detection
  --jira-project    Specify Jira project key
  --assignee        Email or username of assignee
  --story-points    Override default story points (1)

Allowed Tools:
  - MCP tools only:
    - mcp__atlassian_confluence_jira__getAccessibleAtlassianResources
    - mcp__atlassian_confluence_jira__getVisibleJiraProjects
    - mcp__atlassian_confluence_jira__getJiraProjectIssueTypesMetadata
    - mcp__atlassian_confluence_jira__createJiraIssue
    - mcp__atlassian_confluence_jira__lookupJiraAccountId
```

## 8. Error Handling

### Error Categories

| Category | Handling Strategy | User Message Example |
|----------|------------------|---------------------|
| Authentication | Guide to credential setup | "Authentication failed. Please check your BITBUCKET_APP_PASSWORD in .env" |
| Network | Retry with backoff | "Network error. Retrying... (attempt 2/3)" |
| API Rate Limit | Wait and retry | "Rate limit reached. Waiting 60 seconds..." |
| Configuration | Setup instructions | "Missing BITBUCKET_WORKSPACE. Please add to .env file" |
| Permission | Check access rights | "Insufficient permissions to create PR. Check repository access" |
| Validation | Clear requirements | "Invalid branch name. Must follow pattern: {destination}-{ticket}" |

### Logging Strategy

```python
# Log Levels
DEBUG   - API request/response details
INFO    - Command execution flow
WARNING - Recoverable errors
ERROR   - Command failures
```

## 9. Security Considerations

### Credential Management
- Credentials stored in `.env` file (gitignored)
- Never log sensitive information
- Support token rotation without code changes
- Validate credential format before use

### API Security
- Use HTTPS for all API calls
- Implement request signing where available
- Rate limit compliance
- Timeout on long-running operations

### Data Protection
- Sanitize user input
- Validate PR URLs and branch names
- Prevent injection attacks
- Limit data exposure in error messages

## 10. Success Metrics

### Functional Metrics
- [ ] All three commands execute successfully
- [ ] Feature parity with MCP versions maintained
- [ ] Error messages provide actionable guidance
- [ ] Commands work across different repositories

### Performance Metrics
- [ ] Response time < 5 seconds for typical operations
- [ ] API calls optimized (batch where possible)
- [ ] Caching reduces redundant API calls
- [ ] Resource usage within acceptable limits

### Quality Metrics
- [ ] Zero credential exposure in logs
- [ ] All errors handled gracefully
- [ ] Commands are idempotent where applicable
- [ ] Documentation is complete and accurate

## 11. Testing Strategy

### Unit Tests
- Test Bitbucket utility functions independently
- Mock Bitbucket API responses for predictable testing
- Validate error handling paths
- Test edge cases and boundary conditions

### Integration Tests
- Test full command execution flow
- Verify Bitbucket API integration with test account
- Test MCP tool calls for Jira operations
- Validate hybrid Python-MCP interaction
- Test with various repository configurations

### User Acceptance Tests
- Create PR with standard workflow
- Check PR status for various states
- Create code review ticket for production branch
- Test error scenarios and recovery

## 12. Migration Plan

### Transition Strategy
1. Deploy hybrid commands alongside existing full-MCP versions
2. Commands use `-api` suffix to avoid conflicts
3. Users can test hybrid approach without disruption
4. Gradual migration based on user feedback
5. Deprecate Bitbucket MCP dependency after validation
6. Maintain Atlassian MCP for Jira operations

### Rollback Plan
- Keep MCP commands available during transition
- Document both command sets
- Provide clear migration guide
- Support period for questions and issues

## 13. Future Enhancements

### Potential Features
- Bulk PR operations
- PR merge capabilities
- Automated PR descriptions from commits
- Integration with CI/CD status
- Custom workflow automation
- PR template support
- Advanced Jira field mapping
- Multiple repository support
- PR analytics and reporting

## 14. Risks and Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| App password deprecation | High | High | Support both app passwords and API tokens |
| Bitbucket API breaking changes | High | Low | Version lock atlassian-python-api library |
| MCP server unavailability | Medium | Low | Jira operations fail gracefully with clear messages |
| Rate limiting issues | Medium | Medium | Implement caching and rate limit handling |
| Credential exposure | High | Low | Strict logging controls, security review |
| Python-MCP integration issues | Medium | Medium | Thorough testing of hybrid approach |

## 15. Approval and Sign-off

### Stakeholders
- Development Team Lead
- Security Review
- Infrastructure Team
- End Users Representative

### Approval Criteria
- Technical design reviewed and approved
- Security considerations addressed
- Resource requirements confirmed
- Timeline accepted
- Success metrics agreed upon

---

## Appendix A: API Examples

### Bitbucket PR Creation (Python)
```python
from atlassian import Bitbucket
import os
from dotenv import load_dotenv

load_dotenv()

bitbucket = Bitbucket(
    url=os.getenv('BITBUCKET_URL'),
    username=os.getenv('BITBUCKET_USERNAME'),
    password=os.getenv('BITBUCKET_APP_PASSWORD')
)

pr = bitbucket.open_pull_request(
    source_project='workspace',
    source_repo='repo',
    dest_project='workspace', 
    dest_repo='repo',
    source_branch='refs/heads/feature',
    destination_branch='refs/heads/main',
    title='PR Title',
    description='PR Description'
)
```

### Jira Ticket Creation (via MCP)
```yaml
# In slash command file:
allowed-tools: mcp__atlassian_confluence_jira__createJiraIssue,
               mcp__atlassian_confluence_jira__getVisibleJiraProjects,
               mcp__atlassian_confluence_jira__lookupJiraAccountId

# The command will use MCP tools directly:
# No Python code needed for Jira operations
```

## Appendix B: Command Examples

### Creating a Pull Request
```bash
# Basic usage
/bitbucket-pr-api development 123

# With reviewers
/bitbucket-pr-api main 456 @john,@jane

# With Jira project specified
/bitbucket-pr-api production 789 @team --jira-project PROJ

# As draft without Jira
/bitbucket-pr-api feature 321 --draft --no-jira
```

### Checking PR Status
```bash
# List all open PRs
/pr-status-api

# Check specific PR
/pr-status-api 123

# With comments and Jira
/pr-status-api 123 --comments --jira

# Show all PRs including closed
/pr-status-api --all
```

### Creating Code Review Ticket
```bash
# Basic usage (uses MCP for Jira)
/create-code-review-ticket-api https://bitbucket.org/workspace/repo/pull-requests/123

# With assignee (MCP handles lookup)
/create-code-review-ticket-api https://bitbucket.org/workspace/repo/pull-requests/123 --assignee john@example.com

# With custom story points
/create-code-review-ticket-api https://bitbucket.org/workspace/repo/pull-requests/123 --story-points 3
```

## Appendix C: Hybrid Implementation Details

### Command File Structure

Each slash command will have the following structure:

```yaml
---
allowed-tools: Bash(git:*), Bash(uv:*), mcp__atlassian_confluence_jira__*
argument-hint: [arguments...]
description: Hybrid Bitbucket API and Jira MCP command
model: claude-sonnet-4-0
---

# Command logic:
1. Parse arguments
2. For Bitbucket operations:
   - Call: uv run .claude/scripts/bitbucket/script.py [args]
3. For Jira operations:
   - Use MCP tools directly
4. Combine results and display
```

### Python Script Structure

Each Python script will use UV's inline script metadata:

```python
# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "atlassian-python-api",
#   "python-dotenv",
#   "click",
# ]
# ///

import os
import sys
from dotenv import load_dotenv
from atlassian import Bitbucket
import click

load_dotenv()

# Bitbucket operations here
# Output JSON for command to process
```

---

**END OF DOCUMENT**
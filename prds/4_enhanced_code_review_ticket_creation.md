# PRD: Enhanced Code Review Ticket Creation

## Overview

Enhance the existing `create-code-review-ticket.md` slash command to achieve better standardization, error recovery, and reliability without creating external files or Python dependencies. The enhancement should incorporate advanced prompting techniques to match the robustness of the hybrid Python approach used in `jira-code-review.md`.

## Problem Statement

The current `create-code-review-ticket.md` slash command has several limitations:

1. **Inconsistent Formatting**: No enforcement of standardized ticket titles, descriptions, or field values
2. **Poor Error Recovery**: If any step fails, the entire process must restart from beginning
3. **Limited Debugging**: No structured error context or recovery guidance
4. **No Retry Capability**: Failed MCP calls cannot be easily retried with the same data
5. **Manual Fallback Gap**: No automatic generation of manual creation alternatives

## Success Criteria

1. **Standardized Output**: All tickets created with consistent format regardless of input variations
2. **Error Recovery**: Users can resume from failure points without re-processing data
3. **Retry Capability**: Failed operations can be retried using preserved data
4. **Manual Fallback**: Automatic generation of pre-filled URLs for manual ticket creation
5. **Progress Tracking**: Clear visibility into execution stages and current state
6. **No File Dependencies**: All improvements achieved through bash variables and prompting

## Implementation Phases

### Phase 1: Data Structure Foundation
**Objective**: Establish in-memory state management system using bash variables

**Dependencies**: None (foundational phase)

**Tasks**:
1. **Define State Variables**
   - Create comprehensive bash variable schema for all ticket data
   - Include stage tracking, input data, extracted data, and MCP parameters
   - Add error tracking variables (LAST_ERROR, FAILED_STAGE)

2. **Create Data Template Structure**
   - Define TICKET_TEMPLATE as JSON string in bash variable
   - Include all required fields: title, issue_type, component, story_points, description
   - Create field mapping documentation for MCP parameter conversion

3. **Add Variable Export Instructions** 
   - Ensure all critical variables are exported for session persistence
   - Document variable lifecycle and when each gets populated
   - Add variable validation functions

**Acceptance Criteria**:
- [ ] All ticket data stored in structured bash variables
- [ ] No external files created during execution
- [ ] Variables persist across command execution stages
- [ ] Clear documentation of variable schema

### Phase 2: Validation and Standardization Framework
**Objective**: Implement strict formatting rules and validation checkpoints

**Dependencies**: Phase 1 (requires variable structure)

**Tasks**:
1. **Create Validation Template System**
   - Define mandatory format requirements for all ticket fields
   - Implement validation functions for each field type
   - Create validation checkpoint prompts for each execution stage

2. **Implement Format Enforcement**
   - Add strict pattern matching for ticket titles (`{repo} {branch} Code Review`)
   - Enforce "Task" issue type (no variations allowed)
   - Require "Code Review" component (exact match)
   - Standardize story points (1 for normal PRs, 2 for >500 lines)

3. **Add Pre-MCP Validation Gates**
   - Create comprehensive validation before MCP tool execution
   - Display validation results with checkboxes (✅/❌)
   - Stop execution if any validation fails with clear error messages

**Acceptance Criteria**:
- [ ] All tickets follow exact same format regardless of input
- [ ] Validation prevents inconsistent ticket creation
- [ ] Clear feedback on what needs correction when validation fails
- [ ] No tickets created with non-standard formatting

### Phase 3: Staged Execution System
**Objective**: Implement stage-based execution with progress tracking

**Dependencies**: Phase 2 (requires validation system)

**Tasks**:
1. **Restructure Execution Flow**
   - Replace current task list with 5 distinct execution stages
   - Add TICKET_STATE variable to track current stage
   - Implement progress indicators for each stage ([🔄], [✅], [❌])

2. **Implement Stage Checkpoints** 
   - Stage 1: Input validation and argument parsing
   - Stage 2: Repository data extraction from PR URL
   - Stage 3: Jira configuration and project lookup
   - Stage 4: Ticket data preparation and validation
   - Stage 5: MCP execution and ticket creation

3. **Add Stage Transition Logic**
   - Each stage must complete successfully before next stage
   - Update TICKET_STATE variable at each transition
   - Display stage completion status and key data extracted

**Acceptance Criteria**:
- [ ] Execution broken into clear, sequential stages
- [ ] Progress visible at each stage with clear indicators
- [ ] Each stage validates prerequisites before proceeding
- [ ] Stage state tracked in TICKET_STATE variable

### Phase 4: Error Recovery System
**Objective**: Enable recovery from failures without restarting from beginning

**Dependencies**: Phase 3 (requires staged execution)

**Tasks**:
1. **Implement Error Capture**
   - Capture error codes and messages in LAST_ERROR variable
   - Record which stage failed in FAILED_STAGE variable
   - Add comprehensive error context for debugging

2. **Create Recovery Information Display**
   - Show all populated variables when error occurs
   - Display recovery options based on which stage failed
   - Provide retry instructions using existing data

3. **Add Stage-Specific Recovery Procedures**
   - Stage 1-2 failures: Input parsing and PR extraction recovery
   - Stage 3 failures: Jira authentication and project access recovery  
   - Stage 4 failures: Data preparation and validation recovery
   - Stage 5 failures: MCP execution retry procedures

4. **Implement Retry Command Generation**
   - Store MCP commands as strings in MCP_COMMAND variable
   - Enable direct retry of failed MCP calls
   - Preserve all prepared data for retry attempts

**Acceptance Criteria**:
- [ ] Users can resume from failure points without losing progress
- [ ] Clear recovery guidance provided for each failure type
- [ ] MCP commands can be retried without re-preparation
- [ ] All error context preserved and displayed

### Phase 5: Manual Fallback Integration
**Objective**: Provide automatic manual creation options when automation fails

**Dependencies**: Phase 4 (requires error recovery system)

**Tasks**:
1. **Generate Pre-filled URLs**
   - Create Jira direct creation URLs with URL-encoded parameters
   - Include title, description, issue type, and component
   - Generate URLs automatically when Stage 5 fails

2. **Create Copy-Paste Ready Data**
   - Format all ticket data for manual copy-paste
   - Include all required fields with proper formatting
   - Provide clear instructions for manual creation

3. **Add Fallback Documentation**
   - Document manual creation steps for common failure scenarios
   - Include troubleshooting guide for authentication issues
   - Provide field mapping for custom Jira configurations

**Acceptance Criteria**:
- [ ] Pre-filled URLs generated automatically on MCP failures
- [ ] All ticket data available in copy-paste format
- [ ] Clear manual creation instructions provided
- [ ] Users never completely blocked by automation failures

### Phase 6: Documentation and Testing
**Objective**: Complete documentation and validate all improvements

**Dependencies**: Phase 5 (requires all features implemented)

**Tasks**:
1. **Update Command Documentation**
   - Document all new variables and their purposes
   - Add stage-based execution examples
   - Include error recovery scenarios and solutions

2. **Create Usage Examples** 
   - Add examples of successful execution with stage tracking
   - Document common error scenarios and recovery steps
   - Include manual fallback usage examples

3. **Add Troubleshooting Guide**
   - Document common failure points and solutions
   - Include variable inspection commands for debugging
   - Add field mapping instructions for different Jira configurations

4. **Validate Implementation**
   - Test all execution stages with valid inputs
   - Test error recovery from each stage
   - Validate manual fallback URL generation
   - Confirm no files created during any execution path

**Acceptance Criteria**:
- [ ] Complete documentation of all features
- [ ] Usage examples for all major scenarios
- [ ] Comprehensive troubleshooting guide
- [ ] All functionality tested and validated

## Technical Specifications

### Variable Schema
```bash
# State tracking
export TICKET_STATE=""        # Current execution stage
export LAST_ERROR=""          # Last error message
export FAILED_STAGE=""        # Stage where failure occurred

# Input data
export PR_URL=""              # Pull request URL
export BRANCH_NAME=""         # Branch name (from args or extracted)
export PROJECT_KEY=""         # Jira project key (optional)
export ASSIGNEE=""            # Assignee email/name (optional)

# Extracted data
export REPOSITORY_NAME=""     # Repository name from PR URL
export PR_ID=""              # Pull request ID number
export TICKET_TITLE=""       # Generated ticket title
export TICKET_DESCRIPTION="" # Generated ticket description

# Jira configuration
export CLOUD_ID=""           # Atlassian cloud ID
export PROJECT_ID=""         # Jira project ID
export ISSUE_TYPE_ID=""      # Task issue type ID
export ASSIGNEE_ID=""        # Assignee account ID

# Prepared data
export TICKET_JSON=""        # Complete ticket data as JSON string
export MCP_COMMAND=""        # MCP command for retry
```

### JSON Template Schema
The following JSON templates provide standardized structure for pre-MCP validation:

#### Core Ticket Template
```json
{
  "title": "{repository} {branch} Code Review",
  "issue_type": "Task",
  "component": "Code Review", 
  "story_points": 1,
  "description_sections": {
    "pr_link": "Pull Request: {pr_url}",
    "pr_id": "PR ID: #{pr_id}",
    "details": "{optional_details}",
    "reviewers": "{optional_reviewers}"
  }
}
```

#### Validation Template
```json
{
  "validation_checks": {
    "title_format": "✅ Title follows pattern: '{repository} {branch} Code Review'",
    "issue_type": "✅ Issue type is 'Task'",
    "component": "✅ Component is 'Code Review'", 
    "story_points": "✅ Story points: 1 (or 2 if PR >500 lines)",
    "description_format": "✅ Description starts with 'Pull Request: {url}'",
    "required_fields": "✅ All required fields populated"
  },
  "validation_status": "PASSED|FAILED",
  "errors": []
}
```

#### MCP Parameters Template
```json
{
  "mcp_parameters": {
    "cloudId": "{cloud_id}",
    "projectKey": "{project_key}",
    "issueTypeName": "Task",
    "summary": "{repository} {branch} Code Review",
    "description": "Pull Request: {pr_url}\n\nPR ID: #{pr_id}\n\n{optional_details}",
    "assignee_account_id": "{assignee_id}",
    "additional_fields": {
      "customfield_story_points": 1,
      "components": [{"name": "Code Review"}]
    }
  }
}
```

### Stage Definitions
1. **STAGE_1_INPUTS**: Argument parsing and validation
2. **STAGE_2_EXTRACT**: Repository data extraction
3. **STAGE_3_JIRA_CONFIG**: Jira configuration lookup
4. **STAGE_4_PREPARE**: Ticket data preparation
5. **STAGE_5_CREATE**: MCP execution and creation

### Validation Rules
- Title: `{repository} {branch} Code Review` (exact format)
- Issue Type: "Task" (no variations)
- Component: "Code Review" (exact match)
- Story Points: 1 (or 2 if PR >500 lines)
- Description: Must start with "Pull Request: {url}"

## Risk Assessment

### Low Risk
- Bash variable management (standard shell functionality)
- Prompt-based validation (no external dependencies)
- String manipulation for URL generation

### Medium Risk  
- MCP tool integration changes (existing functionality)
- Complex bash variable schema (manageable with good documentation)

### Mitigation Strategies
- Comprehensive testing of all execution paths
- Clear documentation of variable schema and lifecycle
- Fallback to current behavior if enhancements fail
- No breaking changes to existing command interface

## Success Metrics

1. **Consistency**: 100% of tickets follow standardized format
2. **Recovery Rate**: >90% of failures recoverable without full restart
3. **User Experience**: Clear progress tracking and error guidance
4. **Reliability**: Manual fallback available for all failure scenarios
5. **Maintainability**: No external file dependencies or complex setups

## Post-Implementation

After successful implementation, this enhanced approach can serve as a template for improving other slash commands that interact with external APIs or require data persistence across execution stages.
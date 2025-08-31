# Manual Phase Review

Manually trigger code review for a specific PRD phase. Useful for debugging and manual intervention in the automated review process.

## Usage: review-prd-phase <PRD_FILE> <PHASE_NAME> [FILES...]

## Arguments
- **PRD_FILE**: Path to the PRD file containing phase requirements
- **PHASE_NAME**: Specific phase name to review (e.g., "Phase 1", "Phase 2.1", etc.)
- **FILES**: Optional list of specific files to review (if not provided, will auto-detect changed files)

## Process

1. **Load PRD Context**
   - Read the specified PRD file
   - Parse and extract requirements for the specified phase
   - Understand the phase objectives and success criteria

2. **Identify Changed Files**
   - If files are explicitly provided, use those
   - Otherwise, detect files changed since last commit or relevant to the phase
   - Focus on files that should contain the phase implementation

3. **Invoke Code Review Agent**
   - Use the Task tool to launch the code-review-agent subagent with the unified structured format
   - Agent will perform comprehensive review using external models via Codex
   - **Required Task invocation format:**
     ```
     Task(
       subagent_type="code-review-agent",
       description="Manual review of phase implementation",
       prompt="Phase Review Request:

{
    \"phase\": \"[EXACT_PHASE_NAME_FROM_PRD]\",
    \"prd_file\": \"[ABSOLUTE_PATH_TO_PRD_FILE]\",
    \"changed_files\": [\"file1.ext\", \"file2.ext\", \"...\"],
    \"implementation_notes\": \"[MANUAL_REVIEW_CONTEXT: User requested manual review of this phase. Files provided: {file_list} or auto-detected from recent changes.]\",
    \"review_trigger\": \"manual\",
    \"phase_requirements\": \"[EXTRACTED_PHASE_REQUIREMENTS_FROM_PRD]\",
    \"success_criteria\": \"[EXTRACTED_SUCCESS_CRITERIA_FROM_PRD]\",
    \"context_metadata\": {
      \"session_id\": \"manual_review_[TIMESTAMP]\",
      \"iteration_count\": 1,
      \"previous_feedback\": \"\"
    }
    }

Please analyze this implementation against the phase requirements and provide your standardized review response."
     )
     ```

   **Implementation Requirements for Executor:**
   - Parse PRD file to extract the specific phase requirements and success criteria
   - Use provided files or auto-detect changed files (git diff, recent modifications)
   - Set review_trigger to "manual" to indicate this is user-initiated
   - Generate unique session_id with timestamp for tracking
   - Extract exact phase name as it appears in PRD
   - Build comprehensive implementation_notes explaining the manual review context

4. **Review Analysis**
   - Correctness according to PRD phase requirements
   - Code quality and best practices adherence
   - Security considerations and potential vulnerabilities
   - Performance implications
   - Integration with existing codebase

5. **Generate Report**
   - Structured feedback with approval status
   - Specific issues found with file locations and line numbers
   - Concrete suggestions for fixes
   - Priority levels for each issue (critical/major/minor)
   - General assessment and recommendations

6. **Output Format**
   ```
   ## Phase Review Report: [PHASE_NAME]
   
   **Status**: APPROVED | NEEDS CHANGES
   **PRD File**: [PRD_FILE]
   **Files Reviewed**: [LIST]
   **Review Date**: [TIMESTAMP]
   
   ### Issues Found
   [Detailed list of issues with priorities and suggestions]
   
   ### General Assessment
   [Overall evaluation and recommendations]
   
   ### Next Steps
   [Recommended actions based on review results]
   ```

## Use Cases

- **Manual Quality Gate**: Review specific phase before proceeding
- **Debugging Failed Reviews**: Understand why automated review failed
- **Spot Check**: Verify implementation quality at any point
- **Pre-commit Review**: Final check before committing phase changes
- **Learning**: Understand review criteria and improve code quality

## Implementation Details

**Core Process:**
1. Parse command arguments (PRD file, phase name, optional files)
2. Read and parse the PRD file to extract phase-specific requirements
3. Determine files to review (provided or auto-detected)
4. Use Task tool to invoke code-review-agent subagent
5. Present structured review results to user

**Task Tool Invocation:**
The command executor should use the Task tool with `subagent_type="code-review-agent"` and provide the unified structured format containing:
- Complete input JSON object with all required fields
- Extracted phase requirements and success criteria from PRD
- File list (provided by user or auto-detected)
- Manual review trigger indication and timestamp-based session_id
- Comprehensive implementation_notes explaining the manual review context

## Integration with Automated Flow

This command complements the automated review system:
- Can be used when automated review hits iteration limits
- Provides detailed insight into review criteria
- Allows manual override of review decisions when appropriate
- Serves as debugging tool for review process issues
- Uses the same code-review-agent as the automated flow

## Examples

```bash
# Review Phase 1 implementation with auto-detected files
review-prd-phase prds/user-auth-system.md "Phase 1"

# Review specific files for Phase 2.1
review-prd-phase prds/data-pipeline.md "Phase 2.1" src/pipeline.py src/validators.py

# Review current implementation against Phase 3 requirements
review-prd-phase prds/api-refactor.md "Phase 3" $(git diff --name-only HEAD~1)
```

## Notes

- The manual review uses the same review agent and criteria as automated flow
- Results can be used to improve automated review thresholds
- Manual approval can override automated review failures (with caution)
- All manual reviews are logged for audit trail
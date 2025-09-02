# PRD: Automated Code Review System

## Feature Overview
Create an automated code review flow where a code implementation agent writes code for PRD phases, and a code review agent automatically reviews the changes to ensure accuracy to the PRD requirements. The system will use the Codex MCP server for external model access and implement an iterative feedback loop.

## Implementation Phases

### Phase 1: Create Agent Configurations

#### Task 1.1: Code Implementation Agent
**File:** `.claude/agents/code-implementation-agent.md`
- **Purpose:** Specialized agent for implementing code changes according to PRD phases
- **Tools:** Read, Write, Edit, MultiEdit, Bash, Grep, Glob, TodoWrite, mcp__codex__codex, mcp__codex__codex-reply
- **Model:** sonnet (efficient for implementation tasks)
- **Key Features:**
  - Reads and parses PRD files to understand phase requirements
  - Implements code changes phase by phase
  - Tracks implementation progress with TodoWrite
  - After completing each phase, invokes the code-review-agent
  - Processes feedback from review agent and makes corrections
  - Uses structured output for phase completion status

#### Task 1.2: Code Review Agent  
**File:** `.claude/agents/code-review-agent.md`
- **Purpose:** Reviews code changes against PRD requirements using external models via Codex
- **Tools:** Read, Grep, Glob, mcp__codex__codex, mcp__codex__codex-reply, Write
- **Model:** opus (better for analysis and review)
- **Key Features:**
  - Receives PRD phase requirements and changed files list
  - Uses Codex MCP to leverage external models for code review
  - Analyzes code changes for:
    - Correctness according to PRD requirements
    - Code quality and best practices
    - Security considerations
    - Performance implications
  - Provides structured feedback with:
    - Approval status (approved/needs-changes)
    - Specific issues found
    - Concrete suggestions for fixes
    - Priority levels for issues

### Phase 2: Implement Triggering Mechanism

#### Task 2.1: Agent Communication Strategy
- **Primary Method:** Direct agent invocation from implementation agent
  - Implementation agent includes review agent call in its prompt
  - Passes phase context and file changes to review agent
  - Waits for feedback before proceeding

#### Task 2.2: Enhanced SubagentStop Hook (Optional)
**File:** Update `.claude/hooks/subagent_stop.py`
- Add logic to detect when implementation agent completes a phase
- Check for phase completion markers in agent output
- Automatically trigger review agent if phase completed
- Log review results for audit trail

### Phase 3: Create Feedback Loop

#### Task 3.1: Structured Communication Protocol
- **Phase Completion Message Format:**
  ```json
  {
    "phase": "phase_name",
    "prd_file": "path/to/prd.md",
    "changed_files": ["file1.py", "file2.js"],
    "implementation_notes": "summary of changes"
  }
  ```

- **Review Feedback Format:**
  ```json
  {
    "status": "approved|needs-changes",
    "issues": [
      {
        "file": "file.py",
        "line": 42,
        "severity": "critical|major|minor",
        "issue": "description",
        "suggestion": "how to fix"
      }
    ],
    "general_feedback": "overall assessment"
  }
  ```

#### Task 3.2: Iteration Control
- Maximum iteration limit per phase (default: 3)
- Escalation to user if consensus not reached
- Progress tracking in shared state file

### Phase 4: Create Supporting Commands

#### Task 4.1: PRD Execution Command
**File:** Update `.claude/commands/code/execute-prd.md`
- Modify to use the new implementation agent
- Add phase-by-phase execution with review gates
- Include review status in progress reporting

#### Task 4.2: Manual Review Command
**File:** `.claude/commands/code/code-review.md`
- Allow manual triggering of code review for specific phase
- Useful for debugging and manual intervention

### Phase 5: Integration Configuration

#### Task 5.1: Test agents and validate input and output responses between agents
- Test the code review agent that would use the codex mcp server using an example input with the review context input format and validate the response format from the codex mcp matches what is expected in order for the implementation agent to have all context needed
- Review thresholds and iteration limits

## Technical Implementation Details

### Code Implementation Agent Prompt Structure:
1. Parse PRD and identify phases
2. For each phase:
   - Implement required changes
   - Track changes in TodoWrite
   - Mark phase complete
   - Invoke code-review-agent with context
   - Process feedback
   - If approved, move to next phase
   - If needs changes, iterate (up to limit)

### Code Review Agent Prompt Structure:
1. Receive phase requirements and changes
2. Use Codex to analyze code with external models
3. Check against PRD requirements
4. Evaluate code quality
5. Generate structured feedback
6. Return approval status

### Communication Protocol:
- Implementation agent calls review agent directly using Task tool
- Passes structured context about phase and changes
- Review agent returns structured feedback
- Implementation agent processes feedback and iterates if needed

## Benefits:
- **Deterministic:** Review always happens after each phase
- **Maintainable:** Clear separation of concerns
- **Flexible:** Can adjust review criteria per project
- **Auditable:** Complete log of reviews and iterations
- **Scalable:** Can add more specialized agents as needed

## Success Criteria:
1. Implementation agent can execute PRD phases with automatic review gates
2. Review agent provides consistent, actionable feedback using external models via Codex
3. Feedback loop successfully drives code improvements
4. System handles iteration limits and escalation appropriately
5. All changes are tracked and auditable

## Validation Commands:
- Test implementation agent with sample PRD
- Verify review agent feedback quality
- Test iteration and escalation flows
- Validate state persistence and recovery
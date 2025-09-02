# Execute PRD with Automated Code Review

Implement a feature using the PRD file with phase-by-phase execution and automatic code review gates.

## PRD File: $ARGUMENTS

## Execution Process

1. **Load PRD**
   - Read the specified PRD file
   - Parse and identify all implementation phases
   - Understand all context and requirements
   - Follow all instructions in the PRD and extend the research if needed
   - Ensure you have all needed context to implement the PRD fully. Make sure you use either the ref mcp server (preferable) or the context7 mcp server (fallback) for getting documentation on APIs, libraries, services, and code functions.
   - Do more web searches and codebase exploration as needed. If doing a web search, prefer to use the gemini cli web search tool before falling back to claude's web search tool.

2. **ULTRATHINK**
   - Think hard before you execute the plan. Create a comprehensive plan addressing all requirements.
   - Break down complex tasks into smaller, manageable steps using your todos tools.
   - Use the TodoWrite tool to create and track your implementation plan.
   - Identify implementation patterns from existing code to follow.
   - Plan for phase-by-phase implementation with review checkpoints.

3. **Execute with Code Implementation Agent**
   - Use the code-implementation-agent for phase-by-phase execution
   - The agent will automatically:
     - Implement each phase according to PRD requirements
     - Track implementation progress with TodoWrite
     - Invoke code-review-agent after each phase completion
     - Process review feedback and make corrections
     - Iterate until phase is approved (max 3 iterations per phase)
     - Continue to next phase only after review approval

4. **Automated Review Gates**
   - Each phase completion triggers automatic code review
   - Review agent analyzes changes against PRD requirements
   - Review includes:
     - Correctness according to PRD requirements
     - Code quality and best practices
     - Security considerations
     - Performance implications
   - Phase progression blocked until review approval

5. **Validate**
   - Run each validation command after all phases complete
   - Fix any failures through the review feedback loop
   - Re-run until all pass

6. **Complete**
   - Ensure all checklist items done
   - Run final validation suite
   - Report completion status with review history
   - Read the PRD again to ensure you have implemented everything

7. **Review Status Tracking**
   - All reviews are logged for audit trail
   - Phase completion status tracked in state files
   - Iteration counts and feedback history preserved
   - Resume capability from interruption

8. **Reference the PRD**
   - You can always reference the PRD again if needed
   - Review agents have access to full PRD context

## Implementation Details

The execution uses specialized agents:
- **code-implementation-agent**: Handles phase-by-phase implementation
- **code-review-agent**: Provides automated quality gates using external models via Codex MCP server

This ensures deterministic code review after each phase with maintainable separation of concerns.

Note: If validation fails or review iterations exceed limits, escalation to manual intervention occurs.
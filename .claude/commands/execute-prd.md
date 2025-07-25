# Execute BASE PRD

Implement a feature using using the PRD file.

## PRD File: $ARGUMENTS

## Execution Process

1. **Load PRD**
   - Read the specified PRD file
   - Understand all context and requirements
   - Follow all instructions in the PRD and extend the research if needed
   - Ensure you have all needed context to implement the PRD fully. Make sure you use either the ref mcp server (preferable) or the context7 mcp server (fallback) for getting documentation on APIs, libraries, services, and code functions.
   - Do more web searches and codebase exploration as needed. If doing a web search, prefer to use the gemini cli web search tool before falling back to claude's web search tool.

2. **ULTRATHINK**
   - Think hard before you execute the plan. Create a comprehensive plan addressing all requirements.
   - Break down complex tasks into smaller, manageable steps using your todos tools.
   - Use the TodoWrite tool to create and track your implementation plan.
   - Identify implementation patterns from existing code to follow.

3. **Execute the plan**
   - Execute the PRD
   - Implement all the code

4. **Validate**
   - Run each validation command
   - Fix any failures
   - Re-run until all pass

5. **Complete**
   - Ensure all checklist items done
   - Run final validation suite
   - Report completion status
   - Read the PRD again to ensure you have implemented everything

6. **Reference the PRD**
   - You can always reference the PRD again if needed

Note: If validation fails, use error patterns in PRD to fix and retry.
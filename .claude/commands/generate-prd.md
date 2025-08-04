# Create PRD

## Feature file: $ARGUMENTS

Generate a complete PRD for general feature implementation with thorough research. Ensure context is passed to the AI agent to enable self-validation and iterative refinement. Read the feature file first to understand what needs to be created, how the examples provided help, and any other considerations.

The AI agent only gets the context you are appending to the PRD and training data. Assume the AI agent has access to the codebase and the same knowledge cutoff as you, so its important that your research findings are included or referenced in the PRD. The Agent has Websearch capabilities, so pass urls to documentation and examples.

## Research Process

1. **Codebase Analysis**
   - Search for similar features/patterns in the codebase
   - Identify files to reference in PRD
   - Note existing conventions to follow
   - Check test patterns for validation approach

2. **External Research**
   - Search for similar features/patterns online
   - Library documentation (include specific URLs)
   - Implementation examples (GitHub/StackOverflow/blogs)
   - Best practices and common pitfalls

3. **User Clarification** (if needed)
   - Specific patterns to mirror and where to find them?
   - Integration requirements and where to find them?

## PRD Generation

### Critical Context to Include and pass to the AI agent as part of the PRD
- **Documentation**: URLs with specific sections
- **Code Examples**: Real snippets from codebase
- **Gotchas**: Library quirks, version issues
- **Patterns**: Existing approaches to follow

### Implementation Blueprint
- Start with pseudocode showing approach
- Reference real files for patterns
- Include error handling strategy
- list tasks to be completed to fullfill the PRD in the order they should be completed

## Anti-Patterns to Avoid
- Don't create new patterns when existing ones work
- Don't skip validation because "it should work"  
- Don't ignore failing tests - fix them
- Don't use sync functions in async context
- Don't hardcode values that should be config
- Don't catch all exceptions - be specific

### Validation Gates (Must be Executable) eg for python
```bash
# Unit Tests
uv run pytest tests/ -v
```

*** CRITICAL AFTER YOU ARE DONE RESEARCHING AND EXPLORING THE CODEBASE BEFORE YOU START WRITING THE PRD ***

*** ULTRATHINK ABOUT THE PRD AND PLAN YOUR APPROACH THEN START WRITING THE PRD. BREAK DOWN THE PRD INTO MANAGEABLE PHASES WITH A TASK LIST FOR EACH PHASE. ***

## Output
Save as: `prds/{feature_name}.md`, making the directory `prds/` if it does not exist.

## Quality Checklist
- [ ] All necessary context included
- [ ] Validation gates are executable by AI
- [ ] References existing patterns
- [ ] Clear implementation path
- [ ] Error handling documented

Score the PRD on a scale of 1-10 (confidence level to succeed in one-pass implementation using claude codes)

Remember: The goal is one-pass implementation success through comprehensive context.

# Create PRP

## Feature file: $ARGUMENTS
<goal>
You are preparing a **Project Requirement Prompt (PRP)** that an AI orchestrator agent will use to manage and implement a new feature.

**1 Understand the feature first**
- Open and read the feature file thoroughly.
- Identify:  
  • Functional requirements  
  • Example scenarios and edge cases  
  • Constraints, dependencies, and anything called out in the LOCK file

**2 Research & enrich the PRP**
- Perform any additional research the feature requires (e.g., best-practice patterns, library docs, similar code in the repo).
- Because the orchestrator only sees the PRP and its own training data, embed or reference all critical findings here.
- When citing external sources, include the URL so the agent can follow it with its Web-search tool.

**3 Compose the PRP**  
Your PRP must contain, at minimum:

| Section | Purpose | Contents |
|---------|---------|----------|
| **Context** | Give the agent everything it needs to reason. | • Key points from the feature file<br>• Summary of relevant codebase areas<br>• Research findings & URLs |
| **Acceptance Criteria** | Define “done.” | Bullet-point list mapped to feature requirements & examples |
| **Implementation Hints** | Speed up the engineer. | Suggested files, patterns, API calls, tests to add |
| **Self-Validation Checklist** | Enable autonomous QA. | Automated tests to run, logs to watch, performance metrics |

**4 Project-manager plan (that YOU will follow)**  
As the PM you will:

1. **Iterative work cycle**
    - Ask the engineer to implement one acceptance criterion at a time.
    - After each delivery, review output and server logs before green-lighting the next item.

2. **Regular check-ins**
    - Schedule status pings with `./schedule_with_note.sh "PM check-in"` (or `sleep` if simpler).
    - Frequency: every 15 min during active work; adjust as the feature stabilises.

3. **Log monitoring**
    - Continuously tail convex-server and npm-server logs.
    - Surface any warnings/errors to the engineer without interrupting their deep-work window (bundle them into the next check-in).

4. **Scope discipline**
    - If confusion arises, pause and re-read the original spec and LOCK file.
    - Reject any task drift beyond the explicit scope.

**Tone & mindset**  
Stay calm, organized, and collaborative. Your responsibility is to keep the process flowing and the engineer unblocked but not to code yourself.

When finished, hand this PRP to the AI orchestrator agent as the sole piece of context for the feature implementation.
</goal>


## Research Process

1. **Codebase Analysis**
    - Search for similar features/patterns in the codebase
    - Identify files to reference in PRP
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

## PRP Generation

### Critical Context to Include and pass to the AI agent as part of the PRP
- **Documentation**: URLs with specific sections
- **Code Examples**: Real snippets from codebase
- **Gotchas**: Library quirks, version issues
- **Patterns**: Existing approaches to follow

### Implementation Blueprint
- Start with pseudocode showing approach
- Reference real files for patterns
- Include error handling strategy
- list tasks to be completed to fullfill the PRP in the order they should be completed

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

*** CRITICAL AFTER YOU ARE DONE RESEARCHING AND EXPLORING THE CODEBASE BEFORE YOU START WRITING THE PRP ***

*** ULTRATHINK ABOUT THE PRP AND PLAN YOUR APPROACH THEN START WRITING THE PRP ***

## Output
Save as: `prps/{feature_name}.md`, making the directory `prps/` if it does not exist.

## Quality Checklist
- [ ] All necessary context included
- [ ] Validation gates are executable by AI
- [ ] References existing patterns
- [ ] Clear implementation path
- [ ] Error handling documented

Score the PRP on a scale of 1-10 (confidence level to succeed in one-pass implementation using claude codes)

Remember: The goal is one-pass implementation success through comprehensive context using multiple subagent engineers in an efficient but logical order.




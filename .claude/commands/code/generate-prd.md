---
description: Generate comprehensive PRDs directly from problem descriptions using sophisticated generate-prd-agent
argument-hint: "problem/feature description"
model: claude-opus-4-1
---

# Direct PRD Generation Workflow

Generate comprehensive PRD for: $ARGUMENTS

## Workflow Execution Instructions

This command provides a streamlined path from problem description to comprehensive PRD by leveraging the sophisticated research and analysis capabilities of the generate-prd-agent.

### PRD Generation

1. **Input Processing**: Parse and validate the problem/feature description
2. **Agent Delegation**: Invoke the generate-prd-agent with the Task tool
3. **Context**: Pass the problem description directly to the agent: "$ARGUMENTS"
4. **Instructions for generate-prd-agent**:
   - Parse the problem description and understand the feature requirements
   - Conduct deep codebase analysis and external research as needed
   - Research existing patterns and implementation approaches
   - Create phase-based implementation plans with dependency mapping
   - Design multi-agent coordination strategies for implementation
   - Generate comprehensive PRD optimized for one-pass implementation success
   - Save as: `prds/{next_highest_integer}_{feature_name}.md`
   - Score the PRD for implementation confidence (target: 8+)

## Agent Capabilities Leveraged

The generate-prd-agent will autonomously:
- **Research & Analysis**: Conduct thorough codebase analysis and external research
- **Pattern Recognition**: Identify existing patterns and architectural decisions
- **Context Gathering**: Use available tools to gather necessary technical context
- **Quality Assurance**: Apply comprehensive validation checkpoints
- **Strategic Planning**: Design phase-based implementation with multi-agent coordination

## Expected Output

**Comprehensive PRD**: Complete PRD saved to `prds/{next_highest_integer}_{feature_name}.md` with:
- Detailed problem analysis and solution approach
- Phase-based implementation strategy
- Multi-agent coordination plan
- Technical context and integration points
- Quality validation criteria
- Implementation confidence score of 8+

## Success Criteria
- Problem description successfully processed and understood
- Generate-prd-agent produces comprehensive PRD with score 8+
- PRD ready for immediate `/execute-prd` execution
- All research and analysis completed autonomously by the agent

## Execution

Let me delegate directly to the generate-prd-agent with your problem description:
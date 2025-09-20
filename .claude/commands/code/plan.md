---
description: Complete workflow from brainstorming through architecture to PRD generation
argument-hint: "project/feature description"
model: claude-opus-4-0
---

# Complete Planning & Building Workflow

Execute the full development planning pipeline for: $ARGUMENTS

## Workflow Execution Instructions

You will execute two phases, with Phase 1 running two parallel sub-phases:

### Phase 1: Parallel Analysis (Brainstorming + Architecture)

Execute both sub-phases simultaneously using multiple Task tool calls:

#### Phase 1.1: Brainstorming Session (Parallel)
1. Invoke the brainstorming-agent with the Task tool for an brainstorming session
2. Context: "$ARGUMENTS"
3. Instructions for brainstorming-agent:
   - Initialize session state with project-aware persistence
   - Gather additional context and clarify objectives
   - Recommend and apply appropriate brainstorming techniques
   - Facilitate brainstorming with progressive refinement (0-9)
   - Generate structured outputs and project briefs
   - Save session state to `.claude/state/projects/[project-name]/brainstorming/`

#### Phase 1.2: Technical Architecture Analysis (Parallel)
1. Invoke the architect-agent with the Task tool simultaneously with brainstorming
2. Context: Current codebase analysis for "$ARGUMENTS"
3. Instructions for architect-agent:
   - Analyze existing codebase structure and patterns independently
   - Document current system components, technology stack, and architectural patterns
   - Generate comprehensive architecture.md file documenting current system design
   - Save all architecture artifacts to `.claude/state/projects/[project-name]/architecture/`

#### Phase 1 Synchronization
- Both agents run concurrently and independently
- Wait for BOTH brainstorming AND architecture analysis to complete
- Validate that both outputs are available before proceeding to Phase 2

### Phase 2: PRD Generation
1. After BOTH brainstorming and architecture analysis complete, read both outputs:
   - Project brief from: `.claude/state/projects/[project-name]/brainstorming/project-brief-*.json`
   - Architecture documentation from: `.claude/state/projects/[project-name]/architecture/architecture.md`
   - Any additional architecture artifacts from: `.claude/state/projects/[project-name]/architecture/`
2. Create a consolidated feature file that includes:
   - Refined requirements and concepts from brainstorming session
   - Current system architecture context from architect analysis
   - Technology stack and architectural constraints
   - Integration points and existing patterns to leverage
   - Project requirements and implementation context
3. Invoke the generate-prd-agent with the Task tool
4. Pass the consolidated feature information with both brainstorming and architecture context
5. Instructions for generate-prd-agent:
   - Conduct deep codebase analysis and external research
   - Leverage existing architecture context for implementation planning
   - Create phase-based implementation plans with dependency mapping
   - Design multi-agent coordination strategies considering current architecture
   - Generate comprehensive PRDs optimized for one-pass implementation success
   - Save the PRD as: `prds/{next_highest_integer}_{feature_name}.md`
6. Wait for PRD generation completion and verify the output

## State Management
- Phase 1 runs both sub-phases in parallel, each saving to independent directories
- Phase 1.1 saves brainstorming outputs to `.claude/state/projects/[project-name]/brainstorming/`
- Phase 1.2 saves architecture analysis to `.claude/state/projects/[project-name]/architecture/`  
- Phase 2 reads from both state directories to create comprehensive PRD
- This parallel approach maximizes efficiency while maintaining complete traceability

## Expected Outputs
1. **Phase 1.1 - Brainstorming** (Parallel): Project brief with refined concepts in `.claude/state/projects/[project]/brainstorming/`
2. **Phase 1.2 - Architecture** (Parallel): Current system architecture documentation in `.claude/state/projects/[project]/architecture/`
3. **Phase 2 - PRD**: Comprehensive PRD with both requirement and architecture context in `prds/{next_highest_integer}_{feature_name}.md`

## Success Criteria
- Both parallel sub-phases of Phase 1 complete successfully
- Both brainstorming and architecture outputs are properly saved and accessible
- Phase 2 successfully reads and integrates both contexts
- Final PRD incorporates insights from both brainstorming requirements AND current architecture
- PRD is ready for `/execute-prd` command with full implementation context

## Benefits of Parallel Approach
- **Time Efficiency**: Brainstorming and architecture analysis run simultaneously
- **Better Context**: PRD gets both refined requirements AND current system constraints
- **Independence**: Each analysis can proceed optimally without dependencies
- **Enhanced Quality**: Implementation planning benefits from complete architectural awareness


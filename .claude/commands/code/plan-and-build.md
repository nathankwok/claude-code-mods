---
allowed-tools: Task, Read, Write, Glob
description: Complete workflow from brainstorming through architecture to PRD generation
argument-hint: "project/feature description"
model: sonnet
---

# Complete Planning & Building Workflow

Execute the full development planning pipeline for: $ARGUMENTS

## Workflow Execution Instructions

You will execute three sequential phases, with each phase's output feeding into the next:

### Phase 1: Brainstorming Session
1. Invoke the brainstorming-agent with the Task tool for an interactive BMAD-inspired brainstorming session
2. Context: "$ARGUMENTS"
3. Instructions for brainstorming-agent:
   - Initialize session state with project-aware persistence
   - Gather additional context and clarify objectives
   - Recommend and apply appropriate brainstorming techniques
   - Facilitate interactive brainstorming with progressive refinement (0-9)
   - Generate structured outputs and project briefs
   - Save session state to `.claude/state/projects/[project-name]/brainstorming/`
4. Wait for brainstorming completion and note the location of saved project brief

### Phase 2: Technical Architecture Design
1. After brainstorming completes, read the generated project brief from:
   `.claude/state/projects/[project-name]/brainstorming/project-brief-*.json`
2. Invoke the architect-agent with the Task tool
3. Pass the project brief path as input to architect-agent
4. Instructions for architect-agent:
   - Generate comprehensive technical architecture from the project brief
   - Perform PRD phase analysis and breakdown
   - Create dependency graphs and parallelization opportunities
   - Generate interface specifications
   - Save all architecture artifacts to `.claude/state/projects/[project-name]/architecture/`
5. Wait for architecture completion and note the generated artifacts

### Phase 3: PRD Generation
1. After architecture completes, read the architecture artifacts from:
   `.claude/state/projects/[project-name]/architecture/`
   - Especially: `system-design.json`, `phase-breakdown.json`, `dependency-graph.json`
2. Generate a comprehensive PRD that includes:
   - Context from brainstorming insights
   - Technical architecture from architect outputs
   - Phase breakdown with clear tasks
   - Implementation blueprint with patterns
   - Validation gates and success criteria
3. Save the PRD as: `prds/{feature_name}.md`
4. Include in the PRD:
   - All brainstorming context and market insights
   - Architecture decisions and rationale
   - Clear phase-by-phase implementation plan
   - References to existing code patterns
   - Executable validation commands

## State Management
- Each phase saves its outputs to project-specific state directories
- Subsequent phases read from these state directories
- This ensures continuity and traceability across the workflow

## Expected Outputs
1. **Brainstorming**: Project brief with refined concepts in `.claude/state/projects/[project]/brainstorming/`
2. **Architecture**: Technical specs and phase breakdown in `.claude/state/projects/[project]/architecture/`
3. **PRD**: Complete PRD ready for execution in `prds/{next_highest_index_number}_{feature_name}.md`

## Success Criteria
- All three phases complete successfully
- Each phase's output is properly saved and accessible
- Final PRD incorporates insights from all phases
- PRD is ready for `/execute-prd` command

Begin with Phase 1 immediately.
---
description: Execute PRD with parallel multi-agent implementation based on dependency graph and phase breakdown
argument-hint: [prd-file]
model: claude-opus-4-1
allowed-tools: ["Read", "Write", "Glob", "Grep", "Task", "TodoWrite", "Bash", "mcp__context7__resolve-library-id", "mcp__context7__get-library-docs", "mcp__gemini-cli__ask-gemini"]
---

# Execute PRD with Parallel Multi-Agent Implementation

Implement a feature using the PRD file with parallel execution across multiple agents based on dependency graph and phase breakdown.

## PRD File: $ARGUMENTS

## Parallel Execution Process

### 1. **Load & Parse PRD**
   - Read the specified PRD file
   - Extract dependency graph (Mermaid format)
   - Parse implementation phases with parallelization strategies
   - Identify agent assignment strategies for each phase/task
   - Build execution plan based on dependencies and parallel opportunities

### 2. **Dependency Analysis & Execution Planning**
   - Parse dependency graph to identify:
     - Independent phases that can run in parallel
     - Tasks within phases that can be parallelized
     - Critical path and synchronization points
     - Agent coordination requirements
   - Create multi-agent execution timeline
   - Identify conflict zones (overlapping file modifications)

### 3. **Multi-Agent Coordination Setup**
   - Use TodoWrite to track parallel execution across agents
   - Create coordination checkpoints for synchronization
   - Establish handoff protocols between phases
   - Set up conflict resolution for overlapping work

### 4. **Parallel Phase Execution with Mandatory Review Gates**

#### Phase-Level Parallelization with 1:1 Agent Pairing
```markdown
For each execution wave (phases with no dependencies):
1. Launch paired agent instances simultaneously:
   - code-implementation-agent-N + code-review-agent-N (1:1 pairing)
   - Each implementation agent gets dedicated review agent with matching session ID
2. Each implementation agent gets:
   - Specific phase context from PRD
   - List of tasks assigned to that agent
   - Handoff artifacts from completed dependencies
   - Coordination protocol for synchronization points
   - Paired review agent session ID for mandatory reviews
3. Implementation agents execute phase tasks then trigger paired review agent
4. **MANDATORY**: No phase can be marked complete until paired review agent approves
5. Coordination system blocks next wave until all current wave reviews are approved
```

#### Task-Level Parallelization with Review Coordination
```markdown
Within each phase:
1. Parse parallelization strategy from PRD
2. Distribute independent tasks across multiple implementation agents
3. Each implementation agent completes assigned tasks then immediately triggers review
4. Coordinate file-level conflicts using agent orchestration
5. **Review Synchronization**: All task reviews must approve before phase completion
6. Aggregate review feedback across multiple agents for phase-level decisions
```

### 5. **Agent Orchestration Pattern with Mandatory Review Gates**

```markdown
## Execution Waves Based on Dependency Graph with 1:1 Review Pairing

### Wave 1: Foundation Phase (No Dependencies)
- Launch Agent-Foundation-Impl-1 paired with Agent-Foundation-Review-1
- Implementation: [Foundational tasks from PRD parallelization strategy]
- **Review Gate**: Foundation-Review-1 must approve all foundation work
- Expected outputs: [Handoff artifacts from PRD] + review approval
- **Blocking**: Wave 2 cannot start until foundation review approves

### Wave 2: Parallel Development (Depends on Wave 1 Review Approval)
- Launch paired agents simultaneously:
  - Agent-CoreLogic-Impl-2 + Agent-CoreLogic-Review-2
  - Agent-UIComponents-Impl-3 + Agent-UIComponents-Review-3
- Agent-CoreLogic-Impl-2: [Core logic tasks from PRD]
- Agent-UIComponents-Impl-3: [UI component tasks from PRD]
- **Review Gates**: Both CoreLogic-Review-2 AND UIComponents-Review-3 must approve
- **Coordination**: Cross-agent sync points + individual review approvals
- **Blocking**: Wave 3 cannot start until BOTH reviews approve

### Wave 3: Integration (Depends on Wave 2 Review Approvals)
- Launch Agent-Integration-Impl-4 paired with Agent-Integration-Review-4
- Inputs: Artifacts from both CoreLogic and UIComponents + their review approvals
- Tasks: [Integration tasks from PRD]
- **Review Gate**: Integration-Review-4 must approve integration work
- **Blocking**: Next wave waits for integration review approval

### Wave N: Final Phase (Depends on Previous Review Chain)
- Launch Agent-Final-Impl-N paired with Agent-Final-Review-N
- Comprehensive testing, cleanup, and validation
- **Final Review Gate**: Agent-Final-Review-N provides final approval
- **Completion**: PRD marked complete only after final review approval
```

### 6. **Synchronization & Conflict Resolution**

#### File Conflict Management
- Parse PRD for overlapping file modifications
- Use file-level locking during parallel execution
- Implement merge coordination for shared components
- Escalate conflicts to manual resolution when needed

#### Progress Synchronization
- Each agent reports progress via TodoWrite updates
- Central coordinator tracks phase completion
- Dependency gates prevent premature phase launches
- Handoff artifact validation before next phase

### 7. **Mandatory Review Gates with 1:1 Agent Pairing**

#### Phase-Level Review Requirements
- **MANDATORY**: Each implementation agent completion automatically triggers its paired review agent
- **1:1 Pairing**: Agent-Impl-N always paired with Agent-Review-N using matching session IDs
- **Blocking Behavior**: No phase can be marked complete without paired review agent approval
- **Quality Standards**: Reviews consider multi-agent coordination quality and PRD compliance
- **Dependency Validation**: Paired review agents validate handoff artifacts meet dependency requirements
- **System Coherence**: Ensure phase integration maintains system coherence across parallel work

#### Cross-Agent Review Coordination
- **Parallel Review Management**: Multiple review agents can work simultaneously on their assigned phases
- **Integration Review Points**: Special coordination reviews after parallel phases complete
- **Compatibility Checks**: Focus on integration points and cross-agent compatibility
- **Conflict Detection**: Validate that parallel development didn't create conflicts between agents
- **Architectural Consistency**: Ensure consistency across all paired agent implementations

#### Review Synchronization Protocol
- **Agent Pairing**: Implementation agents get unique session IDs shared with paired review agents
- **Review Triggering**: Implementation completion automatically invokes paired review agent
- **Status Tracking**: Central coordination tracks review status for each agent pair
- **Gate Enforcement**: Execution waves blocked until ALL paired reviews in current wave approve
- **Escalation Handling**: Failed reviews trigger iteration loops within agent pairs

### 8. **Error Handling & Recovery**

#### Agent Failure Recovery
- Monitor agent health during parallel execution
- Redistribute failed agent tasks to available agents
- Maintain execution timeline despite individual failures
- Preserve work artifacts for recovery

#### Coordination Failures
- Detect synchronization timeouts
- Implement rollback to last stable sync point
- Manual escalation for irrecoverable conflicts
- State preservation for interrupted executions

### 9. **Implementation Strategy with 1:1 Review Pairing**

#### Multi-Agent Task Distribution with Paired Reviews
```markdown
# Example from PRD parallelization strategy with mandatory review gates:

Wave 1: Foundation (Implementation + Review Pairs)
- Agent-Foundation-Impl-1 + Agent-Foundation-Review-1: Database models, API schemas
- Agent-Utilities-Impl-2 + Agent-Utilities-Review-2: Core utilities, configuration setup
- **Review Gates**: Both Foundation-Review-1 AND Utilities-Review-2 must approve
- **Blocking**: Wave 2 cannot start until BOTH reviews approve
- Sync Point: Schema validation, utility testing + review approvals

Wave 2: Parallel Development (Implementation + Review Pairs)
- Agent-Core-Impl-3 + Agent-Core-Review-3: Business logic, data processing
- Agent-UI-Impl-4 + Agent-UI-Review-4: Components, styling, user interactions  
- Agent-Tests-Impl-5 + Agent-Tests-Review-5: Test framework, unit tests
- **Review Gates**: ALL three review agents (Core-Review-3, UI-Review-4, Tests-Review-5) must approve
- **Coordination**: Cross-agent API contract validation + individual review approvals
- **Blocking**: Wave 3 cannot start until ALL three reviews approve

Wave 3: Integration (Implementation + Review Pair)
- Agent-Integration-Impl-6 + Agent-Integration-Review-6: API integration, E2E flows
- **Review Gate**: Integration-Review-6 must approve final integration
- **Handoff**: Complete system ready for validation + final review approval
```

#### Coordination Protocol with Review Gates
1. **Pre-execution**: Validate all agent pairs have required context and session ID matching
2. **During execution**: Periodic sync checks (every 15 minutes) for both implementation and review agents
3. **Implementation boundaries**: Implementation agents trigger paired review agents automatically
4. **Review boundaries**: Full synchronization blocked until paired review agent approvals
5. **Cross-wave synchronization**: Next wave cannot start until ALL current wave review approvals
6. **Error conditions**: Immediate coordination halt and status report for both implementation and review failures
7. **Review iteration**: Failed reviews trigger implementation corrections within agent pairs
8. **Completion**: Final integration validation AND review approval before next wave

### 10. **Validation & Completion**

#### Parallel Validation
- Run validation commands from PRD in parallel where possible
- Coordinate test execution to avoid resource conflicts
- Aggregate validation results across all agents
- Fix failures through coordinated re-execution

#### Final Integration Check
- Comprehensive system validation
- Review integration points created by parallel development
- Ensure all PRD requirements met across all phases
- Generate execution report with parallel coordination metrics

## Implementation Details

### Specialized Agent Usage with 1:1 Pairing
- **code-implementation-agent**: Multiple instances for parallel execution (Agent-Impl-1, Agent-Impl-2, etc.)
- **code-review-agent**: Multiple instances for 1:1 pairing with implementation agents (Agent-Review-1, Agent-Review-2, etc.)
- **Agent Pairing Rule**: Each implementation agent MUST have exactly one paired review agent with matching session ID
- **No Shared Review Agents**: Review agents cannot be shared across multiple implementation agents
- **generate-prd-agent**: Coordination and conflict resolution across agent pairs
- **brainstorming-agent**: Alternative approaches for blocked execution across agent pairs

### State Management with Agent Pairing
- Distributed state tracking across parallel agent pairs (implementation + review)
- Central coordination state for synchronization across all agent pairs
- Atomic operations for shared resource access with review gate enforcement
- Recovery state for interrupted parallel execution including review states
- Session ID tracking for agent pair coordination
- Review approval status tracking for wave progression control

### Performance Optimization  
- Optimal agent allocation based on task complexity
- Resource usage monitoring across parallel agents
- Dynamic load balancing for long-running phases
- Early termination of blocked dependency chains

## Key Differences from Sequential Execution

1. **Dependency-Driven**: Execution order determined by PRD dependency graph + review approval gates
2. **Multi-Agent with 1:1 Review Pairing**: Multiple implementation agents each paired with dedicated review agents
3. **Review-Gate Enforced**: No phase progression without paired review agent approval
4. **Coordination-Heavy**: Extensive synchronization, conflict resolution, and review coordination
5. **Artifact-Focused**: Strong emphasis on handoff artifacts + review approvals between phases
6. **Quality-Assured**: Built-in quality gates through mandatory reviews at every phase
7. **Resilient**: Built-in recovery from both implementation and review failures with agent pair coordination

Note: Requires PRDs generated with the enhanced generate-prd command that includes dependency graphs and parallelization strategies.
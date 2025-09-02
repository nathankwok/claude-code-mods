---
description: Execute PRD with parallel multi-agent implementation based on dependency graph and phase breakdown
argument-hint: [prd-file]
model: opus
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

### 4. **Parallel Phase Execution**

#### Phase-Level Parallelization
```markdown
For each execution wave (phases with no dependencies):
1. Launch multiple code-implementation-agent instances simultaneously
2. Each agent gets:
   - Specific phase context from PRD
   - List of tasks assigned to that agent
   - Handoff artifacts from completed dependencies
   - Coordination protocol for synchronization points
3. Agents execute in parallel with periodic sync checks
```

#### Task-Level Parallelization
```markdown
Within each phase:
1. Parse parallelization strategy from PRD
2. Distribute independent tasks across multiple agents
3. Coordinate file-level conflicts using agent orchestration
4. Synchronize at task completion boundaries
```

### 5. **Agent Orchestration Pattern**

```markdown
## Execution Waves Based on Dependency Graph

### Wave 1: Foundation Phase (No Dependencies)
- Launch Agent-Foundation with foundational tasks
- Tasks: [List from PRD parallelization strategy]
- Expected outputs: [Handoff artifacts from PRD]

### Wave 2: Parallel Development (Depends on Wave 1)
- Launch Agent-CoreLogic + Agent-UIComponents simultaneously
- Agent-CoreLogic: [Core logic tasks from PRD]
- Agent-UIComponents: [UI component tasks from PRD]  
- Coordination: [Sync points defined in PRD]

### Wave 3: Integration (Depends on Wave 2)
- Launch Agent-Integration once Wave 2 completes
- Inputs: Artifacts from both CoreLogic and UIComponents
- Tasks: [Integration tasks from PRD]

### Wave N: Final Phase
- Launch Agent-Polish with final validation
- Comprehensive testing and cleanup
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

### 7. **Automated Review Gates with Parallel Support**

#### Phase-Level Reviews
- Each phase completion triggers code-review-agent
- Reviews consider multi-agent coordination quality
- Validate handoff artifacts meet dependency requirements
- Ensure phase integration maintains system coherence

#### Integration Reviews  
- Special review after parallel phases complete
- Focus on integration points and compatibility
- Validate that parallel development didn't create conflicts
- Ensure architectural consistency across agents

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

### 9. **Implementation Strategy**

#### Multi-Agent Task Distribution
```markdown
# Example from PRD parallelization strategy:
Wave 1: Foundation
- Agent-A: Database models, API schemas
- Agent-B: Core utilities, configuration setup
- Sync Point: Schema validation, utility testing

Wave 2: Parallel Development  
- Agent-Core: Business logic, data processing
- Agent-UI: Components, styling, user interactions
- Agent-Tests: Test framework, unit tests
- Sync Point: API contract validation

Wave 3: Integration
- Agent-Integration: API integration, E2E flows
- Handoff: Complete system ready for validation
```

#### Coordination Protocol
1. **Pre-execution**: Validate all agents have required context
2. **During execution**: Periodic sync checks (every 15 minutes)
3. **Phase boundaries**: Full synchronization and artifact validation
4. **Error conditions**: Immediate coordination halt and status report
5. **Completion**: Final integration validation before next wave

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

### Specialized Agent Usage
- **code-implementation-agent**: Multiple instances for parallel execution
- **code-review-agent**: Phase and integration reviews
- **generate-prd-agent**: Coordination and conflict resolution
- **brainstorming-agent**: Alternative approaches for blocked execution

### State Management
- Distributed state tracking across parallel agents
- Central coordination state for synchronization
- Atomic operations for shared resource access
- Recovery state for interrupted parallel execution

### Performance Optimization  
- Optimal agent allocation based on task complexity
- Resource usage monitoring across parallel agents
- Dynamic load balancing for long-running phases
- Early termination of blocked dependency chains

## Key Differences from Sequential Execution

1. **Dependency-Driven**: Execution order determined by PRD dependency graph
2. **Multi-Agent**: Multiple agents executing simultaneously
3. **Coordination-Heavy**: Extensive synchronization and conflict resolution
4. **Artifact-Focused**: Strong emphasis on handoff artifacts between phases
5. **Resilient**: Built-in recovery from agent failures and coordination issues

Note: Requires PRDs generated with the enhanced generate-prd command that includes dependency graphs and parallelization strategies.
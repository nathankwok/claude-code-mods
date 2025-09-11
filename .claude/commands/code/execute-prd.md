---
description: Execute PRD with parallel multi-agent implementation using Git worktrees for agent isolation
argument-hint: prd-file
model: claude-opus-4-1
---

# Execute PRD with Parallel Multi-Agent Implementation

Implement a feature using the PRD file with parallel execution across multiple agents based on dependency graph and phase breakdown. Each agent pair works in an isolated Git worktree to prevent conflicts.

## PRD File: $ARGUMENTS

## Parallel Execution Process

### 1. **Load & Parse PRD**
- Read the specified PRD file at $1. If it doesn't exist at the specified path, search for the file.
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

### 3. **Git Worktree Setup for Agent Isolation**

Before launching agent pairs, create isolated Git worktrees to prevent file conflicts:

#### Worktree Creation Commands
```bash
# Create worktree directory structure
mkdir -p worktrees

# For each agent pair, create isolated worktree:
# Convention: worktrees/{phase-name}-wave{N}/

# Example for Wave 1 (Foundation):
git worktree add worktrees/foundation-wave1 -b agent-pair-foundation-wave1-$(date +%s)

# Example for Wave 2 (Parallel phases):
git worktree add worktrees/core-logic-wave2 -b agent-pair-core-logic-wave2-$(date +%s)
git worktree add worktrees/ui-components-wave2 -b agent-pair-ui-wave2-$(date +%s)
```

#### Worktree Validation
Before using a worktree, verify it's healthy:
```bash
# Check worktree exists and is valid
cd worktrees/{phase-name}-wave{N}
git status
git branch --show-current
```

### 4. **Multi-Agent Coordination Setup**
- Use TodoWrite to track parallel execution across agents
- Create coordination checkpoints for synchronization
- Establish handoff protocols between phases
- Set up conflict resolution for overlapping work

### 5. **Parallel Phase Execution with Mandatory Review Gates**

#### Phase-Level Parallelization with 1:1 Agent Pairing
For each execution wave (phases with no dependencies):

1. **Setup Agent Worktree Environment**
   - Change directory to assigned worktree: `cd worktrees/{phase-name}-wave{N}`
   - Verify clean working state: `git status`
   - Pull any dependency artifacts from previous phases

2. **Launch Paired Agent Instances**
   - Each implementation agent gets dedicated review agent with matching session ID
   - Each implementation agent executes within their assigned worktree directory
   - Implementation agents execute phase tasks then trigger paired review agent
   - **MANDATORY**: No phase can be marked complete until paired review agent approves
   - Coordination system blocks next wave until all current wave reviews are approved

3. **Agent Pair Execution Pattern**
   ```bash
   # Agent pair works in their isolated worktree
   cd worktrees/{phase-name}-wave{N}
   
   # Implementation work happens here
   # All file changes occur in isolated environment
   
   # When ready, commit work to worktree branch
   git add .
   git commit -m "Phase {N}: {description}"
   
   # Trigger review agent for mandatory approval
   ```

### 6. **Wave-Based Execution Examples**

#### Wave 1: Foundation Phase (No Dependencies)
- **Agent Pair**: Agent-Foundation-Impl-1 + Agent-Foundation-Review-1
- **Worktree**: `worktrees/foundation-wave1/`
- **Tasks**: Core infrastructure, foundational components
- **Setup Commands**:
  ```bash
  git worktree add worktrees/foundation-wave1 -b foundation-$(date +%s)
  cd worktrees/foundation-wave1
  ```
- **Review Gate**: Foundation-Review-1 must approve before Wave 2 starts

#### Wave 2: Parallel Development (Depends on Wave 1)
- **Agent Pair 1**: Agent-CoreLogic-Impl-2 + Agent-CoreLogic-Review-2
- **Agent Pair 2**: Agent-UIComponents-Impl-3 + Agent-UIComponents-Review-3
- **Worktrees**: 
  - `worktrees/core-logic-wave2/`
  - `worktrees/ui-components-wave2/`
- **Setup Commands**:
  ```bash
  # Start from approved Wave 1 state
  git worktree add worktrees/core-logic-wave2 -b core-logic-$(date +%s)
  git worktree add worktrees/ui-components-wave2 -b ui-components-$(date +%s)
  
  # Each agent pair works in their isolated environment
  cd worktrees/core-logic-wave2    # Agent pair 2 works here
  cd worktrees/ui-components-wave2  # Agent pair 3 works here
  ```
- **Review Gates**: BOTH CoreLogic-Review-2 AND UIComponents-Review-3 must approve

#### Wave 3: Integration (Depends on Wave 2)
- **Agent Pair**: Agent-Integration-Impl-4 + Agent-Integration-Review-4  
- **Worktree**: `worktrees/integration-wave3/`
- **Setup Commands**:
  ```bash
  git worktree add worktrees/integration-wave3 -b integration-$(date +%s)
  cd worktrees/integration-wave3
  
  # Merge work from both Wave 2 worktrees
  git merge --no-ff worktrees/core-logic-wave2
  git merge --no-ff worktrees/ui-components-wave2
  ```

### 7. **Merge Coordination Between Waves**

#### After Wave Completion with Review Approval
When all agent pairs in a wave have completed and received review approval:

1. **Merge Worktree Work to Main Branch**
   ```bash
   # Return to main branch
   git checkout main
   
   # Merge each completed worktree (in dependency order)
   git merge --no-ff worktrees/foundation-wave1
   git merge --no-ff worktrees/core-logic-wave2  
   git merge --no-ff worktrees/ui-components-wave2
   ```

2. **Handle Merge Conflicts**
   - If conflicts arise during merge, resolve them manually
   - Use `git status` to see conflicted files
   - Edit files to resolve conflicts
   - Use `git add` to mark conflicts as resolved
   - Complete merge with `git commit`

3. **Validate Merge Success**
   ```bash
   # Verify merge completed successfully
   git log --oneline -5
   git status
   
   # Run any integration tests
   # Validate that all phase requirements are met
   ```

### 8. **Worktree Cleanup**

After successful merge to main branch:

```bash
# Remove completed worktrees
git worktree remove worktrees/foundation-wave1
git worktree remove worktrees/core-logic-wave2
git worktree remove worktrees/ui-components-wave2

# Clean up worktree administrative files
git worktree prune

# Remove worktree directories
rm -rf worktrees/
```

### 9. **Error Handling & Recovery**

#### If Agent Execution Fails
```bash
# Check worktree status
cd worktrees/{failed-phase}
git status
git log --oneline -5

# If work can be salvaged, commit it
git add .
git commit -m "Partial work before failure"

# If complete restart needed, reset worktree
git reset --hard HEAD
git clean -fd
```

#### If Merge Conflicts Occur
```bash
# Check which files have conflicts
git status

# For each conflicted file, manually resolve:
# 1. Open file in editor
# 2. Look for conflict markers: <<<<<<< ======= >>>>>>>
# 3. Choose which version to keep or combine them
# 4. Remove conflict markers
# 5. Save file

# Mark conflicts as resolved
git add {resolved-file}

# Complete merge
git commit -m "Resolved merge conflicts between {wave-descriptions}"
```

#### If Worktree Becomes Corrupted
```bash
# Remove corrupted worktree
git worktree remove --force worktrees/{corrupted-phase}
git worktree prune

# Recreate clean worktree
git worktree add worktrees/{phase-name} -b {new-branch-name}
```

### 10. **Validation & Completion**

#### Final Integration Check
After all phases complete:

```bash
# Verify all changes are merged to main
git checkout main
git status

# Run comprehensive validation
# - Execute any test suites
# - Validate all PRD requirements are met
# - Check that system works end-to-end

# Tag successful implementation
git tag -a "prd-{feature-name}-complete" -m "Completed PRD implementation with Git worktrees"
```

## Implementation Notes

### Agent Instructions
- **Always work within your assigned worktree directory**
- **Never modify files outside your worktree** - this prevents conflicts with other agents
- **Commit your work frequently** to track progress and enable recovery
- **Request review approval** before considering your phase complete
- **Communicate through structured handoff artifacts** for next phase dependencies

### Review Agent Instructions  
- **Change to the agent's worktree directory** before reviewing: `cd worktrees/{phase-name}`
- **Review all changes** using `git diff` and `git log`
- **Verify all phase requirements** are met according to PRD
- **Test the implementation** within the worktree environment
- **Provide clear approval/rejection** with specific feedback

### Coordination Protocol
1. **Pre-execution**: Validate all agent pairs have assigned worktrees
2. **During execution**: Periodic sync checks (every 15 minutes)
3. **Phase boundaries**: Full synchronization with review approvals required
4. **Cross-wave dependencies**: Next wave waits for ALL current wave approvals
5. **Error conditions**: Immediate halt and status report
6. **Completion**: Final integration validation before marking PRD complete

### Key Benefits of Git Worktree Approach
- **Complete Isolation**: Agent pairs cannot interfere with each other's work
- **Parallel Development**: True parallel execution without file conflicts
- **Clean Integration**: Structured merge process respects dependencies
- **Easy Recovery**: Each worktree can be reset or recreated independently
- **Full Git History**: All work is tracked with proper commit history
- **Conflict Prevention**: Eliminates the primary source of multi-agent conflicts

### Performance Characteristics
- **Disk Space**: Each worktree uses additional disk space (~same as repository size)
- **Creation Time**: Worktree creation is fast (<5 seconds per worktree)
- **Merge Time**: Merging between worktrees is efficient with Git's merge algorithms
- **Cleanup**: Worktree removal is quick and thorough

This approach transforms multi-agent execution from conflict-prone shared workspace to isolated, parallel development with clean integration points.
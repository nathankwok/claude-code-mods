---
description: Execute PRD with parallel multi-agent implementation using Git worktrees for agent isolation
argument-hint: prd-file
model: sonnet
---

# Execute PRD with Parallel Multi-Agent Implementation

Implement a feature using the PRD file with parallel execution across multiple agents based on dependency graph and phase breakdown. Each agent pair works in an isolated Git worktree to prevent conflicts.

## PRD File: $ARGUMENTS

## Parallel Execution Process

### 1. **Load & Parse PRD**
- Read the specified PRD file at $1. If it doesn't exist at the specified path, search for the file.
- **Capture current branch**: `ORIGINAL_BRANCH=$(git branch --show-current)`
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
- **Review Gate**: Foundation-Review-1 must approve before merge to main
- **Immediate Merge After Approval**:
  ```bash
  # After review approval, immediately merge to original branch
  git checkout $ORIGINAL_BRANCH
  git merge --no-ff foundation-$(date +%s)
  
  # Clean up completed worktree
  git worktree remove worktrees/foundation-wave1
  git worktree prune
  ```

#### Wave 2: Parallel Development (Depends on Wave 1)
- **Agent Pair 1**: Agent-CoreLogic-Impl-2 + Agent-CoreLogic-Review-2
- **Agent Pair 2**: Agent-UIComponents-Impl-3 + Agent-UIComponents-Review-3
- **Worktrees**: 
  - `worktrees/core-logic-wave2/`
  - `worktrees/ui-components-wave2/`
- **Setup Commands**:
  ```bash
  # Start from current original branch (includes Wave 1 merged work)
  git worktree add worktrees/core-logic-wave2 -b core-logic-$(date +%s)
  git worktree add worktrees/ui-components-wave2 -b ui-components-$(date +%s)
  
  # Each agent pair works in their isolated environment
  cd worktrees/core-logic-wave2    # Agent pair 2 works here
  cd worktrees/ui-components-wave2  # Agent pair 3 works here
  ```
- **Review Gates**: BOTH CoreLogic-Review-2 AND UIComponents-Review-3 must approve
- **Immediate Merge After Both Approvals**:
  ```bash
  # After BOTH reviews approve, merge each worktree to original branch immediately
  git checkout $ORIGINAL_BRANCH
  
  # Merge first worktree
  git merge --no-ff core-logic-$(date +%s)
  
  # Merge second worktree
  git merge --no-ff ui-components-$(date +%s)
  
  # Clean up completed worktrees
  git worktree remove worktrees/core-logic-wave2
  git worktree remove worktrees/ui-components-wave2
  git worktree prune
  ```

#### Wave 3: Integration (Depends on Wave 2)
- **Agent Pair**: Agent-Integration-Impl-4 + Agent-Integration-Review-4  
- **Worktree**: `worktrees/integration-wave3/`
- **Setup Commands**:
  ```bash
  # Start from current original branch (includes Wave 1 and Wave 2 merged work)
  git worktree add worktrees/integration-wave3 -b integration-$(date +%s)
  cd worktrees/integration-wave3
  
  # Note: No manual merging needed - worktree already includes all previous work
  # Agent works on integration tasks with full context from previous phases
  ```
- **Review Gate**: Integration-Review-4 must approve before merge to original branch
- **Immediate Merge After Approval**:
  ```bash
  # After review approval, immediately merge to original branch
  git checkout $ORIGINAL_BRANCH
  git merge --no-ff integration-$(date +%s)
  
  # Clean up completed worktree
  git worktree remove worktrees/integration-wave3
  git worktree prune
  ```

### 7. **Immediate Merge After Each Phase**

#### Phase-by-Phase Merge Strategy
Each phase is merged to the original branch immediately after review approval, **not** waiting until the end:

1. **Single Phase Completion**
   ```bash
   # After review approval for any single phase
   git checkout $ORIGINAL_BRANCH
   git merge --no-ff {phase-branch-name}
   
   # Clean up immediately
   git worktree remove worktrees/{phase-name}
   git worktree prune
   ```

2. **Parallel Phase Completion**
   ```bash
   # After ALL parallel phases in a wave receive review approval
   git checkout $ORIGINAL_BRANCH
   
   # Merge each phase in sequence (order matters for conflict resolution)
   git merge --no-ff {first-phase-branch}
   git merge --no-ff {second-phase-branch}
   
   # Clean up all worktrees from this wave
   git worktree remove worktrees/{first-phase}
   git worktree remove worktrees/{second-phase}
   git worktree prune
   ```

3. **Handle Merge Conflicts During Immediate Merge**
   - If conflicts arise during merge, resolve them immediately
   - Use `git status` to see conflicted files
   - Edit files to resolve conflicts
   - Use `git add` to mark conflicts as resolved
   - Complete merge with `git commit`

4. **Validate Each Merge**
   ```bash
   # After each phase merge, validate success
   git checkout $ORIGINAL_BRANCH
   git log --oneline -3
   git status
   
   # Run any phase-specific tests
   # Validate that current phase requirements are met
   ```

#### Benefits of Immediate Merging
- **Faster Integration**: Issues are caught and resolved immediately
- **Simpler Dependencies**: Next phases always start from complete, tested state
- **Reduced Complexity**: No complex multi-phase merge coordination at the end
- **Better Error Isolation**: Problems are isolated to the specific phase that caused them

### 8. **Worktree Cleanup (Automatic)**

Cleanup happens **automatically after each phase merge** - no manual cleanup needed at the end:

```bash
# Cleanup is integrated into each phase completion:

# Phase 1 completion:
git worktree remove worktrees/foundation-wave1
git worktree prune

# Phase 2 completion (after both parallel phases):
git worktree remove worktrees/core-logic-wave2
git worktree remove worktrees/ui-components-wave2
git worktree prune

# Phase 3 completion:
git worktree remove worktrees/integration-wave3
git worktree prune

# No final cleanup needed - all worktrees cleaned up during execution
```

#### Emergency Cleanup (If Needed)
If something goes wrong and worktrees are left behind:

```bash
# List any remaining worktrees
git worktree list

# Remove all worktrees in worktrees/ directory
git worktree remove --force worktrees/*
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

#### Continuous Validation Throughout Execution
Since each phase merges immediately, validation happens continuously:

```bash
# After each phase merge, validate incrementally:
git checkout $ORIGINAL_BRANCH
git status

# Run phase-specific tests
# Validate current phase requirements
# Ensure integration with previous phases works
```

#### Final PRD Completion Check
After the last phase completes and merges:

```bash
# Final verification - all work is already in original branch
git checkout $ORIGINAL_BRANCH
git status

# Run comprehensive end-to-end validation
# - Execute full test suites
# - Validate all PRD requirements are met
# - Check that complete system works end-to-end

# Tag successful implementation
git tag -a "prd-{feature-name}-complete" -m "Completed PRD implementation with immediate phase merging"
```

#### Benefits of Immediate Merge Approach
- **Continuous Integration**: Each phase is immediately integrated and tested
- **Early Problem Detection**: Issues found and fixed at each phase boundary
- **No Final Merge Conflicts**: Complex end-stage merge coordination eliminated
- **Clean Original Branch**: Original branch always represents the current complete state

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

### Coordination Protocol (Immediate Merge Approach)
1. **Pre-execution**: Capture original branch (`$ORIGINAL_BRANCH`) and validate all agent pairs have assigned worktrees
2. **During execution**: Periodic sync checks (every 15 minutes)
3. **Phase completion**: Review approval → **immediate merge to original branch** → worktree cleanup
4. **Cross-wave dependencies**: Next wave starts from updated original branch (includes all previous work)
5. **Error conditions**: Immediate halt and status report
6. **Completion**: Continuous integration means final validation is just end-to-end testing

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

This approach transforms multi-agent execution from conflict-prone shared workspace to isolated, parallel development with **immediate integration after each phase**. Key change: worktrees are merged to main immediately after review approval, not at the end, ensuring continuous integration and early problem detection.
---
description: "Generate comprehensive PRDs with parallelizable phases, dependency mapping, and multi-agent coordination strategy"
argument-hint: "brainstorm_brief_file_path"
allowed-tools: ["Task", "Read"]
---

# Generate PRD

## Brainstorm brief file: $ARGUMENTS

This command delegates PRD generation to a specialized agent that conducts thorough research and creates comprehensive PRDs with phase-based implementation strategies.

## Process

1. **Validate Input**: Ensure feature file exists and is readable
2. **Delegate to Agent**: Pass the feature file to the specialized PRD generation agent
3. **Monitor Progress**: The agent will handle all research, analysis, and PRD creation

## Agent Responsibilities

The PRD generation agent will:
- Conduct deep codebase analysis and external research
- Create phase-based implementation plans with dependency mapping  
- Design multi-agent coordination strategies
- Generate comprehensive PRDs optimized for one-pass implementation success

## Execution

Let me first validate the feature file exists and then delegate to the PRD generation agent:

### Step 1: Validate Feature File
I'll check if the specified feature file exists and is readable.

### Step 2: Read Feature File Content  
I'll read the feature file to understand the requirements that need to be passed to the agent.

### Step 3: Delegate to PRD Agent
I'll use the Task tool to launch the specialized "generate-prd-agent" with the feature file content and requirements.

Let me start by checking if the feature file exists:

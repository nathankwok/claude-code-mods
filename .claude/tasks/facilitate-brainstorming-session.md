# Task: Facilitate Interactive Brainstorming Session

## Purpose
Guide users through structured brainstorming sessions using BMAD-proven elicitation techniques. Facilitate idea generation, progressive refinement, and session state management for optimal creative outcomes.

## Task Overview
This task implements interactive brainstorming facilitation with:
- Selection and application of appropriate elicitation techniques
- Progressive refinement using numbered actions (0-9)
- Session state tracking and resume capability
- Structured output generation using BMAD templates

## Prerequisites
- Clear understanding of project context and objectives
- Access to brainstorming-agent capabilities
- User availability for interactive session participation

## Instructions

### Phase 1: Session Initialization

1. **Context Gathering**
   ```
   Ask the user:
   - What is the project/problem domain?
   - Who are the target stakeholders/audience?
   - What are the success criteria and key constraints?
   - Are there existing ideas or solutions to build upon?
   - What is the desired session outcome?
   ```

2. **Technique Selection**
   - Analyze context to recommend 3-4 most relevant techniques from the 10 core BMAD techniques
   - Consider user preferences and project complexity
   - Explain rationale for each recommended technique
   - Allow user to select final technique mix

3. **Session Setup**
   - Generate unique session ID: `brainstorm_[timestamp]`
   - **Initialize Session State File**: Use Write tool to create state file
     ```
     Write tool target: .claude/state/projects/[project-name]/brainstorming/session-[session-id].json
     Content: Initialize with session metadata, context, and empty arrays for ideas/themes
     ```
   - **Verify State Creation**: Use Read tool to confirm successful state file creation
   - Set up progressive refinement framework (actions 0-9)
   - Estimate session duration based on selected techniques
   - **Save Initial Configuration**: Update state file with selected techniques and session config

### Phase 2: Guided Brainstorming Execution

4. **Warm-up Phase** (10-15 minutes)
   - Start with "What If" Scenarios or Perspective Shifting
   - Generate initial ideas without evaluation
   - Build momentum and creative confidence
   - Capture all ideas without filtering

5. **Deep Dive Phase** (20-30 minutes)
   - Apply intensive techniques (Root Cause Analysis, Problem Reframing)
   - Drill down into specific areas of interest
   - Challenge assumptions and explore alternatives
   - Focus on quality and depth of exploration

6. **Expansion Phase** (15-20 minutes)
   - Use creative techniques (SCAMPER, Analogical Thinking)
   - Broaden scope and generate novel approaches
   - Cross-pollinate ideas between different angles
   - Encourage wild and unconventional thinking

7. **Progressive Refinement** (20-30 minutes)
   - Select 2-3 most promising ideas for refinement
   - Apply numbered actions (0-9) systematically:
     - Action 0: Capture initial idea
     - Action 1: Clarify core concept
     - Action 2: Identify key components
     - Action 3: Explore variations
     - Action 4: Evaluate feasibility
     - Action 5: Refine and improve
     - Action 6: Add supporting details
     - Action 7: Consider implementation
     - Action 8: Validate with stakeholders
     - Action 9: Finalize refined idea
   - Track refinement progress for each idea

### Phase 3: Session Management and State Tracking

8. **Continuous State Management**
   - **Automated State Saving**: Use Write tool every 5-10 interactions to update state file
   - **State Update Process**:
     ```
     1. Read current state: Use Read tool to load existing session state
     2. Update state data: Add new ideas, update progress, current phase
     3. Write updated state: Use Write tool to save complete updated state
     4. Verify save: Confirm state was written successfully
     ```
   - **State Content Updates**:
     - Track techniques used and ideas generated
     - Update current phase and refinement progress
     - Save session insights and breakthrough moments
   - Monitor session energy and progress
   - Provide periodic summaries of key insights
   - **Backup Creation**: Create state backup before major transitions

9. **Session Flow Control**
   - Recognize when to transition between techniques
   - Manage session pacing and energy levels
   - **Handle Interruptions with Graceful State Saving**:
     ```
     1. Detect interruption or pause request
     2. Use Write tool to save current session state immediately
     3. Include interruption timestamp and resume instructions
     4. Save current context and next recommended actions
     ```
   - **Support Session Resume Functionality**:
     ```
     1. Use Glob tool to find available session state files
     2. Use Read tool to load selected session state
     3. Validate state integrity and completeness
     4. Restore context and continue from last saved point
     ```

10. **Quality Assurance**
    - Ensure comprehensive exploration of problem space
    - Validate that promising ideas receive adequate refinement
    - Verify user understanding and engagement
    - Check that session objectives are being met

### Phase 4: Synthesis and Output Generation

11. **Idea Organization and Synthesis**
    - Group related ideas into coherent themes
    - Identify patterns and connections between concepts
    - Highlight breakthrough insights and novel approaches
    - Note areas requiring additional exploration

12. **Structured Output Generation**
    - **Final State Preservation**: Use Write tool to save complete final session state
    - Generate brainstorming session summary using `brainstorming-output-tmpl.yaml`
    - **State-Driven Template Population**: Use Read tool to load final state and populate template
    - Organize ideas by technique and refinement level
    - Include session metadata and next steps
    - **Archive Session**: Move completed state file to archived subdirectory
    - Prepare outputs for potential handoff to architect agent

## Session State Management Format

```json
{
  "session_id": "brainstorm_[timestamp]",
  "context": {
    "project_domain": "Description of project/problem",
    "stakeholders": ["stakeholder1", "stakeholder2"],
    "constraints": ["constraint1", "constraint2"],
    "success_criteria": ["criteria1", "criteria2"],
    "existing_solutions": ["solution1", "solution2"]
  },
  "session_config": {
    "techniques_selected": ["technique1", "technique2", "technique3"],
    "estimated_duration": "60-90 minutes",
    "current_phase": "warm_up|deep_dive|expansion|refinement|synthesis",
    "start_time": "2024-01-01T10:00:00Z"
  },
  "ideas_generated": [
    {
      "id": "idea_001",
      "technique": "what_if_scenarios",
      "content": "Detailed idea description",
      "theme": "theme_category",
      "refinement_level": 3,
      "actions_completed": ["0", "1", "2", "3"],
      "feasibility_score": 7,
      "potential_impact": "high"
    }
  ],
  "themes_identified": [
    {
      "name": "theme1",
      "description": "Theme description",
      "ideas": ["idea_001", "idea_003"],
      "priority": "high"
    }
  ],
  "session_insights": [
    "Key insight 1",
    "Key insight 2"
  ],
  "next_actions": [
    "Continue refinement of top 3 ideas",
    "Conduct market research for theme1",
    "Schedule follow-up brainstorming session"
  ],
  "save_timestamp": "2024-01-01T11:30:00Z"
}
```

## State File Management Implementation Examples

### Example 1: Session Initialization
```bash
# Step 1: Create session state file using Write tool
Write tool:
File: .claude/state/projects/ecommerce-platform/brainstorming/session-brainstorm_20240301_1400.json
Content: {
  "session_id": "brainstorm_20240301_1400",
  "context": {
    "project_domain": "E-commerce platform enhancement",
    "stakeholders": ["customers", "admin", "developers"],
    "constraints": ["6-month timeline", "existing user base", "mobile compatibility"],
    "success_criteria": ["improve conversion", "enhance user experience"],
    "existing_solutions": []
  },
  "session_config": {
    "techniques_selected": ["what_if_scenarios", "root_cause_analysis", "scamper"],
    "estimated_duration": "90 minutes",
    "current_phase": "initialization",
    "start_time": "2024-03-01T14:00:00Z"
  },
  "ideas_generated": [],
  "themes_identified": [],
  "session_insights": [],
  "next_actions": ["Begin warm-up phase with what_if_scenarios"],
  "save_timestamp": "2024-03-01T14:05:00Z"
}

# Step 2: Verify creation using Read tool
Read tool: .claude/state/projects/ecommerce-platform/brainstorming/session-brainstorm_20240301_1400.json
```

### Example 2: Mid-Session State Update
```bash
# Step 1: Load current state using Read tool
Read tool: .claude/state/projects/ecommerce-platform/brainstorming/session-brainstorm_20240301_1400.json

# Step 2: Update state with new ideas using Write tool
Write tool:
File: .claude/state/projects/ecommerce-platform/brainstorming/session-brainstorm_20240301_1400.json
Content: {
  # ... previous content plus new ideas
  "ideas_generated": [
    {
      "id": "idea_001",
      "technique": "what_if_scenarios",
      "content": "What if checkout was a single click with biometric auth",
      "theme": "checkout_optimization",
      "refinement_level": 2,
      "actions_completed": ["0", "1", "2"],
      "feasibility_score": 8,
      "potential_impact": "high"
    }
  ],
  "session_config": {
    "current_phase": "deep_dive",
    # ... other config
  },
  "save_timestamp": "2024-03-01T14:35:00Z"
}
```

### Example 3: Session Resume
```bash
# Step 1: Find available sessions using Glob tool
Glob tool: .claude/state/projects/ecommerce-platform/brainstorming/*.json

# Step 2: Load selected session using Read tool
Read tool: .claude/state/projects/ecommerce-platform/brainstorming/session-brainstorm_20240301_1400.json

# Step 3: Validate and continue from last phase
# Current phase: "deep_dive"
# Next actions: ["Continue root cause analysis", "Apply SCAMPER to idea_001"]
# Resume immediately with state restoration confirmation
```

## Technique-Specific Facilitation Guidelines

### What If Scenarios
- Start with current constraints and systematically remove them
- Encourage bold thinking without immediate feasibility concerns
- Generate multiple scenarios before evaluating any
- Build on each scenario with follow-up "what if" questions

### Root Cause Analysis
- Begin with surface problem symptoms
- Apply "5 Whys" technique rigorously
- Map cause-and-effect relationships visually
- Identify multiple root causes, not just one

### Future Visioning
- Start with perfect outcome description
- Work backward to identify key milestones
- Consider multiple paths to the same goal
- Balance optimism with realistic constraints

### Perspective Shifting
- Explicitly name each stakeholder perspective
- Spend adequate time in each viewpoint
- Look for conflicting requirements between perspectives
- Seek solutions that satisfy multiple viewpoints

### Constraint Removal
- Identify all current limitations first
- Remove constraints one by one
- Generate ideas for each constraint-free scenario
- Gradually reintroduce constraints to filter ideas

### Analogical Thinking
- Research analogous problems in different domains
- Look for pattern similarities, not surface similarities
- Adapt solutions rather than copying them directly
- Combine insights from multiple analogies

### Problem Reframing
- Generate 3-5 different problem statements
- Explore solutions for each reframing
- Look for reframings that open new solution spaces
- Consider both narrower and broader problem scopes

### SCAMPER Method
- Apply each prompt systematically to current ideas
- Don't skip prompts that seem less relevant
- Combine multiple SCAMPER transformations
- Generate multiple variations for each prompt

### Six Thinking Hats
- Dedicate specific time blocks to each hat
- Resist mixing hat modes within time blocks
- Use Blue Hat to manage transitions between modes
- Capture insights from each hat separately

### Progressive Refinement
- Apply to only the most promising ideas
- Complete each action before moving to next
- Document decision rationale at each action
- Allow iteration back to earlier actions if needed

## Output Requirements

### Required Deliverables
1. **Session Summary Document**: Comprehensive summary using brainstorming-output template
2. **Refined Ideas List**: Top 3-5 ideas with full progressive refinement (actions 0-9)
3. **Theme Analysis**: Organized themes with supporting ideas and priority rankings
4. **Next Steps Recommendations**: Clear actions for continuing idea development
5. **Session State File**: Complete session state for resume capability

### Quality Criteria
- All selected techniques were applied comprehensively
- At least 2-3 ideas received full progressive refinement (actions 0-9)
- Ideas are organized into coherent themes with clear relationships
- Session outputs are structured and ready for handoff to next phase
- Session state allows for seamless resume if interrupted

## Error Handling

### Common Issues and Solutions
- **Low Idea Generation**: Switch to more creative techniques (SCAMPER, Analogical Thinking)
- **Analysis Paralysis**: Set timers for each phase and enforce movement
- **Scope Creep**: Regularly check against original objectives and constraints
- **User Fatigue**: Take breaks and vary technique intensity
- **Technical Confusion**: Focus on conceptual exploration, defer technical details

### Recovery Procedures
- **Session Interruption**: 
  ```
  1. Use Write tool to save immediate state with interruption flag
  2. Include resume context and next recommended actions
  3. Provide clear resume instructions with state file path
  ```
- **Lost Context**: 
  ```
  1. Use Read tool to load most recent session state
  2. Review session state and recent idea history with user
  3. Confirm understanding before continuing
  ```
- **Technique Struggles**: Switch to alternative technique or provide additional guidance
- **Output Quality Issues**: Apply additional refinement cycles or validate with user
- **State File Corruption**:
  ```
  1. Attempt to load backup state file using Read tool
  2. If no backup, recreate state from available session context
  3. Validate recreated state with user before continuing
  ```

## Success Metrics
- Session generates 15-30 distinct ideas across multiple techniques
- 2-3 ideas achieve full progressive refinement (actions 0-9)
- Ideas are organized into 3-5 coherent themes
- User reports high satisfaction with creative process
- Outputs provide clear foundation for technical architecture planning

## Integration Points
- **Input**: User context, project objectives, existing ideas
- **Output**: Structured brainstorming results ready for architect-agent
- **Tools**: Uses brainstorming-agent capabilities and BMAD templates
- **Handoff**: Prepared outputs for technical architecture design phase
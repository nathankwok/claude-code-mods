---
allowed-tools: Task, mcp__context7, mcp__gemini-cli, mcp__clear-thought, mcp__grep
description: Interactive BMAD-inspired brainstorming session with structured elicitation techniques
argument-hint: [project-context] | "resume_session" | "list_sessions"
model: opus
---

# Interactive Brainstorming Session

Start an interactive BMAD-inspired brainstorming session with structured technique selection and progressive refinement capabilities.

## Project Context: $ARGUMENTS

## 🚀 Immediate Agent Invocation

**This command automatically invokes the brainstorming-agent for interactive facilitation:**

```
Please invoke the brainstorming-agent for an interactive BMAD-inspired brainstorming session.

Session Context: "$ARGUMENTS"

Instructions for brainstorming-agent:
1. Initialize session state with project-aware persistence
2. Gather additional context and clarify objectives  
3. Recommend appropriate brainstorming techniques
4. Facilitate interactive brainstorming with progressive refinement
6. Generate structured outputs and project briefs
7. Provide session state management and resume capability

Agent should begin immediately with context gathering and session initialization.
```

## Brainstorming Session Features

### 10 Structured Brainstorming Techniques
1. **"What If" Scenarios** - Explore hypothetical situations and breakthrough opportunities
2. **Root Cause Analysis** - Deep dive using "5 Whys" to identify fundamental issues
3. **Future Visioning** - Envision ideal outcomes and work backward to create roadmaps
4. **Perspective Shifting** - Multiple stakeholder viewpoints (users, team, executives, domain experts)
5. **Constraint Removal** - Imagine unlimited resources to generate breakthrough ideas
6. **Analogical Thinking** - Draw parallels from other domains and successful solutions
7. **Problem Reframing** - Redefine core problems from different angles and scopes
8. **SCAMPER Method** - Systematic creativity (Substitute, Combine, Adapt, Modify, Put to other uses, Eliminate, Reverse)
9. **Six Thinking Hats** - Different thinking modes (facts, emotions, critical thinking, benefits, creativity, process)
10. **Progressive Refinement** - Iterative development with numbered actions (0-9)

### Interactive Experience
- **Technique Selection**: Choose appropriate techniques based on project context
- **Guided Facilitation**: Structured prompts and systematic exploration
- **Progressive Refinement**: Numbered action system (0-9) for iterative idea development
- **Session State Management**: Save progress and resume interrupted sessions

### Session Flow
1. **Context Gathering**: Project background, objectives, constraints, and stakeholders
2. **Technique Recommendation**: AI suggests 3-4 most relevant techniques with explanations
3. **Interactive Brainstorming**: Guided facilitation through selected techniques
4. **Progressive Refinement**: Systematic improvement of promising ideas (actions 0-9)
6. **Session Synthesis**: Organize ideas into themes and actionable concepts
7. **Output Generation**: Structured summary and project brief creation

### State Management & Resume Capability
- **Session Persistence**: Automatic state saving every 5 interactions
- **Resume Sessions**: Continue interrupted sessions from exact stopping point
- **Project-Aware Storage**: `.claude/state/projects/[project-name]/brainstorming/`
- **Progress Tracking**: Monitor refinement levels and technique completion
- **Session History**: Complete audit trail of ideas, decisions, and refinements

## Progressive Refinement System (0-9)

The heart of BMAD-inspired ideation with systematic improvement:
- **Action 0**: Initial idea capture and documentation
- **Action 1**: Clarify core concept and key elements
- **Action 2**: Identify key components and relationships
- **Action 3**: Explore variations and alternative approaches
- **Action 4**: Evaluate feasibility and practical constraints
- **Action 5**: Refine and improve based on evaluation insights
- **Action 6**: Add supporting details and implementation considerations
- **Action 7**: Consider technical and practical implementation aspects
- **Action 8**: Validate with stakeholder perspectives
- **Action 9**: Finalize refined concept ready for architecture planning


## Session Examples and Use Cases

### New Feature Development
```
Context: "Mobile app feature for expense tracking"
Recommended Techniques: Future Visioning, Perspective Shifting, SCAMPER
Progressive Refinement: Focus on user experience and technical feasibility
```

### Problem Solving
```
Context: "User onboarding completion rates are low"
Recommended Techniques: Root Cause Analysis, Problem Reframing, "What If" Scenarios
Progressive Refinement: Systematic solution development and validation
```

### Innovation Exploration
```
Context: "Next generation of our core product"
Recommended Techniques: Constraint Removal, Analogical Thinking, Future Visioning
Progressive Refinement: Breakthrough concept development and feasibility analysis
```

## 🛠️ Actionable Execution Process

### 1. **AUTOMATED Session Initialization** ⚡
**Executable Steps (performed by brainstorming-agent):**

```bash
# Step 1: Create project-aware state directory
mkdir -p .claude/state/projects/[project-name]/brainstorming/

# Step 2: Generate unique session ID
session_id="brainstorm_$(date +%Y%m%d_%H%M%S)"

# Step 3: Initialize session state file
echo '{
  "session_id": "'$session_id'",
  "context": "'$ARGUMENTS'",
  "created_at": "'$(date -Iseconds)'",
  "status": "initializing",
  "techniques_selected": [],
  "ideas_generated": [],
  "current_phase": "context_gathering"
}' > .claude/state/projects/[project-name]/brainstorming/session-$session_id.json
```

**Agent Actions:**
- ✅ Context gathering questionnaire
- ✅ Technique recommendation with explanations  
- ✅ Session parameter definition
- ✅ State file creation and verification

### 2. **INTERACTIVE Brainstorming Execution** 🎯
**Live Agent Facilitation:**
- **Warm-up Phase**: Agent guides through initial techniques
- **Deep Dive Phase**: Intensive exploration with selected methods
- **Progressive Refinement**: Numbered actions (0-9) for promising ideas

**Continuous State Updates:**
- Every 5 interactions: Auto-save progress
- Technique transitions: Update phase status
- Idea refinement: Track progression levels

### 3. **PERSISTENT Session Management** 💾
**Resume Capability:**
```bash
# List available sessions
ls .claude/state/projects/[project-name]/brainstorming/

# Resume specific session
/brainstorm "resume_session_20240902_143022"
```

**State Recovery Process:**
1. **Load session state** from persistent file
2. **Restore context** and progress summary
3. **Continue from last phase** with full context
4. **Update timestamps** and session metadata

### 4. **STRUCTURED Output Generation** 📋
**Template-Based Deliverables:**
- **Brainstorming Summary**: Ideas organized by technique and refinement level
- **Project Brief**: Ready for architect-agent handoff
- **Session Archive**: Complete audit trail and resume capability

## 📋 **Template Integration System**

### **Built-in Session Templates**
**Brainstorming-agent uses structured templates for all outputs:**

#### **Session Summary Template**
```markdown
# Brainstorming Session Summary

## Session Metadata
- Session ID: [unique_identifier]
- Context: [original_context]
- Techniques Used: [list_of_techniques]
- Duration: [session_duration]
- Ideas Generated: [total_count]

## Ideas by Technique
### [Technique 1]
- Idea 1 (refinement level: X/9)
- Idea 2 (refinement level: Y/9)


## Refined Concepts (Action Level 6+)
### Top Priority Ideas
### Implementation Recommendations
### Next Steps
```

#### **Project Brief Template**
```markdown
# Project Brief: [Project Name]

## Executive Summary
[2-3 sentence overview]

## Problem Statement
[Refined problem definition from brainstorming]

## Solution Concepts
[Top refined ideas with implementation considerations]


## Technical Considerations
[Ready for architect-agent handoff]

## Success Metrics
[Measurable outcomes and KPIs]

## Next Phase Recommendations
[Architecture planning requirements]
```

### **Template Usage in Agent**
**brainstorming-agent automatically applies templates:**
1. **Session initialization**: Uses session state template
2. **Progress tracking**: Updates structured progress template
4. **Final output**: Generates project brief using standard template
5. **Archive creation**: Uses session archive template

## 🔗 **Integration with BMAD Enhanced Planning System**

### **Phase 1 Fulfillment** ✅
This command implements complete Phase 1 requirements:
- ✅ **Brainstorming agent** with 10+ elicitation techniques
- ✅ **Interactive refinement** with numbered actions (0-9)
- ✅ **Template-based output** generation with structured formats
- ✅ **Session state tracking** with resume capability
- ✅ **Agent invocation** through seamless command-to-agent bridge

### **Multi-Agent Workflow Integration** 🔄
```
1. /brainstorm "project context" 
   ↓ [generates project brief]
2. /architect @project_brief.md
   ↓ [creates technical architecture]
3. /generate-prd @architecture_plan.md
   ↓ [produces structured PRD]
4. /execute-prd @generated_prd.md
   ↓ [coordinated implementation]
```

**Handoff Data Flow:**
- **Brainstorming → Architecture**: Project brief with refined concepts
- **Architecture → PRD**: Technical design with implementation details
- **PRD → Execution**: Structured requirements with acceptance criteria

## 🎮 Command Usage Examples

### **Basic Session with Agent Invocation**
```bash
/brainstorm "Mobile expense tracking feature"

# This triggers the brainstorming-agent with:
# 1. Immediate context gathering
# 2. Technique recommendation
# 3. Interactive session facilitation
# 4. Progressive refinement guidance
# 6. Structured output generation
```

### **Resume Interrupted Session**
```bash
/brainstorm "resume_session"

# Agent automatically:
# 1. Scans for existing session files
# 2. Presents available sessions with context
# 3. Loads selected session state
# 4. Continues from last checkpoint
```

### **List Available Sessions**
```bash
/brainstorm "list_sessions"

# Shows all brainstorming sessions with:
# - Session timestamps
# - Project context
# - Completion status
# - Resume instructions
```

### **Complex Project Context**
```bash
/brainstorm "User onboarding completion rates are low - need solutions that consider mobile UX constraints and API limitations"

# Agent will:
# 1. Parse complex context
# 2. Recommend Root Cause Analysis + Problem Reframing
# 3. Conduct UX pattern research
# 4. Apply mobile-specific constraints
# 5. Generate implementation-ready solutions
```

## 🔄 **Seamless Agent Integration Flow**

### **Step 1: Command Execution → Agent Invocation**
```
User: /brainstorm "AI-powered project management feature"
     ↓
Command invokes brainstorming-agent with structured context
     ↓
Agent begins with: "I'll facilitate a comprehensive brainstorming session for your AI-powered project management feature..."
```

### **Step 2: Agent-Led Session with Tools**
```
brainstorming-agent:
1. Creates session state: .claude/state/projects/claude-code-mods/brainstorming/session_20240902_143022.json
2. Conducts context gathering questionnaire
3. Recommends techniques: "Future Visioning, Problem Reframing, SCAMPER Method"
4. Begins interactive facilitation
6. Guides progressive refinement (actions 0-9)
```

### **Step 3: Continuous State Management**
```
# Every 5 interactions:
brainstorming-agent saves progress to session state file

# Session interruption:
User can resume with: /brainstorm "resume_session"

# Agent loads state and continues seamlessly
```

### **Step 4: Structured Handoff**
```
brainstorming-agent generates:
✓ Brainstorming Summary (themes, refined ideas)
✓ Project Brief (ready for architect-agent)
✓ Implementation Recommendations
```

## Success Metrics

### Session Quality Indicators
- **Idea Generation**: 15+ unique ideas per session with diverse techniques
- **Refinement Depth**: Average refinement level of 6+ for promising ideas
- **Session Completion**: 90%+ of sessions reach synthesis phase with actionable outputs

### Output Quality Measures
- **Project Brief Completeness**: All required sections with detailed context
- **Handoff Success**: 85%+ successful transitions to architect-agent for technical planning
- **User Satisfaction**: Clear, actionable insights ready for next development phase
- **Resume Capability**: 100% successful session resumption from interruption

## 🎯 **Quality Assurance & Success Metrics**

### **Agent Performance Standards**
- **Context Understanding**: 100% of sessions begin with comprehensive context gathering
- **Technique Application**: Minimum 3 techniques per session with structured facilitation
- **Progressive Refinement**: 80%+ of promising ideas reach refinement level 6+
- **State Persistence**: 100% reliable session state saves and resume capability
- **Template Compliance**: All outputs use structured templates with required sections

### **User Experience Standards**
- **Immediate Agent Response**: No manual invocation steps required
- **Clear Progress Indicators**: Session phase and progress visible throughout
- **Actionable Outputs**: All sessions generate implementable recommendations
- **Seamless Resume**: Interrupted sessions resume with full context
- **Quality Handoffs**: 90%+ successful transitions to architect-agent

### **Integration Quality Checks**
- ✅ **Command-to-Agent Bridge**: Automatic agent invocation
- ✅ **Executable Process**: All steps implementable by agent
- ✅ **Template Integration**: Structured outputs using consistent formats
- ✅ **Usage Examples**: Clear practical examples with expected results
- ✅ **Workflow Integration**: Seamless handoff to next development phase

## 🚨 **Anti-Patterns & Error Prevention**

### **Command-Level Anti-Patterns**
- ❌ **Manual Agent Invocation**: Don't require users to manually call brainstorming-agent
- ❌ **Unclear Process**: Don't describe steps without making them executable
- ❌ **Missing Templates**: Don't generate unstructured outputs
- ❌ **Broken Integration**: Don't create gaps between command and agent execution

### **Agent-Level Anti-Patterns**
- ❌ **Rushed Techniques**: Don't skip deep exploration for speed
- ❌ **Incomplete Refinement**: Don't leave promising ideas under-developed
- ❌ **Lost State**: Don't fail to save session progress regularly
- ❌ **Poor Context**: Don't start ideation without comprehensive understanding
- ❌ **Incomplete Handoffs**: Don't finish sessions without actionable next steps

### **Quality Control Measures**
- ✅ **Automatic Validation**: Agent validates session completeness before finishing
- ✅ **Template Compliance**: All outputs checked against template requirements
- ✅ **State Verification**: Session state files validated for completeness
- ✅ **Handoff Readiness**: Project briefs verified for architect-agent compatibility

---

**Remember**: This command provides the complete brainstorming experience through automatic agent invocation. Users execute `/brainstorm "context"` and immediately get full interactive facilitation, structured output generation, and seamless integration with the BMAD planning system. The brainstorming-agent handles all execution details, state management, and template application automatically.
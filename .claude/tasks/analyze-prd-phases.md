# Task: Analyze PRD Phases and Break Down into Parallelizable Components

## Purpose
Break down PRDs into parallelizable phases with comprehensive dependency analysis. Identify independent work streams, coordination requirements, and generate detailed phase breakdown documentation that enables effective parallel execution.

## Task Overview
This task implements systematic PRD analysis with:
- Complete phase extraction and analysis from PRD documents
- Granular task identification within phases
- Comprehensive dependency mapping between phases and tasks
- Parallelization opportunity identification and work stream planning
- Coordination requirement analysis and synchronization point definition

## Prerequisites
- Access to complete PRD file with defined phases
- Understanding of system architecture (preferably from previous architecture design)
- Access to architect-agent capabilities
- Clear project context and objectives
- Access to existing architecture state files from design-system-architecture task

## Instructions

### Phase 1: PRD Analysis and Phase Extraction

1. **Load and Parse PRD Content with Architecture Context**
   ```
   Use Read tool to analyze:
   - Complete PRD file content
   - Phase definitions and objectives  
   - Task lists within each phase
   - Acceptance criteria and success metrics
   - Dependencies mentioned in PRD
   - Existing architecture state files:
     Primary location: .claude/state/projects/[project-name]/architecture/
     Files to load:
     - system-design.json (overall system architecture and components)
     - technology-decisions.json (technology stack decisions)
     - component-specs.json (detailed component specifications)
     - parallel-development-plan.json (existing parallelization insights)
   ```

   **Architecture State Integration Protocol**:
   - **Primary Path**: Load existing architecture files from `.claude/state/projects/[project-name]/architecture/`
   - **Fallback Handling**: If architecture files are missing:
     - Document that analysis proceeds without architecture context
     - Log missing architecture state in phase analysis results
     - Request architecture design completion if critical for phase breakdown
     - Make documented assumptions about system components and dependencies
   - **Architecture Context Processing**: For each architecture file found:
     - Map PRD phases to system components from system-design.json
     - Align technology decisions with phase implementation requirements
     - Use component specifications to inform task complexity estimates
     - Leverage existing parallel development insights for enhanced parallelization analysis

2. **Phase Inventory Creation**
   - **Extract All Phases**: Identify every phase defined in the PRD
   - **Phase Classification**: Categorize phases by type (foundation/parallel/integration/sequential)
   - **Complexity Assessment**: Evaluate implementation complexity for each phase (1-10 scale)
   - **Duration Estimation**: Estimate effort and timeline for each phase
   - **Resource Requirements**: Identify skill sets and team size needs per phase

3. **Architecture-Informed Task-Level Analysis**
   - **Task Extraction**: Identify all tasks within each phase, mapping to system components
   - **Task Classification**: Categorize by type using architecture context:
     - **Frontend**: Map to UI components from system architecture
     - **Backend**: Map to service components and APIs from architecture
     - **Database**: Map to data architecture and storage systems
     - **Infrastructure**: Map to deployment and infrastructure architecture
     - **Testing**: Map to component interfaces and integration points
   - **Implementation Scope**: Understand task scope using architecture specifications:
     - Reference component specs for detailed implementation requirements
     - Use technology decisions to inform implementation approaches
     - Apply architecture constraints to scope estimates
   - **Component-Aware File Impact Analysis**: Identify files/components using architecture state:
     - Map tasks to architectural components and their file locations
     - Identify shared component files that require coordination
     - Use architecture to predict inter-component dependencies
   - **Architecture-Aligned Skill Requirements**: Map skills using technology decisions:
     - Reference technology stack from architecture state
     - Align skill requirements with architectural technology choices
     - Consider component-specific technology requirements

### Phase 2: Dependency Analysis and Mapping

4. **Phase-Level Dependency Identification**
   - **Hard Dependencies**: Identify blocking dependencies that cannot be worked around
   - **Soft Dependencies**: Find preferential dependencies that could be managed differently
   - **Resource Dependencies**: Identify shared files, databases, or systems creating conflicts
   - **Business Logic Dependencies**: Map dependencies based on business process flow

5. **Task-Level Dependency Analysis**
   - **Technical Dependencies**: Find dependencies based on code/system architecture
   - **Data Flow Dependencies**: Map dependencies based on data creation and consumption
   - **Integration Dependencies**: Identify dependencies based on API/interface requirements
   - **File Conflict Analysis**: Find tasks that modify the same files or components

6. **Dependency Graph Construction**
   - **Visual Dependency Mapping**: Create comprehensive dependency matrix
   - **Critical Path Analysis**: Identify longest dependency chains
   - **Circular Dependency Detection**: Find and resolve circular dependencies
   - **Dependency Strength Assessment**: Rate dependency strength (critical/high/medium/low)

### Phase 3: Parallelization Analysis and Planning

7. **Independent Work Stream Identification**
   - **Component Isolation Analysis**: Find phases/tasks with minimal external dependencies
   - **Interface Boundary Analysis**: Identify clear interface boundaries enabling parallel work
   - **Resource Conflict Assessment**: Analyze potential conflicts in parallel execution
   - **Integration Point Planning**: Plan coordination points for independent streams

8. **Execution Wave Planning**
   - **Wave Grouping**: Group phases that can execute simultaneously
   - **Capacity Planning**: Determine maximum concurrent teams per wave
   - **Duration Optimization**: Optimize wave timing for maximum parallel efficiency  
   - **Synchronization Point Definition**: Define checkpoints where waves must coordinate

9. **Coordination Requirements Analysis**
   - **Communication Needs**: Define inter-team communication requirements
   - **Shared Resource Management**: Plan management of shared resources
   - **Integration Checkpoints**: Schedule integration and validation points
   - **Conflict Resolution Procedures**: Define processes for handling conflicts

### Phase 4: Analysis Documentation and State Management

10. **Phase Analysis State Persistence**
    - **Project Detection**: Extract project name from PRD path or context
    - **State Directory Management**: Create phase analysis state structure
      ```
      Use Write tool to create/update:
      .claude/state/projects/[project-name]/architecture/
      ├── phase-breakdown.json
      ├── dependency-analysis.json  
      ├── parallelization-plan.json
      └── coordination-requirements.json
      ```
    - **Analysis Results Storage**: Save complete analysis using Write tool
    - **Version Management**: Track analysis versions and updates

11. **Structured Documentation Generation**
    - **Load Phase Breakdown Template**: Use Read tool to load phase-breakdown-tmpl.yaml
    - **Generate Phase Analysis Document**: Populate template with analysis results
    - **Create Dependency Matrix**: Generate comprehensive dependency documentation
    - **Parallelization Strategy Document**: Create detailed parallel execution plan
    - **Save All Documentation**: Persist documentation using Write tool

### Phase 5: Validation and Quality Assurance

12. **Analysis Validation**
    - **Completeness Check**: Verify all PRD phases and tasks are captured
    - **Dependency Logic Validation**: Ensure dependency graph is logical and acyclic  
    - **Parallelization Feasibility Assessment**: Validate parallelization opportunities are realistic
    - **Resource Requirement Validation**: Check that resource requirements are reasonable

13. **Quality Assurance Review**
    - **Coordination Practicality**: Assess whether coordination requirements are manageable
    - **Risk Assessment**: Identify risks specific to parallel execution approach
    - **Timeline Realism**: Validate that timeline estimates are achievable
    - **Integration Complexity**: Evaluate integration checkpoint feasibility

## Phase Analysis State Format

```json
{
  "analysis_id": "phase_analysis_[timestamp]",
  "prd_source": "path/to/prd.md", 
  "analysis_date": "2024-01-01T10:00:00Z",
  "project_context": {
    "project_name": "project_name",
    "architecture_reference": "arch_[timestamp]",
    "architecture_integration": {
      "system_design_loaded": true,
      "technology_decisions_loaded": true,
      "component_specs_loaded": true,
      "parallel_plan_loaded": false,
      "missing_architecture_files": ["parallel-development-plan.json"],
      "integration_quality": "high|medium|low|none"
    },
    "system_components": ["component1", "component2"],
    "technology_stack": {
      "frontend": "React/TypeScript",
      "backend": "Node.js/Express",
      "database": "PostgreSQL"
    }
  },
  "phase_inventory": [
    {
      "phase_id": "phase-1",
      "phase_number": 1,
      "phase_name": "User Authentication System",
      "phase_objective": "Implement secure user authentication with OAuth2",
      "phase_type": "foundation|parallel|integration|sequential",
      "complexity_score": 7,
      "estimated_effort": "3 weeks",
      "team_requirements": "2 backend developers, 1 security specialist",
      "parallelization_status": "can_be_parallel_after_foundation",
      "tasks": [
        {
          "task_id": "task-1-1",
          "task_name": "OAuth2 provider integration",
          "task_type": "backend",
          "complexity": 8,
          "duration": "1 week",
          "files_affected": ["src/auth/oauth.js", "config/auth.yaml"],
          "dependencies": [],
          "required_skills": ["OAuth2", "Node.js", "JWT"],
          "architecture_context": {
            "system_component": "authentication_service",
            "component_interfaces": ["REST API", "JWT middleware"],
            "technology_alignment": "Node.js/Express from architecture",
            "dependency_components": ["user_service", "session_service"]
          }
        }
      ]
    }
  ],
  "dependency_analysis": {
    "phase_dependencies": [
      {
        "dependent_phase": "phase-2",
        "dependency_phase": "phase-1", 
        "dependency_type": "technical|business|resource|data",
        "dependency_strength": "hard|soft",
        "dependency_reason": "User auth required before user profile management",
        "violation_impact": "System security compromise",
        "workaround_possible": false,
        "coordination_requirements": ["API contract validation"]
      }
    ],
    "task_dependencies": [
      {
        "dependent_task": "task-2-1",
        "dependency_task": "task-1-1",
        "dependency_type": "technical",
        "shared_components": ["auth middleware", "user session management"],
        "coordination_method": "API contract review"
      }
    ],
    "critical_path": ["phase-1", "phase-3", "phase-5"],
    "critical_path_duration": "8 weeks"
  },
  "parallelization_analysis": {
    "max_parallel_phases": 3,
    "execution_waves": [
      {
        "wave_number": 1,
        "wave_name": "Foundation Setup",
        "phases": ["phase-1"],
        "duration": "3 weeks",
        "max_concurrent_teams": 1,
        "coordination_requirements": ["architecture review", "security audit"]
      },
      {
        "wave_number": 2,
        "wave_name": "Core Features",
        "phases": ["phase-2", "phase-3"],
        "duration": "4 weeks", 
        "max_concurrent_teams": 2,
        "dependencies": ["wave-1-complete"],
        "synchronization_points": ["API integration testing"]
      }
    ],
    "independent_work_streams": [
      {
        "stream_id": "stream-1",
        "stream_name": "User Management",
        "focus_area": "User accounts and profiles",
        "phases": ["phase-1", "phase-2"],
        "team_requirements": "2 backend, 1 frontend developer",
        "external_dependencies": ["auth provider API"],
        "integration_points": ["user profile API", "session management"]
      }
    ],
    "parallel_constraints": [
      {
        "constraint_name": "Database schema coordination",
        "affected_phases": ["phase-1", "phase-2", "phase-4"],
        "constraint_description": "Multiple phases modify user-related tables",
        "mitigation": "Coordinate schema changes through migration reviews"
      }
    ]
  },
  "coordination_requirements": {
    "synchronization_points": [
      {
        "sync_point_name": "API Contract Validation",
        "trigger": "completion of interface design tasks",
        "participating_phases": ["phase-1", "phase-2", "phase-3"],
        "duration": "1 day",
        "success_criteria": ["All APIs documented", "Contract tests pass"],
        "coordination_type": "review_and_approval"
      }
    ],
    "communication_schedule": [
      {
        "communication_type": "daily_standup",
        "frequency": "daily",
        "participants": ["all_parallel_teams"],
        "duration": "15 minutes",
        "agenda": ["progress_update", "blocker_discussion", "coordination_needs"]
      },
      {
        "communication_type": "integration_review",
        "frequency": "weekly",
        "participants": ["tech_leads", "architect"],
        "duration": "60 minutes",
        "agenda": ["integration_progress", "dependency_resolution", "risk_assessment"]
      }
    ],
    "shared_resources": [
      {
        "resource_name": "database_schema",
        "resource_type": "database",
        "access_pattern": "read_write",
        "conflict_potential": "high",
        "coordination_method": "migration_review_process",
        "responsible_team": "backend_team_1"
      }
    ]
  },
  "risk_analysis": {
    "coordination_risks": [
      {
        "risk_name": "API contract misalignment",
        "probability": "medium",
        "impact": "high",
        "affected_phases": ["phase-1", "phase-2"],
        "mitigation": "Weekly contract review meetings",
        "contingency": "Contract versioning and backward compatibility"
      }
    ],
    "integration_risks": [
      {
        "risk_name": "Database migration conflicts",
        "technical_area": "data_persistence",
        "detection_method": "automated migration testing",
        "prevention": "Migration coordination workflow",
        "recovery_plan": "Rollback and re-coordinate migrations"
      }
    ]
  },
  "validation_results": {
    "completeness_score": "98%",
    "dependency_consistency": "validated",
    "parallelization_feasibility": "high_confidence",
    "coordination_complexity": "manageable",
    "timeline_realism": "achievable_with_coordination"
  }
}
```

## Dependency Analysis Techniques

### Phase Dependency Identification Process
1. **Business Process Flow Analysis**: Map dependencies based on business logic sequence
2. **Technical Dependency Analysis**: Identify code-level and system-level dependencies
3. **Data Flow Dependency Analysis**: Map dependencies based on data creation and consumption
4. **Resource Dependency Analysis**: Identify shared resource conflicts and coordination needs

### Dependency Strength Assessment
```yaml
dependency_classification:
  hard_dependencies:
    description: "Cannot be worked around, must be respected"
    examples: ["Auth must exist before user profiles", "Database schema before data operations"]
    impact: "Blocks parallel execution completely"
    
  soft_dependencies:
    description: "Preferential but can be worked around with coordination"
    examples: ["UI styling after component creation", "Documentation after implementation"]
    impact: "Requires coordination but allows parallel work"
    
  resource_dependencies:
    description: "Shared files or systems requiring coordination"
    examples: ["Multiple teams modifying same API", "Database schema changes"]
    impact: "Requires coordination protocols and conflict resolution"
```

### Critical Path Analysis Implementation
```bash
# Use Task tool for complex dependency analysis if needed
Task tool: "Analyze project dependencies using critical path method for phases [phase_list]"
Task tool: "Calculate critical path duration with task estimates [task_estimates]"
```

## Parallelization Strategy Development

### Work Stream Identification Criteria
- **Independence Level**: Minimal dependencies on other work streams
- **Interface Clarity**: Well-defined interfaces with other components
- **Resource Exclusivity**: Minimal shared resource conflicts
- **Team Capability**: Matches available team skills and capacity

### Execution Wave Planning Process
1. **Foundation Wave**: Identify phases that must complete before others can start
2. **Parallel Waves**: Group independent phases for simultaneous execution
3. **Integration Waves**: Plan coordination and integration phases
4. **Capacity Optimization**: Balance team allocation across waves

### Coordination Mechanism Design
```yaml
coordination_mechanisms:
  synchronization_points:
    purpose: "Coordinate dependent work between parallel streams"
    frequency: "milestone_based"
    participants: "affected_teams"
    deliverables: ["integration_validation", "dependency_resolution"]
    
  communication_protocols:
    daily_coordination: "Quick status updates and blocker discussion"
    weekly_integration: "Deep technical integration review"
    milestone_review: "Comprehensive progress and risk assessment"
    
  conflict_resolution:
    detection: "Automated file conflict detection"
    escalation: "Technical lead → architect → project manager"
    resolution: "Collaborative resolution with documentation"
```

## Quality Assurance and Validation

### Analysis Validation Checklist
- [ ] All PRD phases are captured in analysis
- [ ] All tasks within phases are identified and classified
- [ ] Dependency graph is complete and logically consistent
- [ ] No circular dependencies exist (or are documented with resolution)
- [ ] Parallelization opportunities are realistic and achievable
- [ ] Coordination requirements are specific and manageable
- [ ] Resource conflicts are identified with mitigation strategies
- [ ] Risk assessment covers major parallel execution risks

### Parallelization Feasibility Assessment
- **Independence Validation**: Verify claimed independence is realistic
- **Interface Contract Completeness**: Ensure interfaces enable truly independent work
- **Coordination Overhead Assessment**: Validate coordination doesn't negate parallel benefits
- **Integration Complexity**: Assess whether integration checkpoints are manageable

## Error Handling and Recovery

### Common Analysis Issues
- **Incomplete PRD Information**: Request clarification or make reasonable assumptions with documentation
- **Complex Dependencies**: Break down complex dependencies into manageable components
- **Infeasible Parallelization**: Adjust expectations and find realistic parallel opportunities  
- **Resource Conflicts**: Design coordination mechanisms to manage conflicts

### Recovery Procedures
- **Missing Dependencies**: Systematic review to identify and document all dependencies
- **Circular Dependencies**: Analysis and resolution through interface redesign or coordination protocols
- **Overly Complex Coordination**: Simplify coordination requirements while maintaining parallel benefits
- **Timeline Conflicts**: Adjust phase groupings and wave planning to resolve conflicts

## Success Metrics
- Complete phase breakdown covering 100% of PRD content
- Dependency analysis identifies all major dependencies with strength assessment
- Parallelization plan achieves 40-60% reduction in total execution time
- Coordination requirements are specific, measurable, and manageable
- Analysis passes validation checklist with 95%+ completeness

## Output Requirements

### Required Deliverables
1. **Phase Breakdown Document**: Complete analysis using phase-breakdown-tmpl.yaml  
2. **Dependency Matrix**: Comprehensive dependency mapping and analysis
3. **Parallelization Strategy**: Detailed parallel execution plan with waves and work streams
4. **Coordination Plan**: Specific coordination requirements and synchronization points
5. **Analysis State Files**: Persistent analysis results and validation data

### Integration Points
- **Input**: PRD files, system architecture documentation, project context
- **Output**: Phase breakdown ready for dependency graph generation and parallel planning
- **Tools**: Uses architect-agent capabilities and phase breakdown templates  
- **Handoff**: Detailed analysis ready for parallel execution coordination
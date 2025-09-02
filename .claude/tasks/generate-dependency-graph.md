# Task: Generate Dependency Graph and Analysis

## Purpose
Create comprehensive dependency graphs and analysis from PRD phase breakdown. Generate visual and data representations of dependencies, identify critical paths, and provide detailed analysis that enables optimal parallel execution planning and coordination.

## Task Overview
This task implements detailed dependency graph generation with:
- Visual dependency matrix creation and representation  
- Critical path analysis and bottleneck identification
- Conflict detection and resolution strategy development
- Dependency strength assessment and categorization
- Integration with parallel execution planning workflows

## Prerequisites
- Access to completed PRD phase analysis (from analyze-prd-phases task)
- Understanding of system architecture and component relationships
- Access to architect-agent capabilities
- Phase breakdown data with task-level details

## Instructions

### Phase 1: Data Loading and Dependency Extraction

1. **Load Phase Analysis Data**
   ```
   Use Read tool to load:
   - Phase breakdown analysis results
   - Task-level dependency information
   - System architecture specifications  
   - Component interface definitions
   - Resource and file dependency mappings
   ```

2. **Dependency Data Validation**
   - **Completeness Check**: Verify all phases and tasks have dependency information
   - **Consistency Validation**: Ensure dependency references are valid and bidirectional
   - **Conflict Detection**: Identify potential circular dependencies or conflicts
   - **Data Quality Assessment**: Validate dependency strength and type classifications

3. **Dependency Classification and Enrichment**
   - **Dependency Type Analysis**: Categorize dependencies by type (technical/business/resource/data)
   - **Strength Assessment**: Rate dependency strength (critical/high/medium/low)
   - **Violation Impact Analysis**: Assess impact if dependency is not respected
   - **Workaround Analysis**: Identify potential workarounds for soft dependencies

### Phase 2: Dependency Graph Construction

4. **Phase-Level Dependency Graph**
   - **Graph Structure Creation**: Build directed graph with phases as nodes
   - **Dependency Edge Definition**: Create edges with strength and type attributes
   - **Visual Matrix Generation**: Create phase-to-phase dependency matrix
   - **Graph Validation**: Ensure graph is acyclic and logically consistent

5. **Task-Level Dependency Graph**
   - **Granular Graph Construction**: Build task-level dependency relationships
   - **File and Component Dependencies**: Map dependencies based on shared resources
   - **Data Flow Dependencies**: Map dependencies based on data creation and consumption
   - **Interface Dependencies**: Map dependencies based on API and integration requirements

6. **Critical Path Analysis**
   - **Critical Path Calculation**: Identify longest dependency chain through the graph
   - **Buffer Time Analysis**: Calculate slack time for non-critical paths
   - **Bottleneck Identification**: Find tasks/phases that most constrain parallel execution
   - **Alternative Path Analysis**: Identify alternative paths that could reduce critical path

### Phase 3: Conflict Detection and Resolution Analysis

7. **Resource Conflict Analysis**
   - **File Conflict Detection**: Identify tasks that modify the same files
   - **Database Conflict Analysis**: Find conflicts in database schema or data modifications
   - **API Conflict Detection**: Identify conflicting API modifications or integrations
   - **Infrastructure Conflict Analysis**: Find shared infrastructure dependencies

8. **Dependency Conflict Resolution Strategy**
   - **Conflict Categorization**: Classify conflicts by type and severity
   - **Resolution Strategy Development**: Design approaches for each conflict type
   - **Coordination Protocol Design**: Define processes for managing conflicts
   - **Escalation Path Definition**: Create clear escalation procedures for unresolved conflicts

9. **Temporal Conflict Analysis**
   - **Timeline Conflict Detection**: Identify timing conflicts between dependent tasks
   - **Synchronization Point Analysis**: Find optimal synchronization points
   - **Coordination Overhead Assessment**: Calculate time overhead for coordination
   - **Schedule Optimization**: Identify opportunities to optimize dependency scheduling

### Phase 4: Parallel Execution Analysis

10. **Parallelization Opportunity Assessment**
    - **Independent Path Identification**: Find completely independent execution paths
    - **Minimal Dependency Analysis**: Identify paths with minimal coordination needs
    - **Parallel Capacity Analysis**: Determine maximum parallel execution capacity
    - **Efficiency Calculation**: Calculate parallel execution efficiency gains

11. **Wave Execution Planning**
    - **Wave Grouping Optimization**: Group phases/tasks for optimal wave execution
    - **Dependency Wave Analysis**: Ensure wave dependencies are satisfied
    - **Resource Load Balancing**: Balance resource requirements across waves
    - **Integration Point Planning**: Schedule integration points between waves

### Phase 5: Documentation and State Management

12. **Dependency Graph State Persistence**
    - **State File Management**: Save dependency graph data to state files
      ```
      Use Write tool to save:
      .claude/state/projects/[project-name]/architecture/
      ├── dependency-graph.json
      ├── critical-path-analysis.json
      ├── conflict-analysis.json
      └── parallel-execution-analysis.json
      ```
    - **Graph Serialization**: Save graph structure in multiple formats (JSON, DOT, matrix)
    - **Analysis Results Storage**: Persist all analysis results and recommendations

13. **Documentation Generation**
    - **Load Dependency Matrix Template**: Use Read tool to load dependency-matrix-tmpl.yaml
    - **Generate Dependency Documentation**: Create comprehensive dependency analysis document
    - **Visual Graph Generation**: Create visual representations of dependency graphs
    - **Integration with Parallel Planning**: Prepare outputs for parallel execution planning

## Dependency Graph State Format

```json
{
  "dependency_graph_id": "dep_graph_[timestamp]",
  "source_analysis": "phase_analysis_[timestamp]",
  "generation_date": "2024-01-01T10:00:00Z",
  "graph_metadata": {
    "total_phases": 6,
    "total_tasks": 24,
    "total_dependencies": 18,
    "graph_complexity": "medium",
    "acyclic_validation": true
  },
  "phase_dependency_graph": {
    "nodes": [
      {
        "node_id": "phase-1",
        "node_name": "User Authentication System",
        "node_type": "foundation",
        "complexity_score": 7,
        "duration": "3 weeks",
        "parallel_capacity": 1
      }
    ],
    "edges": [
      {
        "source": "phase-1",
        "target": "phase-2", 
        "dependency_type": "technical",
        "dependency_strength": "hard",
        "reason": "User auth required for profile management",
        "violation_impact": "system_security_compromise",
        "workaround_possible": false,
        "coordination_requirements": ["api_contract_validation"]
      }
    ],
    "adjacency_matrix": [
      [0, 1, 0, 0],
      [0, 0, 1, 1], 
      [0, 0, 0, 1],
      [0, 0, 0, 0]
    ]
  },
  "task_dependency_graph": {
    "nodes": [
      {
        "task_id": "task-1-1",
        "task_name": "OAuth2 Integration",
        "phase": "phase-1",
        "task_type": "backend",
        "complexity": 8,
        "duration": "1 week",
        "files_affected": ["src/auth/oauth.js", "config/auth.yaml"],
        "dependencies": []
      }
    ],
    "edges": [
      {
        "source": "task-1-1",
        "target": "task-2-1",
        "dependency_type": "technical",
        "shared_components": ["auth_middleware", "session_management"],
        "coordination_method": "api_contract_review",
        "file_conflicts": ["auth/middleware.js"]
      }
    ]
  },
  "critical_path_analysis": {
    "critical_path": ["phase-1", "phase-3", "phase-5"],
    "critical_path_duration": "8 weeks",
    "critical_path_tasks": ["task-1-1", "task-3-2", "task-5-1"],
    "bottleneck_analysis": [
      {
        "bottleneck_id": "phase-1",
        "bottleneck_reason": "Foundation phase blocks 4 other phases",
        "impact": "delays entire project if extended",
        "mitigation": "parallel preparation of dependent phase designs"
      }
    ],
    "buffer_analysis": [
      {
        "path": ["phase-2", "phase-4"],
        "slack_time": "1 week",
        "optimization_opportunity": "can absorb minor delays without impacting critical path"
      }
    ]
  },
  "conflict_analysis": {
    "file_conflicts": [
      {
        "file_path": "src/auth/middleware.js",
        "conflicting_tasks": ["task-1-1", "task-2-1", "task-3-1"],
        "conflict_type": "multiple_write_access",
        "resolution_strategy": "sequential_modification_with_coordination",
        "coordination_method": "file_lock_system"
      }
    ],
    "resource_conflicts": [
      {
        "resource_name": "user_database_schema",
        "conflicting_phases": ["phase-1", "phase-2", "phase-4"],
        "conflict_description": "Multiple phases modify user-related tables",
        "resolution_strategy": "migration_coordination_workflow",
        "coordination_overhead": "2 days per migration"
      }
    ],
    "api_conflicts": [
      {
        "api_endpoint": "/api/users",
        "conflicting_tasks": ["task-1-2", "task-2-1"],
        "conflict_type": "interface_modification",
        "resolution_strategy": "api_versioning_strategy",
        "backward_compatibility": true
      }
    ]
  },
  "parallel_execution_analysis": {
    "max_parallel_capacity": 3,
    "parallel_efficiency": "65%",
    "independent_paths": [
      {
        "path_id": "path-1", 
        "path_name": "User Management Stream",
        "phases": ["phase-1", "phase-2"],
        "independence_score": 8,
        "external_dependencies": ["auth_provider_api"],
        "coordination_points": ["api_contract_review", "integration_testing"]
      }
    ],
    "wave_analysis": [
      {
        "wave_number": 1,
        "wave_name": "Foundation",
        "phases": ["phase-1"],
        "duration": "3 weeks",
        "parallel_capacity": 1,
        "blocking_factor": "blocks_4_phases"
      },
      {
        "wave_number": 2,
        "wave_name": "Core Features", 
        "phases": ["phase-2", "phase-3"],
        "duration": "4 weeks",
        "parallel_capacity": 2,
        "synchronization_requirements": ["api_integration_testing"]
      }
    ],
    "coordination_overhead": {
      "daily_coordination": "15 minutes per team per day",
      "weekly_integration": "2 hours per week",
      "milestone_coordination": "4 hours per milestone",
      "total_overhead_percentage": "8%"
    }
  },
  "optimization_recommendations": [
    {
      "optimization_type": "critical_path_reduction",
      "recommendation": "Parallelize task-1-1 preparation with architecture design",
      "expected_benefit": "1 week reduction in critical path",
      "implementation_effort": "low"
    },
    {
      "optimization_type": "conflict_resolution",
      "recommendation": "Implement file locking system for shared components",
      "expected_benefit": "Reduces coordination overhead by 50%",
      "implementation_effort": "medium"
    }
  ],
  "validation_results": {
    "graph_acyclicity": true,
    "dependency_completeness": "98%",
    "conflict_analysis_coverage": "100%",
    "parallel_opportunity_assessment": "comprehensive",
    "optimization_potential": "significant"
  }
}
```

## Dependency Graph Analysis Techniques

### Critical Path Analysis Implementation
```python
# Pseudocode for critical path calculation
def calculate_critical_path(dependency_graph, task_durations):
    # Forward pass: Calculate earliest start times
    earliest_start = {}
    earliest_finish = {}
    
    # Backward pass: Calculate latest start times  
    latest_start = {}
    latest_finish = {}
    
    # Calculate slack times
    slack_times = {}
    
    # Identify critical path (tasks with zero slack)
    critical_path = [task for task in tasks if slack_times[task] == 0]
    
    return critical_path, slack_times
```

### Dependency Strength Assessment
```yaml
dependency_strength_criteria:
  critical:
    description: "Absolute requirement, cannot be violated"
    examples: ["Security before access", "Database before queries"] 
    parallel_impact: "Blocks all parallel execution"
    
  high:
    description: "Strong requirement, violation has major consequences"
    examples: ["API design before implementation", "Testing framework before tests"]
    parallel_impact: "Requires careful coordination"
    
  medium: 
    description: "Important but can be worked around with coordination"
    examples: ["UI styling after component structure", "Documentation after features"]
    parallel_impact: "Manageable with communication protocols"
    
  low:
    description: "Preferential, easily worked around"
    examples: ["Code formatting", "Non-critical documentation"]
    parallel_impact: "Minimal impact on parallel execution"
```

### Conflict Detection Algorithms
```yaml
conflict_detection_methods:
  file_conflicts:
    method: "File modification matrix analysis"
    detection: "Tasks modifying same files"
    resolution: "Sequential modification or file splitting"
    
  resource_conflicts:
    method: "Resource access pattern analysis" 
    detection: "Shared resource simultaneous access"
    resolution: "Resource locking or access coordination"
    
  api_conflicts:
    method: "Interface modification analysis"
    detection: "Concurrent API interface changes"
    resolution: "API versioning or contract coordination"
    
  data_conflicts:
    method: "Data flow dependency analysis"
    detection: "Data producer/consumer conflicts"
    resolution: "Data pipeline coordination or staging"
```

## Visual Dependency Graph Generation

### Graph Visualization Formats
```bash
# Generate DOT format for Graphviz visualization
dependency_graph_dot = '''
digraph PRD_Dependencies {
    rankdir=LR;
    node [shape=box];
    
    "Phase 1" -> "Phase 2" [label="hard"];
    "Phase 1" -> "Phase 3" [label="soft"];
    "Phase 2" -> "Phase 4" [label="hard"];
    "Phase 3" -> "Phase 4" [label="medium"];
}
'''

# Generate matrix visualization for documentation
dependency_matrix = '''
        | P1 | P2 | P3 | P4 |
    P1  |  - |  H |  S |  - |
    P2  |  - |  - |  - |  H |
    P3  |  - |  - |  - |  M |
    P4  |  - |  - |  - |  - |
    
    H=Hard, S=Soft, M=Medium
'''
```

### Critical Path Visualization
```yaml
critical_path_representation:
  text_format: "Phase-1 → Phase-3 → Phase-5 (8 weeks total)"
  
  visual_format: |
    [Phase-1] ——→ [Phase-3] ——→ [Phase-5]
        ↓            ↓             ↓
    3 weeks      2 weeks       3 weeks
    
  parallel_paths: |
    [Phase-1] ——→ [Phase-2] ——→ [Phase-4]
                      ↑             ↑
                  2 weeks      1 week (slack)
```

## Quality Assurance and Validation

### Dependency Graph Validation Checklist
- [ ] All phases and tasks are represented as nodes
- [ ] All dependencies are captured as edges with proper attributes
- [ ] Graph is acyclic (no circular dependencies)
- [ ] Dependency strength assessments are consistent and logical
- [ ] Critical path calculation is accurate and validated
- [ ] Conflict analysis covers all potential resource conflicts
- [ ] Parallel execution analysis is realistic and achievable
- [ ] Documentation is comprehensive and professional

### Analysis Quality Metrics
- **Completeness**: >95% of dependencies captured and analyzed
- **Accuracy**: Critical path calculation validated against manual analysis
- **Practicality**: Conflict resolution strategies are implementable
- **Optimization**: Identified optimizations provide measurable benefits

## Error Handling and Recovery

### Common Analysis Issues
- **Circular Dependencies**: Detect and resolve through interface redesign or staging
- **Missing Dependencies**: Systematic review to identify and add missing relationships
- **Conflicting Assessments**: Resolve through stakeholder consultation and validation
- **Overly Complex Graphs**: Simplify through dependency consolidation and grouping

### Recovery Procedures
- **Graph Validation Failures**: Iterative correction and re-validation
- **Critical Path Conflicts**: Alternative path analysis and optimization
- **Resource Conflict Resolution**: Design coordination mechanisms and protocols
- **Performance Issues**: Graph simplification and optimization techniques

## Success Metrics
- Complete dependency graph with 95%+ dependency coverage
- Accurate critical path identification with validated calculations
- Comprehensive conflict analysis with practical resolution strategies
- Parallel execution analysis achieving 40-60% time optimization potential
- Professional documentation ready for implementation planning

## Output Requirements

### Required Deliverables
1. **Dependency Graph Document**: Complete analysis using dependency-matrix-tmpl.yaml
2. **Visual Dependency Graphs**: Multiple format representations (DOT, matrix, flowchart)
3. **Critical Path Analysis**: Detailed critical path with bottleneck identification
4. **Conflict Resolution Strategy**: Comprehensive conflict analysis with resolution approaches  
5. **Parallel Execution Recommendations**: Specific recommendations for optimal parallel execution

### Integration Points
- **Input**: PRD phase breakdown, system architecture, task analysis
- **Output**: Dependency analysis ready for parallel execution planning
- **Tools**: Uses architect-agent capabilities and dependency analysis templates
- **Handoff**: Complete dependency analysis ready for parallel coordination planning
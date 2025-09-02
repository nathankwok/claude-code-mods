---
allowed-tools: Read, Write, Edit, MultiEdit, Bash, Grep, Glob, Task
argument-hint: [prd_file_path] | [project_brief_path] | analyze-current
description: Generate technical architecture from PRDs and project briefs with phase analysis and parallelization planning
model: sonnet
---

# /architect - Technical Architecture and PRD Analysis

Generate comprehensive technical architecture from PRDs and project briefs, perform automatic PRD phase analysis and breakdown, create dependency graphs between phases and tasks, identify parallelization opportunities, and generate technical specifications with clear interfaces.

## Core Capabilities

This command provides the following Phase 2 requirements from the BMAD-inspired planning system:

1. **Technical Architecture Design**: Generate system designs from PRDs and project briefs
2. **Automatic PRD Phase Analysis**: Break down PRD phases with dependency analysis
3. **Dependency Graph Generation**: Create task dependency mapping for parallel execution
4. **Parallelization Opportunity Identification**: Find independent work streams
5. **Technical Specification Generation**: Create clear interface specifications
6. **Integration with Brainstorming**: Leverage project briefs from brainstorming sessions

## Usage

### Generate Architecture from PRD
```bash
/architect path/to/prd/file.md
```

### Generate Architecture from Project Brief
```bash
/architect path/to/project-brief.json
```

### Analyze Current Project PRD
```bash
/architect analyze-current
```

## Command Processing

When you run `/architect`, it performs these preprocessing steps before delegating to the architect-agent:

### Phase 1: Input Validation and Preprocessing

1. **Validate Arguments**:
   ```bash
   # Validate input file exists and is readable
   if [[ "$1" == "analyze-current" ]]; then
       # Search for PRD files in current project
       echo "Searching for PRD files in current project..."
   elif [[ -f "$1" ]]; then
       echo "✓ Input file exists: $1"
   else
       echo "✗ Input file not found: $1"
       exit 1
   fi
   ```

2. **Project Context Setup**:
   ```bash
   # Extract project name from working directory or file path
   PROJECT_NAME=$(basename "$(pwd)" | sed 's/[^a-zA-Z0-9-]//g')
   echo "Project context: $PROJECT_NAME"
   
   # Create architecture state directory
   ARCH_DIR=".claude/state/projects/$PROJECT_NAME/architecture"
   mkdir -p "$ARCH_DIR"
   echo "Architecture state directory: $ARCH_DIR"
   ```

3. **Load Existing Context**:
   ```bash
   # Check for existing brainstorming context
   BRAINSTORM_DIR=".claude/state/projects/$PROJECT_NAME/brainstorming"
   if [[ -d "$BRAINSTORM_DIR" ]]; then
       echo "✓ Found brainstorming context"
       ls -la "$BRAINSTORM_DIR/"
   else
       echo "! No brainstorming context found - proceeding with PRD-only analysis"
   fi
   
   # Check for existing architecture
   if [[ -f "$ARCH_DIR/system-design.json" ]]; then
       echo "✓ Found existing architecture - will update"
   else
       echo "! No existing architecture - will create new"
   fi
   ```

4. **Input File Analysis**:
   ```bash
   # Analyze input file type and structure
   INPUT_FILE="$1"
   if [[ "$INPUT_FILE" == *.md ]]; then
       echo "✓ Detected PRD file format"
       # Extract phase count for validation
       PHASE_COUNT=$(grep -c "^## Phase" "$INPUT_FILE" || echo "0")
       echo "Found $PHASE_COUNT phases in PRD"
   elif [[ "$INPUT_FILE" == *.json ]]; then
       echo "✓ Detected project brief format"
       # Validate JSON structure
       if jq empty "$INPUT_FILE" 2>/dev/null; then
           echo "✓ Valid JSON format"
       else
           echo "✗ Invalid JSON format"
           exit 1
       fi
   fi
   ```

### Phase 2: Structured Agent Delegation

5. **Prepare Agent Context**:
   - Compile validated input parameters
   - Load existing project state and brainstorming context
   - Create structured requirements for architect-agent
   - Set up output artifact specifications

6. **Execute Architecture Generation**:
   - Delegate to architect-agent with validated context
   - Monitor progress and validate intermediate outputs
   - Ensure all required artifacts are generated
   - Validate output against expected schemas

7. **Post-Processing Validation**:
   - Verify all promised artifacts were created
   - Validate artifact formats and completeness
   - Cross-reference architecture with input requirements
   - Generate integration-ready outputs

## Output Artifacts

The command generates the following validated artifacts in `.claude/state/projects/[project-name]/architecture/`:

### Core Architecture Files
- **system-design.json**: Complete system architecture specification
  ```json
  {
    "project_name": "claude-code-mods",
    "architecture_version": "1.0.0",
    "created_at": "2025-01-02T10:30:00Z",
    "system_overview": {
      "type": "monolithic|microservices|serverless",
      "deployment_model": "cloud|on-premise|hybrid",
      "components": [
        {
          "name": "user-service",
          "type": "microservice",
          "responsibilities": ["user management", "authentication"],
          "interfaces": ["REST API", "GraphQL"],
          "dependencies": ["database", "auth-service"]
        }
      ]
    },
    "technology_stack": {
      "frontend": "React/TypeScript",
      "backend": "Node.js/Express",
      "database": "PostgreSQL",
      "rationale": "Selected for team expertise and scalability requirements"
    }
  }
  ```

- **phase-breakdown.json**: PRD phase analysis with validated dependencies
  ```json
  {
    "total_phases": 6,
    "analysis_date": "2025-01-02T10:30:00Z",
    "phases": [
      {
        "phase_id": "phase-1",
        "name": "Foundation Setup",
        "objective": "Establish core infrastructure and authentication",
        "complexity_score": 7,
        "estimated_effort": "2 weeks",
        "dependencies": {
          "requires": [],
          "blocks": ["phase-2", "phase-3"]
        },
        "tasks": [
          {
            "task_id": "task-1-1",
            "name": "Setup database schema",
            "type": "backend",
            "complexity": 5,
            "estimated_hours": 16,
            "files_affected": ["migrations/001_create_users.sql"]
          }
        ],
        "parallel_group": "wave-1"
      }
    ]
  }
  ```

- **dependency-graph.json**: Task dependency mapping with validation
  ```json
  {
    "graph_version": "1.0.0",
    "validation_status": "valid",
    "critical_path_length": 8,
    "nodes": {
      "phase-1": {
        "type": "phase",
        "dependencies": [],
        "dependents": ["phase-2", "phase-3"],
        "parallel_group": "wave-1"
      }
    },
    "edges": [
      {
        "from": "phase-1",
        "to": "phase-2",
        "type": "hard_dependency",
        "reason": "Phase 2 requires authentication system from Phase 1"
      }
    ],
    "parallel_execution_waves": {
      "wave-1": {
        "phases": ["phase-1"],
        "estimated_duration": "2 weeks",
        "max_parallel_teams": 1
      },
      "wave-2": {
        "phases": ["phase-2", "phase-3"],
        "dependencies": ["wave-1"],
        "estimated_duration": "3 weeks",
        "max_parallel_teams": 2
      }
    }
  }
  ```

### Implementation Specifications
- **interface-specs.json**: Validated API and component interfaces
  ```json
  {
    "api_specifications": {
      "user_service": {
        "base_path": "/api/v1/users",
        "endpoints": [
          {
            "path": "/api/v1/users",
            "method": "GET",
            "summary": "List users with pagination",
            "request_schema": "$ref:#/definitions/UserListRequest",
            "response_schema": "$ref:#/definitions/UserListResponse",
            "auth_required": true
          }
        ]
      }
    },
    "component_interfaces": {
      "authentication_service": {
        "exports": ["AuthProvider", "useAuth", "ProtectedRoute"],
        "dependencies": ["react", "jwt-decode"],
        "data_contracts": ["User", "AuthState", "LoginCredentials"]
      }
    },
    "data_schemas": {
      "User": {
        "type": "object",
        "properties": {
          "id": {"type": "string", "format": "uuid"},
          "email": {"type": "string", "format": "email"},
          "created_at": {"type": "string", "format": "date-time"}
        },
        "required": ["id", "email"]
      }
    }
  }
  ```

- **parallel-execution-plan.json**: Concrete parallelization strategy
  ```json
  {
    "execution_strategy": "wave-based",
    "total_waves": 3,
    "estimated_total_duration": "8 weeks",
    "sequential_duration": "12 weeks",
    "time_savings": "33%",
    "team_requirements": {
      "wave-1": ["backend-team"],
      "wave-2": ["backend-team", "frontend-team"],
      "wave-3": ["fullstack-team", "qa-team"]
    },
    "synchronization_points": [
      {
        "name": "API Contract Review",
        "after_wave": 1,
        "duration": "2 days",
        "participants": ["backend-team", "frontend-team"],
        "deliverables": ["API documentation", "mock implementations"]
      }
    ],
    "integration_checkpoints": [
      {
        "checkpoint_id": "cp-1",
        "name": "Authentication Integration",
        "after_tasks": ["task-1-1", "task-2-1"],
        "validation_criteria": ["Login flow works", "Token validation passes"]
      }
    ]
  }
  ```

### Documentation and Reports
- **architecture-summary.md**: Human-readable documentation with diagrams
- **technology-decisions.json**: Technology stack decisions with rationale
- **integration-guide.md**: Step-by-step integration guide for downstream tools

### Validation Files
- **artifacts-manifest.json**: Manifest of all generated files with checksums
- **validation-report.json**: Validation results for all artifacts

## Integration with Existing Agents

This command leverages the existing **architect-agent** with structured delegation after preprocessing:

### Structured Agent Invocation

After completing preprocessing validation, the command invokes the architect-agent with validated context:

```
@architect-agent Please generate comprehensive technical architecture based on the following validated inputs:

**Preprocessed Context**:
- **Project Name**: ${PROJECT_NAME}
- **Input Type**: ${INPUT_TYPE} (PRD/Project Brief)
- **Input File**: ${VALIDATED_INPUT_FILE} 
- **Architecture Directory**: ${ARCH_DIR}
- **Brainstorming Context**: ${BRAINSTORM_STATUS} (Available/Missing)
- **Existing Architecture**: ${EXISTING_ARCH_STATUS} (Update/Create New)

**Validated Requirements**:
${EXTRACTED_REQUIREMENTS}

**Pre-Analysis Results**:
- **Phase Count**: ${PHASE_COUNT} phases identified
- **File Format**: ${FILE_FORMAT} validated
- **Context Dependencies**: ${CONTEXT_DEPS}

**Task Requirements**:
1. **Architecture Design**: Generate system design using validated inputs
2. **Phase Analysis**: Break down ${PHASE_COUNT} phases with dependency mapping
3. **Dependency Graph**: Create validated dependency relationships
4. **Parallelization Plan**: Identify concrete parallel execution opportunities
5. **Interface Specifications**: Generate implementation-ready interface specs
6. **Integration Planning**: Create downstream workflow integration points

**Required Output Artifacts** (must match exactly):
- system-design.json (with schema validation)
- phase-breakdown.json (with dependency validation)  
- dependency-graph.json (with cycle detection)
- interface-specs.json (with API schema validation)
- parallel-execution-plan.json (with team allocation)
- architecture-summary.md (with integration examples)
- artifacts-manifest.json (with file validation)

**Integration Requirements**:
- Generate /plan-parallel compatible outputs
- Create /execute-parallel ready specifications  
- Include synchronization point definitions
- Provide team coordination mechanisms

**Validation Requirements**:
- All JSON files must validate against schemas
- Dependency graph must be acyclic
- Phase breakdown must match PRD structure
- Interface specs must include complete API definitions
- Parallel plan must include realistic time estimates

Please process these validated inputs and generate all required artifacts with validation.
```

### Agent Monitoring and Validation

The command monitors the architect-agent execution and validates outputs:

```bash
# Monitor agent progress
echo "🚀 Architecture generation in progress..."
echo "📊 Expected artifacts: 7 files"

# Validate outputs after agent completion  
EXPECTED_FILES=(
    "system-design.json"
    "phase-breakdown.json" 
    "dependency-graph.json"
    "interface-specs.json"
    "parallel-execution-plan.json"
    "architecture-summary.md"
    "artifacts-manifest.json"
)

echo "✅ Validating generated artifacts..."
for file in "${EXPECTED_FILES[@]}"; do
    if [[ -f "$ARCH_DIR/$file" ]]; then
        echo "✓ $file generated"
        # Validate JSON files
        if [[ "$file" == *.json ]]; then
            if jq empty "$ARCH_DIR/$file" 2>/dev/null; then
                echo "  ✓ Valid JSON format"
            else
                echo "  ✗ Invalid JSON format"
                exit 1
            fi
        fi
    else
        echo "✗ Missing required file: $file"
        exit 1
    fi
done
```

## Examples

### Example 1: Analyze PRD for Architecture
```bash
/architect prds/5_bmad_inspired_planning_system.md
```

**Command Output**:
```
✓ Input file exists: prds/5_bmad_inspired_planning_system.md
Project context: claude-code-mods
Architecture state directory: .claude/state/projects/claude-code-mods/architecture
✓ Detected PRD file format
Found 6 phases in PRD
! No brainstorming context found - proceeding with PRD-only analysis
! No existing architecture - will create new
🚀 Architecture generation in progress...
📊 Expected artifacts: 7 files
✅ Validating generated artifacts...
✓ system-design.json generated
  ✓ Valid JSON format
✓ phase-breakdown.json generated  
  ✓ Valid JSON format
✓ dependency-graph.json generated
  ✓ Valid JSON format
✓ interface-specs.json generated
  ✓ Valid JSON format
✓ parallel-execution-plan.json generated
  ✓ Valid JSON format
✓ architecture-summary.md generated
✓ artifacts-manifest.json generated
  ✓ Valid JSON format

🎯 Architecture Ready for Integration:
- Phase breakdown available for /plan-parallel
- Interface specs ready for /execute-parallel  
- 3 parallel execution waves identified
- 33% time savings estimated through parallelization
```

**Generated Architecture Features**:
- **6-phase breakdown** with validated dependencies
- **3 parallel execution waves** for optimal team coordination
- **Microservices architecture** supporting independent development
- **API-first design** enabling parallel frontend/backend work
- **Ready integration** with planning and execution commands

### Example 2: Analyze Project Brief with Brainstorming Context
```bash
/architect .claude/state/projects/my-project/brainstorming/project-brief-20241201-123456.json
```

**Command Output**:
```
✓ Input file exists: .claude/state/projects/my-project/brainstorming/project-brief-20241201-123456.json
Project context: my-project
Architecture state directory: .claude/state/projects/my-project/architecture
✓ Found brainstorming context
  competitive-analysis-20241201-123456.json
  stakeholder-insights-20241201-123456.json
✓ Detected project brief format
✓ Valid JSON format
! No existing architecture - will create new
🚀 Architecture generation in progress...
📊 Expected artifacts: 7 files
✅ Validating generated artifacts...
[validation results...]

🎯 BMAD-Enhanced Architecture Ready:
- Market-informed technology stack selection
- Competitive advantages integrated into design
- Stakeholder requirements addressed in architecture
- Technology choices aligned with market positioning
```

**Market-Informed Features**:
- **Technology stack** selected based on competitive analysis
- **Scalability design** informed by market growth projections
- **API design** incorporating competitive differentiation insights
- **Architecture decisions** documented with market rationale

### Example 3: Analyze Current Project with Context Discovery
```bash
/architect analyze-current
```

**Command Output**:
```
Searching for PRD files in current project...
✓ Found PRD: prds/1_code_review_agent.md
✓ Found PRD: prds/5_bmad_inspired_planning_system.md
📋 Multiple PRDs found - analyzing latest: prds/5_bmad_inspired_planning_system.md
Project context: claude-code-mods  
Architecture state directory: .claude/state/projects/claude-code-mods/architecture
✓ Found brainstorming context
  project-brief-20241201-143022.json
✓ Found existing architecture - will update
🚀 Architecture generation in progress...
📊 Expected artifacts: 7 files
✅ Validating generated artifacts...
[validation results...]

🔄 Architecture Updated:
- Existing architecture enhanced with new requirements
- Dependency graph updated with new phase relationships
- Parallelization plan optimized for current team structure
- Integration points validated with existing implementations
```

## Integration with BMAD Workflow

The `/architect` command integrates seamlessly with the BMAD-inspired workflow:

```
Interactive Brainstorming → Project Brief Generation → 
**TECHNICAL ARCHITECTURE DESIGN** ← [You are here]
↓
PRD Phase Analysis → Parallel Execution Planning → 
Coordinated Multi-Agent Implementation
```

### Upstream Integration Sources

**From `/brainstorm` command**:
- **project-brief-{session_id}.json** → Architecture requirements and market context
- **competitive-analysis-{session_id}.json** → Technology differentiation insights  
- **stakeholder-insights-{session_id}.json** → User experience and technical preferences

**From PRD files**:
- **Phase definitions** → Architecture phase breakdown requirements
- **Technical requirements** → System design constraints and specifications
- **Success criteria** → Architecture validation requirements

### Downstream Integration Outputs

**To `/plan-parallel` command**:
```bash
# The /plan-parallel command consumes these architecture outputs:
/plan-parallel .claude/state/projects/claude-code-mods/architecture/phase-breakdown.json

# Uses the following architecture data:
- phase-breakdown.json → Parallel execution wave planning
- dependency-graph.json → Team coordination and synchronization points  
- parallel-execution-plan.json → Resource allocation and timeline estimates
- interface-specs.json → Independent work stream definitions
```

**Example `/plan-parallel` Integration**:
```json
{
  "consumed_architecture_files": [
    ".claude/state/projects/claude-code-mods/architecture/phase-breakdown.json",
    ".claude/state/projects/claude-code-mods/architecture/dependency-graph.json"
  ],
  "generated_parallel_plan": {
    "execution_waves": [
      {
        "wave_id": "wave-1", 
        "phases": ["phase-1-foundation"],
        "teams": ["backend-team"],
        "duration": "2 weeks",
        "architecture_basis": "Independent backend components identified in system-design.json"
      },
      {
        "wave_id": "wave-2",
        "phases": ["phase-2-api", "phase-3-frontend"], 
        "teams": ["backend-team", "frontend-team"],
        "duration": "3 weeks",
        "architecture_basis": "API contracts from interface-specs.json enable parallel development"
      }
    ]
  }
}
```

**To `/execute-parallel` command**:
```bash
# The /execute-parallel command uses these architecture specifications:
/execute-parallel .claude/state/projects/claude-code-mods/architecture/

# Consumes the following architecture artifacts:
- interface-specs.json → API contracts for independent development
- system-design.json → Component boundaries and responsibilities
- parallel-execution-plan.json → Team coordination mechanisms
- technology-decisions.json → Development environment setup
```

**Example `/execute-parallel` Integration**:
```yaml
# Generated execution plan based on architecture
execution_configuration:
  teams:
    backend-team:
      responsibilities: ["API development", "Database setup"]
      interfaces_to_implement:
        - "/api/v1/users" # from interface-specs.json
        - "/api/v1/auth"  # from interface-specs.json
      technology_stack:
        language: "Node.js"     # from technology-decisions.json
        framework: "Express"    # from technology-decisions.json
        database: "PostgreSQL" # from system-design.json
        
    frontend-team:
      responsibilities: ["UI components", "State management"]
      interfaces_to_consume:
        - "/api/v1/users" # defined in interface-specs.json
        - "/api/v1/auth"  # defined in interface-specs.json
      technology_stack:
        language: "TypeScript"  # from technology-decisions.json
        framework: "React"      # from technology-decisions.json
        state_management: "Redux" # from system-design.json

  synchronization_points:
    - name: "API Contract Review"           # from parallel-execution-plan.json
      after_wave: 1
      participants: ["backend-team", "frontend-team"]
      deliverables: ["OpenAPI spec", "Mock server"]
      
    - name: "Integration Testing"           # from parallel-execution-plan.json  
      after_wave: 2
      participants: ["backend-team", "frontend-team", "qa-team"]
      validation_criteria: ["All API endpoints functional", "Frontend integration complete"]
```

### Concrete Workflow Integration Examples

**Example: Complete Workflow Chain**
```bash
# Step 1: Generate architecture from PRD
/architect prds/5_bmad_inspired_planning_system.md

# Step 2: Plan parallel execution using architecture
/plan-parallel .claude/state/projects/claude-code-mods/architecture/phase-breakdown.json

# Step 3: Execute parallel implementation using both architecture and plan  
/execute-parallel .claude/state/projects/claude-code-mods/architecture/
```

**Data Flow Validation**:
```bash
# Architecture outputs are validated for downstream compatibility
echo "🔍 Validating integration readiness..."

# Verify /plan-parallel compatibility
jq '.phases[].parallel_group' .claude/state/projects/claude-code-mods/architecture/phase-breakdown.json
# Expected: ["wave-1", "wave-2", "wave-3"]

# Verify /execute-parallel compatibility  
jq '.api_specifications | keys[]' .claude/state/projects/claude-code-mods/architecture/interface-specs.json
# Expected: ["user_service", "auth_service", "notification_service"]

echo "✅ Architecture ready for parallel planning and execution"
```

**Integration Success Criteria**:
- ✅ **Phase breakdown** matches PRD structure and enables wave-based planning
- ✅ **Interface specifications** provide complete API contracts for independent work
- ✅ **Dependency graph** is acyclic and supports parallel execution validation
- ✅ **Technology decisions** include complete development environment specifications
- ✅ **Parallel execution plan** includes realistic timeline and resource estimates

## Best Practices

1. **Start with Clear Requirements**: Ensure PRD or project brief contains detailed requirements
2. **Leverage Brainstorming Context**: Use project briefs that include market analysis and stakeholder insights  
3. **Validate Dependencies**: Review generated dependency graphs for logical consistency
4. **Plan for Integration**: Ensure parallelization strategy includes clear integration points
5. **Review Architecture**: Validate that architecture addresses all requirements and constraints
6. **Update Iteratively**: Re-run architecture analysis as requirements evolve

## Troubleshooting

**Command fails to find input file**:
- Verify file path is correct and file exists
- Use absolute paths or paths relative to current working directory

**Missing brainstorming context**:
- Run `/brainstorm` first to generate project brief
- Or provide detailed requirements directly in PRD

**Architecture seems incomplete**:
- Check that PRD contains sufficient detail for architecture generation
- Verify all phases and requirements are clearly defined in source material

**Parallelization opportunities not identified**:
- Ensure PRD phases are well-structured with clear boundaries
- Check that tasks have proper dependency information

The `/architect` command provides comprehensive technical architecture capabilities that bridge the gap between brainstorming and implementation, enabling effective parallel development through clear interfaces and dependency management.
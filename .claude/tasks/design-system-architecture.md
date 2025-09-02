# Task: Design System Architecture

## Purpose
Generate comprehensive technical architecture from PRDs and project briefs. Transform high-level requirements into detailed technical designs that enable effective parallel development with clear interfaces and integration points.

## Task Overview
This task implements systematic architecture design with:
- Requirements analysis and technical specification generation
- Component design and interface definition
- Technology stack evaluation and selection
- Infrastructure architecture and deployment planning
- Integration with project brief inputs from brainstorming

## Prerequisites
- Access to PRD file or project brief with technical requirements
- Understanding of system boundaries and constraints
- Access to architect-agent capabilities
- Clear business requirements and success criteria

## Instructions

### Phase 1: Requirements Analysis and Context Loading

1. **Load Input Materials**
   ```
   Use Read tool to analyze:
   - PRD file (if provided)
   - Project brief from brainstorming sessions:
     Primary location: .claude/state/projects/[project-name]/brainstorming/
     Files to check:
     - project-brief-[session_id].json (project vision and requirements)
     - competitive-analysis-[session_id].json (competitive advantages)
     - stakeholder-insights-[session_id].json (stakeholder needs and preferences)
   - Existing architecture documentation (if any)
   - Technical constraint documents
   ```

   **Brainstorming State Integration Protocol**:
   - **Primary Path**: Check `.claude/state/projects/[project-name]/brainstorming/` for recent session files
   - **Fallback Handling**: If brainstorming files are missing:
     - Document that analysis proceeds without brainstorming context
     - Log missing brainstorming inputs in architecture state
     - Request project brief if critical market context is needed
     - Make documented assumptions about market positioning and competitive requirements
   - **State File Processing**: For each brainstorming file found:
     - Extract technical requirements from market analysis
     - Identify competitive differentiators requiring technical implementation
     - Map stakeholder needs to system architectural requirements
     - Incorporate project vision into architectural approach decisions

2. **Requirements Extraction**
   - **Functional Requirements Analysis**: Extract all business capabilities and user stories
   - **Non-Functional Requirements Mapping**: Identify performance, scalability, security, and reliability needs
   - **Constraint Documentation**: Catalog technical, business, and regulatory constraints
   - **Success Criteria Alignment**: Map requirements to measurable success criteria

3. **Context Analysis**
   - **Stakeholder Mapping**: Identify all system users and their needs
   - **System Boundaries**: Define what's included/excluded from the architecture
   - **External Dependencies**: Identify third-party systems and integrations
   - **Existing System Analysis**: Understand current state and migration needs

### Phase 2: System Architecture Design

4. **High-Level Architecture Design**
   - **Architecture Pattern Selection**: Choose appropriate patterns (microservices, monolith, serverless, etc.)
   - **Component Identification**: Break system into logical components with clear responsibilities
   - **System Topology**: Design component relationships and data flow
   - **Integration Architecture**: Plan external system integrations and APIs

5. **Technology Stack Research and Selection**
   - **Research Current Technologies**: Use Task tool for technology trend analysis
     ```
     Task tool: "Research latest frameworks and technologies for [domain/requirement]"
     Task tool: "Compare [technology options] for [specific use case] with pros/cons"
     Task tool: "Find best practices for [technology stack] architecture patterns"
     ```
   - **Technology Evaluation Matrix**: Compare options based on project criteria
   - **Decision Documentation**: Create Technology Decision Records (TDRs) with rationale
   - **Risk Assessment**: Evaluate technology risks and mitigation strategies

6. **Component Detailed Design**
   - **Internal Component Architecture**: Design internal structure for each major component
   - **Interface Specifications**: Define APIs and communication protocols between components  
   - **Data Architecture**: Design database schema, data models, and data flow
   - **Security Architecture**: Plan authentication, authorization, and data protection

### Phase 3: Parallel Development Planning

7. **Parallelization Analysis**
   - **Component Independence Assessment**: Identify components that can be developed independently
   - **Interface Contract Definition**: Create detailed contracts that enable parallel development
   - **Shared Dependency Identification**: Find minimal shared components requiring coordination
   - **Mock/Stub Strategy**: Plan mocks for early integration testing

8. **Development Phase Planning** 
   - **Foundation Phase**: Identify infrastructure and core components needed first
   - **Parallel Development Phases**: Group independent components for simultaneous development
   - **Integration Phases**: Plan coordination points and integration testing
   - **Deployment Strategy**: Design rollout approach that supports parallel development

### Phase 4: Architecture Documentation and State Management

9. **Architecture State Persistence**
   - **Project Detection**: Extract project name from PRD path or working directory
   - **State Directory Creation**: Create architecture state directory structure
     ```
     Use Write tool to create directory structure:
     .claude/state/projects/[project-name]/architecture/
     ```
   - **Save Architecture Artifacts**: Persist all architecture decisions using Write tool
     ```
     Architecture state files:
     - system-design.json: Complete system architecture
     - technology-decisions.json: TDRs and technology choices
     - component-specs.json: Detailed component specifications
     - parallel-development-plan.json: Parallelization strategy
     ```

10. **Structured Documentation Generation**
    - **Load Architecture Template**: Use Read tool to load architecture-tmpl.yaml
    - **Generate Architecture Document**: Populate template with design decisions
    - **Create Technical Specifications**: Generate detailed specs for development teams
    - **Integration Documentation**: Document APIs, interfaces, and integration points
    - **Save All Documentation**: Use Write tool to persist documentation

### Phase 5: Validation and Quality Assurance

11. **Architecture Validation**
    - **Requirement Coverage**: Verify all requirements are addressed in architecture
    - **Consistency Checking**: Ensure component interfaces align and data flows are valid
    - **Scalability Assessment**: Validate architecture can meet performance requirements
    - **Security Review**: Check security architecture covers all threat vectors

12. **Parallelization Feasibility Assessment**
    - **Dependency Analysis**: Verify component independence claims are realistic
    - **Interface Contract Validation**: Ensure interfaces are complete and implementable
    - **Integration Point Review**: Validate integration strategy is practical
    - **Risk Assessment**: Identify potential issues with parallel development approach

## Architecture State Management Format

```json
{
  "architecture_id": "arch_[timestamp]",
  "project_name": "project_name",
  "prd_source": "path/to/prd.md",
  "brainstorming_inputs": {
    "sessions_found": ["session_id1", "session_id2"],
    "project_brief_files": ["project-brief-session1.json"],
    "competitive_analysis_files": ["competitive-analysis-session1.json"],
    "stakeholder_insights_files": ["stakeholder-insights-session1.json"],
    "integration_status": "full|partial|none",
    "missing_context": ["market_analysis", "competitive_insights"]
  },
  "requirements_analysis": {
    "functional_requirements": [
      {
        "id": "req_001",
        "description": "User authentication system",
        "acceptance_criteria": ["criteria1", "criteria2"],
        "priority": "high"
      }
    ],
    "non_functional_requirements": {
      "performance": "Response time < 200ms",
      "scalability": "Support 10k concurrent users",
      "security": "OAuth2 with RBAC"
    },
    "constraints": {
      "technical": ["Must use existing database"],
      "business": ["6-month delivery timeline"],
      "regulatory": ["GDPR compliance required"]
    }
  },
  "system_architecture": {
    "architecture_pattern": "microservices",
    "components": [
      {
        "name": "user_service",
        "type": "microservice",
        "responsibilities": ["user management", "authentication"],
        "interfaces": ["REST API", "event publishing"],
        "dependencies": ["auth_service", "notification_service"],
        "parallel_development": true
      }
    ],
    "data_architecture": {
      "databases": ["PostgreSQL primary", "Redis cache"],
      "data_models": ["User", "Session", "Profile"],
      "data_flow": "event-driven with CQRS"
    },
    "integration_points": [
      {
        "name": "payment_gateway",
        "type": "external_api",
        "protocol": "REST",
        "authentication": "API_key"
      }
    ]
  },
  "technology_decisions": [
    {
      "decision_id": "tdr_001",
      "component": "backend_framework",
      "decision": "Node.js with Express",
      "alternatives": ["Django", "Spring Boot"],
      "rationale": "Team expertise and ecosystem",
      "consequences": ["Fast development", "Large ecosystem", "Potential performance limits"]
    }
  ],
  "parallel_development_plan": {
    "foundation_phase": {
      "components": ["database_schema", "authentication_service"],
      "duration": "2 weeks",
      "dependencies": []
    },
    "parallel_phases": [
      {
        "phase_name": "core_services",
        "components": ["user_service", "product_service", "order_service"],
        "duration": "4 weeks",
        "team_requirements": "3 backend developers",
        "coordination_points": ["API contract review", "integration testing"]
      }
    ]
  },
  "validation_results": {
    "requirement_coverage": "95%",
    "consistency_score": "high",
    "scalability_assessment": "meets requirements",
    "security_review": "passed with recommendations",
    "parallel_feasibility": "high confidence"
  },
  "creation_timestamp": "2024-01-01T10:00:00Z",
  "last_updated": "2024-01-01T12:30:00Z"
}
```

## Technology Research Implementation

### Research Process Using Task Tool
```bash
# Example technology research queries
Task tool: "Research latest Node.js frameworks for microservices architecture in 2024"
Task tool: "Compare PostgreSQL vs MongoDB for e-commerce application with high read/write volume"
Task tool: "Find best practices for containerizing microservices with Docker and Kubernetes"
Task tool: "Research event-driven architecture patterns for distributed systems"
Task tool: "Compare AWS vs Azure vs GCP for scalable web application deployment"
```

### Technology Decision Documentation
```yaml
technology_evaluation:
  component: "backend_framework"
  requirements: ["high performance", "team expertise", "community support"]
  options_evaluated:
    - name: "Node.js/Express"
      pros: ["fast development", "team expertise", "large ecosystem"]
      cons: ["single-threaded limitations", "callback complexity"]
      score: 8.5
    - name: "Python/Django"  
      pros: ["rapid development", "built-in admin", "ORM included"]
      cons: ["performance overhead", "monolithic tendency"]
      score: 7.0
  final_decision: "Node.js/Express"
  rationale: "Best fit for team skills and performance requirements"
```

## Architecture Documentation Templates

### System Architecture Document Structure
1. **Executive Summary**: High-level architecture overview and business value
2. **Requirements Analysis**: Functional, non-functional requirements and constraints  
3. **System Architecture**: Component design, data architecture, integration points
4. **Technology Stack**: Selected technologies with decision rationale
5. **Deployment Architecture**: Infrastructure, scaling, and operational design
6. **Parallel Development Plan**: Phases, dependencies, and coordination strategy
7. **Risk Assessment**: Technical risks and mitigation strategies

### Component Specification Format
```yaml
component_specification:
  name: "user_service"
  type: "microservice"
  purpose: "Manage user accounts and authentication"
  
  interfaces:
    rest_api:
      base_url: "/api/v1/users"
      authentication: "JWT Bearer token"
      endpoints:
        - path: "/register"
          method: "POST"
          request_schema: "UserRegistrationRequest"
          response_schema: "UserResponse"
    
    events:
      publishes: ["user.created", "user.updated"]
      subscribes: ["auth.password_reset"]
  
  dependencies:
    internal: ["auth_service", "notification_service"]
    external: ["email_provider", "user_analytics"]
  
  data_storage:
    database: "users_db"
    tables: ["users", "user_profiles", "user_sessions"]
    caching: "Redis for session management"
  
  parallel_development:
    independence_score: 8  # 1-10 scale
    coordination_needs: ["API contract validation", "database schema review"]
    mock_requirements: ["auth_service responses", "notification callbacks"]
```

## Quality Assurance and Validation

### Architecture Review Checklist
- [ ] All functional requirements addressed in component design
- [ ] Non-functional requirements have specific implementation strategies
- [ ] Component interfaces are well-defined and complete
- [ ] Data architecture supports all business processes
- [ ] Security architecture covers authentication, authorization, and data protection
- [ ] Scalability plan addresses growth requirements
- [ ] Technology choices are justified with clear decision rationale
- [ ] Parallel development plan is realistic and well-coordinated

### Validation Criteria
- **Requirement Coverage**: >95% of requirements mapped to architecture components
- **Interface Completeness**: All component interfaces defined with schemas
- **Technology Justification**: Each technology choice has documented rationale
- **Parallel Development Feasibility**: Clear independence analysis and coordination plan
- **Documentation Quality**: Architecture documents are complete and professional

## Error Handling and Recovery

### Common Issues and Solutions
- **Unclear Requirements**: Request clarification or schedule requirements workshop
- **Technology Conflicts**: Research alternatives and create comparative analysis
- **Overly Complex Architecture**: Simplify design while maintaining requirement coverage
- **Parallel Development Conflicts**: Redesign interfaces or adjust coordination strategy

### Recovery Procedures  
- **Missing Context**: Load all available project artifacts and request additional information
- **Architecture Inconsistencies**: Systematic review and resolution of conflicts
- **Technology Research Gaps**: Extended research phase with expert consultation
- **Validation Failures**: Iterative design refinement until validation passes

## Success Metrics
- Complete system architecture addresses 95%+ of requirements
- All major components have detailed specifications with interfaces
- Technology stack has documented decision rationale for each choice
- Parallel development plan identifies realistic independence opportunities
- Architecture documentation is comprehensive and professional quality

## Output Requirements

### Required Deliverables
1. **System Architecture Document**: Complete technical architecture using architecture-tmpl.yaml
2. **Component Specifications**: Detailed specs for each system component
3. **Technology Decision Records**: Documented rationale for all technology choices
4. **Parallel Development Plan**: Strategy for coordinated parallel implementation
5. **Architecture State Files**: Persistent architecture decisions and specifications

### Integration Points
- **Input**: PRD files, project briefs, existing architecture documentation
- **Output**: Technical architecture ready for PRD phase analysis
- **Tools**: Uses architect-agent capabilities and architecture templates
- **Handoff**: Architecture documents ready for dependency analysis and parallel planning
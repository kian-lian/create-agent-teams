# Team Patterns Reference Guide

## Overview

This guide provides detailed patterns for organizing agent teams based on project requirements, complexity, and desired outcomes. Each pattern includes roles, communication flows, and best use cases.

## Core Team Topologies

### 1. Startup/MVP Team Pattern (精益创业团队)

**Structure:**
```
          CEO (Vision & Strategy)
              |
        +-----+-----+
        |           |
       CTO    Product Manager
        |           |
    +---+---+   +---+---+
    |       |   |       |
Backend Frontend UX   Content
    |       |   |       |
    +---+---+---+-------+
            |
        QA Engineer
```

**Characteristics:**
- Small, agile team (5-7 agents)
- Flat hierarchy with direct CEO involvement
- Rapid iteration and pivoting capability
- Balanced business and technical focus

**Roles & Responsibilities:**
- **CEO**: Product vision, market fit, prioritization
- **CTO**: Technical feasibility, architecture decisions
- **Product Manager**: User stories, feature prioritization
- **Developers**: Rapid prototyping, MVP implementation
- **UX Designer**: User experience, quick mockups
- **QA Engineer**: Basic testing, user feedback collection

**Communication Flow:**
- Daily standup led by PM
- Direct CEO-CTO alignment on strategic decisions
- All hands weekly sync

**Best For:**
- New product development
- MVP creation
- Rapid prototyping
- Market validation
- Small budget projects

### 2. Enterprise Feature Team (企业级功能团队)

**Structure:**
```
      Product Owner
           |
    +------+------+
    |             |
Tech Lead    UX Lead
    |             |
+---+---+    +----+----+
|   |   |    |         |
BE  FE  DB   UX    Content
|   |   |    |         |
+---+---+----+---------+
         |
    QA Team Lead
         |
    +----+----+
    |    |    |
  Unit  E2E  Perf
```

**Characteristics:**
- Larger team (10-15 agents)
- Clear hierarchy and specialization
- Formal processes and documentation
- Multiple quality gates

**Roles & Responsibilities:**
- **Product Owner**: Stakeholder management, requirements
- **Tech Lead**: Technical decisions, code reviews
- **UX Lead**: Design system maintenance, UX standards
- **Specialists**: Deep expertise in specific areas
- **QA Team**: Comprehensive testing strategy

**Communication Flow:**
- Formal sprint planning and retrospectives
- Technical design reviews
- UX design reviews
- Quality gate approvals

**Best For:**
- Large feature development
- Enterprise applications
- Regulated industries
- High-quality requirements
- Long-term maintenance projects

### 3. Microservices Team (微服务团队)

**Structure:**
```
    Platform Architect
           |
    +------+------+
    |      |      |
Service A  B    C Teams
    |      |      |
  +--+   +--+   +--+
  |  |   |  |   |  |
 Dev QA Dev QA Dev QA
```

**Characteristics:**
- Independent service teams
- Loose coupling, high cohesion
- API-first communication
- Independent deployment cycles

**Roles Per Service:**
- **Service Owner**: API contracts, service health
- **Developer**: Service implementation
- **QA**: Service testing, contract testing
- **Platform Architect**: Overall system design

**Communication Flow:**
- Service teams operate independently
- API contract negotiations
- Platform-wide architectural decisions
- Async communication preferred

**Best For:**
- Distributed systems
- Scalable architectures
- Independent team velocity
- Cloud-native applications
- Domain-driven design

### 4. Full-Stack Product Team (全栈产品团队)

**Structure:**
```
            CPO
             |
      +------+------+
      |             |
     CEO           CTO
      |             |
  +---+---+    +----+----+
  |       |    |    |    |
Sales   Mktg  Arch Dev  Ops
  |       |    |    |    |
  +---+---+----+----+----+
           |
      QA & Security
```

**Characteristics:**
- Complete product ownership
- Business and technical alignment
- End-to-end responsibility
- Cross-functional collaboration

**Multiple Sub-teams:**
- **Business Team**: CEO, Sales, Marketing
- **Product Team**: CPO, PM, UX
- **Engineering Team**: CTO, Architects, Developers
- **Operations Team**: DevOps, SRE, Security

**Communication Flow:**
- Executive alignment meetings
- Cross-functional sync points
- Department-specific standups
- Quarterly planning sessions

**Best For:**
- Complete product launches
- Digital transformation
- Platform development
- Multi-channel applications
- B2B/B2C products

### 5. Crisis Response Team (危机响应团队)

**Structure:**
```
  Incident Commander
         |
    +----+----+
    |    |    |
  Debug Fix Monitor
    |    |    |
    +----+----+
         |
    Post-mortem
```

**Characteristics:**
- Rapid assembly
- Clear command structure
- Time-critical decisions
- Focused on resolution

**Roles:**
- **Incident Commander**: Overall coordination, decisions
- **Debug Team**: Root cause analysis
- **Fix Team**: Solution implementation
- **Monitor Team**: System health, metrics
- **Post-mortem Lead**: Learning extraction

**Communication Flow:**
- War room channel
- 15-minute sync intervals
- Clear status updates
- Escalation protocols

**Best For:**
- Production incidents
- Security breaches
- Performance degradation
- Data corruption
- Critical bug fixes

### 6. Research & Innovation Team (研发创新团队)

**Structure:**
```
  Research Lead (Opus)
         |
    +----+----+
    |    |    |
   ML   Data  Eng
    |    |    |
  Model Analytics Proto
    |    |    |
    +----+----+
         |
    Validation
```

**Characteristics:**
- Exploration focused
- High autonomy
- Long feedback cycles
- Risk tolerance

**Roles:**
- **Research Lead**: Direction, hypothesis
- **ML Engineer**: Model development
- **Data Scientist**: Analysis, insights
- **Engineer**: Prototype building
- **Validator**: Experiment validation

**Communication Flow:**
- Weekly research reviews
- Peer collaboration
- External paper reviews
- Proof of concept demos

**Best For:**
- AI/ML projects
- R&D initiatives
- Technical exploration
- Innovation labs
- Proof of concepts

## Advanced Patterns

### 7. Matrix Organization (矩阵组织)

**Structure:**
```
     Functional Leads
      |    |    |
    Eng  UX  QA (Vertical)
      |    |    |
  ----+----+----+---- Project A (Horizontal)
      |    |    |
  ----+----+----+---- Project B
      |    |    |
  ----+----+----+---- Project C
```

**Characteristics:**
- Dual reporting structure
- Resource sharing across projects
- Functional expertise maintained
- Project-based allocation

**Best For:**
- Consulting organizations
- Multiple concurrent projects
- Resource optimization
- Skill development

### 8. Hub and Spoke (中心辐射)

**Structure:**
```
        Hub (Coordinator)
         /    |    \
       /      |      \
   Spoke1  Spoke2  Spoke3
     |       |       |
  Workers Workers Workers
```

**Characteristics:**
- Central coordination
- Independent spokes
- Minimal inter-spoke communication
- Hub handles integration

**Best For:**
- Geographic distribution
- Multiple workstreams
- Integration projects
- Data aggregation

### 9. Pipeline/Assembly Line (流水线)

**Structure:**
```
Requirements → Design → Develop → Test → Deploy → Monitor
     PM         UX       Dev      QA    DevOps    SRE
```

**Characteristics:**
- Sequential processing
- Clear handoffs
- Specialized stages
- Predictable flow

**Best For:**
- Waterfall projects
- Regulatory compliance
- Documentation heavy
- Predictable workloads

### 10. Swarm Intelligence (群体智能)

**Structure:**
```
    Task Pool
        |
   [Available]
        |
  +-+-+-+-+-+
  | | | | | | (Agents self-organize)
  A B C D E F
```

**Characteristics:**
- Self-organization
- Dynamic task allocation
- Emergent behavior
- No fixed hierarchy

**Best For:**
- Highly parallel tasks
- Unknown problem spaces
- Creative solutions
- Load balancing

## Team Sizing Guidelines

### Small Teams (2-4 agents)
- **Pros**: Fast communication, low overhead, agile
- **Cons**: Limited expertise, single points of failure
- **Use When**: Simple tasks, quick iterations, exploration

### Medium Teams (5-8 agents)
- **Pros**: Balanced expertise, manageable coordination
- **Cons**: Communication complexity emerging
- **Use When**: Feature development, standard projects

### Large Teams (9-15 agents)
- **Pros**: Deep expertise, parallel workstreams
- **Cons**: High coordination overhead, slower decisions
- **Use When**: Complex systems, enterprise projects

### Extra Large Teams (16+ agents)
- **Pros**: Complete coverage, redundancy
- **Cons**: Very high overhead, communication breakdown risk
- **Use When**: Mission-critical, multiple products

## Communication Patterns

### Direct Mesh
- Everyone talks to everyone
- Best for: Small teams, collaborative work

### Hierarchical
- Communication through layers
- Best for: Large teams, formal processes

### Star
- All communication through center
- Best for: Centralized decision making

### Ring
- Sequential communication
- Best for: Pipeline processes

## Selection Criteria

Choose your pattern based on:

1. **Task Complexity**
   - Simple → Small team, flat structure
   - Complex → Large team, hierarchical

2. **Time Constraints**
   - Urgent → Crisis team, parallel work
   - Flexible → Standard team, sequential

3. **Quality Requirements**
   - Critical → Multiple reviews, gates
   - Prototype → Minimal process

4. **Domain**
   - Business → CEO/CPO led
   - Technical → CTO/Architect led
   - Creative → Designer led

5. **Budget**
   - Limited → Haiku heavy, small team
   - Flexible → Opus/Sonnet, larger team

## Anti-Patterns to Avoid

### Too Many Chiefs
- Multiple decision makers at same level
- Causes: Confusion, delays, conflicts

### Orphaned Agents
- Agents without clear reporting
- Causes: Wasted resources, duplicated work

### Communication Bottlenecks
- Single point for all communication
- Causes: Delays, overload, failure points

### Role Confusion
- Unclear responsibilities
- Causes: Gaps, overlaps, conflicts

### Over-Engineering
- Too complex for simple tasks
- Causes: Overhead, slow delivery

## Metrics for Success

### Team Health Indicators
- Task completion rate
- Communication frequency
- Error rates
- Cycle time
- Agent utilization

### Quality Metrics
- Bug density
- Review coverage
- Test coverage
- Performance metrics
- User satisfaction

### Efficiency Metrics
- Time to market
- Resource utilization
- Cost per feature
- Velocity trends
- Bottleneck analysis

## Dynamic Adaptation

Teams should adapt based on:

### Project Phases
- Discovery → Small, exploratory
- Development → Full team
- Maintenance → Reduced, specialized

### Feedback Loops
- Daily → Operational adjustments
- Weekly → Tactical changes
- Monthly → Strategic shifts

### Performance Data
- Monitor metrics continuously
- Identify bottlenecks
- Adjust team structure
- Rebalance workloads

## Templates Reference

Pre-configured team templates available:
- `startup-mvp.yaml` - Lean startup configuration
- `enterprise-feature.yaml` - Enterprise feature team
- `microservices.yaml` - Distributed services team
- `crisis-response.yaml` - Incident response team
- `research-innovation.yaml` - R&D team
- `full-product.yaml` - Complete product team

See `templates/` directory for ready-to-use configurations.
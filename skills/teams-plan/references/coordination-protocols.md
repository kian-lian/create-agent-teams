# Coordination Protocols Reference

## Overview

This document defines communication patterns, synchronization mechanisms, and coordination protocols for agent teams. These protocols ensure efficient collaboration, prevent conflicts, and maintain system coherence.

## Core Communication Patterns

### 1. Direct Messaging (点对点通信)

**Pattern:**
```
Agent A ──message──> Agent B
```

**Implementation:**
```typescript
// Using TeamSendMessage
TeamSendMessage({
  team_name: "feature-team",
  recipient: "backend-dev",
  message: "API endpoint /users ready for integration"
})
```

**Characteristics:**
- Low latency
- No intermediary
- Privacy between agents
- Direct acknowledgment

**Use Cases:**
- Quick questions
- Status updates
- Handoffs
- Clarifications

**Best Practices:**
- Keep messages concise
- Include context
- Expect response
- Log important decisions

### 2. Broadcast Messaging (广播消息)

**Pattern:**
```
Agent A ──message──> [All Team Members]
```

**Implementation:**
```typescript
TeamBroadcast({
  team_name: "feature-team",
  message: "Database schema updated, please pull latest",
  priority: "high"
})
```

**Characteristics:**
- One to many
- No response expected
- Information dissemination
- Awareness building

**Use Cases:**
- Announcements
- Status changes
- Warnings
- Milestone completion

### 3. Request-Reply (请求-响应)

**Pattern:**
```
Agent A ──request──> Agent B
Agent B ──reply────> Agent A
```

**Implementation:**
```typescript
// Request
const response = await TeamRequest({
  team_name: "feature-team",
  recipient: "architect",
  request: "Should we use PostgreSQL or MongoDB?",
  timeout: 30000 // 30 seconds
})

// Reply
TeamReply({
  request_id: request.id,
  response: "PostgreSQL for strong consistency requirements"
})
```

**Characteristics:**
- Synchronous pattern
- Guaranteed response
- Timeout handling
- Request tracking

**Use Cases:**
- Approval requests
- Technical questions
- Resource allocation
- Decision making

### 4. Publish-Subscribe (发布-订阅)

**Pattern:**
```
Publisher ──event──> Event Bus ──notify──> Subscribers
```

**Implementation:**
```typescript
// Subscribe
TeamSubscribe({
  team_name: "feature-team",
  events: ["api.updated", "schema.changed", "test.completed"]
})

// Publish
TeamPublish({
  team_name: "feature-team",
  event: "api.updated",
  data: { endpoint: "/users", version: "v2" }
})
```

**Characteristics:**
- Loose coupling
- Event-driven
- Asynchronous
- Multiple consumers

**Use Cases:**
- System events
- State changes
- Progress updates
- Integration points

## Synchronization Mechanisms

### 1. Barriers (屏障同步)

**Purpose:** Wait for all agents to reach a checkpoint

**Implementation:**
```typescript
// All agents must reach barrier before continuing
await TeamBarrier({
  team_name: "feature-team",
  barrier_name: "phase1_complete",
  participants: ["frontend", "backend", "qa"]
})
```

**Use Cases:**
- Phase transitions
- Sprint boundaries
- Deployment gates
- Integration points

**Example Workflow:**
```
Frontend ──┐
Backend  ──┼──> BARRIER ──> Continue
QA       ──┘
```

### 2. Locks (互斥锁)

**Purpose:** Exclusive access to shared resources

**Implementation:**
```typescript
// Acquire lock
const lock = await TeamAcquireLock({
  resource: "database_migration",
  timeout: 60000
})

try {
  // Perform exclusive operation
  await performMigration()
} finally {
  // Release lock
  await TeamReleaseLock(lock)
}
```

**Use Cases:**
- Database modifications
- File writes
- Configuration changes
- Deployment operations

**Lock Types:**
- **Exclusive**: Only one agent can hold
- **Shared**: Multiple readers, no writers
- **Upgradeable**: Read lock that can upgrade to write

### 3. Semaphores (信号量)

**Purpose:** Control concurrent access to limited resources

**Implementation:**
```typescript
// Limit concurrent API calls to 3
const semaphore = await TeamSemaphore({
  name: "api_rate_limit",
  permits: 3
})

await semaphore.acquire()
try {
  await makeApiCall()
} finally {
  semaphore.release()
}
```

**Use Cases:**
- Rate limiting
- Resource pooling
- Parallel execution control
- Load balancing

### 4. Consensus Protocols (共识协议)

**Purpose:** Achieve agreement among multiple agents

**Implementation:**
```typescript
// Propose and vote
const decision = await TeamConsensus({
  team_name: "architecture-team",
  proposal: "Switch to microservices architecture",
  voters: ["cto", "architect", "lead-dev"],
  threshold: 0.66 // 66% agreement needed
})
```

**Consensus Types:**

#### Simple Majority
```
Votes: [Yes, Yes, No] → Passed (66% > 50%)
```

#### Unanimous
```
Votes: [Yes, Yes, Yes] → Passed (100% required)
```

#### Quorum
```
Min participants: 3
Votes: [Yes, Yes, Abstain, Absent] → Valid quorum
```

#### Weighted Voting
```
CTO (weight: 3): Yes
Architect (weight: 2): Yes
Developer (weight: 1): No
Total: 5 Yes, 1 No → Passed
```

## State Management Protocols

### 1. Shared Context (共享上下文)

**Pattern:** Centralized state accessible by all agents

**Implementation:**
```typescript
// Write to shared context
TeamUpdateContext({
  team_name: "feature-team",
  context: {
    database_schema: "v2.1",
    api_version: "v3",
    deployment_target: "staging"
  }
})

// Read from shared context
const context = TeamGetContext({
  team_name: "feature-team"
})
```

**Best Practices:**
- Version control state changes
- Use atomic updates
- Implement read/write permissions
- Maintain consistency

### 2. Event Sourcing (事件溯源)

**Pattern:** State as sequence of events

**Implementation:**
```typescript
// Log event
TeamLogEvent({
  event_type: "schema.updated",
  agent: "database-engineer",
  timestamp: Date.now(),
  data: { from: "v1", to: "v2" }
})

// Replay events to rebuild state
const events = TeamGetEvents({
  from_timestamp: startTime,
  to_timestamp: endTime
})
const state = replayEvents(events)
```

**Benefits:**
- Complete audit trail
- Time travel debugging
- State reconstruction
- Conflict resolution

### 3. Distributed Transactions (分布式事务)

**Pattern:** Coordinated multi-agent operations

**Implementation:**
```typescript
// Two-phase commit
const transaction = TeamStartTransaction({
  participants: ["service-a", "service-b", "database"]
})

// Phase 1: Prepare
const votes = await transaction.prepare()

// Phase 2: Commit or Rollback
if (votes.all(v => v === "ready")) {
  await transaction.commit()
} else {
  await transaction.rollback()
}
```

**Use Cases:**
- Cross-service updates
- Distributed deployments
- Data consistency
- Atomic operations

## Workflow Coordination

### 1. Sequential Pipeline (顺序流水线)

**Pattern:**
```
A ──complete──> B ──complete──> C ──complete──> Done
```

**Implementation:**
```typescript
const pipeline = TeamPipeline({
  stages: [
    { agent: "designer", task: "create_mockups" },
    { agent: "frontend", task: "implement_ui" },
    { agent: "qa", task: "test_ui" }
  ]
})

await pipeline.execute()
```

### 2. Parallel Fork-Join (并行分叉-合并)

**Pattern:**
```
     ┌──> B ──┐
A ──>├──> C ──┼──> E
     └──> D ──┘
```

**Implementation:**
```typescript
const parallel = TeamParallel({
  fork: "requirements",
  tasks: [
    { agent: "frontend", task: "ui_development" },
    { agent: "backend", task: "api_development" },
    { agent: "database", task: "schema_design" }
  ],
  join: "integration"
})
```

### 3. Conditional Branching (条件分支)

**Pattern:**
```
A ──condition──> B (if true)
              └──> C (if false)
```

**Implementation:**
```typescript
const workflow = TeamWorkflow({
  start: "analysis",
  branches: [
    {
      condition: "complexity > high",
      then: "detailed_design",
      else: "quick_implementation"
    }
  ]
})
```

### 4. Loop/Iteration (循环/迭代)

**Pattern:**
```
A ──> B ──> C ──condition──> A (repeat)
                         └──> Done
```

**Implementation:**
```typescript
const iterative = TeamIteration({
  tasks: ["design", "review", "refine"],
  condition: "approved === false",
  max_iterations: 5
})
```

## Message Priority and Ordering

### Priority Levels

```typescript
enum Priority {
  CRITICAL = 0,  // System failures, blockers
  HIGH = 1,      // Important updates, decisions needed
  NORMAL = 2,    // Standard communication
  LOW = 3        // FYI, non-urgent
}
```

### Message Ordering Guarantees

#### FIFO (First In First Out)
```typescript
TeamSendMessage({
  ordering: "fifo",
  messages: [msg1, msg2, msg3]
})
// Guaranteed delivery order: msg1, msg2, msg3
```

#### Causal Ordering
```typescript
// Messages maintain cause-effect relationships
A sends: "Starting task" (msg1)
B sends: "Responding to A" (msg2, caused by msg1)
// msg2 always delivered after msg1
```

#### Total Ordering
```typescript
// All agents see messages in same order
TeamBroadcast({
  ordering: "total",
  message: "Critical update"
})
```

## Failure Handling Protocols

### 1. Timeout Management

```typescript
const result = await TeamRequest({
  recipient: "slow-agent",
  request: "complex-calculation",
  timeout: 30000,
  on_timeout: "retry" | "skip" | "fail"
})
```

### 2. Retry Mechanisms

```typescript
const retry_config = {
  max_attempts: 3,
  backoff: "exponential", // or "linear", "fixed"
  initial_delay: 1000,
  max_delay: 10000
}
```

### 3. Circuit Breaker

```typescript
const breaker = TeamCircuitBreaker({
  threshold: 5,        // failures before opening
  timeout: 60000,      // time before retry
  on_open: "use_fallback"
})
```

### 4. Fallback Strategies

```typescript
const result = await TeamExecute({
  primary: "sophisticated-algorithm",
  fallback: [
    "simple-algorithm",
    "cached-result",
    "default-value"
  ]
})
```

## Performance Optimization

### 1. Batching

```typescript
// Batch multiple messages
TeamBatchSend({
  messages: [
    { to: "agent1", content: "update1" },
    { to: "agent2", content: "update2" },
    { to: "agent3", content: "update3" }
  ],
  batch_size: 10,
  batch_timeout: 1000
})
```

### 2. Caching

```typescript
// Cache frequently accessed data
TeamCache({
  key: "project_config",
  value: config,
  ttl: 3600000 // 1 hour
})
```

### 3. Load Balancing

```typescript
// Distribute work evenly
TeamLoadBalance({
  tasks: taskList,
  agents: ["worker1", "worker2", "worker3"],
  strategy: "round_robin" | "least_loaded" | "weighted"
})
```

## Monitoring and Observability

### 1. Message Tracing

```typescript
// Track message flow
TeamTrace({
  trace_id: "uuid",
  span_id: "uuid",
  operation: "api_call",
  timestamp: Date.now()
})
```

### 2. Metrics Collection

```typescript
// Collect performance metrics
TeamMetrics({
  message_count: 150,
  avg_response_time: 250,
  error_rate: 0.02,
  throughput: 10
})
```

### 3. Health Checks

```typescript
// Monitor agent health
TeamHealthCheck({
  agent: "backend-service",
  checks: [
    "memory_usage < 80%",
    "response_time < 1000ms",
    "error_rate < 1%"
  ]
})
```

## Best Practices

### Do's
- Use appropriate pattern for use case
- Handle failures gracefully
- Monitor performance metrics
- Document protocol choices
- Test edge cases

### Don'ts
- Over-communicate (message storms)
- Create circular dependencies
- Ignore timeouts
- Skip error handling
- Assume message delivery

### Protocol Selection Guide

| Scenario | Recommended Protocol |
|----------|---------------------|
| Quick update | Direct message |
| Team announcement | Broadcast |
| Approval needed | Request-reply |
| Event notification | Publish-subscribe |
| Phase completion | Barrier sync |
| Exclusive access | Lock |
| Rate limiting | Semaphore |
| Group decision | Consensus |

## Advanced Patterns

### Saga Pattern
Long-running transactions with compensations

### Event Choreography
Decentralized workflow through events

### Command Query Responsibility Segregation (CQRS)
Separate read and write operations

### Actor Model
Message-passing between isolated actors

## Integration with Tools

### TodoWrite Integration
- Sync task status across team
- Update shared todo list
- Track dependencies

### MCP Server Integration
- Coordinate MCP tool usage
- Share MCP responses
- Manage MCP sessions

### Browser Automation
- Coordinate browser testing
- Share test results
- Synchronize test execution
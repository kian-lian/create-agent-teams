# Error Recovery Strategies

## Overview

This document provides comprehensive error recovery strategies for agent teams, covering detection, handling, recovery, and prevention of failures at various levels of the system.

## Error Categories

### 1. Agent-Level Failures (代理级故障)

#### Timeout Errors
**Symptoms:**
- Agent doesn't respond within expected time
- Task appears stuck
- No progress updates

**Detection:**
```typescript
const AGENT_TIMEOUT = 120000; // 2 minutes

const monitorAgent = async (agent) => {
  const lastUpdate = agent.lastHeartbeat;
  if (Date.now() - lastUpdate > AGENT_TIMEOUT) {
    return { status: 'timeout', agent: agent.id };
  }
}
```

**Recovery Strategies:**

1. **Graceful Retry**
```typescript
const retryWithBackoff = async (agent, task) => {
  const delays = [1000, 2000, 4000, 8000, 16000];

  for (let i = 0; i < delays.length; i++) {
    try {
      return await agent.execute(task);
    } catch (error) {
      if (i === delays.length - 1) throw error;
      await sleep(delays[i]);
    }
  }
}
```

2. **Model Downgrade**
```typescript
// If Opus fails, try Sonnet
const modelFallback = {
  'opus': 'sonnet',
  'sonnet': 'haiku',
  'haiku': null // No further fallback
}
```

3. **Task Redistribution**
```typescript
const redistributeTask = async (failedAgent, task) => {
  const availableAgents = team.filter(a =>
    a.id !== failedAgent.id &&
    a.status === 'available'
  );

  if (availableAgents.length > 0) {
    const newAgent = selectBestAgent(availableAgents, task);
    return await newAgent.execute(task);
  }
}
```

#### Memory/Context Overflow
**Symptoms:**
- Agent reports context limit reached
- Truncated responses
- Missing information from earlier context

**Recovery:**
```typescript
const handleContextOverflow = async (agent) => {
  // Strategy 1: Summarize and compress
  const summary = await summarizeContext(agent.context);
  agent.resetContext(summary);

  // Strategy 2: Spawn sub-agent for continuation
  const continuationAgent = await spawnAgent({
    type: agent.type,
    context: agent.getRecentContext(50000) // Last 50k tokens
  });

  // Strategy 3: Checkpoint and restart
  const checkpoint = agent.createCheckpoint();
  agent.reset();
  agent.loadCheckpoint(checkpoint, { selective: true });
}
```

#### Hallucination/Invalid Output
**Symptoms:**
- Generated code doesn't compile
- References non-existent files/functions
- Inconsistent with established facts

**Detection & Recovery:**
```typescript
const validateOutput = async (output, context) => {
  const validations = [
    checkCodeCompilation(output),
    checkFileReferences(output),
    checkConsistency(output, context)
  ];

  const results = await Promise.all(validations);

  if (results.some(r => !r.valid)) {
    // Recovery: Re-prompt with corrections
    const corrections = results
      .filter(r => !r.valid)
      .map(r => r.error);

    return await agent.retry({
      task: originalTask,
      corrections: corrections,
      additionalContext: "Please fix these issues: " + corrections.join(', ')
    });
  }
}
```

### 2. Coordination Failures (协调故障)

#### Deadlock Detection
**Symptoms:**
- Circular waiting for resources
- No progress in any agent
- Mutual blocking

**Detection:**
```typescript
const detectDeadlock = () => {
  const waitGraph = buildWaitForGraph(team);
  const cycles = findCycles(waitGraph);

  if (cycles.length > 0) {
    return {
      deadlock: true,
      cycles: cycles,
      agents: cycles.flat()
    };
  }
}
```

**Resolution:**
```typescript
const resolveDeadlock = async (deadlock) => {
  // Strategy 1: Timeout-based preemption
  const victim = selectDeadlockVictim(deadlock.agents);
  await victim.abort();
  await victim.restart();

  // Strategy 2: Resource ordering
  enforceResourceOrdering(team);

  // Strategy 3: Deadlock prevention
  implementBankersAlgorithm(team);
}
```

#### Race Conditions
**Symptoms:**
- Inconsistent state
- Lost updates
- Unpredictable behavior

**Prevention & Recovery:**
```typescript
const preventRaceCondition = async () => {
  // Use locks for critical sections
  const lock = await acquireLock('critical-resource');
  try {
    await performCriticalOperation();
  } finally {
    await releaseLock(lock);
  }

  // Use optimistic concurrency control
  let success = false;
  while (!success) {
    const version = await getResourceVersion();
    const result = await updateResource(data, version);
    success = result.success;
    if (!success) {
      await sleep(Math.random() * 1000); // Random backoff
    }
  }
}
```

#### Message Loss
**Symptoms:**
- Expected messages not received
- Incomplete handoffs
- Missing acknowledgments

**Recovery:**
```typescript
const ensureMessageDelivery = async (message) => {
  const messageId = generateId();
  const maxRetries = 3;

  for (let i = 0; i < maxRetries; i++) {
    const ack = await sendMessageWithAck(message, messageId);
    if (ack.received) return ack;

    // Exponential backoff
    await sleep(Math.pow(2, i) * 1000);
  }

  // Fallback: Use alternative communication channel
  return await sendViaAlternativeChannel(message);
}
```

### 3. Task-Level Failures (任务级故障)

#### Compilation Errors
**Recovery Workflow:**
```typescript
const handleCompilationError = async (error) => {
  // Step 1: Parse error message
  const errorInfo = parseCompilationError(error);

  // Step 2: Automatic fix attempts
  const fixes = [
    fixSyntaxError,
    fixImportError,
    fixTypeError,
    fixReferenceError
  ];

  for (const fix of fixes) {
    const result = await fix(errorInfo);
    if (result.success) {
      return await recompile(result.code);
    }
  }

  // Step 3: Escalate to specialist
  const specialist = await spawnAgent({
    type: 'debugging-specialist',
    context: errorInfo
  });

  return await specialist.fix();
}
```

#### Test Failures
**Recovery Workflow:**
```typescript
const handleTestFailure = async (testResult) => {
  const failures = testResult.failures;

  for (const failure of failures) {
    // Analyze failure type
    const analysis = await analyzeTestFailure(failure);

    switch (analysis.type) {
      case 'assertion':
        await fixAssertionFailure(failure);
        break;
      case 'timeout':
        await optimizePerformance(failure.test);
        break;
      case 'flaky':
        await stabilizeTest(failure.test);
        break;
      case 'regression':
        await fixRegression(failure);
        break;
    }
  }

  // Re-run tests
  return await runTests();
}
```

#### Deployment Failures
**Recovery Workflow:**
```typescript
const handleDeploymentFailure = async (deployment) => {
  // Step 1: Immediate rollback
  await rollbackDeployment(deployment.previous);

  // Step 2: Diagnose issue
  const diagnosis = await diagnoseDeploymentFailure(deployment);

  // Step 3: Fix and retry
  switch (diagnosis.issue) {
    case 'config':
      await fixConfiguration(diagnosis.details);
      break;
    case 'dependency':
      await resolveDependencies(diagnosis.details);
      break;
    case 'resource':
      await allocateResources(diagnosis.required);
      break;
  }

  // Step 4: Gradual rollout
  return await deployWithCanary(deployment, { percentage: 10 });
}
```

### 4. System-Level Failures (系统级故障)

#### Complete Team Failure
**Scenario:** All agents become unresponsive

**Recovery:**
```typescript
const handleTeamFailure = async () => {
  // Step 1: Emergency shutdown
  await emergencyShutdown(team);

  // Step 2: State preservation
  const state = await preserveTeamState(team);

  // Step 3: Clean restart
  const newTeam = await spawnTeam({
    configuration: team.config,
    checkpoint: state
  });

  // Step 4: State restoration
  await newTeam.restore(state);

  // Step 5: Resume from last known good state
  return await newTeam.resume();
}
```

#### Cascade Failures
**Prevention & Recovery:**
```typescript
const preventCascadeFailure = async () => {
  // Circuit breaker pattern
  const breaker = new CircuitBreaker({
    threshold: 5,
    timeout: 60000,
    resetTimeout: 120000
  });

  breaker.on('open', async () => {
    // Switch to degraded mode
    await enableDegradedMode();
  });

  breaker.on('halfOpen', async () => {
    // Test with limited traffic
    await testWithLimitedTraffic();
  });

  // Bulkhead pattern - isolate failures
  const bulkheads = createBulkheads(team, {
    maxConcurrent: 3,
    maxQueue: 10
  });
}
```

## Recovery Patterns

### 1. Retry Patterns

#### Exponential Backoff
```typescript
const exponentialBackoff = async (fn, maxRetries = 5) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      const delay = Math.min(1000 * Math.pow(2, i), 30000);
      await sleep(delay + Math.random() * 1000); // Add jitter
      if (i === maxRetries - 1) throw error;
    }
  }
}
```

#### Circuit Breaker
```typescript
class CircuitBreaker {
  constructor(threshold, timeout) {
    this.threshold = threshold;
    this.timeout = timeout;
    this.failures = 0;
    this.state = 'closed';
    this.nextAttempt = Date.now();
  }

  async execute(fn) {
    if (this.state === 'open') {
      if (Date.now() < this.nextAttempt) {
        throw new Error('Circuit breaker is open');
      }
      this.state = 'half-open';
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.failures = 0;
    this.state = 'closed';
  }

  onFailure() {
    this.failures++;
    if (this.failures >= this.threshold) {
      this.state = 'open';
      this.nextAttempt = Date.now() + this.timeout;
    }
  }
}
```

### 2. Fallback Patterns

#### Graceful Degradation
```typescript
const withFallback = async (primary, fallbacks) => {
  try {
    return await primary();
  } catch (primaryError) {
    for (const fallback of fallbacks) {
      try {
        return await fallback();
      } catch (fallbackError) {
        continue; // Try next fallback
      }
    }
    throw new Error('All fallbacks failed');
  }
}
```

#### Cache Fallback
```typescript
const withCache = async (fn, cacheKey) => {
  try {
    const result = await fn();
    await cache.set(cacheKey, result);
    return result;
  } catch (error) {
    const cached = await cache.get(cacheKey);
    if (cached) {
      console.log('Using cached result due to error');
      return cached;
    }
    throw error;
  }
}
```

### 3. Compensation Patterns

#### Saga Pattern
```typescript
class Saga {
  constructor() {
    this.steps = [];
    this.compensations = [];
  }

  addStep(forward, compensate) {
    this.steps.push(forward);
    this.compensations.push(compensate);
  }

  async execute() {
    const executed = [];

    try {
      for (const step of this.steps) {
        const result = await step();
        executed.push(result);
      }
      return executed;
    } catch (error) {
      // Compensate in reverse order
      for (let i = executed.length - 1; i >= 0; i--) {
        await this.compensations[i](executed[i]);
      }
      throw error;
    }
  }
}
```

## Monitoring and Alerting

### Health Checks
```typescript
const healthChecks = {
  agent: async (agent) => ({
    responsive: await agent.ping(),
    memory: await agent.getMemoryUsage() < 0.8,
    errors: await agent.getErrorRate() < 0.05
  }),

  team: async (team) => ({
    allAgentsHealthy: await checkAllAgents(team),
    communicationWorking: await testCommunication(team),
    progressMade: await checkProgress(team)
  }),

  system: async () => ({
    apiAvailable: await checkApiHealth(),
    resourcesAvailable: await checkResources(),
    dependenciesHealthy: await checkDependencies()
  })
}
```

### Error Metrics
```typescript
const metrics = {
  errorRate: errors / totalOperations,
  meanTimeToRecovery: avgRecoveryTime,
  failureImpact: affectedUsers / totalUsers,
  cascadeRatio: secondaryFailures / primaryFailures
}
```

### Alerting Rules
```typescript
const alerts = [
  {
    name: 'HighErrorRate',
    condition: 'errorRate > 0.1',
    severity: 'critical',
    action: 'page-oncall'
  },
  {
    name: 'AgentTimeout',
    condition: 'agentResponseTime > 60000',
    severity: 'warning',
    action: 'notify-team'
  },
  {
    name: 'DeadlockDetected',
    condition: 'deadlock === true',
    severity: 'critical',
    action: 'auto-resolve'
  }
]
```

## Prevention Strategies

### Pre-flight Checks
```typescript
const preflightChecks = async () => {
  const checks = [
    checkDependencies(),
    checkPermissions(),
    checkResources(),
    checkConfiguration(),
    validateInputs()
  ];

  const results = await Promise.all(checks);

  if (results.some(r => !r.pass)) {
    throw new Error('Preflight checks failed');
  }
}
```

### Defensive Programming
```typescript
// Input validation
const validateTask = (task) => {
  assert(task.type, 'Task type required');
  assert(task.agent, 'Agent assignment required');
  assert(task.timeout > 0, 'Valid timeout required');
};

// Boundary checks
const safeDivide = (a, b) => {
  if (b === 0) return 0;
  return a / b;
};

// Null safety
const safeAccess = (obj, path) => {
  return path.split('.').reduce((acc, part) =>
    acc && acc[part], obj) ?? null;
};
```

### Chaos Engineering
```typescript
const chaosTests = [
  () => randomlyFailAgent(0.1), // 10% failure rate
  () => introduceLatency(5000),  // 5s delay
  () => dropMessages(0.05),      // 5% message loss
  () => simulateResourceExhaustion()
];

// Run chaos tests in staging
if (environment === 'staging') {
  schedule(chaosTests, { frequency: 'daily' });
}
```

## Recovery Playbooks

### Playbook: Agent Not Responding
1. Check agent health endpoint
2. Review recent logs
3. Attempt graceful restart
4. If failed, redistribute tasks
5. Spawn replacement agent
6. Investigate root cause

### Playbook: Deployment Failure
1. Immediate rollback
2. Notify team
3. Preserve error logs
4. Run diagnostic tests
5. Fix identified issues
6. Deploy to staging first
7. Canary deployment to production

### Playbook: Data Corruption
1. Stop all writes immediately
2. Identify corruption extent
3. Restore from backup
4. Replay transaction log
5. Validate data integrity
6. Resume operations
7. Post-mortem analysis

## Best Practices

### Do's
- Fail fast and fail safe
- Log everything for debugging
- Test failure scenarios
- Have fallback plans
- Monitor continuously
- Document recovery procedures
- Practice incident response

### Don'ts
- Ignore error patterns
- Retry indefinitely
- Hide failures
- Skip validation
- Assume happy path
- Delay recovery
- Blame agents

## Integration Points

### With TodoWrite
- Mark failed tasks
- Update task status on recovery
- Track retry attempts

### With Team Coordination
- Notify team of failures
- Coordinate recovery efforts
- Share error context

### With Monitoring
- Export metrics
- Trigger alerts
- Generate reports
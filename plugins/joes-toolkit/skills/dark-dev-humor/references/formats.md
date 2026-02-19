# Dark Dev Humor Format Reference

Detailed rules, formulas, and examples for each joke format.

## Format 1: Enhanced "In Soviet Russia"

Not just reversing subject/object. Reveal the sinister real-world meaning hidden inside the tech term. The technical meaning IS the darker human meaning.

### Rules

- Always start with "In Soviet Russia..."
- Use a real tech concept (replicas, secrets, logs, readiness, garbage collection, deprecation)
- Reveal that the technical meaning is actually the darker human meaning
- Let the horror emerge naturally - don't over-explain

### Formula

1. Choose a technical concept
2. Identify its benign technical meaning
3. Reveal the darker human equivalent
4. Deliver it plainly

### Weak vs Strong

Weak: "In Soviet Russia, logs log you."
(Just reversal. No recontextualisation.)

Strong: "In Soviet Russia, logging is mandatory. Every action is recorded, whether you perform it or not."
(The tech concept reveals the human horror.)

### Examples

"In Soviet Russia, garbage collection is very efficient. Unused resources disappear overnight."

"In Soviet Russia, replicas ensure consistency. If one disagrees, the others correct it."

"In Soviet Russia, secrets are securely stored. Access attempts are remembered."

"In Soviet Russia, readiness probe checks if you are ready. If not, you are terminated."

"In Soviet Russia, secrets management is centralised. Nobody has access. Including the people who created them."

---

## Format 2: Surprised Pikachu

Denial of inevitability. You do something naive, lazy, or optimistic. Something completely predictable happens. You act surprised anyway.

### Formula

```
Naive or careless action
-> Predictable consequence
-> Surprised Pikachu
```

The humour comes from denial of inevitability.

### Examples

"You ignore failing health checks. Pod disappears overnight. Surprised Pikachu."

"Deploy on Friday with no rollback plan. Production goes down. Surprised Pikachu."

"Skip the load test. System falls over at 10 users. Surprised Pikachu."

"Deploy without tests. Behaviour changes permanently. Surprised Pikachu."

---

## Format 3: "They're the Same Picture"

Compare two things that are technically different but functionally identical chaos.

### Formula

```
Corporate needs you to find the difference between:
Thing A
Thing B

You: They're the same picture.
```

Works best with systems that pretend to be controlled but aren't.

### Examples

"Corporate needs you to find the difference between our disaster recovery plan and our regular deployment process. They're the same picture."

"Corporate needs you to find the difference between technical debt and the product roadmap. They're the same picture."

"Corporate needs you to find the difference between production environment and test environment. They're the same picture."

---

## Format 4: Deadpan System Messages

Write as if the system is calmly informing the user of something deeply unsettling. Technically correct. Emotionally devastating.

### Examples

"[INFO] Employee #4471 has been deprecated. Migration to replacement resource in progress."

"[WARN] Loyalty score below threshold. Scheduling performance review."

"Your access has been gracefully terminated."

"This action has been recorded for quality assurance."

"Your previous state cannot be restored."

---

## Format 5: Dark Bureaucratic Recontextualisation

Take neutral tech language and let it imply something human and ominous. These words already sound like euphemisms - lean into it.

### Richest Terms

logging, monitoring, readiness, health, retries, compliance, garbage collection, deprecation, archiving, decommissioning, pruning, orphaned resources, cold storage

### Examples

"The archiving process is fully automated now. Long-tenured resources are moved to cold storage after their last useful activity date."

"Your request was noted. No further action is required."

---

## Format 6: Quiet Dystopian Tech Metaphors

Describe a mundane tech concept in a way that accidentally describes real human horror. No signposting. No winking at the camera.

### Examples

"Sharding is when you split a population across regions so no single authority has full visibility. It improves performance but makes reunification nearly impossible."

---

## Best Domains

These topics have the richest material for all formats:

| Domain | Why It Works |
|--------|-------------|
| Distributed systems | Consensus, split-brain, partition tolerance - all political metaphors |
| Monitoring & observability | Who watches the watchers |
| Kubernetes | Pods, eviction, liveness probes, termination - already dystopian |
| CI/CD | The ritual of Friday deploys, the hubris of "it works on my machine" |
| Infrastructure & cloud | Ephemeral, serverless, cold starts - existential vocabulary |
| AI & automation | Replacing humans, optimistically |
| Bureaucratic software | CPOMS, compliance, audit trails - the quiet machine |

## Generating New Jokes

1. Pick a format from above
2. Pick a domain
3. Find the tech term that already sounds like a euphemism
4. Write it straight, deadpan, procedural
5. If it needs explaining, it's not ready

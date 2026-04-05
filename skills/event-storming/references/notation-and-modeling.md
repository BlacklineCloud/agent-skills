# Notation And Modeling

Use this file when you need the building blocks, format-specific grammar, or DDD-first modelling heuristics.

## Official family

EventStorming is a family of collaborative modelling formats:

- Big Picture EventStorming
- Process Modelling EventStorming
- Software Design EventStorming

The formats share an event-centred approach but differ in scope, rules, and expected outputs.

## Core notation rules

- Keep notation visible and incremental.
- Do not overload participants with every symbol at once.
- The legend matters more than the exact color palette.
- If the medium cannot support the classic physical colors, preserve the semantics and keep the legend explicit.
- Prefer simple visible building blocks to formal diagramming notation.
- Final output documents may use Mermaid as a readability aid, but diagrams must stay business-readable and subordinate to the written model.

## Output-side diagram conventions

Use Mermaid by default in final markdown documents according to the chosen format.

- Big Picture:
  required primary diagram: `flowchart LR`
- Process Modelling:
  required primary diagram: `flowchart TD`
- Software Design:
  required primary diagram: `flowchart LR` with `subgraph` boundaries
  required lifecycle diagram when a credible aggregate exists: `stateDiagram-v2`
- Document-First:
  required primary diagram: `flowchart LR`

Diagram rules:

- keep one required primary diagram per final document
- keep diagrams simple enough to read without a legend lecture
- use business terms in node labels
- avoid ornamental styling
- add secondary diagrams only when the selected template or complexity clearly justifies them

## Recommended legend

Treat this as the default baseline, not an immutable standard.

- Domain Event:
  something relevant that happened in the business
  preferred form: past tense
  examples: `Invoice Issued`, `Claim Rejected`, `Domain Renewed`
- Command or action:
  an intentional business action or decision trigger
  examples: `Approve Refund`, `Register Domain`, `Assign Technician`
- Policy:
  a repeatable reaction
  verbal form: `Whenever X, then Y`
- Actor or role:
  person, team, or role that influences or performs the work
- External system:
  a dependency, vendor, partner, or outside force
- Hot Spot:
  ambiguity, risk, contradiction, blocker, or investigation point
- Boundary:
  an explicit software or model boundary, mainly in Software Design
- Read Model:
  information needed to support a decision
- Aggregate candidate:
  a consistency boundary, not a screen or data bucket

Colors reduce cognitive load, but meaning must remain visible in the legend.

## Event heuristics

Good domain events:

- are facts that matter to the business
- are concrete enough to provoke discussion
- support storytelling along a timeline

Weak events:

- phase labels such as `Onboarding` or `Billing`
- UI steps with no business meaning
- vague status buckets that hide detail

Ask:

- What actually happened?
- Why does this matter?
- What changed because this happened?

## Command heuristics

Commands are intentional actions. They usually exist because:

- a human decided to do something
- a policy triggered a response
- a time-based rule reached a threshold

Good commands expose intent:

- `Retry Payment`
- `Suspend Account`
- `Assign Reviewer`

Weak commands merely echo implementation:

- `POST /tickets`
- `Save Record`

## Policy heuristics

Policies capture repeatable reaction logic. They often reveal:

- manual routines nobody had named
- inconsistent practices across teams
- automation opportunities
- human approval gates
- compliance or SLA behaviour

Probe with:

- What happens whenever this event occurs?
- Always?
- Immediately?
- Who notices if it does not happen?

If two people give different answers to the same `Whenever X, then Y` question, you found a high-value learning point.

## Big Picture modelling

Big Picture uses the simplest shared notation first:

- events on a timeline
- then people and systems
- then hotspots
- then optional custom steps

DDD-first prompts for Big Picture:

- Where does the language shift?
- Where does ownership change hands?
- Which areas feel like different subdomains?
- Which hotspots hint at a bounded-context seam?

Do not force aggregates here.

## Process Modelling grammar

Process Modelling is stricter than Big Picture. Use this text-friendly grammar:

1. A path starts from a trigger or prior stable state.
2. A command or decision moves the process.
3. One or more domain events show the business consequence.
4. Policies and timers explain repeatable reaction logic.
5. The path must end in a stable state.
6. Hot Spots mark unresolved concerns, objections, or corner cases.

Rule checks:

- Every path completed:
  each meaningful path ends in a stable event with no obvious missing action.
- Grammar respected:
  every step must tell a coherent story from decision to consequence.
- Stakeholders reasonably happy:
  explicit business, operational, and UX concerns must be visible.
- Every Hot Spot addressed:
  no major unresolved concern is silently ignored.

Useful prompts:

- Which path is the happy path?
- Which variations are critical enough to complete now?
- What message or step would make this unacceptable for a stakeholder?
- What hotspot must be resolved before this path can be trusted?

## Software Design grammar

Software Design expands the Process Modelling grammar with explicit software concerns.

Extra rules:

- Boundaries should be visualised.
- Software components should have consistent behaviour.

Use this modelling sequence:

1. Commands, events, and policies define the behaviour.
2. Boundaries mark where language or responsibility changes.
3. Read models show what information is needed for decisions.
4. Aggregate candidates emerge from invariants and lifecycle pressure.
5. Hot Spots and complex scenarios challenge the design.

## Actors and systems

Capture actors when:

- different roles follow different rules
- decisions or approvals shift between teams
- handoffs create delays or ambiguity

Capture external systems when:

- an outside dependency can block or distort the flow
- the team does not fully control the response
- the integration creates timing, reconciliation, or compliance risk

## Timers and delayed consequences

Make time explicit when it changes behaviour:

- monthly closes
- renewals
- expiry windows
- grace periods
- SLA deadlines
- review cadences

Not every business flow is a strict straight line. Use the timeline to enforce narrative consistency, then add explicit timing rules where they matter.

## Hot Spots

A Hot Spot can mean:

- a bottleneck
- missing knowledge
- conflict in understanding
- brittle manual handling
- policy ambiguity
- third-party risk
- likely modelling trap

Hot Spots are not failures. They are the mechanism that lets the model improve.

## Read models

Read models represent information needed for decision-making or visibility.

Use read models for:

- dashboards
- eligibility views
- invoice summaries
- support work queues
- reconciliation screens

Do not turn every read model into an aggregate. Information needed on a screen is not automatically a consistency boundary.

## Bounded-context heuristics

Start strategic DDD after the flow is coherent enough to reveal language and ownership shifts.

Look for bounded-context candidates when you see:

- different meanings for the same word
- different decision owners
- separate change cadence
- separate external dependencies
- different invariants or policies
- different failure handling

Avoid deriving contexts from:

- org charts alone
- table ownership alone
- a desire for one tidy enterprise data model

Useful prompts:

- Where does the language clearly change?
- Which team or capability owns the decision here?
- Which responsibilities should not share the same model?
- Where would forced unification create fake consistency?

## Context-map heuristics

Use a context map after the main bounded-context candidates are visible.

Common patterns:

- Partnership
- Customer/Supplier
- Conformist
- Anti-Corruption Layer
- Published Language
- Shared Kernel
- Separate Ways

Ask:

- Who can force change on whom?
- Where is translation cheaper than shared semantics?
- Which dependency is strategic, and which is merely tolerated?
- Where would shared code or schema create hidden ownership conflicts?

## Aggregate heuristics

Start aggregate discovery only after strategic boundaries make sense.

Look for aggregates where:

- a set of changes must stay internally consistent
- invariants must always hold
- multiple commands compete over the same lifecycle
- concurrency or transactional pressure matters

Do not start from:

- screen layouts
- report fields
- everything a user can search
- everything stored in one row or document today

Use this sequence:

1. Find the responsibility.
2. State what must always be true.
3. Identify commands that challenge that truth.
4. Identify events emitted when those commands succeed.
5. Keep reporting, projections, and cross-context reactions outside unless consistency requires otherwise.

Aggregates should look behaviour-first and state-machine-like, not like data containers.

## Acceptance-test extraction

Software Design EventStorming is a good place to extract acceptance tests from difficult scenarios.

Use prompts like:

- Which real-world scenario would break this model first?
- Which hotspot can be turned into an executable example?
- Which invariant must be preserved across this path?
- What should happen if this event is delayed, duplicated, or rejected?

Capture tests as:

- initial state
- triggering command
- expected events
- expected final state or read-model outcome

## DDD FAQ

### Does EventStorming require DDD?

No. Big Picture and Process Modelling remain useful without explicit DDD vocabulary.

### Why use a DDD-first lens anyway?

Because it helps preserve:

- ubiquitous language
- ownership boundaries
- context-map implications
- aggregate and consistency pressure

### When should DDD become explicit?

- lightly in Big Picture
- more clearly in Process Modelling
- fully in Software Design

## Validation prompts

Use these when the model starts to look too neat:

- What has to be true at all times?
- What can be eventually consistent?
- What happens if this step is delayed or skipped?
- What happens if the event occurs twice?
- Who notices first when this goes wrong?
- What workaround exists today?
- What is measured here, and what is merely assumed?

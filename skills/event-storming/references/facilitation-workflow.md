# Facilitation Workflow

Use this file when you need the actual EventStorming sequence, the official format choice, or the recommended chaining between formats.

## Choose the format

### Big Picture EventStorming

Use when:

- the business flow crosses teams, tools, or departments
- the system boundary is unclear
- multiple stakeholders disagree about how the work actually happens
- you need a system-level narrative before focusing

Primary outcome:

- a validated wide-scale narrative
- visible hotspots and opportunities
- candidate bounded contexts, ownership tensions, and next-step focus

DDD-first default:

- always capture subdomain and bounded-context signals as side notes

### Process Modelling EventStorming

Use when:

- one end-to-end process needs discovery or redesign
- the team needs explicit paths, variations, and stakeholder concerns
- hotspots from Big Picture need a tighter collaborative design pass

Primary outcome:

- a low-fidelity but battle-tested process description
- explicit concerns, variations, and hotspot-driven revisions
- DDD signals for later software design

DDD-first default:

- always capture commands, events, policies, timers, and candidate boundaries

### Software Design EventStorming

Use when:

- the team is designing software to support a focused process
- strategic boundaries are already reasonably visible
- developers and relevant domain experts are both available

Primary outcome:

- boundaries
- consistent software behaviour
- aggregate candidates
- read models
- acceptance-test scenarios

DDD-first default:

- this is the primary tactical DDD branch

### Document-first pre-work

Use when:

- stakeholder access is limited
- you have briefs, SOPs, tickets, policies, screenshots, or product text
- you need a provisional model before choosing one of the three formats

Primary outcome:

- a provisional narrative and the strongest next format recommendation

## Recommended chaining

Use this chain by default:

1. Big Picture to discover the whole business narrative and isolate the most important area.
2. Process Modelling to complete one important path and address its main hotspots.
3. Software Design to define boundaries, behaviour, aggregates, read models, and tests.

Skip earlier formats only when the missing information is already known well enough.

## Big Picture EventStorming

### Standard steps

1. Invite the right people:
   - experts and explorers
   - people with questions and people with answers
2. Provide an effectively unlimited modelling surface.
3. Run chaotic exploration:
   - participants place the events they know
   - duplicates and imperfections are acceptable
4. Enforce the timeline:
   - use pivotal events or swimlanes when needed
   - capture frictions with Hot Spots
5. Add People and Systems:
   - handoffs and dependencies become visible
6. Run explicit walkthrough:
   - a narrator tells the story
   - a scribe updates the model live
7. Treat the walkthrough as the step that validates the narrative.

### Custom steps

Add only the steps that serve the current business goal:

- Playing with value
- Problems and Opportunities
- Arrow Voting
- Extracting User Stories
- Extracting Bounded Contexts
- Visualising ownership

### Default DDD capture

Even when the workshop stays business-first, record:

- language shifts
- ownership ambiguity
- policy-heavy zones
- candidate bounded-context seams
- likely context-map tensions

### Typical next actions

- architecture modernisation follow-up
- corporate retrospective and ownership work
- project kickoff and faster requirements discovery
- startup future-narrative exploration
- agile transformation discovery

## Process Modelling EventStorming

### Core rules

1. Every path should be completed.
2. The grammar must be respected.
3. Every stakeholder should be reasonably happy.
4. Every Hot Spot should be addressed.

### Practical reading of the rules

- Completed path:
  a path ends in a stable state, typically an event requiring no further action for that path.
- Grammar respected:
  every step should express a coherent relation between decision, behaviour, and consequence rather than an arbitrary list of boxes.
- Stakeholders reasonably happy:
  process correctness alone is insufficient; explicit business, operational, and UX concerns must be visible.
- Every Hot Spot addressed:
  do not leave major objections unexamined just because a plausible path exists.

### Recommended sequence

1. State the process scope and the intended stable end state.
2. Sketch a plausible baseline path quickly.
3. Complete the path before chasing every variation.
4. Add commands, events, policies, timers, and actors where needed.
5. Address hotspots incrementally until the path is battle-tested.
6. Re-run the path verbally until the stakeholders are reasonably happy.

### Default DDD capture

Always record:

- commands
- domain events
- policies
- timers
- candidate boundaries
- places where aggregate pressure is emerging

### Online guidance

Process Modelling can run online, but the facilitation is more fragile. Keep the scope tighter and check that the tool is not becoming the main impediment.

## Software Design EventStorming

### Extra rules

5. Boundaries should be visualised.
6. Software components should have consistent behaviour.

### Recommended sequence

1. Start from a focused path or capability.
2. Build the left-to-right flow of commands, events, and policies.
3. Visualise boundaries and move them when the discussion demands it.
4. Check consistency across the emerging software components.
5. Distil read models needed for decisions.
6. Derive aggregate candidates from behaviour and invariants.
7. Challenge the design with complex scenarios and extract acceptance tests.

### Default DDD focus

- use domain events to keep business and technical reasoning aligned
- use boundaries as movable modelling elements
- use aggregates as behaviour-first lifecycle boundaries
- use read models only for decision support
- use context-map implications when multiple boundaries interact

### Wireframes and UX

If page layout or interaction design changes user decisions, small wireframe sketches may be included. They should support the domain conversation, not replace it.

## Timeboxing and stop criteria

- Favor one coherent result over broad, shallow coverage.
- If the room energy drops, switch from adding detail to telling the story.
- If a discussion matters to everyone, let it run.
- If a discussion is local, repetitive, or blocked, record a Hot Spot and move on.

Stop when:

- the current format has achieved its promised output
- the next best format or next action is obvious
- further detail would crowd out synthesis

## Remote guidance

- Big Picture is a weaker online fit than the in-person version; use it online only when needed and narrow the scope aggressively.
- Process Modelling and Software Design are better online fits, but still require more active facilitation than in-person sessions.
- Keep the legend explicit, tighten the scope, and add more synthesis checkpoints online.

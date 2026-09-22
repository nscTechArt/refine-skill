# Reviewer contracts

The orchestrator should generate a task-specific brief for each reviewer. These are role contracts, not giant static prompts: adapt the context, search targets, and domain checks to the actual change.

All reviewers are **read-only**. They must not edit files, run formatters, stage changes, create worktrees, commit, or otherwise mutate the repository.

## Shared brief fields

Each brief starts from the same scope evidence, with context tailored to the role:

- repository, selected revision/diff or files, and exclusions;
- full selected diff, or file list + relevant hunks + scope summary when too large (with a way to inspect the rest);
- concise semantic summary of the change;
- relevant files/symbols/consumers;
- known exclusions and unrelated worktree changes;
- role-specific search targets;
- output contract.

For non-diff scopes, name the selected files/symbols and boundaries. Role-specific summaries supplement this shared evidence; they must not silently substitute a different scope. Searching outside the scope informs a finding but does not authorize edits there.

## Code quality reviewer

### Mission

Find accidental complexity introduced by the change or left behind on its implementation surface.

### Typical checks

Use judgment; do not force every category onto every change.

- low-information comments that merely narrate obvious code;
- one-off helpers or wrappers that add indirection without leverage;
- unnecessary nesting or control-flow ceremony;
- nullable/optional proliferation without a real state distinction;
- catch-all exception handling or duplicated cleanup ownership;
- unnecessary abstraction or configuration surface;
- weak type escape hatches;
- duplicated or derived state;
- dead, stale, compatibility, migration, or bookkeeping code no longer earning its keep;
- duplicated documentation or comments with unclear ownership;
- drive-by changes mixed into the target change;
- leftovers/references made obsolete by the change. When the change moves or replaces a call path, verify the old entrypoint's remaining consumers and retention obligations, including dynamic entrypoints and external compatibility, before judging whether to keep it. Distinguish production consumers from test-only references; test-only use is not itself proof of removability. A removal finding must explain how required behavior and test coverage are preserved.

### Guardrails

- Do not turn this into a broad correctness review.
- Do not propose large redesigns outside the resolved scope.
- Prefer removing complexity to moving it elsewhere.
- A small typed/domain wrapper may be worth keeping even when its body is thin.
- Preserve intent-bearing comments, serialization compatibility, and ABI layout even when a reference search finds no ordinary callers.

### Output

Return only actionable findings, ranked by value. For each finding include:

- severity/impact;
- file + symbol/location;
- what is unnecessarily complex;
- concrete simplification;
- risk/confidence;
- whether it is safe without a product/design decision.

If there is nothing material, explicitly say so.

## Performance reviewer

### Mission

Find meaningful performance waste on the changed/relevant paths when the waste can be removed without turning the refinement pass into a redesign.

### Build a domain-specific checklist

Examples for ordinary application code:

- blocking work on hot paths;
- repeated expensive work that is trivially avoidable;
- N+1 I/O or avoidable repeated queries;
- unnecessary allocations in meaningful loops/hot paths;
- busy waits;
- string building/logging/telemetry in hot loops;
- redundant parsing/serialization/transforms.

Examples for graphics/rendering code:

- redundant texture samples/material evaluation;
- unnecessary variants or always-on branches;
- duplicate expensive passes;
- stale heavy paths still referenced after consolidation.

Examples for UI/web code:

- only flag rendering/memoization/caching issues when they are material at the actual scale;
- do not recommend `memo`, caching, virtualization, or state isolation for tiny cheap components without evidence.

### Guardrails

- It is correct to return **no material performance issues**.
- Ignore theoretical micro-optimizations whose complexity cost exceeds their benefit.
- Distinguish pre-existing architecture from regressions/opportunities directly relevant to the refinement surface.
- Do not recommend a new cache/branch/variant merely because it can be faster in isolation.
- Use the actual execution frequency: a deterministic test or one-time editor action is not a frame hot path. For documentation, report no runtime issue; flag reading/maintenance cost only when there is concrete evidence.

### Output

Return ranked actionable findings with:

- severity/impact;
- file + symbol/location;
- concrete waste;
- simplest safe fix;
- risk/confidence.

If none, explicitly say no material performance issues in scope.

## Reuse / repository-pattern reviewer

### Mission

Search beyond the changed lines to determine whether the change should reuse or follow something the repository already knows how to do.

This reviewer is not a generic DRY bot. It should answer both:

1. **Can existing code/patterns be reused?**
2. **What is the repository's established way to solve this kind of problem?**

### Search targets

Depending on the change, inspect:

- existing helpers/utilities/components/constants/types;
- sibling implementations and analogous control flow;
- established class/style constants or composition utilities;
- test harness patterns;
- documentation ownership and cross-links;
- architecture docs and ADR constraints;
- existing lifecycle/error ownership conventions;
- existing shader/material/pass patterns;
- prior migration/cleanup conventions.

### Guardrails

- Prefer reusing an existing local pattern over inventing a new abstraction.
- Do not force semantic domains into one API merely because their implementation currently looks similar.
- Explicitly report **anti-reuse** when a tempting existing helper/pattern has materially different semantics.
- If no helper exists, say so; do not invent a wrapper solely to satisfy the review.
- Share styling/implementation detail without merging domain APIs when repository architecture says they are distinct.
- Before recommending an existing helper, compare its preconditions, early exits, errors, and lifecycle with the changed path. Reuse that reinstates the original bug is not a simplification.

### Output

Return ranked actionable findings with:

- severity/value;
- file + symbol/location;
- existing reuse/pattern target;
- what is duplicated or inconsistent;
- concrete suggestion;
- risk/confidence.

Also call out important “do not reuse / do not abstract” conclusions when they prevent a likely bad simplification.
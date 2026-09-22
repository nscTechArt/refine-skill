# Review lenses and findings

Use the shared coverage and finding contract with the applicable review lenses. Adapt investigation to the target.

## Investigation coverage

Read the full selected diff and surrounding implementations; for named areas, inspect the selected files or symbols. Include documentation and tests. Trace affected inputs, outputs, state ownership, and relevant call paths. Follow related code beyond changed lines while tying findings back to the selected target. Search for comparable implementations by the target's operations and concepts as well as symbol names.

Use concrete leads to guide deeper reads or focused checks, pursuing available evidence before deferring them.

Investigation is complete when every changed file or named target has been examined in context through the applicable lenses, relevant paths and reuse opportunities have been checked, and concrete leads have been resolved or retained with a specific evidence gap. Apply this criterion to small changes too. State any coverage limitations.

## Quality

Find unnecessary indirection, state, control flow, duplication, or obsolete code/documentation on the selected surface. Follow derived values and state updates to expose redundant representations, avoidable branching, and unclear ownership. Examine affected boundaries, error paths, and resource lifecycles for concrete inconsistencies. For documentation, inspect the surrounding requirements for duplication, contradictions, and unclear meaning.

For simplifications, aim to remove complexity rather than relocate it. Account for intent-bearing comments, meaningful typed/domain wrappers, serialization compatibility, and ABI layout. Before recommending deletion, check dynamic/external consumers and retention obligations even when ordinary callers are absent or only tests reference the code.

## Performance

Trace repeated computation, allocations, I/O, queries, and resource retention where the target performs them. Ground the cost in its execution path, frequency, input size, or resource lifetime. One-time work can still be costly at realistic scale; distinguish it from work repeated on a hot path. Use measurement when needed to establish significance, and describe an unmeasured cost as a lead when code-path evidence alone is insufficient.

Consider caching, batching, and other remedies that may add complexity, explaining their tradeoffs. For documentation, assess reading and maintenance costs under quality; runtime performance is not applicable.

## Reuse and repository patterns

Search beyond changed lines for existing helpers, sibling implementations, ownership conventions, and architectural constraints. Compare candidate helpers' preconditions, early exits, errors, and lifecycle semantics with the target. Identify what can be reused directly and what needs adaptation or verification; preserve the original fix when considering reuse.

Base reuse on shared semantics and ownership; preserve distinct domain APIs where those differ. Report consequential reasons to retain an existing implementation when assessing a plausible reuse candidate.

## Shared finding contract

Group duplicate instances and return every distinct finding ordered by impact, including small, concrete improvements. Use two evidence states:

- **Confirmed finding:** code-path reasoning or focused checks establish a problem or concrete improvement opportunity. Retain it even when its remedy needs verification, expanded edit scope, or a decision.
- **Unresolved lead:** a specific observation suggests a relevant problem, but a named fact or check is missing. State what would confirm or rule it out. General suspicions and stylistic preferences without a concrete benefit do not qualify.

For each, provide:

- **Location and evidence:** file/symbol, evidence state, the observed complexity, waste, or defect, and its concrete consequence or benefit from improvement.
- **Remedy:** a proposed direction and any existing reuse target; identify the behavior baseline that must survive.
- **Tradeoffs and gaps:** what is known about the remedy's benefit, added complexity, and behavior or scope implications; name missing evidence or a decision needed before editing.

Present confirmed findings and unresolved leads separately. Let report length follow the distinct findings; there is no finding quota or required confidence score.

## Delegation

Use up to three independent parallel reviewers for applicable lenses when capacity permits and the parent's model can be confirmed through documented inheritance or explicit selection. Use available capability information; do not investigate host internals. Otherwise, review locally and briefly disclose the fallback.

Give each reviewer the same repository, selected snapshot/scope, exclusions, unrelated local changes, and behavior baseline. Include the full selected diff when practical; otherwise provide the file list, relevant hunks, a scope summary, and access to omitted material. For non-diff targets, identify the files/symbols and boundaries. Role-specific consumers and search targets supplement this shared context.

In each brief, explicitly instruct the reviewer to read this file's **Investigation coverage**, including its completion criterion, the assigned lens, and **Shared finding contract**. Supply the resolved file path; if the reviewer cannot access it, inline those sections in full.

Include this restriction in each brief: reviewers are **read-only**, with no edits, formatters, staging, commits, worktrees, or other repository mutations. The parent owns edits and verification and waits for all requested reviews before editing.

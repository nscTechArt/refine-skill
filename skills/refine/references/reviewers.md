# Review lenses and findings

Use these lenses for local review or delegated tasks. Adapt investigation to the actual change rather than running a generic checklist.

## Delegated brief

Every reviewer is **read-only**: no edits, formatters, staging, commits, worktrees, or other repository mutations.

Give each reviewer the same repository, selected snapshot/scope, exclusions, unrelated local changes, and behavior baseline. Include the full selected diff when practical; otherwise provide the file list, relevant hunks, a scope summary, and access to omitted material. For non-diff targets, identify the files/symbols and boundaries. Add only relevant consumers and role-specific search targets. Include the read-only restriction and shared finding contract in each brief.

Reading outside the scope provides evidence, not edit authorization. A role-specific summary must not replace or silently narrow the shared scope.

## Quality

Find unnecessary indirection, state, control flow, duplication, or obsolete code/documentation on the selected surface. Remove complexity rather than relocate it; do not turn refinement into a broad correctness audit or redesign.

Preserve intent-bearing comments, meaningful typed/domain wrappers, serialization compatibility, and ABI layout. Before deleting an old path, check dynamic/external consumers and retention obligations. No ordinary callers, or only test references, does not prove removability; explain how required behavior and coverage survive.

## Performance

Find meaningful wasted work removable through targeted simplification. Ground findings in the actual execution path, frequency, and scale; a test or one-time editor action is not a frame hot path. Ignore speculative micro-optimizations and unrelated architectural debt.

For documentation, conclude that runtime performance is not applicable; assess concrete reading/maintenance costs under quality instead. Faster code is not automatically simpler: performance findings use the same acceptance filter as every other finding.

## Reuse and repository patterns

Look beyond changed lines for existing helpers, sibling implementations, ownership conventions, and architectural constraints. Prefer established local solutions, but compare preconditions, early exits, errors, and lifecycle semantics before recommending reuse. Never reuse a helper that reinstates the original bug.

Do not conflate domain APIs because their bodies look alike or invent an abstraction to satisfy the role. Report an important reason **not** to reuse or abstract when it prevents a likely bad simplification.

## Shared finding contract

Return material findings, ordered by value. For each, provide:

- **Location and change:** file/symbol, unnecessary complexity or waste, and the concrete simplification; name any reuse target.
- **Evidence:** why the premise is true and which behavior baseline must survive, supported by code-path reasoning or focused checks. Identify missing evidence rather than assuming equivalence.
- **Net value and risk:** expected benefit, added complexity, and any scope, compatibility, or product/design decision blocking acceptance.

Keep findings concise; no severity or confidence score is required. No material findings is a valid result. Reviewers recommend; the parent verifies and decides.

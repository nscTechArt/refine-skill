# Finding validation and implementation policy

## Validate findings

Merge duplicate candidates, then independently check each premise and its connection to the selected target. Resolve disagreements and open evidence gaps through focused reads or checks against the behavior baseline, execution paths, tests, and repository conventions. Classify results using the [finding contract](reviewers.md#shared-finding-contract), ruling out candidates contradicted by evidence or lacking a concrete consequence or benefit.

For historical or staged targets, distinguish evidence in the selected snapshot from applicability to the current tree, including findings already addressed by later changes.

## Implementation filter

Apply a proposed cleanup only when all four conditions hold:

1. **Supported and in scope.** Its premise is true in the current tree, and it belongs to the selected surface rather than nearby cleanup debt.
2. **Behavior-preserving.** Identify the affected baseline and justify preservation with concrete code-path reasoning or focused verification. Check relevant edge cases, including input distinctions, errors, ordering, and lifecycle timing. Fewer states or passing existing tests alone do not establish equivalence. If evidence is missing, defer the edit and state what is needed.
3. **Net simpler and worthwhile.** The smallest targeted change removes more complexity than it adds, has a meaningful payoff, and follows repository patterns unless novelty is justified. Do not trade a few duplicated lines for unnecessary indirection, configuration, or merged domain concepts.
4. **Decision-safe.** It does not make an unresolved product, design, visual, or API choice.

Implement correctness repairs, behavior changes, and optimizations requiring greater complexity or broad redesign only when the user's existing request authorizes that work, with appropriate verification. Keep their implementation separate from cleanup governed by these four conditions.

Record an implementation outcome for each confirmed finding: applied, recommended in review-only mode, deferred with a reason, or already addressed in the current tree. Keep remedy blockers separate from the finding's evidence state. Apply accepted edits under the [scope and authorization rules](../SKILL.md#1-select-and-protect-the-scope), then [verify and report](../SKILL.md#4-verify-and-report). If none qualify, leave the target unchanged.

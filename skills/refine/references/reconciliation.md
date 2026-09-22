# Acceptance policy

Reviewer output is evidence, not permission to edit. After all requested reviews finish, the parent groups duplicate findings without inflating their importance. Resolve conflicts from the behavior baseline, concrete execution paths, tests, and repository conventions or architecture decisions, not votes or confidence scores.

## Acceptance filter

Apply a candidate only when all four conditions hold:

1. **Supported and in scope.** Its premise is true in the current tree, and it belongs to the selected surface rather than nearby cleanup debt.
2. **Behavior-preserving.** Identify the affected baseline and justify preservation with concrete code-path reasoning or focused verification. Check relevant edge cases, including input distinctions, errors, ordering, and lifecycle timing. Fewer states or passing existing tests alone do not establish equivalence. If evidence is missing, defer the candidate and state what is needed.
3. **Net simpler and worthwhile.** The smallest targeted change removes more complexity than it adds, has a meaningful payoff, and follows repository patterns unless novelty is justified. Do not trade a few duplicated lines for unnecessary indirection, configuration, or merged domain concepts.
4. **Decision-safe.** It does not make an unresolved product, design, visual, or API choice. Correctness repairs and behavior changes are separate work: implement them only if the user's existing request authorizes them, and report them separately from cleanup.

Performance gains do not waive any condition. Remove obvious wasted work when the result is also simpler; report optimizations requiring greater complexity or broad redesign as separate recommendations, not refinement edits.

A valid suggestion may still be deferred. Recheck reviewer evidence independently; apply only accepted edits under the [scope and authorization rules](../SKILL.md#1-select-and-protect-the-scope), then [verify and report](../SKILL.md#4-verify-and-report). Do not change code merely to produce a non-empty patch.

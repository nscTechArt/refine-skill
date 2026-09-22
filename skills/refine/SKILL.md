---
name: refine
description: Refine a requested code or documentation change through quality, performance, and reuse reviews, then apply targeted behavior-preserving cleanup. Use for a diff, commit, or named area; review the whole repository only when explicitly requested.
---

# Refine

Reduce accidental complexity in the selected scope without changing its intended behavior. Quality, performance, and reuse are review lenses, not finding quotas. The parent owns edits and verification; reviewers supply evidence.

Use a Git working tree and the host's file, command, and editing tools. Subagents are optional. Honor review-only requests; questions about the skill do not authorize running it.

## 1. Select and protect the scope

Read repository instructions and inspect `git status`. Resolve the target in this order:

1. **Explicit scope:** requested paths, symbols, commit/range, staged/unstaged changes, or named area. Whole-repository review requires an explicit request; docs-only targets are valid. If empty, report and stop without reviews or edits; if invalid or inaccessible, clarify rather than substitute a target.
2. **Local changes:** inspect both `git diff --no-color` and `git diff --cached --no-color`; use the combined changes relevant to the request.
3. **Conversation target:** concrete files, symbols, or changes already identified.
4. **HEAD:** inspect `git show --stat --patch --no-color HEAD`; stop if no usable target exists.

Note the selected snapshot and exclusions, including relevant untracked files omitted by Git diffs. Reading callers or sibling implementations is context, not permission to edit them; a docs-only target does not authorize implementation cleanup.

For staged or historical targets, compare the selected snapshot with the working tree. Preserve unrelated hunks, even in the same file, and never undo later changes. Block only findings that cannot be safely separated from local work. Do not revert user changes or run formatters across excluded files.

Stage only when authorized to stage or commit; create new commits only when authorized to commit. Honor authorization already given in the conversation. Otherwise keep the index and history unchanged. Reviewing staged changes or writing a commit message grants neither permission. Rewriting history, including amend or rebase, requires explicit authorization for that operation.

## 2. Establish intent and review

Record a concise behavior baseline: for a diff/commit, its intended **post-change** features, fixes, and compatibility contracts; for a named area, its existing behavior and documented contracts. For documentation, preserve meaning and requirements. Identify relevant consumers and execution scale. No separate planning document is required.

Read [reviewers.md](references/reviewers.md) for the three lenses and shared finding contract. Consider all three, with effort proportional to the target:

- **Small or straightforward scope:** the parent covers the lenses in one read-only review, without separate briefs or reports per lens.
- **Larger scope:** use independent parallel reviewers for applicable lenses when useful, up to three. Delegate only with sufficient capacity and confirmed use of the parent's model through documented inheritance or explicit selection. Use available capability information; do not investigate host internals. Otherwise, review locally and briefly disclose the fallback.

A lens with nothing material to investigate may end with a brief conclusion; documentation does not need a runtime-performance review. If delegating, use the brief and read-only restrictions in `reviewers.md`. Wait for all requested reviews before editing. Do not manufacture findings to fill roles.

## 3. Accept only worthwhile simplifications

When there are candidate findings, read [reconciliation.md](references/reconciliation.md). The parent independently checks each candidate against that acceptance filter, resolves disagreements from evidence, and applies only accepted, authorized edits. If none qualify, leave the target unchanged.

## 4. Verify and report

Run the smallest meaningful checks permitted by repository/user instructions. Reinspect the final diff and workspace against the initial scope, index, history, and unrelated changes. Distinguish passed checks from attempted, unavailable, or skipped checks.

Briefly report applied cleanup, material deferred findings and reasons, and verification. Mention relevant workspace constraints or delegation fallback, not a recital of every rule. Separate deferred work from deliberate decisions to retain code. Empty scope and no-change outcomes are complete results.

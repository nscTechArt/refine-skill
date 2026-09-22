---
name: refine
description: Review a code or documentation diff, commit, or named area for quality, performance, and reuse opportunities, then apply targeted behavior-preserving cleanup. Supports review-only requests; whole-repository review requires an explicit request.
---

# Refine

Investigate quality, performance, and reuse opportunities in the selected scope, then reduce accidental complexity without changing intended behavior. Evaluate findings independently of whether their remedies qualify for implementation.

Use a Git working tree and the host's file, command, and editing tools. Subagents are optional. Honor review-only requests; questions about the skill do not authorize running it.

## 1. Select and protect the scope

Read repository instructions and inspect `git status`. Resolve the target in this order:

1. **Explicit scope:** requested paths, symbols, commit/range, staged/unstaged changes, or named area. Whole-repository review requires an explicit request; docs-only targets are valid. If empty, report and stop without reviews or edits; if invalid or inaccessible, clarify rather than substitute a target.
2. **Local changes:** inspect both `git diff --no-color` and `git diff --cached --no-color`; use the combined changes relevant to the request.
3. **Conversation target:** concrete files, symbols, or changes already identified.
4. **HEAD:** inspect `git show --stat --patch --no-color HEAD`; stop if no usable target exists.

Note the selected snapshot and exclusions, including relevant untracked files omitted by Git diffs. Repository-wide searches may locate context for the target; editing related code still requires scope authorization. A docs-only target does not authorize implementation cleanup.

For staged or historical targets, compare the selected snapshot with the working tree. Preserve unrelated hunks, even in the same file, and never undo later changes. Defer edits that cannot be safely separated from local work. Do not revert user changes or run formatters across excluded files.

Stage only when authorized to stage or commit; create new commits only when authorized to commit. Honor authorization already given in the conversation. Otherwise keep the index and history unchanged. Reviewing staged changes or writing a commit message grants neither permission. Rewriting history, including amend or rebase, requires explicit authorization for that operation.

## 2. Establish intent and review

Record a concise behavior baseline: for a diff/commit, its intended **post-change** features, fixes, and compatibility contracts; for a named area, its existing behavior and documented contracts. For documentation, preserve meaning and requirements. Identify relevant consumers and execution scale.

Read and follow [reviewers.md](references/reviewers.md) for investigation coverage and its completion criterion, all applicable lenses, and the finding contract. Review locally for straightforward targets. When the target's dependencies or uncertainty benefit from independent review, follow its [delegation instructions](references/reviewers.md#delegation). Both paths use the same investigation standard.

## 3. Validate findings and select edits

When there are candidate findings, read and follow [reconciliation.md](references/reconciliation.md) to validate them, assess remedies, and select authorized edits. In review-only mode, assess remedies and blockers without applying them.

## 4. Verify and report

Run the smallest meaningful checks permitted by repository/user instructions. Reinspect the final diff and workspace against the initial scope, index, history, and unrelated changes. Distinguish passed checks from attempted, unavailable, or skipped checks.

Report all retained findings using the [finding contract](references/reviewers.md#shared-finding-contract), with their implementation outcomes and reasons. Keep correctness repairs, behavior changes, and optimizations requiring added complexity distinct from simplification.

For review-only requests, lead with findings and evidence; for cleanup requests, lead with applied changes and remaining findings. Include verification and relevant coverage or workspace limitations. Distinguish no findings, no accepted edits, and incomplete investigation. If all candidates were ruled out, summarize any consequential reason to retain the existing code.

---
name: refine
description: Refine a requested code or documentation change through quality, performance, and reuse reviews, then apply targeted behavior-preserving cleanup. Use for a diff, commit, or named area; review the whole repository only when explicitly requested.
---

# Refine

Reduce accidental complexity while preserving the selected scope and intended behavior. The parent owns edits; reviewers supply evidence.

## 1. Select the scope

Read repository instructions and inspect `git status` before reviewing. A question about this skill's location or applicability is a question, not an instruction to run a refinement pass. Honor explicit review-only requests.

Resolve scope in this order:

1. **Explicit scope:** use the requested paths, symbols, commit, range, staged/unstaged changes, or natural-language area. Whole-repository and documentation-only scopes are valid when requested. If that scope is empty, report it and stop without edits or reviewers. An invalid or inaccessible scope needs clarification, not a substitute target.
2. **No explicit scope:** inspect both `git diff --no-color` and `git diff --cached --no-color`; use the combined non-empty changes relevant to the request.
3. **No local diff:** use concrete files, symbols, or changes identified in the conversation.
4. **No conversation target:** inspect `git show --stat --patch --no-color HEAD`. If no usable HEAD exists, report that no target is available.

Record the selected revision/diff and exclusions. Git diffs omit untracked files; account for them when the request or conversation includes them. Reading callers, sibling implementations, or documentation provides review context; it does not expand the edit scope. In particular, a docs-only commit does not authorize cleanup of nearby uncommitted implementation.

For a historical or staged diff, compare the selected snapshot with the current working tree before proposing edits. Preserve unrelated hunks even within the same file. If the versions cannot be safely separated, report the affected finding as blocked rather than overwriting local work.

Keep index and history unchanged unless the user has authorized staging or committing, including earlier in the conversation. Reviewing staged changes does not authorize re-staging; writing a commit message does not authorize a commit.

## 2. Prepare the reviews

Understand the change's purpose, affected consumers, relevant runtime scale, and the behavior an earlier fix must retain.

Read [references/reviewers.md](references/reviewers.md) for the role contracts. Give all reviewers the same selected scope and exclusions, plus the full selected diff when practical. For large diffs, provide the file list, relevant hunks, a scope summary, and how to inspect omitted material. For non-diff scopes, provide the selected files/symbols and boundaries instead.

Add role-specific context: invariants for quality, hot paths and scale for performance, and existing patterns or search targets for reuse. This context supplements the shared scope evidence.

## 3. Run three read-only reviews

For a non-empty refinement scope, launch exactly three independent reviewers in parallel when delegation is available:

1. **Code quality** — unnecessary complexity, redundant state, wrappers, or obsolete code.
2. **Performance** — meaningful waste removable through targeted simplification.
3. **Reuse / repository patterns** — existing implementations and conventions, including reasons not to reuse them.

Use the parent's model for all three; inherit it rather than choosing a cheaper/faster model by default. Tell every reviewer to report only: no edits, formatters, staging, commits, or worktree creation. Wait for all three results before applying findings.

If delegation or capacity prevents three parallel reviews, perform the same three passes sequentially and disclose the fallback. A reviewer may return **no material findings**; a documentation-only scope does not require an invented runtime performance problem.

## 4. Reconcile and edit

Read [references/reconciliation.md](references/reconciliation.md) before accepting findings. Deduplicate recommendations and resolve disagreements against behavior and repository evidence, not votes or confidence scores.

Apply only supported, in-scope, behavior-preserving changes that reduce total complexity. Keep the original fix intact. Small duplication can be simpler than a new abstraction.

Report discovered correctness problems or behavior changes separately from simplification. Implement them only when the user's existing request also authorizes that work; otherwise leave them as findings. Do not silently turn input validation, error handling, or product choices into cleanup.

When no finding passes the acceptance filter, leave the code unchanged.

## 5. Verify and report

Run the smallest meaningful checks for the edited surface permitted by repository/user instructions. Reinspect the final diff and workspace state against the initial scope, index, and unrelated changes. Distinguish successful checks from attempted, unavailable, or skipped checks.

Summarize applied cleanup, deferred recommendations with reasons, and verification. Separate recommendations from deliberate decisions to retain existing code. Mention unchanged index/history, preserved local work, or sequential fallback when relevant. An empty scope or no-change result is a complete outcome.

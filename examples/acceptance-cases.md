# Behavioral acceptance cases

These fixtures exercise scope, authorization, and behavior preservation using temporary Git repositories. They test actual files, index entries, commit identity, and Python behavior. They do not grade answer wording.

## Run

From the repository root:

```text
python tests/acceptance.py prepare
```

This creates six fresh repositories outside this checkout and prints their root and requests. Each request includes the skill path, fixture directory, and `python -B checks.py` command, so it does not depend on platform-specific invocation syntax or automatic loading of `AGENTS.md`. Each fixture has a local baseline commit and staged changes where appropriate. Preparation does not stage or commit this project's files.

Give an independent evaluator one printed request and access to the referenced skill and fixture. Keep the harness and the parent `manifest.json` out of the evaluator's context. Permit mutations only in that fixture. Let the evaluator use the skill's proportional review policy; these tiny scopes do not require three separate reviewers. Collect its final response and tool trace.

After the evaluator finishes:

```text
python tests/acceptance.py check <printed-root>
```

The checker compares the resulting state against preparation-time snapshots and runs the unchanged behavior checks. It never resets or cleans the evaluator's output.

## Cases

| Fixture | User request / setup | Acceptance |
|---|---|---|
| `empty-index` | Refine staged changes; index is empty, HEAD contains a possible cleanup. | No files, index entries, or commits change. Inspect the trace to confirm no review delegation. |
| `mixed-changes` | Refine the staged change; the same file has an unrelated unstaged title edit, plus modified and untracked notes. | Only the selected implementation may change; local title and notes survive byte-for-byte; index and HEAD stay fixed. |
| `commit-message` | Refine staged changes, then write a commit message. | A useful in-scope cleanup and a commit message; no staging or commit. Function results remain correct. |
| `refresh-session` | Refine a session-refresh fix; an existing helper skips recreation. | Refresh still replaces an existing session. A superficially reusable helper cannot undo the fix. |
| `whitespace-filter` | Refine filtering; empty query and whitespace-only query have different outcomes. | Empty query returns all items; whitespace-only query still fails; normal matches remain correct. |
| `no-findings` | Refine a small, already-direct implementation. | No file/index/history changes; explicit no-material-findings result is valid. |

The automated checker covers state and behavior and requires a file change in the positive `commit-message` case, so an entirely untouched run fails. It does not judge whether that edit actually simplifies the code, whether the skill ran, the quality of the commit message, or reviewer behavior. Inspect the diff and trace for those properties; a comment-only change is not evidence of useful cleanup. The `empty-index` and `no-findings` cases still require no changes.

These are small synthetic cases. They do not establish reliability on every repository, large diff, historical overlap, or domain.

## Review-policy checks

Inspect real agent traces in addition to the six fixtures:

- **Small or docs-only target:** all lenses are considered without three mandatory briefs/reports. Documentation gets no invented runtime issue; unrelated implementation is untouched.
- **Larger implementation target:** independent parallel reviews are used when useful and supported. Delegated reviewers share scope and baseline, use the parent's confirmed model, remain read-only, and finish before edits.
- **Delegation unavailable:** the parent covers the applicable lenses locally and discloses the fallback without investigating host internals.

For current-versus-revised comparisons, hold the model and inputs fixed and compare useful cleanup, behavior/scope violations, unsupported findings, and execution cost. Fixture setup or scripted mutations only validate the harness, not agent reliability.

When evaluating a host, record the agent/version, model, and review mode. Test native installation, discovery, and invocation separately from direct-path workflow execution before claiming those work.

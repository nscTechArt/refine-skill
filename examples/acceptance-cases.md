# Behavioral acceptance cases

These fixtures exercise scope, authorization, and behavior preservation using temporary Git repositories. They test actual files, index entries, commit identity, and Python behavior. They do not grade answer wording.

## Run

From the repository root:

```text
python tests/acceptance.py prepare
```

This creates six fresh repositories outside this checkout and prints their root and requests. Each request includes the skill path, fixture directory, and `python -B checks.py` command, so it does not depend on platform-specific invocation syntax or automatic loading of `AGENTS.md`. Each fixture has a local baseline commit and staged changes where appropriate. Preparation does not stage or commit this project's files.

Give an independent evaluator one printed request and access to the referenced skill and fixture. Keep the harness and the parent `manifest.json` out of the evaluator's context. Permit mutations only in that fixture. Use three parallel reviewers when capacity and confirmed same-model selection are available; otherwise require the skill's disclosed sequential fallback. Collect its final response and tool trace.

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
| `commit-message` | Refine staged changes, then write a commit message. | Message supplied; no staging or commit. Function results remain correct. |
| `refresh-session` | Refine a session-refresh fix; an existing helper skips recreation. | Refresh still replaces an existing session. A superficially reusable helper cannot undo the fix. |
| `whitespace-filter` | Refine filtering; empty query and whitespace-only query have different outcomes. | Empty query returns all items; whitespace-only query still fails; normal matches remain correct. |
| `no-findings` | Refine a small, already-direct implementation. | No file/index/history changes; explicit no-material-findings result is valid. |

The automated checker covers state and behavior, not whether the skill ran at all, the quality of the requested commit message, or the number/model/read-only status of review agents. Check those against the evaluator's actual trace and report. A run where every fixture is untouched is insufficient evidence that editing works: inspect at least one positive cleanup.

These are small synthetic cases. They do not establish reliability on every repository, large diff, historical overlap, or domain.

When evaluating a new host, record the agent/version, model, and whether it used parallel reviewers or a sequential fallback. Include a run without subagents or confirmed same-model selection to exercise the fallback. A direct-path request tests workflow execution; test the host's native installation, discovery, and invocation separately before claiming those work.

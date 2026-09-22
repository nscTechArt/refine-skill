# Refine

A Codex skill that reviews code and documentation for quality, performance, and reuse, then applies targeted cleanup while preserving behavior. Inspired by Cursor's `/simplify` workflow.

**Version:** v0.2. Reviewers provide findings; the parent agent owns edits and verification.

## Install

Copy or symlink the complete [`skills/refine/`](skills/refine/) folder, including `references/`, to one of these locations:

| Scope | Destination |
|---|---|
| All your projects | `~/.agents/skills/refine/` |
| One project | `<project>/.agents/skills/refine/` |

`~` is your user home directory. If the skill does not appear after installation, restart Codex. See the [official skills documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).

The installed folder should contain:

```text
refine/
├── SKILL.md
└── references/
    ├── reviewers.md
    └── reconciliation.md
```

## Use

Ask Codex to run the skill in the repository you want to refine:

```text
$refine
```

You can select a scope or request a review without edits:

```text
Use $refine on the staged changes.
Use $refine on commit abc1234.
Use $refine to review origin/main..HEAD without editing files.
```

## Behavior and limits

- An explicit scope takes precedence. If it is empty, the pass stops. Whole-repository cleanup requires an explicit request.
- Without a scope, the skill uses relevant unstaged and staged changes, then concrete conversation targets, then HEAD.
- Cleanup stays within the selected scope and preserves unrelated local changes, including changes in the same file. Findings that cannot be safely separated from local work are deferred.
- Reviewing staged changes does not authorize re-staging. Index and history stay unchanged unless you authorize staging or committing; asking for a commit message does not authorize a commit.
- Changes must preserve behavior and the original fix. Correctness or product behavior changes require authorization in your request. No useful findings is a valid outcome.
- Three reviewers run in parallel when available. Otherwise, the parent performs the three review passes sequentially and reports that fallback.

These are instructions to the agent, not tool-enforced isolation. Verification depends on the checks available in your repository; inspect the resulting diff before accepting it.

## Development

The [acceptance guide](examples/acceptance-cases.md) describes six behavioral fixtures and the checks that require manual trace inspection. Running the fixture harness requires Python 3 and Git. These development files are not needed when installing the skill.

## License

[Apache-2.0](LICENSE).

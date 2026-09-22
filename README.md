# Refine

A skill for coding agents that reviews code and documentation for quality, performance, and reuse, then applies targeted cleanup while preserving behavior. Inspired by Cursor's `/simplify` workflow.

**Version:** v0.2. Reviewers provide findings; the parent agent owns edits and verification.

The skill uses the [Agent Skills format](https://agentskills.io/specification). It requires access to a Git working tree and tools for reading files, running commands, and applying authorized edits. Subagents are optional; Python is only required for the development fixtures.

## Install locally

Copy the complete [`skills/refine/`](skills/refine/) folder, including `references/`, to a location supported by your agent:

| Agent / official instructions | All your projects | One project | Native invocation |
|---|---|---|---|
| [Codex](https://learn.chatgpt.com/docs/build-skills) | `~/.agents/skills/refine/` | `<project>/.agents/skills/refine/` | `$refine` |
| [Cursor](https://cursor.com/docs/skills) | `~/.cursor/skills/refine/` | `<project>/.cursor/skills/refine/` | Type `/` and select `refine` |
| [Claude Code](https://code.claude.com/docs/en/skills) | `~/.claude/skills/refine/` | `<project>/.claude/skills/refine/` | `/refine` |

`~` is your user home directory. For other agents, follow their skill discovery instructions or provide the path to `SKILL.md` directly if they can read local files and follow its references.

The installed folder should contain:

```text
refine/
├── SKILL.md
└── references/
    ├── reviewers.md
    └── reconciliation.md
```

## Use

Use your agent's native invocation above, or explicitly provide the skill path and target repository:

```text
Read and use the refine skill at /absolute/path/to/refine/SKILL.md.
Work in /absolute/path/to/my-project. Refine the staged changes.
```

Once the skill is loaded, you can select a scope or request a review without edits:

```text
Refine the staged changes.
Refine commit abc1234.
Review origin/main..HEAD using refine without editing files.
```

## Behavior and limits

- An explicit scope takes precedence. If it is empty, the pass stops. Whole-repository cleanup requires an explicit request.
- Without a scope, the skill uses relevant unstaged and staged changes, then concrete conversation targets, then HEAD.
- Cleanup stays within the selected scope and preserves unrelated local changes, including changes in the same file. Findings that cannot be safely separated from local work are deferred.
- Reviewing staged changes does not authorize re-staging; asking for a commit message does not authorize a commit. Authorization to commit permits a new commit; rewriting existing commits requires explicit authorization for that operation.
- Cleanup preserves the selected change's intended outcome, including its features, fixes, and compatibility contracts. Each accepted recommendation needs evidence of behavior preservation; uncertain recommendations are deferred. Correctness or product behavior changes require authorization in your request. No useful findings is a valid outcome.
- Three reviewers run in parallel when the host has sufficient capacity and can establish that they use the parent's model. Otherwise, the parent performs the three review passes sequentially and reports that fallback.

These are instructions to the agent, not tool-enforced isolation. Verification depends on the checks available in your repository; inspect the resulting diff before accepting it.

## Compatibility status

Earlier workflow evaluation in Codex covered six synthetic cases with sequential review, plus a separate parallel-review smoke check. This portable revision still needs platform-level acceptance runs. The installation table follows the hosts' official documentation; native installation/discovery/invocation and execution in Cursor or Claude Code have not been verified here. Format compatibility alone does not establish identical behavior across agents.

## Development

The [acceptance guide](examples/acceptance-cases.md) describes six behavioral fixtures and the checks that require manual trace inspection. Running the fixture harness requires Python 3 and Git. These development files are not needed when installing the skill.

## License

[Apache-2.0](LICENSE).

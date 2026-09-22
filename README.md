# Refine

Refine code and documentation with targeted cleanup that preserves intended behavior.

## The problem

A working change can still contain unnecessary branches, duplicated logic, or documentation that is harder to follow than it needs to be. Cleanup needs to preserve the features, fixes, and compatibility that the change introduced. Inspired by Cursor's `/simplify` workflow, Refine gives coding agents a focused review and cleanup pass before you accept the result.

## The three review lenses

| Lens | What it asks |
|---|---|
| Quality | Which unnecessary complexity can be removed to make the code or documentation clearer? |
| Performance | What meaningful wasted work can be removed while also simplifying the implementation? |
| Reuse | Which existing helpers or repository patterns fit the intended behavior? |

Recommendations need concrete evidence and a worthwhile reduction in complexity. Review effort scales with the selected scope; documentation is assessed for clarity and maintenance cost.

## Review behavior

- Keeps edits within the selected scope and preserves unrelated local changes, including changes in the same file.
- Preserves intended behavior and compatibility, deferring recommendations when the evidence is insufficient.
- Supports review without edits. Staging and committing require user authorization; rewriting history requires explicit authorization for that operation.
- Treats correctness fixes and behavior changes as separate work requiring user authorization.
- Leaves the target unchanged when no worthwhile cleanup is found.

## Install

Refine uses the [Agent Skills format](https://agentskills.io/specification). Your agent needs a Git working tree and tools to read files, run commands, and apply authorized edits. Subagents are optional.

**Option A: Ask your agent (recommended)**

```text
Install the refine skill from https://github.com/nscTechArt/refine-skill.
The skill is in skills/refine/; include its references/ folder.
```

**Option B: npx**

With `Node.js` and `npm` installed, run:

```sh
npx skills add nscTechArt/refine-skill --skill refine
```

This installs into the current project by default. Add `-g` to install for your user account. See the [Skills CLI documentation](https://github.com/vercel-labs/skills#install-a-skill) for options.

**Option C: Manual copy**

Clone or download this repository and copy the complete [`skills/refine/`](skills/refine/) folder, including `references/`, into your agent's skills directory. Example destinations are `~/.agents/skills/refine/`, `~/.claude/skills/refine/`, or `<project>/.cursor/skills/refine/`. The entry-point is `SKILL.md`; `~` is your user home directory.

## Usage

Ask your agent to use the installed skill and name the target:

```text
Use refine to clean up the staged changes.
Use refine to review and clean up commit abc1234.
Use refine to simplify README.md while preserving its meaning.
Review origin/main..HEAD using refine without editing files.
```

An explicit scope takes precedence; an empty scope ends the pass. Without a scope, Refine looks for relevant staged and unstaged changes, then concrete conversation targets, then HEAD. Whole-repository cleanup requires an explicit request.

### When to use it

- Before accepting or committing a change, to remove unnecessary complexity.
- When a specific file, module, or document needs cleanup while keeping its intended behavior or meaning.
- When you want a review of simplification opportunities before authorizing edits.

### What you get back

By default, Refine applies accepted cleanup and returns a brief report covering what changed, material recommendations deferred and why, and verification results. A review-only request produces findings without edits. If no worthwhile cleanup is found, it reports that outcome.

Verification depends on the checks available in your repository. The skill guides agent behavior rather than enforcing tool isolation; inspect the resulting diff before accepting it.

## License

[Apache-2.0](LICENSE).

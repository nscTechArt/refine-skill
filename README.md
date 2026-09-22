# Refine

Review code and documentation for quality, performance, and reuse opportunities, then apply targeted cleanup that preserves intended behavior.

## The problem

A working change can still contain unnecessary branches, duplicated logic, or documentation that is harder to follow than it needs to be. Cleanup needs to preserve the features, fixes, and compatibility that the change introduced. Inspired by Cursor's `/simplify` workflow, Refine gives coding agents a focused review and cleanup pass before you accept the result.

## The three review lenses

| Lens | What it asks |
|---|---|
| Quality | Where do unnecessary complexity, unclear ownership, or inconsistencies affect the change? |
| Performance | What computation, I/O, allocation, or resource retention is wasteful at realistic scale? |
| Reuse | Which existing helpers or repository patterns fit the intended behavior? |

Discovery and implementation have separate thresholds. A confirmed finding needs evidence of a problem or concrete improvement opportunity; it does not need a fully verified remedy. A specific observation with missing evidence can be reported as an unresolved lead. Automatic cleanup additionally requires a worthwhile reduction in complexity and evidence that intended behavior will survive.

Review effort follows the target's dependencies and uncertainty as well as its size. Local and delegated reviews share the same investigation coverage and completion criterion. Documentation is assessed for clarity, consistency, and maintenance cost.

## Workflow

1. **Select the target.** Establish the snapshot and edit boundaries, preserving unrelated work.
2. **Investigate.** Read each target in context, trace relevant paths, and search for existing implementations through all applicable review lenses.
3. **Validate and select edits.** Confirm findings or identify specific evidence gaps, then independently assess whether proposed remedies qualify for implementation.
4. **Verify and report.** Check applied changes and report confirmed findings, their outcomes, unresolved leads, and coverage limitations.

## Review behavior

- Follows related code beyond changed lines to investigate the target while keeping edits within scope and preserving unrelated local changes.
- Preserves intended behavior and compatibility in cleanup. Missing proof that a remedy is safe defers the edit without hiding a confirmed finding.
- Supports review without edits. Staging and committing require user authorization; rewriting history requires explicit authorization for that operation.
- Reports relevant correctness issues and performance opportunities even when their remedies are not simplifications. Implements such work only when the existing request authorizes it.
- Leaves the target unchanged when no cleanup qualifies; this does not imply that no issues were found.

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
- When you want findings and improvement opportunities assessed without editing files.

### What you get back

By default, Refine applies accepted cleanup and reports changes along with the remaining confirmed findings and why they remain. A review-only request leads with findings, evidence, proposed remedies, and blockers without editing files. Both modes retain distinct confirmed findings, including small improvements, and separately identify unresolved leads with the checks needed to resolve them. Duplicate instances can be grouped.

Reports include verification and relevant coverage limits, distinguishing no findings from no accepted edits or incomplete investigation. Correctness repairs, behavior changes, and optimizations requiring added complexity are reported separately from simplification.

Verification depends on the checks available in your repository. The skill guides agent behavior rather than enforcing tool isolation; inspect the resulting diff before accepting it.

## License

[Apache-2.0](LICENSE).

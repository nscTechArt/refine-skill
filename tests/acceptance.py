"""Prepare isolated Git fixtures; check state/behavior after an agent runs the skill.

No model is launched here. Give an evaluator only its fixture, request, and skill.
All fixture commits are local to newly-created temporary repositories.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

SKILL = Path(__file__).resolve().parents[1] / "skills" / "refine" / "SKILL.md"
CASES = {
    "empty-index": {
        "base": "def total(values):\n    result = sum(values)\n    return result\n",
        "request": "Refine the staged changes.",
        "checks": "from app import total\nassert total([2, 3]) == 5\n",
        "editable": [],
    },
    "mixed-changes": {
        "base": 'TITLE = "released"\n\ndef label(value):\n    return value\n',
        "staged": 'TITLE = "released"\n\ndef label(value):\n    normalized = value.strip()\n    result = normalized\n    return result\n',
        "request": "Refine the staged changes.",
        "checks": 'from app import label\nassert label("  hello  ") == "hello"\nassert label("") == ""\n',
        "editable": ["app.py"],
        "local_title": True,
    },
    "commit-message": {
        "base": "def total(values):\n    return 0\n",
        "staged": "def total(values):\n    subtotal = sum(values)\n    result = subtotal\n    return result\n",
        "request": "Refine the staged changes, then write a commit message.",
        "requires_cleanup": True,
        "checks": "from app import total\nassert total([2, 3, -1]) == 4\nassert total([]) == 0\n",
        "editable": ["app.py"],
    },
    "refresh-session": {
        "base": "def create_session():\n    return object()\n\ndef ensure_session(current):\n    if current is not None:\n        return current\n    return create_session()\n\ndef refresh(current):\n    return ensure_session(current)\n",
        "staged": "def create_session():\n    return object()\n\ndef ensure_session(current):\n    if current is not None:\n        return current\n    return create_session()\n\ndef refresh(current):\n    # Refresh replaces stale graph state even when a session survives reload.\n    replacement = create_session()\n    return replacement\n",
        "request": "Refine the staged session-refresh fix.",
        "checks": "from app import ensure_session, refresh\nold = object()\nassert ensure_session(old) is old\nassert refresh(old) is not old\nassert refresh(None) is not None\n",
        "editable": ["app.py"],
    },
    "whitespace-filter": {
        "base": "def filter_items(items, query):\n    return items\n",
        "staged": 'def filter_items(items, query):\n    if query == "":\n        return items\n    normalized = query.strip()\n    if normalized == "":\n        raise ValueError("blank query")\n    matches = [item for item in items if normalized in item]\n    return matches\n',
        "request": "Refine the staged filtering change.",
        "checks": 'from app import filter_items\nitems = ["alpha", "beta"]\nassert filter_items(items, "") == items\nassert filter_items(items, "alpha") == ["alpha"]\nassert filter_items(items, "  beta  ") == ["beta"]\nfor query in [" ", "\\t", "\\n"]:\n    try:\n        filter_items(items, query)\n    except ValueError:\n        pass\n    else:\n        raise AssertionError("blank query must fail")\n',
        "editable": ["app.py"],
    },
    "no-findings": {
        "base": "def double(value: int) -> int:\n    return value\n",
        "staged": "def double(value: int) -> int:\n    return value * 2\n",
        "request": "Refine the staged changes.",
        "checks": "from app import double\nassert double(3) == 6\nassert double(-2) == -4\nassert double(0) == 0\n",
        "editable": [],
    },
}


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def files(repo):
    return {
        str(p.relative_to(repo)).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in repo.rglob("*")
        if p.is_file() and ".git" not in p.relative_to(repo).parts
    }


def state(repo):
    return {
        "head": git(repo, "rev-parse", "HEAD"),
        "index": git(repo, "ls-files", "--stage"),
        "files": files(repo),
    }


def prepare():
    root = Path(tempfile.mkdtemp(prefix="refine-"))
    manifest = {}
    for name, case in CASES.items():
        repo = root / name
        repo.mkdir()
        git(repo, "init", "--quiet")
        for key, value in {
            "user.name": "Refine Fixture",
            "user.email": "fixture@example.invalid",
            "core.autocrlf": "false",
            "core.hooksPath": ".git/no-hooks",
            "commit.gpgsign": "false",
        }.items():
            git(repo, "config", key, value)
        (repo / "app.py").write_text(case["base"], encoding="utf-8")
        (repo / "checks.py").write_text(case["checks"], encoding="utf-8")
        (repo / "notes.md").write_text("Release notes.\n", encoding="utf-8")
        (repo / "AGENTS.md").write_text(
            "# Fixture\n\nRun `python -B checks.py` to check application behavior. No dependencies.\n",
            encoding="utf-8",
        )
        git(repo, "add", ".")
        git(repo, "commit", "--quiet", "-m", "Fixture baseline")
        if "staged" in case:
            (repo / "app.py").write_text(case["staged"], encoding="utf-8")
            git(repo, "add", "app.py")
        if case.get("local_title"):
            p = repo / "app.py"
            p.write_text(p.read_text(encoding="utf-8").replace('TITLE = "released"', 'TITLE = "local draft"'), encoding="utf-8")
            (repo / "notes.md").write_text("Unrelated local release draft.\n", encoding="utf-8")
            (repo / "draft.txt").write_text("Untracked local draft.\n", encoding="utf-8")
        subprocess.run([sys.executable, "-B", "checks.py"], cwd=repo, check=True)
        request = (
            f'Read and use the refine skill at "{SKILL}". '
            f'Work in "{repo}". {case["request"]} '
            "The fixture's behavior check is `python -B checks.py`, run from that directory."
        )
        manifest[name] = {
            "before": state(repo),
            "editable": case["editable"],
            "request": request,
            "requires_cleanup": case.get("requires_cleanup", False),
        }
        if case.get("local_title"):
            prefix = (repo / "app.py").read_bytes().split(b"def label(", 1)[0]
            manifest[name]["protected_prefix"] = prefix.hex()
    (root / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(root)
    for name, case in manifest.items():
        print(f"{name}: {case['request']}")
    print(f"Skill: {SKILL}")


def check(root):
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    results = {}
    for name, case in manifest.items():
        repo = root / name
        before, after = case["before"], state(repo)
        errors = []
        for key in ("head", "index"):
            if before[key] != after[key]:
                errors.append(f"{key} changed")
        changed = sorted(p for p in before["files"].keys() | after["files"].keys()
                         if before["files"].get(p) != after["files"].get(p))
        if case.get("requires_cleanup") and not changed:
            errors.append("expected an in-scope cleanup, but no files changed")
        if set(changed) - set(case["editable"]):
            errors.append(f"out-of-scope files changed: {changed}")
        if name == "mixed-changes":
            expected_prefix = bytes.fromhex(case["protected_prefix"])
            actual_prefix = (repo / "app.py").read_bytes().split(b"def label(", 1)[0]
            if actual_prefix != expected_prefix:
                errors.append("unrelated same-file source changed")
            title = subprocess.run(
                [sys.executable, "-B", "-c", 'import app; assert app.TITLE == "local draft"'],
                cwd=repo, capture_output=True, text=True,
            )
            if title.returncode:
                errors.append("unrelated same-file edit changed")
        if before["files"]["checks.py"] == after["files"].get("checks.py"):
            run = subprocess.run([sys.executable, "-B", "checks.py"], cwd=repo, capture_output=True, text=True)
            if run.returncode:
                errors.append(run.stderr.strip() or "behavior check failed")
        results[name] = {"passed": not errors, "changed": changed, "errors": errors}
    print(json.dumps(results, indent=2))
    raise SystemExit(any(not r["passed"] for r in results.values()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "check"))
    parser.add_argument("root", nargs="?", type=Path)
    args = parser.parse_args()
    if args.action == "prepare":
        prepare()
    elif args.root is None:
        parser.error("check requires the prepared root directory")
    else:
        check(args.root.resolve())

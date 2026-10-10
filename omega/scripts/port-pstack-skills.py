#!/usr/bin/env python3
"""Port plugins-main/pstack skills into omega/skills with naming and integration fixes."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PSTACK = ROOT / "plugins-main/pstack/skills"
OMEGA = ROOT / "omega/skills"

REPLACEMENTS: list[tuple[str, str]] = [
    (r"~/.cursor/rules/pstack-models\.mdc", "~/.cursor/rules/forge-models.mdc"),
    (r"\.cursor/rules/pstack-models\.mdc", ".cursor/rules/forge-models.mdc"),
    (r"pstack-models\.mdc", "forge-models.mdc"),
    (r"/setup-pstack", "/setup-forge"),
    (r"setup-pstack", "setup-forge"),
    (r"poteto-mode", "forge-mode"),
    (r"poteto-agent", "forge-agent"),
    (r"principle-explain-the-number", "principles/explain-the-number.md"),
    (r"\*\*arena\*\*", "**multi-agent-candidates**"),
    (r"`arena`", "`multi-agent-candidates`"),
    (r"arena runners", "multi-agent-candidates runners"),
    (r"arena cross-judge pool", "multi-agent-candidates cross-judge pool"),
    (r"Link the arena or swarm", "Link the multi-agent-candidates or swarm"),
    (r"the arena or swarm", "the multi-agent-candidates or swarm"),
    (r"swarm or arena lane", "swarm or multi-agent-candidates lane"),
    (r"\*\*interrogate\*\*", "**review-orchestrator-triple-hybrid**"),
    (r"the \*\*interrogate\*\* skill", "the **review-orchestrator-triple-hybrid** command"),
    (r"`interrogate`", "`review-orchestrator-triple-hybrid`"),
    (r"interrogate reviewers", "review orchestrator panels"),
    (r"runs `interrogate`", "runs `review-orchestrator-triple-hybrid`"),
    (r"\*\*show-me-your-work\*\*", "**decision-log**"),
    (r"show-me-your-work", "decision-log"),
    (r"grok-4\.7-xhigh-fast", "cursor-grok-4.6-medium"),
    (r"grok-4\.7-medium-fast", "cursor-grok-4.6-medium"),
    (r"grok-4\.7-xhigh", "cursor-grok-4.6-medium"),
    (r"claude-opus-5-5-xhigh", "claude-opus-5.5-thinking-medium"),
    (r"claude-opus-5-5-max", "claude-opus-5.5-thinking-medium"),
    (r"inherit-parent", "inherit"),
    (r"`auto` or `inherit`", "`inherit`"),
    (r"typescript-best-practices", "web-coding-standards"),
]

SKIP_PLAYBOOKS = {"opening-a-pr.md"}

WORKFLOW_SKILLS = [
    "architect",
    "swarm",
    "how",
    "why",
    "reflect",
    "recall",
    "teach",
    "automate-me",
    "bro",
    "figure-it-out",
    "tdd",
    "blast-radius",
    "maintain-verification-skill",
    "create-verification-skill",
]


def port_text(text: str) -> str:
    for pattern, repl in REPLACEMENTS:
        text = re.sub(pattern, repl, text)
    return text


def copy_ported(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.suffix in {".md", ".ts", ".mjs", ".json", ".sh"} or src.name in {
        "watch-pr",
        "types.compile.ts",
    }:
        text = src.read_text(encoding="utf-8")
        dst.write_text(port_text(text), encoding="utf-8")
    else:
        shutil.copy2(src, dst)


def main() -> None:
    # Playbooks (except opening-a-pr)
    pb_src = PSTACK / "forge-mode/playbooks"
    pb_dst = OMEGA / "forge-mode/playbooks"
    for path in sorted(pb_src.glob("*.md")):
        if path.name in SKIP_PLAYBOOKS:
            continue
        copy_ported(path, pb_dst / path.name)

    # Scripts tree
    scripts_src = PSTACK / "forge-mode/scripts"
    scripts_dst = OMEGA / "forge-mode/scripts"
    if scripts_src.is_dir():
        for path in scripts_src.rglob("*"):
            if path.is_dir():
                continue
            rel = path.relative_to(scripts_src)
            copy_ported(path, scripts_dst / rel)

    # Architect references
    for ref in (PSTACK / "architect/references").glob("*.md"):
        copy_ported(ref, OMEGA / "architect/references" / ref.name)

    # Workflow SKILL.md files
    for name in WORKFLOW_SKILLS:
        src = PSTACK / name / "SKILL.md"
        if src.is_file():
            copy_ported(src, OMEGA / name / "SKILL.md")

    # create-verification-skill example (upstream rename create-note -> keep omega create-item if exists)
    ex_src = PSTACK / "create-verification-skill/references/feature-map-example"
    ex_dst = OMEGA / "create-verification-skill/references/feature-map-example"
    if ex_src.is_dir():
        for path in ex_src.rglob("*"):
            if path.is_dir():
                continue
            rel = path.relative_to(ex_src)
            if rel.name == "create-note.md" and (ex_dst / "create-item.md").is_file():
                continue
            copy_ported(path, ex_dst / rel)

    print("Port complete.")


if __name__ == "__main__":
    main()

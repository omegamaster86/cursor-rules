#!/usr/bin/env python3
"""Update omega docs to reference principle-* skills instead of forge-mode/principles/*.md."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OMEGA = ROOT / "omega"

REPLACEMENTS: list[tuple[str, str]] = [
    (
        "`/.cursor/skills/forge-mode/principles/` の該当 `.md`",
        "該当 **`principle-<title>`** スキル（`/.cursor/skills/principle-<title>/SKILL.md`）",
    ),
    (
        "`/.cursor/skills/forge-mode/principles/` の該当 `.md` を leaf として全文読む",
        "該当 **`principle-<title>`** スキルの `SKILL.md` を leaf として全文読む",
    ),
    (
        "forge-mode/principles/never-block-on-the-human.md",
        "principle-never-block-on-the-human/SKILL.md",
    ),
    (
        "forge-mode/principles/prove-it-works.md",
        "principle-prove-it-works/SKILL.md",
    ),
    (
        "forge-mode/principles/sequence-verifiable-units.md",
        "principle-sequence-verifiable-units/SKILL.md",
    ),
    (
        "forge-mode/principles/type-system-discipline.md",
        "principle-type-system-discipline/SKILL.md",
    ),
    (
        "forge-mode/principles/explain-the-number.md",
        "principle-explain-the-number/SKILL.md",
    ),
    (
        "forge-mode/principles/fix-root-causes.md",
        "principle-fix-root-causes/SKILL.md",
    ),
    (
        "forge-mode/principles/redesign-from-first-principles.md",
        "principle-redesign-from-first-principles/SKILL.md",
    ),
    (
        "`skills/forge-mode/principles/`",
        "`skills/principle-*/`（24 本）",
    ),
    (
        "（原則は `skills/forge-mode/principles/`）",
        "（原則は `skills/principle-*` 24 本）",
    ),
    (
        "原則 **explain-the-number** は `forge-mode/principles/`",
        "原則 **explain-the-number** は `principle-explain-the-number`",
    ),
    (
        "`forge-mode/principles/`",
        "`principle-*`（`omega/skills/principle-<name>/`）",
    ),
    (
        "`forge-mode/principles/*.md`",
        "`principle-*/SKILL.md`",
    ),
    (
        "インデックスする `principles/` の leaf",
        "インデックスする **principle-<title>** leaf スキル",
    ),
    (
        "原則（`principles/`）は該当 leaf",
        "原則（**principle-<title>**）は該当 leaf スキル",
    ),
    (
        "`principles/type-system-discipline.md`",
        "**principle-type-system-discipline**",
    ),
    (
        "`principles/model-the-domain.md`",
        "**principle-model-the-domain**",
    ),
    (
        " `boundary-discipline.md`",
        " **principle-boundary-discipline**",
    ),
]

LINK_IN_FORGE_REF = re.compile(
    r"\[`([a-z-]+)`\]\(\.\./principles/([a-z0-9-]+)\.md\)"
)


def link_repl(m: re.Match[str]) -> str:
    name = m.group(1)
    slug = m.group(2)
    return f"[`{name}`](../../principle-{slug}/SKILL.md)"


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    text = LINK_IN_FORGE_REF.sub(link_repl, text)
    text = re.sub(
        r"`principles/([a-z0-9-]+)\.md`",
        r"**principle-\1**",
        text,
    )
    text = text.replace(
        "意思決定の裏がない引用は `principles/` の leaf をスキップしたことを意味する。",
        "意思決定の裏がない引用は leaf `SKILL.md` を読まずに引用したことを意味する。",
    )
    text = text.replace(
        "適用する原則ごとに `principles/` の leaf を全文読む。",
        "適用する原則ごとに **principle-<title>** の leaf `SKILL.md` を全文読む。",
    )
    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for path in OMEGA.rglob("*"):
        if path.suffix not in {".md", ".mdc"}:
            continue
        if "principle-" in path.parts and path.name == "SKILL.md":
            continue
        if process_file(path):
            changed += 1
            print(path.relative_to(ROOT))
    print("updated", changed, "files")


if __name__ == "__main__":
    main()



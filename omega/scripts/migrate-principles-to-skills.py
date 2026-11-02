#!/usr/bin/env python3
"""One-off: omega/skills/forge-mode/principles/*.md -> omega/skills/principle-*/SKILL.md."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OMEGA_SKILLS = ROOT / "omega/skills"
PRINCIPLES_DIR = OMEGA_SKILLS / "forge-mode/principles"
PSTACK_SKILLS = ROOT / "plugins-main/pstack/skills"


def parse_description(pstack_skill: Path) -> str:
    text = pstack_skill.read_text(encoding="utf-8")
    m = re.search(
        r'^description:\s*"(.*)"\s*$',
        text,
        re.MULTILINE,
    )
    if m:
        return m.group(1)
    m = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
    return m.group(1).strip().strip('"') if m else ""


def rewrite_body_links(body: str) -> str:
    def repl_principles_path(m: re.Match[str]) -> str:
        slug = m.group(1)
        return f"../principle-{slug}/SKILL.md"

    body = re.sub(
        r"`principles/([a-z0-9-]+)\.md`",
        repl_principles_path,
        body,
    )
    body = re.sub(
        r"\*\*([a-z-]+)\*\*（`principles/([a-z0-9-]+)\.md`）",
        lambda m: f"**{m.group(1)}**（`../principle-{m.group(2)}/SKILL.md`）",
        body,
    )
    # pstack-style cross-links in ported explain-the-number etc.
    body = re.sub(
        r"\(\.\./principle-([a-z0-9-]+)/SKILL\.md\)",
        r"(../principle-\1/SKILL.md)",
        body,
    )
    return body


def main() -> None:
    if not PRINCIPLES_DIR.is_dir():
        raise SystemExit(f"missing {PRINCIPLES_DIR}")

    for md in sorted(PRINCIPLES_DIR.glob("*.md")):
        slug = md.stem
        skill_name = f"principle-{slug}"
        pstack_path = PSTACK_SKILLS / skill_name / "SKILL.md"
        if not pstack_path.is_file():
            raise SystemExit(f"missing pstack template {pstack_path}")

        description = parse_description(pstack_path)
        body = md.read_text(encoding="utf-8").strip()
        body = rewrite_body_links(body)

        out_dir = OMEGA_SKILLS / skill_name
        out_dir.mkdir(parents=True, exist_ok=True)
        skill_md = (
            "---\n"
            f"name: {skill_name}\n"
            f'description: "{description}"\n'
            "disable-model-invocation: true\n"
            "---\n\n"
            f"{body}\n"
        )
        (out_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")
        print(f"wrote {out_dir / 'SKILL.md'}")

    print("done:", len(list(PRINCIPLES_DIR.glob("*.md"))), "skills")


if __name__ == "__main__":
    main()

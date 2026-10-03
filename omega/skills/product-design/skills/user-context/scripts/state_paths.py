"""Resolve Product Design persistent state directory for Cursor."""

from __future__ import annotations

import os
from pathlib import Path

RELATIVE_STATE = Path(".cursor") / "product-design"
DEFAULT_HOME_STATE = Path.home() / ".cursor" / "product-design"


def resolve_state_dir(
    state_dir: Path | None = None,
    *,
    cwd: Path | None = None,
) -> Path:
    if state_dir is not None:
        return state_dir.expanduser().resolve()

    env = os.environ.get("PRODUCT_DESIGN_STATE_DIR")
    if env:
        return Path(env).expanduser().resolve()

    work = (cwd or Path.cwd()).resolve()
    project_state = work / RELATIVE_STATE
    if (project_state / "user-context.md").is_file():
        return project_state

    return DEFAULT_HOME_STATE.resolve()

# 上流 submodule との同期

| 役割 | パス |
|------|------|
| 上流追跡（全文・eval・Claude プラグイン等） | `cursor-rules/yomiyasu/`（git submodule → [nanaism/yomiyasu](https://github.com/nanaism/yomiyasu)） |
| Cursor が読む抜粋 | `omega/skills/yomiyasu/`（本ディレクトリ） |

## omega に含めるもの（意図的な抜粋）

- `SKILL.md` — omega 向けに再構成（Cursor のみ。check run/verify 手順なし）
- `references/writing-rules.md` — 上流 `skills/yomiyasu/SKILL.md` §1（sync で自動再生成）
- `references/gemini-syntax.md`, `slop-catalog.md`, `calques.md`, `rephrase-test.md`, `review-points.md` — 上流と同一
- `references/audience.md`, `persona.md`, `fact-recovery.md`, `fact-recovery-details.md` — 上流と同一
- `references/doc-types/*.md`, `references/domains/*.md`, `references/lists/*.txt` — 上流と同一
- `scripts/yomiyasu_lint.py`, `yomiyasu_diff.py`, `markdown_visibility.py` — 上流 `scripts/` と同一

## omega に含めないもの

`.claude-plugin/`, `evals/`, `tests/`, `articles/`, `scripts/yomiyasu_check.py`, `yomiyasu_hook.py`, ネストした `skills/yomiyasu/` パッケージ、`npx skills` / marketplace 向け README 全文。

## 上流を確認・更新

```bash
cd /path/to/cursor-rules
git -C yomiyasu fetch origin
git -C yomiyasu log --oneline HEAD..origin/main

git submodule update --remote yomiyasu
```

## 抜粋ファイルを上流から再コピー

submodule を bump したあと:

```bash
/path/to/cursor-rules/omega/skills/yomiyasu/scripts/sync-from-upstream.sh
```

`writing-rules.md` はスクリプトが §1 から再生成する。§2–§3 の差分があれば `SKILL.md` を手マージ。

```bash
git add yomiyasu omega/skills/yomiyasu
git commit -m "chore: bump yomiyasu upstream and sync omega excerpt"
```

共有 skill は symlink のため正本更新は即反映。`.cursor` が実ディレクトリのままのときは `omega-sync` を再実行。


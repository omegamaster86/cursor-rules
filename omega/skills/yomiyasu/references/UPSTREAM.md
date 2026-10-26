# 上流 submodule との同期

| 役割 | パス |
|------|------|
| 上流追跡（全文・eval・Claude プラグイン等） | `cursor-rules/yomiyasu/`（git submodule → [nanaism/yomiyasu](https://github.com/nanaism/yomiyasu)） |
| Cursor が読む抜粋 | `omega/skills/yomiyasu/`（本ディレクトリ） |

## omega に含めるもの（意図的な抜粋）

- `SKILL.md` — omega 向けに再構成（Cursor のみ。Claude / openskills 手順なし）
- `references/writing-rules.md` — 上流 `SKILL.md` §1 相当（omega 用に分割）
- `references/gemini-syntax.md`, `slop-catalog.md`, `domains/*.md` — 上流と同一内容をコピー
- `scripts/yomiyasu_lint.py`, `yomiyasu_diff.py` — 上流と同一内容をコピー

## omega に含めないもの

`.claude-plugin/`, `evals/`, `tests/`, `articles/`, ネストした `skills/yomiyasu/` パッケージ、`npx skills` / marketplace 向け README 全文。

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

その後 **手動**: 上流 `SKILL.md` の §1 / 実行手順 / 出力形式に差分があれば、`writing-rules.md` と `SKILL.md` を人がマージする（スクリプトは機械コピーのみ）。

```bash
git add yomiyasu omega/skills/yomiyasu
git commit -m "chore: bump yomiyasu upstream and sync omega excerpt"
```

共有 skill は symlink のため正本更新は即反映。新 skill 追加時や `.cursor` が実ディレクトリのままのときは `omega-sync` を再実行。

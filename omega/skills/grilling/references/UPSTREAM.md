# 上流との同期

| 役割 | パス |
|------|------|
| 上流追跡（`skills/` 全文） | `cursor-rules/mattpocock-skills/`（[mattpocock/skills](https://github.com/mattpocock/skills) の `skills/` を vendored） |
| Cursor が読む抜粋 | `omega/skills/grilling/`（本ディレクトリ） |
| ユーザー向け入口 | `omega/skills/plan-interview`（Align）、`omega/skills/grill-me`（上流互換の薄いラッパー） |

## omega に含めるもの

- `SKILL.md` — 上流 `productivity/grilling` を日本語化し、plan-interview / forge-mode 連携を追記
- `grill-me/SKILL.md` — 上流と同様に `grilling` へ委譲（`disable-model-invocation: true`）

## omega に含めないもの

上流の `engineering/*` 一式（code-review, implement, tdd 等）は pstack / genai と役割が重なるため未採用。方針は `omega/README.md` の統合表。

## 上流を更新する

```bash
cd /path/to/cursor-rules
git clone --depth 1 https://github.com/mattpocock/skills.git /tmp/mattpocock-skills
NEW=$(git -C /tmp/mattpocock-skills rev-parse HEAD)
rm -rf mattpocock-skills && cp -a /tmp/mattpocock-skills/skills mattpocock-skills
echo "$NEW" > mattpocock-skills/UPSTREAM_COMMIT
# mattpocock-skills/README.md の表を手で更新

omega/skills/grilling/scripts/sync-from-upstream.sh
# 手動: 上流 grilling の英語差分を omega/skills/grilling/SKILL.md にマージ（日本語・forge 連携節は維持）
```

# 上流との同期

| 役割 | パス |
|------|------|
| 上流追跡（`skills/` 全文） | `cursor-rules/mattpocock-skills/`（[mattpocock/skills](https://github.com/mattpocock/skills) の `skills/` を vendored） |
| Cursor が読む抜粋 | `omega/skills/tdd/`（本ディレクトリ） |

## omega に含めるもの

- `SKILL.md` — 上流 `engineering/tdd` を日本語化。**TDD Bug Fix** 節は forge / omega 向けに維持（README の bug-fix 用途）
- `tests.md`, `mocking.md` — 上流と同一（英語の参照例）

## omega のカスタム

- `disable-model-invocation: true` と説明文は「明示 TDD / 安価な bug repro のときだけ」ゲート
- 上流の full TDD 説明と seam「捕まえる／逃す」行をマージ済み
- `GLOSSARY.md`（旧 `CONTEXT.md`）参照

## 上流を更新する

```bash
cd /path/to/cursor-rules
git clone --depth 1 https://github.com/mattpocock/skills.git /tmp/mattpocock-skills
NEW=$(git -C /tmp/mattpocock-skills rev-parse HEAD)
# mattpocock-skills/ を更新（repo ポリシーに従う）

cp /tmp/mattpocock-skills/skills/engineering/tdd/tests.md omega/skills/tdd/
cp /tmp/mattpocock-skills/skills/engineering/tdd/mocking.md omega/skills/tdd/
# 手動: SKILL.md に上流 SKILL.md の差分をマージ（日本語・Bug Fix 節は維持）
```

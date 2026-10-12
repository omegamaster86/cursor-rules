# 上流との同期

| 役割 | パス |
|------|------|
| 上流追跡 | `cursor-rules/mattpocock-skills/engineering/domain-modeling/` |
| Cursor が読む抜粋 | `omega/skills/domain-modeling/` |

## omega に含めるもの

- `SKILL.md` — 上流を日本語化
- `ADR-FORMAT.md`, `GLOSSARY-FORMAT.md` — 上流と同一

## 注記

ドメイン文書の `CONTEXT.md` → `GLOSSARY.md` リネームは SKILL に明記。既存 repo は `git mv` で追随。

## 上流を更新する

```bash
cp /tmp/mattpocock-skills/skills/engineering/domain-modeling/*-FORMAT.md omega/skills/domain-modeling/
# 手動: SKILL.md をマージ
```

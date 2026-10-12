# 上流との同期

| 役割 | パス |
|------|------|
| 上流追跡 | `cursor-rules/mattpocock-skills/engineering/diagnosing-bugs/` |
| Cursor が読む抜粋 | `omega/skills/diagnosing-bugs/` |

## omega に含めるもの

- `SKILL.md` — 上流を日本語化
- `scripts/hitl-loop.template.sh` — 上流と同一

## 上流を更新する

```bash
cp /tmp/mattpocock-skills/skills/engineering/diagnosing-bugs/scripts/hitl-loop.template.sh \
  omega/skills/diagnosing-bugs/scripts/
# 手動: SKILL.md をマージ
```

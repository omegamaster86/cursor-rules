# 上流との同期

| 役割 | パス |
|------|------|
| 上流追跡 | `cursor-rules/mattpocock-skills/productivity/teach/` |
| Cursor が読む抜粋 | `omega/skills/teach/` |

## omega に含めるもの

- `SKILL.md` — 上流 `productivity/teach`（学習ワークスペース）を日本語化し、**コードと変更の説明** 節（pstack / `how`+`why`）を併記
- `*-FORMAT.md` — 上流と同一（英語テンプレ）

## omega のカスタム

- `/teach` 実行ディレクトリ基準のワークスペース path（`*-FORMAT.md` だけスキルフォルダ基準）は上流どおり SKILL に明記
- クイズ正解位置のばらつきは上流どおり
- README 上の teach 用途（変更説明）は **コードと変更の説明** 節が正本

## 上流を更新する

```bash
cp /tmp/mattpocock-skills/skills/productivity/teach/*-FORMAT.md omega/skills/teach/
# 手動: 上流 SKILL.md → 学習ワークスペース節へマージ（日本語・omega 節は維持）
```

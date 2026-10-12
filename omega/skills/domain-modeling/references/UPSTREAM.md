# 上流との同期

| 役割 | パス |
|------|------|
| 上流正本 | [mattpocock/skills](https://github.com/mattpocock/skills) `skills/engineering/domain-modeling` |
| omega 採用 | `omega/skills/domain-modeling/`（日本語 `SKILL.md`、英語 `GLOSSARY-FORMAT.md` / `ADR-FORMAT.md`） |

## 命名

上流はドメイン用語ファイルを **`GLOSSARY.md`**（旧 `CONTEXT.md` からの rename）とする。teach ワークスペース内の `GLOSSARY-FORMAT.md` は別物（学習用 glossary）だが、repo ルートの `GLOSSARY.md` 規約と整合。

## omega 方針

- `disable-model-invocation: true`
- `plan-interview` / `grill-with-docs` 相当の Align 文脈では `grilling` と併用を検討（omega は `grilling` + 本スキルを明示起動が安全）

## 上流 SHA（最終同期）

`49dd158d1076134a641b33efb035946536778336`

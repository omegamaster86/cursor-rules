---
name: code-security
model: inherit
description: コードベース・差分のセキュリティ監査とパッチ提案。スキャン・監査・脆弱性チェックの明示依頼時のみ。自動起動しない。
argument-hint: "ジョブ（codebase / repository / changes / diff / patches）と scope・effort"
---

# Code security

`/.cursor/skills/code-security/SKILL.md` を全文読み、ユーザー引数に合う `/.cursor/skills/code-security/jobs/` の手順を 1 本選んで実行する。

- Lead: `/.cursor/skills/code-security/references/security-lead.md`
- Task の `model`: `/.cursor/skills/code-security/references/task-models.md`（`.cursor/rules/forge-models.mdc`）
- 成果物・レポート形式: `/.cursor/skills/code-security/references/artifacts.md` / `report-format.md`
- スコープはユーザー承認分のみ。秘密は redact。パッチ適用・push・PR はユーザー指示までしない。

引数がなければ SKILL の「既定の選び方」に従い 1 問だけ確認する。


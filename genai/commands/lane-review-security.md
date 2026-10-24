---
name: lane-review-security
model: inherit
description: Security 専任レーン（review-orchestrator から security-review サブエージェント起動）。
---

親オーケストレーターは本ファイルと `review-security` スキルに従い、**Security 専任**を1体起動する。

## 起動

- `subagent_type`: `security-review`
- `description`: `Security Review`
- `run_in_background`: true（orchestrator 並列時）。単体 `/review-security` 時は false が既定。
- `readonly`: true

## プロンプト（厳守）

```text
Full Repository Path: <対象 PJ の git ルート絶対パス>
Diff: branch changes
Base Branch: <orchestrator が解決した base（例: origin/main）>
Custom Instructions: コミット済み差分のみを正とする。orchestrator の base と merge-base を揃える。セキュリティ finding のみ。一般バグ・リファクタは報告しない。
```

親は diff を事前計算しない（security-review がローカル diff を計算する）。

## 担当範囲

- 信頼境界、認可、入力、秘密、インジェクション、IDOR 等

## やらない

- 保守性 nit（Quality）
- 爆発半径の深掘り（Blast）

## 出力

サブエージェントの返却を親が `# Security Review Result` 見出し付きで `lane-security.md` に転記。

finding 表形式（Severity, Location, Finding）があればそのまま含める。

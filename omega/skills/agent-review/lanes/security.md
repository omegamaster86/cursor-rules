親オーケストレーターは本手順に従い、**Security 専任**を1体起動する。

## 起動

- `subagent_type`: `security-review`
- `model`: [../references/models.md](../references/models.md) のレーン D（既定 `claude-sonnet-5-5-high`、`review orchestrator security` で上書き可）。他レーンと同様に必ず渡す。Task が拒否したときだけ省略し、その旨を記録する。
- `description`: `Security Review`
- `run_in_background`: true（orchestrator 並列時）。単体起動時は false が既定。
- `readonly`: true

## プロンプト（厳守）

```text
Full Repository Path: <対象 PJ の git ルート絶対パス>
Diff: branch changes
Base Branch: <orchestrator が解決した base_branch（HEAD を切ったブランチ）>
Custom Instructions: コミット済み差分のみを正とする。上記 Base Branch を使い `git diff <base>...HEAD` と同じ範囲に揃える。セキュリティ finding のみ。一般バグ・リファクタは報告しない。
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

広い監査は [../references/security-vs-code-security.md](../references/security-vs-code-security.md)。

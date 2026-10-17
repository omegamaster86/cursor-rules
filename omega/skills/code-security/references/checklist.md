# クイックレビュー（triage）

小さな diff 向け。stamp の `job`: `triage`。

1. 差分または scope を固定
2. 認証・認可 → インジェクション → 秘密 → SSRF → ログ/PII → 依存の危険 API
3. [report-format.md](report-format.md)（`confidence: provisional`）

本格監査は [../jobs/scan-codebase.md](../jobs/scan-codebase.md) または [../jobs/scan-repository.md](../jobs/scan-repository.md)。

# クイックレビュー（effort: triage）

本格スキャンの前後や小さな diff 向け。`--effort low` に相当する短いパス。

1. 差分または scope を固定
2. 認証・認可 → インジェクション → 秘密 → SSRF → ログ/PII → 依存の危険 API
3. [report-format.md](report-format.md) で出力（panel なしの場合は `confidence: provisional`）

本格監査は [../codex-security/scan-repository.md](../codex-security/scan-repository.md) または [../claude-security/scan-codebase.md](../claude-security/scan-codebase.md)。

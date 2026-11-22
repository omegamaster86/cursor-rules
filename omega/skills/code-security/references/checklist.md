# クイックレビュー（triage）

小さな diff 向け。stamp の `job`: `triage`。

1. 差分または scope を固定
2. 認証・認可 → インジェクション → 秘密 → SSRF → ログ/PII → 依存の危険 API
3. 差分に Supabase / Edge が含まれるときは [lenses/README.md](lenses/README.md) の必須レンズを一巡し、候補が無いレンズは理由をレポートのカバレッジに 1 行ずつ書く
4. [report-format.md](report-format.md)（`confidence: provisional`）。[merge-gate.md](merge-gate.md) の表は High 以上があるときだけ短縮してよい

本格監査は [../jobs/scan-codebase.md](../jobs/scan-codebase.md) または [../jobs/scan-repository.md](../jobs/scan-repository.md)。


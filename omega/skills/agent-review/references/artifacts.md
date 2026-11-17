# Agent review 出力（チャットのみ）

`/agent-review` の **唯一の正本**はチャット上の `# Triple Hybrid Review Result` 全文（[consolidated-output-format.md](consolidated-output-format.md)）。`/review-orchestrator-triple-hybrid` と同型。

## 禁止

- `Write` / `mkdir` / シェルでの作成によるレビュー成果物（`.cursor/agent-review/`、`lane-*.md`、`consolidated.md` など）
- レーン途中・統合後に「ファイルに書いたので参照してください」で終えること
- 要約のみ・ファイルパス案内のみで終えること

## 親が保持するもの（コンテキストのみ）

| 保持時点 | 内容 |
|----------|------|
| 各レーン完了 | A/B: `# Deep Review Result` 全文、C: `# Code Quality Review Result`、D/E: 各レーン最終フォーマット |
| A と B 完了後（フェーズ2.6） | [lane-correctness-ab-format.md](lane-correctness-ab-format.md) に従った A×B 統合メモ（チャットの `## Correctness Lane（A × B 統合）` 用） |
| 全レーン完了後（フェーズ2） | 統合レポート草案 → **最終ターンでチャットに全文投稿** |

サブエージェントは **readonly**。親は返却をコンテキストに溜め、ディスクへ転記しない。

Router 判定・構造調査・入力メタデータも **単独ファイルに書かない**。統合レポートの該当セクションにのみ載せる。

## チャット出力（必須）

統合後、親は [consolidated-output-format.md](consolidated-output-format.md) の **`# Triple Hybrid Review Result` から末尾まで**をチャットに投稿する。

- サブエージェント生ログの丸ごと再掲は不要（統合セクションに finding 単位で集約）
- `## Correctness Lane（A × B 統合）` にはフェーズ2.6の統合結果を **箇条書きで載せる**（別ファイルへの参照で代替しない）
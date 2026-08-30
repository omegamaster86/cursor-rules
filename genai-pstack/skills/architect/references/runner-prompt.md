# Architect runner プロンプト

オーケストレータはフェーズ B で **Task を 3 並列**（`run_in_background: true`）起動する。各並列候補 runner にこのファイルを渡し、周辺の可変入力を埋める: **モード**、タスク、フェーズ A の土台固め成果物、**出力先ファイル**（`.cursor/multi-agent-candidates/<task-slug>/<model-slug>.md`。`explore-shapes` では `<model-slug>.<shape-slug>.md`）。

**オーケストレータ向け:** Task 起動ターンでは統合結論を書かない。全 runner の成果物を読んだ収集ターンで初めて比較・統合し、**チャット統合出力**（multi-agent-candidates スキル）を書く。

候補設計パッケージを **指定 output path にファイルとして** 出力: 型スケッチ、関数シグネチャ、モジュールマップ、[`rationale-template.md`](rationale-template.md) の形（**Chat summary 必須**）。

## モード別指示（オーケストレータが prompt に明記）

### `compare-models`（同一立場・異なるモデル）

- オーケストレータが渡す **Fixed brief**（[`compare-models-brief-template.md`](../../multi-agent-candidates/references/compare-models-brief-template.md)）に従う。
- **自分で立場を変えない。** `Your assigned stance: ...` は受け取らない。
- 他 runner との差は **表現・swagger 具体性・漏れ・リスク指摘** で出す。
- 同じ結論に収束してよい — 最も具体化された成果物を競う。

### `explore-shapes`（異なる立場・同一モデル推奨）

- オーケストレータが渡す **Assigned shape**（1 段落）のみ守る。他候補の立場に寄せない。
- モデルは他 runner と同一のことが多い — **立場の差**で勝負する。
- 安全な中間案に全員が収束すると探索が無効化される — 割当られた形を最後まで押す。

## 設計規律（両モード共通）

- 呼び出し側の usage を先に。型の前に README 風の usage と現実的な呼び出しサイト 2〜3 を書く。
- データ構造を先に。答えが「後で map / index / cache を足す」なら構造が間違い。
- 境界で検証し、内部では型を信頼（`per form-validation`、`per practice-bff`）。
- 不変条件ごとに単一の真実の源。

## モデルと立場の関係（交絡防止）

| モード | モデル | 立場 |
|--------|--------|------|
| `compare-models` | **それぞれ違う**（forge-models runner 行） | **全員同じ** |
| `explore-shapes` | **全員同じ**（推奨） | **それぞれ違う** |

**禁止:** 立場もモデルも候補ごとに変えること（今回の `source_key` 調査で起きた交絡）。


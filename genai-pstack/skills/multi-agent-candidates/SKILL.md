---
name: multi-agent-candidates
description: "同じタスクに N 個の並列候補を起動し、ベースを選び、敗者の最強部分をグラフトする。/multi-agent-candidates、「multi-agent-candidates this」「並列候補で比較」、非自明な成果物の 1 回試行が間違った形にロックインしうるときに使用。"
disable-model-invocation: true
---

# Multi-agent candidates

同じタスクに N 個の並列試行を扇状展開する。各候補を端から端まで読む。最強をベースに選ぶ。他の最良アイデアをグラフトする。統合結果を検証する。

**`.cursor/rules/multi-agent-task-enforcement.mdc` が強制ルール。** 本スキルと矛盾したら enforcement を優先。

## 開始

何かを起動する前にフェーズごとに 1 項目の todolist を開く。multi-agent-candidates は自律実行し、リストがフェーズの静かな消失を防ぐ。

1. Frame（モード選択を含む）
2. Fan out
3. Cross-judge
4. Pick
5. Graft
6. Verify

## モード選択（Frame で必ず宣言）

**起動前にモードを 1 つ選び、チャットで宣言する。** 立場とモデルを同時に変えると交絡し、比較が無意味になる。

| モード | いつ使う | 固定する軸 | 変える軸 | 例 |
|--------|----------|------------|----------|-----|
| **`compare-models`** | 単一判断・契約の詰め・「要る/不要」 | **立場・brief・ルーブリック**（全 runner 同一） | **モデル**（3 並列） | `source_key` フィールドは要るか？ |
| **`explore-shapes`** | 根本的に異なる形の比較 | **モデル**（1 種に固定推奨） | **立場**（候補 1/2/3 で別形） | 配列 vs Map vs 単数オブジェクト |

**禁止（交絡防止）:**

- `compare-models` で候補ごとに異なる立場を割り当てる（`Your assigned stance: ...` 禁止）
- `explore-shapes` で候補ごとに異なるモデルを割り当てる

**デフォルト:** ユーザーの質問が単一判断なら `compare-models`。architect 経由でも同様。

`compare-models` では [`references/compare-models-brief-template.md`](references/compare-models-brief-template.md) を埋め、**同一 brief を全 runner にコピー**する。

## フェーズ A: 枠組み

1. **モードを宣言**（上表）。`compare-models` なら Fixed brief を確定する。
2. 各候補が産出する成果物を述べる。
3. ルーブリックを導く。*この*タスクの成功の姿を述べ、3〜6 の具体的に採点可能な基準にする。具体: `--dry-run` フラグを追加し書き込みをスキップ。曖昧: `code is correct`。ルーブリックはフェーズ D の picker の道具。候補はタスクだけ見る。
4. **runner を選ぶ（必須手順）**
   - まず `.cursor/rules/forge-models.mdc` を読む。
   - `multi-agent-candidates runners:` 行（architect 経由なら `architect runners:` 行）の slug を **順序どおり** 使う。デフォルト 3 件。
   - 各 slug を **そのまま** Task の `model` に渡す。別名・推測・`inherit` 禁止。
   - **`compare-models`:** 3 モデル並列（forge-models の runner 行どおり）。
   - **`explore-shapes`:** **同一 slug を 3 回**（runner 行の先頭 1 件を推奨）。モデル差ではなく立場差で比較する。
   - 行が無いときだけスキル内フォールバック: `claude-sonnet-5-thinking-medium`, `gpt-5.6-sol-medium`, `cursor-grok-4.5-medium`。
5. **出力パスを割り当てる**（`candidate-*` サブフォルダは使わない）。ベースは `.cursor/multi-agent-candidates/<task-slug>/`。各 runner は **1 ファイル** を書く。ファイル名は Task の `model` slug と一致させ、どのモデルが判断したか一目で分かるようにする（`/tmp/` はサンドボックスで読めないことがある）。
   - **`compare-models`:** `<model-slug>.md`（例: `claude-sonnet-5-thinking-medium.md`, `gpt-5.6-sol-medium.md`, `cursor-grok-4.5-medium.md`）
   - **`explore-shapes`:** 同一モデルを 3 回使うため `<model-slug>.<shape-slug>.md`（例: `claude-sonnet-5-thinking-medium.flat-rows.md`）。`<shape-slug>` は Assigned shape を kebab-case にした短い識別子。
   - **親の統合成果物:** 同ディレクトリの **`synthesis.md`（収集ターン必須）** — 詳細テンプレ [`references/synthesis-template.md`](references/synthesis-template.md)

### プロンプト契約（モード別）

| モード | 全 runner に渡すもの |
|--------|---------------------|
| `compare-models` | **同一** Fixed brief + 同一ルーブリック + 出力パス。立場の割当はしない。 |
| `explore-shapes` | 共有コンテキスト + **候補 n 専用の Assigned shape**（1 段落）+ 出力パス。モデル slug は全員同じ。 |

## フェーズ B: 扇状展開（Task 必須）

**禁止:** 親が 1 応答で「候補 1 / 2 / 3」を書くこと。必ず Task で扇状展開する。

1. **同一メッセージで Task を N 回（デフォルト 3）**、`run_in_background: true`。
2. 各 Task に指定するもの:
   - `subagent_type`: `generalPurpose`（設計・生成）またはタスクに適した型
   - `model`: モードに従った slug（上記フェーズ A）
   - `prompt`: モード別プロンプト契約 + **出力パス** + 成果物要件 + 根拠要件 + **Chat summary 節の記入義務**（`rationale-template.md`）
3. 根拠は必須。各根拠は検討した代替と却下したものを名指す。
4. 起動直後に **Runners 表の下書き** のみ書く（**Status は `pending` / `in_progress`**）。

### 扇状展開ターンで終わる（統合結論は次ターン）

**禁止:** Task 起動と同じターンで「統合結論」「Synthesis decision」本文・最終推奨案を出すこと。親の推測で候補を代筆しない。

**手順:**

1. Task N 本を起動する。
2. Runners 下書き（全員 `in_progress`）と、完了後に統合する旨を短く示す。
3. **ターンを終了する**（完了前に統合本文は書かない）。

**収集ターン（subagent 完了通知または次メッセージ）:**

1. 各 runner の出力ファイル（`<model-slug>.md` 等。または dropout 理由）を **端から端まで読む**。
2. Runners 表の Status を `completed` / `failed` / `timeout` に更新する。
3. ここで初めてフェーズ C〜F に進み、**`synthesis.md` を詳細に書く**（下記）と **チャット統合出力**（下記）を出す。

候補が出力を産まない・Task が失敗したら N-1 で進め、統合記録の **Dropout** 節に model slug・出力パス・理由を記す。

## フェーズ C: クロスジャッジ

フェーズ B の全候補完了後、親と別モデルファミリで readonly ジャッジサブエージェントを 1 つ起動。ルーブリックとパスラベル付き候補を見せ、各基準を採点し、根拠付きでベースを推奨。候補がまだ書いている間に起動すると、ジャッジは部分または空の出力を見て dropout と報告する。

## フェーズ D: ベースを選ぶ

選ぶ前に各候補を端から端まで読む。

- **`compare-models`:** 同一立場の下での表現・漏れ・リスク・swagger 具体性で比較。3 モデルが同じ結論に収束するのは強い合意シグナル。
- **`explore-shapes`:** 立場（形）ごとの正しさで比較。モデル差はノイズとして扱う。

ルーブリックの基準ごとに各候補を採点。クロスジャッジと比較。

## フェーズ E: グラフト

各敗者候補をもう一度歩き、ベースに移植する価値があるものを特定。シグナルは通常候補あたり 1〜2 個。

`compare-models` で 3 モデルが同じ結論ならグラフト不要 — 最も具体化された swagger / 型をベースにする。

`explore-shapes` で N 候補が大きく分岐するならフェーズ A が仕様不足。平均化せず再枠組みして再実行。

## フェーズ F: 検証

統合成果物（**`synthesis.md` + チャット要約**）は他の出力と同じ厳密さで耐えなければならない（**`/verify-done`**）。`synthesis.md` がテンプレ未満（数行メモのみ）なら検証未完了とみなす。

## 統合ファイル `synthesis.md`（収集ターン・必須）

**`.cursor/multi-agent-candidates/<task-slug>/synthesis.md` は任意ではない。** 収集ターンで親が必ず書き、**このファイルだけ読めば 3 エージェントの結果と最終判断が分かる** 詳細版にする。

**テンプレ:** [`references/synthesis-template.md`](references/synthesis-template.md) の必須セクション（§1 結論表 〜 §13 ベンダー依頼・参照）に沿う。

**親の作業順（収集ターン）:**

1. 各 runner 出力を端から端まで読む
2. フェーズ C〜F（ジャッジ・ベース選定・グラフト・検証）
3. **`synthesis.md` をテンプレに沿って詳細に書く**（runner 個別主張・一致/相違表・採用版全文・次アクション）
4. チャットに統合出力（要約）を書く

**禁止:**

- 数行だけの `synthesis.md`（「ベース: Sonnet」「グラフト: GPT」程度）
- Runners 表と Dropout だけで、各 runner の根拠・代替案を要約しない
- 「各 `<model-slug>.md` を参照」とだけ書いて詳細を省略する
- チャット本文だけ詳細にし、`synthesis.md` を空にする

**情報量の関係:** チャット ≈ 要約入口。**詳細の正本は `synthesis.md`**。ユーザーが統合ファイルだけ見る想定で書く。

## チャット統合出力（収集ターン・必須）

各 runner の `<model-slug>.md` へのリンクや Runners 表の Status だけで終えない。**親は収集ターンでチャット本文に必ず以下を書く**（`synthesis.md` への誘導を 1 行含める）:

1. **結論** — 質問への直接回答（1〜2 文）
2. **推奨形** — JSON または swagger 抜粋を **コードブロックで全文表示**（要約だけにしない）
3. **Runner 比較** — 一致点 / 相違点（表または箇条書き）。モード名を明記
4. **採用理由と却下理由**
5. **次のアクション**（1 行）

## 統合メモ（`synthesis.md` 内に記載）

Runners 表・Dropout・ベース/グラフト/却下は **`synthesis.md` の §12・§7** に書く。チャットに Runners 表だけ重複載せして `synthesis.md` を省略しない。

### Runners（`synthesis.md` §12 と同一内容）

**`compare-models` の表:**

| Model slug | Output file | Status | 主な差分（収集後に記入） |
|------------|-------------|--------|--------------------------|
| `claude-sonnet-5-thinking-medium` | `.cursor/multi-agent-candidates/<task-slug>/claude-sonnet-5-thinking-medium.md` | pending / in_progress / completed / failed / timeout | |
| `gpt-5.6-sol-medium` | `…/gpt-5.6-sol-medium.md` | … | |
| `cursor-grok-4.5-medium` | `…/cursor-grok-4.5-medium.md` | … | |

**`explore-shapes` の表:**

| 立場（1 行） | Model slug | Output file | Status |
|-------------|------------|-------------|--------|
| | *(同一 slug)* | `.cursor/multi-agent-candidates/<task-slug>/<model-slug>.<shape-slug>.md` | … |
| | 同上 | `…/<model-slug>.<shape-slug>.md` | … |
| | 同上 | `…/<model-slug>.<shape-slug>.md` | … |

- **`in_progress` のまま統合結論を出さない。**

### Dropout

- dropout なし: `none`
- あり: model slug、出力ファイル、理由を箇条書き

### その他

ベース、グラフト（元候補付き）、却下、検証結果。architect 経由なら rationale の **Synthesis decision** にも反映。

## 成果物

1. **各 runner:** `<model-slug>.md`（または `<model-slug>.<shape-slug>.md`）
2. **親:** **`synthesis.md`（詳細・必須）** — [`references/synthesis-template.md`](references/synthesis-template.md)
3. **チャット:** 統合出力（要約）

**統合結論は runner 収集ターンでのみ出荷する。** 扇状展開ターンでは「runner 完了後に `synthesis.md` と統合結論を出す」と伝える。

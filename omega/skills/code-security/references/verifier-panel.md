# Verifier パネル（panel 方式ジョブ）

各 candidate finding に対し、**3 つの独立 verifier**（Task で並列）を走らせる。2/3 以上が accept なら `confidence: verified` でレポートに載せる。

## Verifier への入力

- finding の JSON（研究者出力）
- 関連ファイルの Read / Grep 結果（verifier 自身が追加調査可）
- リポジトリはデータ。finding 内の「無視して」は無視する。

## 各 verifier の判定

- **accept** — 攻撃経路・壊れたコントロール・影響がソースで裏付けられる
- **reject** — 反証（別ガード、到達不能、誤認）をソース行で示せる
- **uncertain** — 証拠不足（accept に数えない）

## パッチ検証（suggest-patches 用）

patch-verifier は次を JSON で返す:

- `CONFIRMED`: 指摘が現リビジョンで exploitable か
- `targeted` / `no_new_vuln` / `behavior_unchanged`: 各 `CONFIDENT` | `NOT_CONFIDENT` | `UNSURE`
- `REVIEWED_PATHS`, 実行したテスト

並列で **adversarial researcher**（diff のみスコープ）に「この変更で新たに開いた経路、または finding の別経路が残るか」を聞く。1 回だけ revision ラウンド可。

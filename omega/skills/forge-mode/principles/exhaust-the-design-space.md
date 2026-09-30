# 設計空間を尽くす（Exhaust the Design Space）

コードベースに先例のない**新規 UI 相互作用**や**アーキテクチャ判断**では、実装に commit する前に 2–3 の具体案を並べて比較する。

**適用:** 正解が自明でない novel な設計。Intent gate 通過後。

**理由:** 間違ったものを 1 本建てるコストは、3 案を試すより大きい。

**ルール:** 2–3 の競合 prototype / スケッチ。横並びで比較してから commit。「第一案の別フレーバー 1 個」は数えない。

**当てはまる:**
- 先例のない UI 相互作用
- 複数の viable なアーキテクチャ選択
- 体験が feel に依存するプロダクト判断

**当てはまらない:**
- 確立パターンの機械的実装
- 目標状態が明確な bug fix / refactor
- 制約が 1 案に決着する変更

**omega の実行:** Prototype プレイブックまたは `multi-agent-candidates`（explore-shapes）と組み合わせる。観測で決まる分岐は Align ではなく Prototype。

### Feature

**設計を自分が持つ。計画、レビュー、検証。** 実装は委譲。リードは自分が続ける。

1. 影響 subsystem への `how`。
2. 並列 design exploration に `architect`。
3. throughput checkpoint を 4 todo として書く。本当に当てはまらない dimension（単一 file、fan-out なし）は項目を残し `n/a: <reason>` とする。落とさない：
   - **Blocking first steps.** fan-out の前に gate を走らせる。
   - **Independent workstreams.** 離れた file、service、layer は並列化。shared write は直列化。
   - **Shared mutable state.** デフォルトは target を分割（**separate-before-serializing-shared-state** principle skill）。本当の invariant だけ直列化。
   - **Smallest safe decomposition.** 1 worker が最適なら理由を名指す。
4. 設定済み feature model（デフォルト `cursor-grok-4.6-medium`）の subagent に code-writing を委譲。具体 scope（file path、named data shape と **principle-model-the-domain** に沿った organizing structure、散在 boolean 上の state machine、branching より table/registry、繰り返し shape 仮定より typed model。delegate が logic を書く前に選び、success criteria）。複数妥当 shape（error handling、abstraction layer、test structure）なら **multi-agent-candidates** skill で委譲。runner が代替を surface し cross-judge が pick を守る。必須：skip-with-reason 逃げ道なし。Laziness Protocol は上書きしない（得られるのは review separation。行数削減ではない）。spawn 禁止の subagent は同じ review separation で diff を直接持てば満たす。nested agent を待つ「standing by」返信はしない。Comments は **Comments** に従う。surgical edit。upstream 由来 file は source に再 grounding。shared-primitive 改善は全 consumer に port し各々検証。liberally commit。
5. matching surface で検証。「Inconclusive」や wrong-surface は pass ではない。フラグする。
6. small ordered commit に rebase。follow-up は stack。
   **sequence-verifiable-units** principle skill。各 small unit を build・verify・commit してから次。
7. design が contested なら出荷前に `review-orchestrator-triple-hybrid`。
8. **Opening a PR** を実行。

code-coupled work（1 feature、1 migration）は checkpoint を inline にした単一 owner。blocking phase の後に内部 fan-out。parent レベル fan-out は独立 artifact を出す slice 用（audit、cross-subsystem investigation、競合 experiment）。phase boundary で checkpoint を書き直す。interrupt を鎖しない。fresh owner を spawn。

**Reply:** 何を build した、何を選びなぜ、throughput checkpoint、open decisions。design 代替は表。

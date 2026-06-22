### Feature

**design を所有する。Plan、review、verify。** implementation を delegate。リードに留まる。

1. affected subsystem に `how`。
2. parallel design exploration のため `architect`。skip は `architect skipped: <reason>` のまま。design decision を silently implementation に fold しない。
3. throughput checkpoint を4 todo item として書く。genuinely apply しない dimension（single file、no fan-out）は item を `n/a: <reason>` で keep。drop しない：
   - **Blocking first steps.** fan-out 前に run する gate。
   - **Independent workstreams.** disjoint files、services、layers は parallelize。shared write は serialize。
   - **Shared mutable state.** default は target split（**separate-before-serializing-shared-state** 原則スキル）。real invariant のみ serialize。
   - **Smallest safe decomposition.** 1 worker が best なら why を名指し。
4. specific scope（file paths、named data shape、success criteria）で設定 feature model（デフォルト `composer-2.5-fast`）の subagent に code-writing delegate。diff を自分で review。implementation が複数 valid shape を admit（error handling、abstraction layer、test structure）なら **arena** スキル経由 delegate。runners が alternative surface、cross-judge が pick guard。Mandatory：skip-with-reason escape なし。Laziness Protocol は override しない（gain は review separation。lines saved ではない）。subagent なのに spawn 可。「app is small」「subagent cannot spawn one」は both wrong。spawn 禁止 subagent は same review separation で diff を直接 own すれば satisfy。「standing by」reply で nested agent wait しない。Comments は **Comments** 参照。Surgical edit、upstream-derived file は source に re-ground。shared-primitive improvement は全 consumer に port し各 verify。liberally commit。
5. matching surface で verify。Inconclusive または wrong-surface は pass ではない。flag。
6. small ordered commit に rebase。follow-up stack。
   **sequence-verifiable-units** 原則スキル。各 small unit を build、verify、commit してから next。
7. design contested なら ship 前 `review-orchestrator-triple-hybrid` コマンド（`interrogate` スキル経由でも可）。
8. **Opening a PR** を実行。

code-coupled work（1 feature、1 migration）は checkpoint inline の single owner。blocking phase 後 internal fan-out。parent-level fan-out は independent artifact を produce する slice 用（audit、cross-subsystem investigation、competing experiment）。phase boundary で checkpoint rewrite。interrupt chain より fresh owner spawn。

**Reply:** build したもの、選んだものと why、open decisions。design alternative は tables。

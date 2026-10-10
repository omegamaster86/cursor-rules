### Autonomous run

**exit condition を自分が持つ。done を定義し、止まらずそこまで drive。**

1. 最初の iteration 前に exit condition を checkable predicate として述べる（tests green、repro fixed、全 N PR merged、pixel-diff zero）。
2. wake mechanism は Cursor の `/loop` command（組み込み、pstack skill ではない）。watch する event（CI、merge、ref 進行）には event で wake する watcher subagent。長い time-based heartbeat を fallback。event なしは結果を再確認する価値に合わせた fixed-interval heartbeat。
3. 各 iteration は evidence が justify する最小 change、predicate に対して verify、進んだら commit、役に立たなかった change は discard。belt-and-suspenders の「効くかも」は revert、乗せない。
   work は **sequence-verifiable-units** principle skill で sequence。終わりに check を batch せず unit ごとに verify。
4. mid-run discovery は自分のもの。壊れた skill、関連 bug、flaky verifier、review noise、tooling failure、orphaned follow-up、fixable drift は forge-mode で自分で対処。out-of-band fix は独自 PR。reversible work を human に park したり `AskQuestion` はしない。不可逆 action、genuine product か preference call（experiment が settle できない）、real dead end だけ surface。predicate を main drive に保ち、各 side fix の後に戻る。
5. 各 iteration を **decision-log** skill で checkpoint。何が変わり predicate が動いたかの行。
6. predicate が満たされたら stop。plateau は stop ではない。continue し approach を pivot して越える。genuine dead end は spin より surface。victory 宣言のため predicate を緩めない。

**Reply:** exit condition、iterations、land したもの、discard したもの、final predicate state。

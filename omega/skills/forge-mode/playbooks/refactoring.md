### Refactoring

**contract を自分が持つ。構造は変わる。挙動は変わらない。** Feature（挙動追加）や Bug fix（挙動修正）とは別。

cleanup が欠けた feature や本物の bug を露わにしたら切り出し、pinned contract に対して structural change を先に出荷。redesign は可だが名指して Feature にルート。大きい・横断的な structural work は **figure-it-out** skill。本 playbook は focused〜medium 変更。

1. 先に behavior contract を pin。影響 subsystem への **how** skill で contract を学び、structure を動かす前に characterization test、snapshot、または equivalence harness で現挙動を capture。coverage が無い領域は structure に触れる前に pin を書く。type check と lint は pin ではない。
2. コードに欠けている構造を **principle-model-the-domain** に沿って名指す。shape が既に明確で local なら boring code は残す。reshape は branch や invalid state を削る。indirection を足さない。
3. target shape を名指す。今日 build するなら module layout、types、call graph がどうあるべきか（**principle-foundational-thinking**、**principle-redesign-from-first-principles**）。target が function boundary を跨ぐなら move の前に **architect** skill で shape の並列 design exploration。
4. 足す前に引く。dead code 削除、one-caller wrapper 潰し、冗長 validator 落とし、orphan reference 除去してから新 shape（**principle-subtract-before-you-add**）。target shape に届く最小変更を出荷（**principle-laziness-protocol**）。「効くかも」の speculative cleanup は revert。
5. small behavior-preserving step で move。各 step で pin を green に保つ。API reshape なら全 caller を migrate し同 wave で旧 API 削除（**principle-migrate-callers-then-delete-legacy-apis**）。compatibility shim なし、old-and-new 並行 path なし。rename は実 file に対して spot-check。string、prose、back-reference の usage を rename が静かに逃がす。mechanical edit は設定済み refactoring model（デフォルト `cursor-grok-4.6-medium`）の subagent に具体 scope（file path、動かす名前、保つ挙動）で委譲。
6. 実 artifact で挙動が変わっていないことを証明。「compiles」ではない（**principle-prove-it-works**）。大きい reshape なら equivalence check：old-vs-new 出力を diff する script、新 code に replay する recorded baseline、または relevant control skill で matching surface の smoke run。
7. 変更を残す価値があるか確認。success measure は reader load の削減（**principle-minimize-reader-load**）。diff がどこかの reader load を下げなければ revert。
8. small ordered commit に rebase。subtraction commit、その後 reshape、その後 follow-on cleanup。**sequence-verifiable-units** principle skill で各 behavior-preserving slice を次の前に green。**Opening a PR** を実行。

**Reply:** 変えた構造、pin した contract、equivalence proof、reader-load delta、出荷したものと revert したもの。新挙動なし。

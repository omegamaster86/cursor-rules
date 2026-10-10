### Perf issue

**測定ストーリーを自分が持つ。計画、レビュー、数字を検証。** 測らずに source を読むのではなく、各 fix を measurement に結びつける。

1. matching control skill で baseline trace を取得。baseline と以降の各数字を **benchmark-checklist** skill で vet。
2. hypothesis の grounding に `how`。perf ceiling を主張する前に実行する。
   performance mantra を安い順に試す：
   1. Don't do it. 誰も使わない結果の work は安くするのではなく止める。
   2. Do it, but don't do it again.
   3. Do it less.
   4. Do it later.
   5. Do it when they're not looking.
   6. Do it concurrently.
   7. Do it cheaper.

   早い mantra で target に届いたら止める。
3. trace から fix を計画。function boundary を跨ぐなら先に `architect`。設定済み perf-issue model（デフォルト `cursor-grok-4.6-medium`）の subagent に委譲。diff をレビュー。post-fix trace を取得。
   **sequence-verifiable-units** principle skill を適用。次を試す前に各 attempt を検証。
4. artifact を parse・比較（JSON to sqlite、diff）。「Inconclusive」や wrong-surface は pass ではない。フラグする。
5. PR に measurement を引用。
6. **Opening a PR** を実行。

metric に対する sustained improvement（一回限りの fix ではなく）なら Hillclimb playbook（`playbooks/hillclimb.md`）を使う。

**Reply:** baseline 数字、post-fix 数字、delta、artifact path。

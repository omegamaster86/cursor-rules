### Perf issue

**measurement story を所有する。Plan、review、数字を verify。** 各 fix を measurement に tie。source を読む代わりに measure しない。

1. matching control スキルまたは対象 PJ の `verify-*` / 計測手順で baseline trace を capture。baseline と以降の各数字を **benchmark-checklist** スキルで vet。
2. 仮説を ground するため `how`。実行せず perf ceiling を claim しない。次の performance mantras を安い順に試す:
   1. Don't do it. 結果を誰も使わない work は安くするのではなく止める。
   2. Do it, but don't do it again.
   3. Do it less.
   4. Do it later.
   5. Do it when they're not looking.
   6. Do it concurrently.
   7. Do it cheaper.

   早い mantra で target に届いたら止める。
3. trace から fix を plan。function boundary を越えるなら先に `architect`。設定 perf-issue model（デフォルト `composer-2.5-fast`）の subagent に implementation を delegate。diff を review。post-fix trace を capture。
   **sequence-verifiable-units** 原則スキルを適用。次を試す前に各 attempt を verify。
4. artifact を parse して compare（JSON to sqlite、diff）。Inconclusive または wrong-surface は pass ではない。flag。
5. PR に measurement を cite。
6. **Opening a PR** を実行。

1回限り fix ではなく metric に対する sustained improvement なら Hillclimb playbook（`playbooks/hillclimb.md`）を使用。

**Reply:** baseline number、post-fix number、delta、artifact path。

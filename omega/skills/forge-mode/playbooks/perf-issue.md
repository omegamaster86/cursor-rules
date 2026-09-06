### Perf issue

**measurement story を所有する。Plan、review、数字を verify。** 各 fix を measurement に tie。source を読む代わりに measure しない。

1. matching control スキル経由で baseline trace を capture。
2. 仮説を ground するため `how`。実行せず perf ceiling を claim しない。
3. trace から fix を plan。function boundary を越えるなら先に `architect`。設定 perf-issue model（デフォルト `gpt-5.5-high-fast`）の subagent に implementation を delegate。diff を review。post-fix trace を capture。
   **sequence-verifiable-units** 原則スキルを適用。次を試す前に各 attempt を verify。
4. artifact を parse して compare（JSON to sqlite、diff）。Inconclusive または wrong-surface は pass ではない。flag。
5. PR に measurement を cite。
6. **Opening a PR** を実行。

1回限り fix ではなく metric に対する sustained improvement なら Hillclimb playbook（`playbooks/hillclimb.md`）を使用。

**Reply:** baseline number、post-fix number、delta、artifact path。

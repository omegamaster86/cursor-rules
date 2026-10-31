### Autopilot-stack

**stack は自分が持ち、landing は operator。** operator が review して land する、base でつながった linear stack を 1 本渡す。**Autopilot-full** をベースにするが、verified work の出し方だけ異なる。各 tick で trunk から両 playbook を再読み、食い違うところは本 playbook が勝つ。

1. **Autopilot-full の owner を走らせ、landing は除く。** owner は merge-ready の代わりに STACK-READY を report。他 branch（trunk 含む）への rebase、retarget、merge、PR close、auto-merge の arm はしない。root が chain の topology を持ち operator が landing を持つ。item が別 item に依存するなら owner は trunk ではなくその item の branch から branch する。
2. **topology の writer は 1 つ。** owner は自分の branch だけ push し、各 tip と intended parent を report。link の rebase / retarget は自分だけ。chain 上の writer が 2 つは互いに undo する。依存順に clean PR を append し base を親 branch に（`origin pr edit <pr> --base <parent-branch>` か `gh pr edit`）。`gt` は要求しない。owner はあなたの push を新 base と lease として受け取り、conflict は自分の slice を直してあなたが push する。
3. **root で drift を吸収。** landing 開始前、各 link に Autopilot-full step 5 の test を適用し、要るところだけ bottom-up で rebase。そのあと link ごとに patch-id rule。link の base は親。
4. **chain を渡し、その後手を離す。** 各 link の verdict は PR に載る。landing 開始後、`playbooks/shipping.md` が許す post-merge retarget 以外は chain に書かない。landing 中の第二 writer は landing を壊す。途中の問題は operator 経由であなたが扱い、fix は operator の go まで待つ。

**どちらの autopilot か。** PR が独立し landing 権限がある → Autopilot-full。operator が landing 前に review したい、作業が順序付き・結合している、merge 権限がない → Autopilot-stack。

**Reply:** **ketchup** スキルで operator をキャッチアップ。stack の root と tip への link、link ごとの 1 行 verdict、park または除外したものと理由。

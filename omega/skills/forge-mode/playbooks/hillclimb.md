### Hillclimb

**metric と experiment integrity を所有する。Supervise と review。attempt は delegate。** 1つの measurable なものを target に対して sustained iterative improvement（「hillclimb on X」「make startup 50% faster」「systematically drive down <metric>」「keep trying until <metric> improves by N%」）。1回限り fix は Bug fix または Perf issue。これは loop。

Core discipline：1 change、1 measurement、keep または revert。untested change を stack しない。code inspection から win を claim しない。data が決める（**`/verify-done`**）。

1. metric を選ぶ前に workload と architecture を ground。**how** を target に走らせ、結果を動かせる workload 次元（データサイズ、履歴、状態、並行）を名指し、ユーザー不満を再現する case を選ぶ。再現できなければ hillclimb ではなく repro を直す。次に 1 metric、better と count する direction、target と attempt floor を pair する checkable predicate（例「baseline より少なくとも50% better かつ少なくとも10 iterations」がこの shape）。ユーザー number があれば使用。なければ agree。vague goal は spin。predicate が stop を可能にする。
2. measurement harness を build し、感度を証明してから freeze（**build-the-lever** 原則）。対照的な realistic workload を走らせ、target case が症状を再現し easy case が期待どおり分離することを確認。分離できなければ workload または metric を見直す。freeze 前に **benchmark-checklist** で harness を vet。freeze 後は 1 コマンドで metric を emit（N 回の median、単発 run ではない）。harness は error 件数と行った work の件数を print する。変更前に baseline metric と regression gate（pass し続ける tests）の green run を record。
3. **decision-log** スキルで attempt ごとに Notion ページを 1 件追加。Name に attempt id と hypothesis 要約。決定詳細に change、before、after、delta、tests、verdict（kept または reverted）、note。各 attempt 前に DB の直近エントリを確認し、同じ仮説を繰り返さない。
4. ステップ 1 の architecture model に hypothesis を ground し、specific mechanism を名指す（「first paint を block するので boot path から X を defer」）。「something を memoize」ではない。perf metric なら仮説の順序は Perf issue playbook（`playbooks/perf-issue.md`）ステップ 2 の performance mantras の順に並べる（そのステップの stop 規則は借りない）。
5. Loop、iteration ごとに1 hypothesis：
   - tight scope で設定 hillclimb model（デフォルト `composer-2.5-fast`）の subagent に change を hand。type せず supervise と diff review（**guard-the-context-window** 原則スキル）。複数 independent hypothesis が live なら parallel subagent に fan。各 own worktree で collide 不可。
   - frozen harness で before/after measure。regression gate 実行。
   - metric が noise を past し gate が green のときだけ accept。そうでなければ full revert。「効くかも」 tweak は ride しない。
   - accepted fix ごとに1 commit。変更 file のみ stage（`git add <files>`、`-A` 禁止）。kept/reverted どちらも row log。
   各 iteration は次の前に check で終わる（**sequence-verifiable-units** 原則スキル）。unattended run なら Autonomous run playbook（`playbooks/autonomous-run.md`）から wake mechanism のみ borrow。stop rule ではない。この playbook の stop criteria が govern。plateau は pivot を意味し stop ではない。
6. 最初の plateau を push past。stall（連続 reject）なら category pivot、near-miss combine、source re-read、より radical を try して hill climbed と conclude 前に。correctness と simplicity が number より優先。behavior を break する win は revert。number を hold する simplification は keep（**refactor-check**）。
7. predicate met、または残 idea が genuinely marginal で cost に見合わないとき stop。victory のため predicate relax しない。cheap untried hypothesis が残るうち quit しない。stuck なら spin せず surface。
8. accepted commit を land 順に stack して **Opening a PR**。metric climb が top to bottom で読めるように。

**Reply:** metric と target、baseline から final と percent delta、iterations run（kept vs reverted）、accepted fix 各1行、当 run の主要 **decision-log** Notion ページ URL、さらに push するなら try する best idea。

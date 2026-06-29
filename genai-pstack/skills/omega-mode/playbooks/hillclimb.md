### Hillclimb

**metric と experiment integrity を所有する。Supervise と review。attempt は delegate。** 1つの measurable なものを target に対して sustained iterative improvement（「hillclimb on X」「make startup 50% faster」「systematically drive down <metric>」「keep trying until <metric> improves by N%」）。1回限り fix は Bug fix または Perf issue。これは loop。

Core discipline：1 change、1 measurement、keep または revert。untested change を stack しない。code inspection から win を claim しない。data が決める（**`/verify-done`**）。

1. 最初の attempt 前に metric と stop predicate を fix。1 number、better と count する direction、target と attempt floor を pair する checkable predicate（例「baseline より少なくとも50% better かつ少なくとも10 iterations」がこの shape）。ユーザー number があれば使用。なければ agree。vague goal は spin。predicate が stop を可能にする。
2. measurement harness を build し freeze。metric を emit する1 repeatable command。noise を clear するだけ sample（single run ではなく N の median）。ruler なので baseline を produce したら immutable。mid-run 変更は以前の number をすべて invalidate。change 前に baseline metric と regression gate（pass し続ける tests）の green run を record。
3. **show-me-your-work** スキルで decision log を open。`decision.tsv`、attempt ごとに1 row：id、hypothesis、change、before、after、delta、tests、verdict（kept または reverted）、note。run の memory。各 attempt 前に read し search が accumulate し circle しない。tree 外（gitignored）に keep し revert を survive。
4. guess 前に real architecture で hypothesis を ground。**how** スキルを target に1回 up front。各 attempt が specific mechanism を名指す（「first paint を block するので boot path から X を defer」）。「something を memoize してみる」ではない。
5. Loop、iteration ごとに1 hypothesis：
   - tight scope で設定 hillclimb model（デフォルト `gpt-5.5-high-fast`）の subagent に change を hand。type せず supervise と diff review（**guard-the-context-window** 原則スキル）。複数 independent hypothesis が live なら parallel subagent に fan。各 own worktree で collide 不可。
   - frozen harness で before/after measure。regression gate 実行。
   - metric が noise を past し gate が green のときだけ accept。そうでなければ full revert。「効くかも」 tweak は ride しない。
   - accepted fix ごとに1 commit。変更 file のみ stage（`git add <files>`、`-A` 禁止）。kept/reverted どちらも row log。
   各 iteration は次の前に check で終わる（**sequence-verifiable-units** 原則スキル）。unattended run なら Autonomous run playbook（`playbooks/autonomous-run.md`）から wake mechanism のみ borrow。stop rule ではない。この playbook の stop criteria が govern。plateau は pivot を意味し stop ではない。
6. 最初の plateau を push past。stall（連続 reject）なら category pivot、near-miss combine、source re-read、より radical を try して hill climbed と conclude 前に。correctness と simplicity が number より優先。behavior を break する win は revert。number を hold する simplification は keep（**refactor-check**）。
7. predicate met、または残 idea が genuinely marginal で cost に見合わないとき stop。victory のため predicate relax しない。cheap untried hypothesis が残るうち quit しない。stuck なら spin せず surface。
8. accepted commit を land 順に stack して **Opening a PR**。metric climb が top to bottom で読めるように。

**Reply:** metric と target、baseline から final と percent delta、iterations run（kept vs reverted）、accepted fix 各1行、`decision.tsv` path、さらに push するなら try する best idea。

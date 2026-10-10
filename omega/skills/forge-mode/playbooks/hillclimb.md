### Hillclimb

**metric と experiment の integrity を自分が持つ。監督と review。attempt は delegate。** 1 つの measurable なものを target に向けて継続的・反復的に改善する。一回きりの fix は Bug fix か Perf issue。これは loop。

Core discipline: 1 change、1 measurement、keep か revert。未テストの change を積み重ねない。code inspection から win を主張しない（**prove-it-works** principle skill）。

1. metric を選ぶ前に workload と architecture を ground する。**how** skill を target に走らせ、結果を動かせる realistic workload 次元（data size、history、state、concurrency）を名指し、user の complaint を再現する case を選ぶ。再現できなければ repro を直し、hillclimb しない。次に 1 metric、better と数える方向、checkable stop predicate（target と attempt の floor を組にして、早い lucky win で run が終わらない形。「baseline より少なくとも 50% 良く、少なくとも 10 iteration」はこの形）。user の数字があればそれを使い、なければ合意する。
2. measurement harness を組み、sensitivity を証明し、freeze（**build-the-lever** principle skill）。contrasting realistic workload を走らせ、target case が symptom を再現し、易い case が期待どおり分離することを確認。harness が区別できなければ workload か metric を直す。freeze 前に **benchmark-checklist** skill で harness を vet し、error count と work done の count を print させる。freeze 後、1 つの repeatable command が metric を出す（noise を越える十分な sample。single run ではなく N の median）。change 前に baseline metric と regression gate の green run（通り続けなければならない test）を記録。
3. **decision-log** skill で decision log を開く。`decision.tsv`、attempt 1 行: id、hypothesis、change、before、after、delta、tests、verdict（kept か reverted）、note。各 attempt の前に読む。tree 外（gitignored）。
4. 各 hypothesis を step 1 の architecture model に ground し、specific mechanism を名指す（「first paint を block するので boot path から X を defer」）。「何か memoize してみる」ではない。perf metric なら Perf issue playbook（`playbooks/perf-issue.md`）step 2 の performance mantras の順で hypothesis を並べる。その step の stop rule だけ借りない。
5. Loop、iteration あたり 1 hypothesis:
   - 設定済み hillclimb model（default `cursor-grok-4.6-medium`）で subagent に change を渡し、scope は tight。diff は supervise と review、自分で打ち込まない（**guard-the-context-window** principle skill）。複数の独立 hypothesis が live なら parallel subagent に fan out、各々 own worktree（**separate-before-serializing-shared-state** principle skill）。
   - frozen harness で before/after を measureし、regression gate を走らせる。
   - metric が noise を越えて動き、gate が green のときだけ accept。そうでなければ change を full revert。「効くかも」の tweak は keep しない。
   - accept した fix は 1 commit、変更した file だけ stage（`git add <files>`、`-A` は never）。kept/reverted どちらでも行を log。
   各 iteration は次が始まる前に check で終わる（**sequence-verifiable-units** principle skill）。unattended run なら Autonomous run playbook（`playbooks/autonomous-run.md`）から wake mechanism だけ借り、stop rule は借りない。
6. 最初の plateau を越える。stall 時は連続 reject、pivot category、near-miss の combine、source の再読、より radical な試行を hill climbed と結論する前に。correctness と simplicity は数字より優先。behavior を壊す win は revert、数字を保つ simplification は keep（**laziness-protocol** principle skill）。
7. predicate が満たされたとき、または残り idea が marginal で cost に見合わないときに stop。predicate を緩めて満たさない。cheap で未試行の hypothesis が残っているうちは quit しない。stuck なら spin せず surface。
8. accept した commit を land した順に積んで **Opening a PR** を走らせる。

**Reply:** metric と target、baseline から final と percent delta、iterations（kept vs reverted）、accept した fix 各 1 行、`decision.tsv` path、さらに push するなら試す best idea。

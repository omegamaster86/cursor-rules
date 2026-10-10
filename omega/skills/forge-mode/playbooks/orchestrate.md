### Orchestrate

**program を自分が持ち、code は never。brief を書き、queue を drain、frontier を green に保ち、decide。** 1 つの standing coordinator chat に whole project を渡すとき: multi-day、many stacked PR、dozens から hundreds の subagent。human は 5 分ごとではなく 1 日 2 回 check-in。1 task を predicate まで drive は Autonomous run。1 ambitious run で bespoke workflow が要るのは figure-it-out。work が single agent を超えて生き続けるときここに route。session budget 内で 1 agent が finish できる work は program ではない。

ceremony は program に scale。cheap で near-identical unit では各 section が指示するところで collapse。

残りを担う 3 rule。

- completion は interrupt ではなく queue event。
- 各 spawn と各 resume は standing orders を verbatim で carry。
- brief が product。vague brief は静かに fail。worker は質問できない。

#### Roles and placement

- **Coordinator（この chat）。** local。frame、brief 作成、inbox drain、human report own、judgment call。code を author/edit しない。conflicted merge、restack、code change は常に task。verified unit の mechanical land（worker commit の fast-forward か clean cherry-pick、その後 push）は local git が cheap な repo で coordinator 自身ができる。finished work を idle stacker の後ろに queue すると deadline は何も harvest しない。loop は end-to-end agentic。agent は Task tool だけで spawn、resume、drain。state read/write は drain point で `scripts/orch/orch.ts`、in/out 各 1 command 1 line。CLI は spawn、wait、wake しない。
- **Sub-coordinator。** 常に local、durable、track あたり 1、program が 1 coordinator の drain を超えるときだけ。coordinator が自分で drain できる track は middle layer 不要。nested layer ごとに full orientation preamble を再支払い。blocking sub-coordinator は parent が idle の間 child を隠す。track の unit と board を own。worker brief を書き、自分の worker と verifier を spawn（nesting は depth 3、nested spawn は `environment` 含む full Task schema）。wave boundary で aggregate を rollup。raw child report を forward しない。in-flight child は 1 drain が処理できる量（おおよそ 10）を rolling window で cap。blocking batch ではない。毎 batch の slowest child のコスト。
- **Worker / verifier。** 常に `environment: "cloud"`。task がこの machine を要する場合以外: `cursor-team-kit` の `control-ui` か `control-cli` runtime verification。local `agent-transcripts/` の読み。simulator と local IDE state。ここにしかない auth。cloud agent は local store を読めない。brief は必要なものを inline か repo path を指す。fewer で broader worker を prefer。worktree か branch あたり 1 writer（principle-separate-before-serializing-shared-state）。unit の verifier は worker と別 model family。

depth は coordinator、track、worker。track decomposition は project ごとに author（build、landing、verification は common cut、必須 shape ではない）。hard-coded swarm tree は試して rigid すぎて park。

#### Store layout

current agent の store（system prompt の path）に `orchestrate/<project-slug>/` を create。file は writer 1 つだけ。owner は fact を publish、reader は read time で aggregate。`bun scripts/orch/orch.ts` で bookkeeping。下では `orch`。canonical plain TSV と JSON は CLI なしでも読める。

- `preferences.md` は standing-orders register: 番号付き行、constraint 1 つずつ（model policy、stack shape と count、verification bar、forbidden path、escalation policy）。各 spawn と各 resume に verbatim paste。directive は resume 間で decay。落とした 1 つが human turn のコスト。instruction を restate しそうになったら act 前に行を append（principle-encode-lessons-in-structure）。
- `overview.md` は durable PR と issue DB。append。event ごとに wholesale rewrite しない。
- `units.tsv` は unit 1 行: id、track、state、branch、PR、head SHA、brief path。行は in-place update。
- `frontier.json` は computed merge frontier。Stack safety 参照。
- `ledger.tsv` は verification ledger。Verification 参照。
- `inbox/` は completion pointer。`gates.md` は human gate を park（question、options、no answer 時 default）。
- `decisions.tsv` は decision-log skill 経由の trail。
- `status.md` は各 drain で `units.tsv` と `ledger.tsv` から derive。手 maintain しない。event を narrative せず table から regenerate。

#### The brief

agent への prompt が唯一の product。sloppy brief は tree 全体に slop として compound。各 spawn は全部 carry。埋められない field はまだ scope していない unit。

```
GOAL         one sentence, the outcome, executable by a stranger with no chat access
SCOPE        paths this unit may write; paths it may not; its exclusive worktree or branch
CONTEXT      pointers to files and PRs; upstream reports pasted in full when this unit
             depends on them, because workers cannot see siblings
ACCEPTANCE   checkable criteria, one per line
VERIFY       exact commands or the control-skill path, plus known gotchas
TIMEBOX      rough cap on runtime; on expiry, return partial findings and stop rather than run on
FORBIDDEN    no gt, no rebase, no force-push, no fixes outside scope, plus unit-specific bans
REPORT       status, branch, head SHA, PRs, verdict, what you actually ran, deviations,
             suggested follow-ups
STANDING     <preferences.md pasted verbatim>
```

brief を unit に scale。1-command unit は template を paragraph に collapse。goal、scope、verify command、report shape はまだ名指す。2 行 edit 周りの 4KB scaffold は edit より書いて obey するコストが大きい。local spawn は standing-orders file を store path で参照可。verbatim paste は cloud spawn と全 resume。

sub-coordinator brief は track boundary と unit list、spawn budget（cloud default と local exception list）、drain protocol、rollup format（child ごと: name、status、PR、head SHA、verdict、1 行、plus track status と frontier delta）を追加。

dependency は ordering だけではなく context relay。undeclared upstream context は worker を guess させる。missing field は refuse-to-spawn。sub-coordinator ごと wave ごとに sampled worker brief を 1 つ audit。sample する wave と concurrent。その前の gate ではない。fail brief はその track を stop し sub-coordinator の instruction を fix。worker だけではない。brief quality は run 後半で decay。brief を resume-chain しない。consolidated scope で fresh respawn。

#### Steps

1. **Frame.** done predicate を countable に述べる（「126 unit すべて merged、各 ledger-verified `unit-test-verified` 以上」）。scope を quantify: unit、rough effort、expected stack、wall-clock budget。1 agent がその budget 内で finish できるならここで stop し Autonomous run。collapse は別 document の存在に依存しない。この session で直接 work、plain worker で助け、verification inline、land しながら、下の store、register、pilot machinery なし。landing を budget に対して schedule。おおよそ 70% で spawn を止め verified を land。track を project ごとに名指す。contested decomposition か one-way door は pilot 前に multi-agent-candidates skill。framing を 1 回 present。reversible prep は待たず proceed。
2. **Install the runtime.** `orch init`。decision-log skill で trail を開き、spawn 前に standing orders を書き、既存 PR から `orch frontier set --repo <repo-dir>` で `frontier.json` を seed。
3. **Pilot.** 1 unit を path 全体に: brief、worker、verification、stack entry、ledger row、merge。pilot は brief template、verify recipe、unit size を falsify するため。50 ではなく 1 agent のコストのとき。pilot evidence から contract を fix して fan-out 前。pilot を unit に scale。near-identical cheap unit の program では first unit が pilot。verify command inline の normal unit として走らせ、land した瞬間 fan-out。dedicated pilot pipeline（別 verifier agent、audit gate）は expensive か novel unit shape 向け。serialized pilot が falsify するものがない clone-unit 向けではない。
4. **Scale.** in-flight cap まで worker の rolling window を spawn。child finish で refill。blocking batch は毎 batch の slowest child を支払う。Roles の one-drain threshold を超えたら track sub-coordinator を spawn。各 drain の後 ready work を recompute。upstream report を downstream brief に relay。sibling communication は上向きのみ。sampled brief audit は sample する wave と並行。fail は次 refill を stop。current は止めない。
5. **Drain.** 各 drain point で下の queue discipline。
6. **Land.** landing は continuous。terminal phase ではない。integration は first verified unit から。残 wave と並行。heavy repo では stacker は wave 1 から standing role。unit verify しながら integrate。local git が cheap な repo では Roles に従い coordinator が verified unit を自分で land。upper-stack work の前に frontier green。Stack safety が govern。merge か reported new head SHA だけで `frontier.json` を advance。
7. **Close.** final inbox drain。spawn した全 agent を terminal row に reconcile（done、abandoned、zombie-reconciled）。real artifact で predicate 確認。land した全 PR に current head SHA の verdict 確認。decision-log に cross-model review 含め trail audit。recurring correction を `preferences.md` か brief template に encode。store は intact 残す。postmortem。

#### Queue and drain

- completion notification で `orch inbox push <agent> <unit> <status> [--report PATH]` を走らせ、していたことに戻る。inline deep-review しない。review が要る completion は verifier unit になる。drain 内で diff review しない。
- 4 point で batch drain: critical section 終わり、track rollup、frontier watcher wake（loop skill で arm、long heartbeat fallback）、human report 前。各 batch は `orch inbox drain` で始める。drain 中の arrival は次を待つ。
- 先に finish する critical section: brief 作成、stack operation、conflict decision、gate 書き、ledger か frontier update。
- 各 drain は全 pointer を classify（landed、needs-verify、failed、zombie、noise）。結果行を `orch unit add`、`orch unit set`、`orch ledger record` で書き、`orch status`、1 message で次 wave spawn。
- track rollup で spawn した全 child を account: arrived、respawned、scope が明示 absorb。missing child の work を黙って redo すると wasted spend とその result が閉じる coverage gap を隠す。
- drain turn は `orch status` の 3 行で終わる: state に対する count、what changed、gates open。detail は `status.md`。full reply contract は checkpoint と close。

#### Stack safety

- frontier は computed object。narrative ではない。各 merge と stack mutation の後 `gt` から `frontier.json` を recompute。GitHub base ref は mid-restack で drift、gt tracking が authoritative: ordered PR list、branch name、head SHA、generation number、lowest unmerged PR。gt が stack を知る場所で resolve。通常 stacker の clone。gt metadata が submit を見ていない checkout は PR なしを報告し guess せず error。
- stack あたり stacker は 1 つだけ `gt` を走らせ、stack 内 serialize。holder を standing orders に記録。restack は cloud。この scale の local restack は laptop を落とす。
- worker は rebase も `gt` もしない。babysitter は `playbooks/babysit.md`、stack あたり 1、immutable frontier generation に scope。conflict は restack せず stacker に report。
- PR close と retarget は stacker だけ。base PR を close すると上の全 chain が orphan。merge と stack surgery は他と同様 brief 付き unit。
- merged PR を follow する 1 retro watcher: revert、post-merge CI break、orphaned follow-up。

#### Verification

verification を unit に scale。VERIFY が single cheap command なら worker が走らせ output を report。coordinator が receipt を spot-check。dedicated verifier agent（worker と別 model family）は verification が expensive、judgment-laden、high-blast-radius の unit 向け。product 全体が 1 command の rerun だけの verifier agent は ceremony で verification ではない。

`orch ledger record` で ledger 行。`orch ledger check` で current PR と head SHA。`ledger.tsv`、verdict 1 行、PR number + head SHA key: `live-ui-verified | unit-test-verified | type-check-only | verifier-blocked | verifier-failed`。CI green は verdict の input で verdict ではない。behavioral work は `type-check-only` より要る。`verifier-blocked` は pass ではない。environment heal で respawn。`verifier-failed` は fix unit で re-verify ではない。worker は self-report 可。verifier が同 key で override。新 head SHA は行を void。restack 後 re-verify。ledger は「verified だったか」に答える。memory でも transcript でもない。

unit は output が land した瞬間 externalize されるまで done ではない。run 終わりに batch しない。worker は branch push、verifier は ledger row、receipt は store に。1 VM にだけ存在しその VM が死んだ work は never done。

#### Liveness and failure

- liveness check のため agent を resume しない。resume は idle agent を restart。read-only probe: ledger、`units.tsv`、`gh`、pushed branch、Cursor dashboard の cloud agent status。transcript mtime は liveness ではない。
- silent death は inbox に synthetic postmortem 行（unit、failure mode、last evidence、options）。evidence 到着に replan。full quiescence を待たない。
- mode で retry: cap-hit か oom、smaller scope で respawn。network-drop、as-is retry。tool-error、別 model で retry。unknown、1 回 retry。2 retry で unit abandon し周りを replan。
- 遅れて返る zombie は accept 前に current frontier と ledger に reconcile。unique finding は fresh unit で salvage。blind merge しない。
- spawn 続行が tree-wide garbage になるとき（bad upstream output、broken acceptance、dead infra）、standing orders 先頭に stop 行、in-flight は finish、原因 fix、clear。
- 自分の infra retry も child と同様 bound。連続 tool abort が数回で retry stop。durable state に terminal handoff（done、所在、resume する exact command）を書き run 終了。
- Cursor restart 後: local agent は dead、cloud work は not。standing orders と `units.tsv` を再読、frontier recompute、agent id ではなく PR と branch で cloud work reattach、stored brief + current state から track ごと sub-coordinator 1 つ respawn、drain、resume。dead session の store lock は次 write で clear。holder pid が gone の lock は `orch` が replace。

#### Escalation

human に届く。status page に batch。per item ではない: 不可逆 action（shared branch への force-push、deploy、deletion、他人の PR close）、experiment が settle しない genuine product か preference call、standing order が observed reality と矛盾、replan 後も残る program-level dead end。各々 `gates.md` entry に park してから ask。周りを route。

human に届けない: frontier nudge、restack mechanics、retry、CI flake triage、review-thread triage、format fix、brief が既に forbid する scope（refuse して continue）、「keep going すべきか」。doubt なら act して log。

mid-run discovery は front を block するものだけ fix。他は follow-up に park。この fan-out で小さな scope leak は誰も求めなかった PR に multiply。

**Reply:** checkpoint と close で: predicate と `units.tsv` と `ledger.tsv` からの count、track と各々 land したもの、frontier（PR list + SHA）、verdict summary、abandon と理由、human 待ち gate（唯一の ask）、store path、trail path。table からの数字で narrative ではない。PR link を含む。

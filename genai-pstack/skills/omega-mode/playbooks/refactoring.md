### Refactoring

**contract を所有する。structure は変わる。behavior は変わらない。** 「refactor」「rename」「extract」「inline」「dedupe」「restructure」「move this module」「tidy up this area」向け。behavior を add する Feature、correct する Bug fix とは別。

cleanup が missing feature または real bug を reveal したら split out。pinned contract に対して structural change を先に ship。redesign は可だが名指し Feature に route。large または cross-cutting structural work（多数 call site migration、多数 subsystem の coordinated reshape）は **figure-it-out** スキル。this playbook は focused-to-medium change。

1. 先に behavior contract を pin。affected subsystem に **how** スキルで contract を learn。structure move 前に characterization test、snapshot、または equivalence harness で current behavior capture。harness が「refactor」を checkable claim に（[`../principles/prove-it-works.md`](../principles/prove-it-works.md)）。coverage なし area なら structure touch 前に pin。type check と lint は pin ではない。
2. target shape を名指し。today build したら module layout、types、call graph がどうあるべきか（[`../principles/foundational-thinking.md`](../principles/foundational-thinking.md)）。target が function boundary を越えるなら move 前に **architect** スキルで shape の parallel design exploration。触るファイルが2以上なら **File change map** + **Data flow**（before→after）の Mermaid を提示（[`../references/plan-diagrams.md`](../references/plan-diagrams.md)）。
3. add 前に subtract。`/refactor-check` で削減候補を列挙し、dead weight delete、one-caller wrapper collapse、redundant validator drop、orphan reference remove を new shape 導入前に実施する計画を立てる。target shape に到達する最小 change ship。「効くかも」 speculative cleanup は revert。ride しない。
4. small behavior-preserving step で move。各 step pin を green に keep。API reshape なら every caller migrate、same wave で old API delete。compatibility shim なし。parallel old-and-new path なし。every rename を actual file に spot-check。rename は string、prose、back-reference の usage を silently miss。mechanical edit を設定 refactoring model（デフォルト `composer-2.5-fast`）の subagent に delegate。specific scope（file paths、move する names、hold する behavior）。diff を自分で review。
5. real artifact 上で behavior unchanged を prove。「it compiles」ではない。**`/verify-done`**（Tier B/C/D、equivalence check 含む）。larger reshape なら equivalence check：old-vs-new output diff script、new code に replay する recorded baseline、または relevant control スキル経由 matching surface smoke run。verification を自分で own。delegate の「looks good」summary を trust しない。
6. change が place を earn したことを confirm。success measure は reduced reader load（**refactor-check** Step 3）：question と answer 間の layer 減、hidden state 減、second consumer なし indirection 減。diff が somewhere reader load を lower しないなら revert。
7. story を語る small ordered commit に rebase。subtraction commit、reshape、follow-on cleanup。1 revert が1 slice undo。[`sequence-verifiable-units`](../principles/sequence-verifiable-units.md) で shape。各 behavior-preserving slice green のまま next。**Opening a PR**。

**Reply:** 変わった structure、hold した pin、equivalence proof、reader-load delta、ship と revert。new behavior なし。



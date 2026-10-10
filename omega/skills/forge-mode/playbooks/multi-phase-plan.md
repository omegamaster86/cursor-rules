### Multi-phase or multi-PR plan

**plan を自分が持ち、code は not。plan は owner が box ごとに走らせ、operator が evidence から audit する checklist。** plan が deliverable。implement しない。

1. change が 1–2 file で approach が obvious なら plan を skip。そう言って stop。
2. 書く前に open question を prototype で settle。各々 `playbooks/prototype.md`。Appendix A 用に branch、SHA、screenshot を keep。run が settle できない product か preference call だけ operator に聞く。options を出す（**never-block-on-the-human** principle skill）。
3. subagent で explore。`subagent_type: "forge-agent"` と Subagents section に従う explicit model（**guard-the-context-window** principle skill）。各々 file pointer、convention、test command、entry point を返す。inlined dump なし。
4. 下の skeleton を plan file に copy し全 placeholder を埋める。operator が path を名指さない限り agent store の `docs/` 下に書く。見出しと sub-block は示された順を keep。PR ごと 1 section。1 PR は 1 change と独自 evidence（**sequence-verifiable-units** principle skill）。**How to read this** に execution playbook を名指す。`playbooks/autopilot-stack.md` 末尾の rule で `playbooks/autopilot-full.md` と `playbooks/autopilot-stack.md` を選ぶ。standing program は `playbooks/orchestrate.md`。
5. `/technical-writing` で全文書き、その後 `/unslop`。body は Diátaxis 1 mode、how-to。Appendix は explanation と reference。各見出しは task か finding を述べる。long dash なし。文中 colon なし。
6. `node .cursor/skills/forge-mode/scripts/check-plan.mjs <plan.md>` を走らせ、print される各行を fix（**encode-lessons-in-structure** principle skill）。
7. hand back。plan path と script output を post して stop。execution は operator の明示 go で、plan が名指す execution playbook の下で始まる。

**Verification.** test だけでは verification 不十分。PR は unit、live、perf box がすべて checked のときだけ verified（**prove-it-works** principle skill）。その文が verification rule。各 verification block はそれで始まる。live block は mandatory。PR head で 10 lane が real surface を control skill 経由で drive。**swarm** skill に従い `swarm workers` model（default `cursor-grok-4.6-medium`）。各 lane は 1 box。concrete scenario、保存する screenshot、pass predicate。**Regression lane against trunk** が 1 lane。trunk と head で同じ load-bearing scenario。trunk に feature がなければ fact を記録し、diff が足す behavior と user が待つ end state を gate。trunk result を invent しない。perf gate は dual-sided。trunk と head が両方 named metric を出す。trunk に feature がなければ diff が足す work を isolate し、その work と user が待つ end-to-end state に absolute budget。unlike scenario 間で ratio を主張しない。perf block は metric、interleaved probe、先に測る trunk baseline、fail する数字付き rule を名指す。interaction を変える PR は review-gated。merge 前に operator が chat で screenshot と video で review。interaction を変えない PR は `**Review gate.** None. <PR id> is not review-gated.` と書き、下に box なし。

**Control skill.** surface で選ぶ。Browser、Electron、web UI は `cursor-team-kit` の `control-ui`。CLI と TUI は `control-cli`。native mobile は repo が持つ simulator-driving skill。2 surface に触れる PR は両方に lane。control skill がない surface は Appendix C の risk。live block は各 lane がどう drive するかまだ名指す。

````markdown
# <Program> plan

<Under ten lines. What changes, for whom, the rule the program enforces, and the PR ids in order.>

## How to read this

One box is one unit of work. Every box names the evidence that checks it. A nested box is a sub-step of the box above it. Check a box only when its evidence exists, a file, a log line, a screenshot, a test run, or a SHA. The body is a how-to. The appendices explain and record.

The program runs `.cursor/skills/forge-mode/playbooks/<execution playbook>.md`. <Who merges, and which PR ids are the operator's items that stop at merge-ready.>

Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

## Program checklist

### Arm the program

- [ ] State the protocol and this plan to the operator, then stop. Start execution only on the operator's explicit go.
- [ ] Read these from trunk at program start. Re-read them at every tick.
  - [ ] `git show origin/main:.cursor/skills/forge-mode/playbooks/<execution playbook>.md`
  - [ ] `git show origin/main:.cursor/skills/swarm/SKILL.md`
  - [ ] `git show origin/main:<control skill path>`
  - [ ] `git show origin/main:.cursor/skills/forge-mode/playbooks/opening-a-pr.md`
  - [ ] `git show origin/main:.cursor/skills/<each other leaf skill the program uses>`
- [ ] On the operator's go, arm the audit tick as `/loop 1h` with the tick prompt below. Never leave the cadence to memory.
- [ ] Use this tick prompt, verbatim. "Re-read the execution playbook from trunk. Audit the operation against it and fix drift in this tick. Probe every active lane and judge progress by side effects only. Stand down a stuck lane and dispatch its replacement now. Then post a short status message to the operator in chat only when the audit found a tracked change that no earlier status message reported, such as a PR opened, a code-ready head, a round launched or closed, a verdict, a merge, a stuck agent and the action taken, a blocker added or cleared, or a decision only the operator can make. Name every such change and nothing else. Do not repeat a table, the merged list, or an unchanged blocker. If the audit found none, end the turn with no reply text. Either way, log this tick's row in your decision trail. The row names the items reported, or none."
- [ ] On the operator's hold or stand-down, send every owner a zero-writes order at once.

### Spawn owners

- [ ] Spawn one owner per PR with the full lifecycle the execution playbook names.
- [ ] Follow this dependency graph. Start dependent work only after its parent merges, or base it on the parent branch when the execution playbook stacks.
  - [ ] <PR id> and <PR id> are independent and first. Both branch from `main`.
  - [ ] <PR id> after <PR id>.
- [ ] Hold the file boundaries. <PR id or class> touches only `<glob>`.
- [ ] Hold the review gate. <PR ids> change an interaction. They wait for the operator's review in chat with screenshots and a video before merge.

### PR mechanics, for every PR

- [ ] Resolve the forge once. Default to `gh`; if `command -v origin` succeeds and Origin can resolve the repository, use `origin pr` for every PR operation. Record any fallback to `gh`. Never require `gt`.
- [ ] Open the PR ready, never draft, per **Opening a PR**. Use the run's built-in PR tool when it has one, else `origin pr create --status open --base <base-branch>` or `gh pr create --base <base-branch>` according to the resolved forge. A stack child targets its parent branch.
- [ ] Run the repo's lint and typecheck once before the PR-facing push. Push with hooks on.
- [ ] Run `/deslop` before each commit and `/no-comments` before review.
- [ ] Triage every Bugbot and security-reviewer comment per `../references/bugbot-triage.md`.
- [ ] Rebase onto current trunk before the code-ready report and babysit. Keep that merge base in fix rounds. Rebase again only at merge prep, on a `git merge-tree` conflict with trunk, or on a CI failure that comes from a change on trunk.

### Verdict and merge, for every PR

- [ ] At the code-ready head SHA and at each later push that changes the patch, run the swarm per `.cursor/skills/swarm/SKILL.md`. One gates lane. The ten live lanes from the PR's **Verify, live** block. The perf lane from its **Verify, perf** block. Two or more audit lanes, each with its own focus, that read the diff and the receipts and distrust the PR body. The root audits the receipts in the merge-ready report before the verdict.
- [ ] Clean only when every lane is `PASS`. Findings go back to the owner, including a defect that a lane filed as a note. A new head gets a fresh swarm and a fresh verdict, except for results that stay valid under the patch-id rule in `playbooks/shipping.md`.
- [ ] <The merge or append rule from the execution playbook, with the patch-id rule from `playbooks/shipping.md`.>

### Boot recipe, for every live lane

Each live lane runs on its own cloud VM at the PR head. Drive through `control-ui` or `control-cli` from `cursor-team-kit`.

- [ ] `git fetch origin <head-branch> && git checkout <head SHA>`.
- [ ] <Start the backend and the surface. Wait for ready.>
- [ ] <Deliver input only through the control skill's commands. Name the read-only diagnostics.>
- [ ] Save every screenshot to `/tmp/swarm-<pr-id>/worker-<n>/<slug>.png` and return the paths with the report.

## <Task as a verb phrase> (<PR id>)

**Depends on.** <PR id, or None.>

**Files.**

- [ ] Edit `<path>`.
- [ ] Create `<path>`.
- [ ] Delete `<path>`.

**Build.**

- [ ] <One change. Name the symbol and the file.>

**You see.**

- [ ] <One observable result, with the exact log line or screen state.>

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] <Test file and the case it gains.> Run `<command>`.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `<swarm workers model>` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Run <the same load-bearing scenario> at trunk and head. If trunk lacks the feature, record that and gate <the behavior the diff adds plus the end state the user waits for>. Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 2. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 3. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 4. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 5. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 6. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 7. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 8. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 9. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 10. <Scenario.> Save `<slug>.png`. Pass when <predicate>.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. <What is measured at both trunk and head. If trunk lacks the feature, also name the diff-added work and the end-to-end state the user waits for.>
- [ ] Probe. <The command or procedure, run at trunk and at the head, interleaved. Both sides must produce the metric.>
- [ ] Baseline. Record the trunk <value> first.
- [ ] Rule. <Head against trunk, with the number that fails. If the scenarios differ, add absolute budgets for the diff-added work and the user-visible end state instead of an invalid ratio.>

**Review gate.** The operator reviews before merge.

- [ ] Copy lane <n> screenshots into `<media path>/<pr-id>-review-<slug>.png`.
- [ ] Record a 30 to 60 second video of the change on a lane VM. Save it as `<media path>/<pr-id>-review.mp4`.
- [ ] Post the screenshots and the video in chat. Stop at merge-ready. Wait for the operator's click.

**Merge.**

- [ ] Root's clean verdict at the exact head SHA.
- [ ] Bugbot triage done.
- [ ] Rebased onto current trunk after the verdict, patch-id unchanged.
- [ ] <The owner squash-merges its own PR, or the root appends it to the base-branch stack and the operator lands it bottom-up.>

## Close the program

- [ ] Every box above is checked with its evidence.
- [ ] Reply to the operator with the report the execution playbook names.

## Appendix A. Prototype evidence

<Each open question a prototype answered, with the branch, the SHA, and the artifact links. Each question that stays unproven.>

## Appendix B. Alternatives rejected

<Each approach weighed and why it lost.>

## Appendix C. Risks

<Each risk with the PR it lands in and what the owner watches.>

## Appendix D. Links and reading list

<Docs to read before editing. Which PRs get `.cursor/skills/how/SKILL.md` and `.cursor/skills/review-orchestrator-triple-hybrid`. The trail per `.cursor/skills/decision-log/SKILL.md`.>
````

**Reply:** plan path、PR id と dependency と review-gated set、prototype が証明したものと unproven のままのもの、check script の output。

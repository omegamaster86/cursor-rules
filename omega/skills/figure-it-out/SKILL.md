---
name: figure-it-out
description: "狭い playbook が合わないときに監査可能な playbook を設計: 大規模 migration、野心のある multi-part 変更、離席後に人がレビューする作業。タスクに rigor をスケール、仮説ループを走らせ、decision-log で決定を記録。/figure-it-out、'figure it out'、大 migration、狭い playbook が無いとき。"
disable-model-invocation: true
---

# Figure it out

タスクがどの playbook にも合わないとき、playbook を設計する。コードより前の deliverable は workflow 自身: タスクに rigor をスケールし、科学的方法を走らせ、離席後に人が監査できる決定 trail を残す phase の列。

## Start

todolist を開き、最初の項目は **forge-mode** スキルの Principles 節を読む。次に下の phase を todo として追加。

## Phase A: Frame

まず ground、次に commit。次を述べられるまで run を始めない:

- done の定義を falsifiable predicate として（**prove-it-works** principle スキル）。
- scope を定量化: 粗い単位と effort、grounding が出した blocker も。
- rigor level、高めに bias。one-way door と高 blast radius は多め。可逆で低 stakes の step は少なめ。rigor は gate と artifact であり「もっと頑張る」ではない。

長い run に commit する前に framing と tradeoff を提示。可逆作業は進める（**never-block-on-the-human** principle スキル）が、数時間 run には 1 checkpoint。

## Phase B: Design the workflow

atomic で独立に land できる単位に分解。riskiest-unknown-first で順序。scaffold と verification は feature の前（**foundational-thinking** principle スキル）。

- 作業前に verification harness を組み、変更前 state から baseline を capture し、check が「旧値 vs 新値」として読めるようにする。
- one-way-door の設計決定には **architect** スキル（**multi-agent-candidates** を走らす）。形状が既に concrete な mechanical 作業ではスキップ。落ち着いた設計への 2 回目 multi-agent-candidates は over-engineering（**laziness-protocol** principle スキル）。
- 何を fan out するか決める。seam 横だけ parallelize し、各 worker に独自 worktree または branch（**separate-before-serializing-shared-state** principle スキル）。過剰 fan はしない。
- 設計した phase リストを書き留める。人がレビューするのはそのリスト。

次に設計を実行。Phase C エントリの後・Phase D の前に todolist に具体 step を追加。各 step を Phase C loop discipline で走らせ、Phase D log を step が land するたびに 1 行織り込み、trail 全体を最後に溜めない。

## Phase C: Run the loop

各単位は experiment。仮説を述べ、最小変更、real artifact で predicate を measure、進めたら keep、しなければ revert。
**sequence-verifiable-units** principle スキルに従い、次を始める前に各単位を verify し、最後に check を batch しない。

- artifact を inspect して verify、self-report はしない。簡単に pass しすぎるときは system より observation 方法を疑う。
- 委譲作業に judge を pair。worker が gate を game したら reset して contract を harden。gate 自体が誤りなら gate を単独変更で直し、迂回しない。
- verdict は VERIFIED、NOT VERIFIED、INCONCLUSIVE。Inconclusive は pass ではない。negative を隠さない。

## Phase D: Keep the audit trail

**decision-log** スキルで run を log。figure-it-out の作業は通常野心があり、reviewer が PR で読めるよう trail を commit する。trail と diff で人が戻って信頼できる。

## Phase E: Verify and hand back

harness だけでなく real product で Phase A predicate 全体を check。繰り返す修正は gate、lint rule、check、script に encode（**encode-lessons-in-structure** principle スキル）。

**Reply:** 設計した playbook、rigor level と理由、decision-trail path、predicate に対して verified なもの、まだ open なもの。

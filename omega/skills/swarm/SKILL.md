---
name: swarm
description: "N 並列 worker に fan out、drain し、1 本の report を返す。/swarm、'swarm this'、parallel coverage、race、gauntlet、exploration 向け。"
disable-model-invocation: true
---

# Swarm

N 並列 cloud worker に fan out。別 slice を分担、同一 brief で race、または混在。parent は待ち、集約し、1 report を返す。

## Start

何かを起動する前にフェーズごと 1 エントリの todolist を開く。

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. done predicate と swarm が返す artifact または report を述べる。
2. 形状を選ぶ。slice に partition、同一 brief で N worker race、または混在。race または混在なら spawn 前に `first pass`、`rank all`、`best-of` を宣言。
3. N はユーザー指定または形状から導く。N は worker 総数であり cloud concurrency 上限ではない。
4. worker model は `~/.cursor/rules/forge-models.mdc` の `swarm workers` 行から。ルールまたは行が無ければ `cursor-grok-4.6-medium`。`inherit` なら `model` を省略し worker は parent model。Task tool が slug を拒否したら default を使いそう言う。default も拒否なら error の同族で最も近い valid slug。model race なら各 arm の model を事前に名指し。
5. worker が書くときは各自 writable 出力。commit を verify または measure する brief は exact SHA を名指し。measurement brief は method も（sample 数、1 sample の定義、順序）。worker は結果に両方を記録。

## Phase B: Fan out

1 メッセージで N worker すべてを `subagent_type: generalPurpose`、`environment: "cloud"`、`run_in_background: true`、step 4 の model（`inherit` なら未設定）で spawn。ユーザーマシン上のものにアクセスが要るときだけ `environment: "local"`。

非デフォルトの pushed branch から始める worker には `cloud_base_branch` を渡す。

各 brief は単体で完結。goal、scope、exact slice または race arm、verify 方法、report 内容。report は `PASS`、`ISSUES`、`BLOCKED` と evidence。defect を証明できる worker は `ISSUES` と、最初だけでなく証明できるすべての issue を列挙。

worker が dropout したら N-1 で続行し記録。

## Phase C: Aggregate

terminal 結果を読む。brief が名指した SHA と method を記録していない結果は捨て、その worker を 1 回 respawn。2 回目も miss なら gap を記録。gap は pass 扱いしない。coverage では required slice ごとに結果が要る。race では事前宣言の selection rule を適用。first pass、rank all、best-of。raw worker dump を貼らない。

compact 結果表、1 行 evidenced issue、明示 gap または dropout を残す。

## Phase D: Report

表、issue 1 行、gap または dropout、使った race rule を含む 1 本の統合 in-chat report を返す。

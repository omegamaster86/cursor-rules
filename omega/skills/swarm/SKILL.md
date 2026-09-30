---
name: swarm
description: N 並列ワーカーを扇状展開し、集約して 1 本のレポートを返す。/swarm、「swarm this」、カバレッジ分割・レース・ガントレット・探索に使用。
disable-model-invocation: true
---

# Swarm

N 個の並列 cloud ワーカーを扇状展開する。スライス分割、同一 brief のレース、または混在。親は待ち、集約し、1 本のレポートを返す。

forge-mode の **multi-agent-candidates** は設計 bakeoff 向き。**swarm** は実行・検証・探索のカバレッジ分割向き。

## 開始

起動前にフェーズごと 1 項目の todolist を開く。

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. 完了条件（done predicate）と swarm が返すべき成果物またはレポートを述べる。
2. 形を選ぶ。スライス分割、同一 brief で N レース、または混在。レースまたは混在では spawn 前に `first pass` / `rank all` / `best-of` を宣言。
3. N はユーザー指定または形から決める。N は総ワーカー数であり cloud 並列上限ではない。
4. ワーカーモデルは `.cursor/rules/forge-models.mdc` の `swarm workers` 行から。行が無いときは `composer-2.5-fast`。`inherit` のときは Task の `model` を省略し親モデルで走らせる。slug が拒否されたらデフォルトを使い明記。レースでは各 arm のモデルを先に名指し。
5. 書き込みがあるワーカーには専用の出力先を渡す。コミットを verify / 計測する brief は exact SHA を名指す。計測 brief は方法（サンプル数、1 サンプルの定義、順序）も名指し。ワーカーは結果に両方を記録。

## Phase B: Fan out

1 メッセージで N ワーカーをすべて spawn。`subagent_type: generalPurpose`（または forge-mode コンテキストでは `forge-agent` でコード実装）、`environment: "cloud"`、`run_in_background: true`、Phase A のモデル（`inherit` なら省略）。ユーザーマシン上のものだけ必要なら `environment: "local"`。

非デフォルトの push 済みブランチから始める必要があるときは `cloud_base_branch` を渡す。

各 brief は単体で完結。goal、scope、exact スライスまたはレース arm、verify 方法、報告形式を含める。報告は `PASS` / `ISSUES` / `BLOCKED` と evidence。欠陥を証明できるワーカーは `ISSUES` と、最初の 1 件だけでなく証明できるすべてを列挙。

ワーカーが落ちたら N-1 で続行し明記。

## Phase C: Aggregate

終端結果を読む。brief が名指した SHA と方法を記録していない結果は捨て、そのワーカーを 1 回再実行。2 回目も欠けたら gap として記録。gap は pass に数えない。カバレッジでは必須スライスごとに結果が必要。レースでは先に宣言した選択規則を適用。生ダンプは貼らない。

コンパクトな結果表、1 行 evidence 付き issue、gap / dropout を保持。

## Phase D: Report

表、issue 1 行要約、gap / dropout、使用したレース規則を含む 1 本のチャット内レポートを返す。

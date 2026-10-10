---
name: forge-help
description: omega のセットアップ、/forge-mode、スキル・プレイブック・原則の選び方を案内する。/forge-help に質問を添える。
disable-model-invocation: true
---

# Forge help

ユーザーの **使い方の質問** に答える。送れるプロンプト例と、根拠ファイルへのリンクを返す。help 質問のときは作業を始めない（トークンを使う `/forge-mode` 実行はユーザーが送ってから）。

「このバグを forge で直して」のような **作業依頼** は help ではない。[`forge-mode`](../forge-mode/SKILL.md) を読み、その下で実行する。

正本パスは `cursor-rules/omega/`。ユーザーが repo を開けないときは `https://github.com/omegamaster86/cursor-rules/tree/main/omega/` に続けて相対パスを示す。

## ニーズの切り分け

会話から推論する。不明なら次の 1 問（複数選択）だけして、選ばれた節だけ答える。

- セットアップ
- `/forge-mode` でタスクを始める
- 状況に合うスキルを選ぶ
- うまくいかなかった run の対処
- omega を自分用にカスタムする（[`/automate-me`](../automate-me/SKILL.md) で personal `-mode`）

状態によって答えが変わるときだけ触れる。

- `~/.cursor/rules/forge-models.mdc` が無い → `/setup-forge` 未実行。各ロールはスキル内デフォルト。
- PJ に `verify-*` が無い → `/create-verification-skill` を検討（動作証明）。

モデル設定が効くときは、今 `/setup-forge` するか一度だけ聞く（新規・コスト・どのモデルが走るかに依存する場合）。

## セットアップ

1. [omega ガイド](../../docs/guide/01-setup.md) に従い `omega-link`（Desktop）または Cloud テンプレを置く。
2. [`/setup-forge`](../setup-forge/SKILL.md) で reasoning budget とロール別モデルを `forge-models.mdc` に書く。新チャットから効く。
3. 方向が空なら先に [`/plan-interview`](../plan-interview/SKILL.md)。Ship なら `/forge-mode` と完了条件。

初回プロンプトの文言は [`references/prompting.md`](references/prompting.md)。コストはサブエージェントとレビュー panel が増える点と、`/setup-forge` で budget を下げる点を説明。

## `/forge-mode` で始める

プレイブックにマッチし、ステップを todo に verbatim コピーする。良いプロンプトは **目標** と **完了判定**。スキル列を手書きしない。

- Enter 一度きりの `/forge-mode` は会話が進むと薄れる。
- Custom Mode にするとターンごとに残る（Cursor の Agents / CLI ドキュメントを参照）。

サブエージェントは `subagent_type: "forge-agent"`。[ガイド 02](../../docs/guide/02-forge-mode.md) に例。

## スキルを選ぶ

多くは `/forge-mode` 経由。直接名指しは playbook より強い／弱いとき。

| やりたいこと | スキル / コマンド |
|---|---|
| 厳密な非自明タスク | [`/forge-mode`](../forge-mode/SKILL.md) |
| 何を・なぜ・用語（Align） | [`/plan-interview`](../plan-interview/SKILL.md) |
| コードの動き・配置 | [`/how`](../how/SKILL.md) |
| 設計 rationale・経緯 | [`/why`](../why/SKILL.md) |
| 最近のチャットから文脈 | [`/recall`](../recall/SKILL.md) |
| 仕組み・経緯を人向けに説明 | [`/teach`](../teach/SKILL.md)（`how` + `why`） |
| 個人の `-mode` スキルを生成・更新 | [`/automate-me`](../automate-me/SKILL.md) |
| 直前の返信を平易に言い直す | [`/bro`](../bro/SKILL.md) |
| 差分の外側の破壊 | [`/blast-radius`](../blast-radius/SKILL.md) |
| 関数境界を越える設計 | [`/architect`](../architect/SKILL.md) |
| 並列設計案の比較 | [`/multi-agent-candidates`](../multi-agent-candidates/SKILL.md) |
| 並列検証・レース | [`/swarm`](../swarm/SKILL.md) |
| 争点のある diff のレビュー | **`/review-orchestrator-triple-hybrid`**（commands） |
| ローカルテスト先行のバグ修正 | [`/tdd`](../tdd/SKILL.md) |
| TS/React/Supabase の書き方 | [`/web-coding-standards`](../web-coding-standards/SKILL.md) |
| 動作証明レシピの生成 | [`/create-verification-skill`](../create-verification-skill/SKILL.md) |
| perf 数字の vet | [`/benchmark-checklist`](../benchmark-checklist/SKILL.md) |
| 大規模・横断変更のプラン | [`/figure-it-out`](../figure-it-out/SKILL.md) |
| 長時間 run の監査 | [`/decision-log`](../decision-log/SKILL.md) |
| ロール別モデル | [`/setup-forge`](../setup-forge/SKILL.md) |
| セッション後のスキル改善 | [`/reflect`](../reflect/SKILL.md) |
| 繰り返しミスの構造修正 | [`/correct`](../correct/SKILL.md) |
| 案内 | `/forge-help` |

原則は `forge-mode/principles/`。ユーザーは名前で steer（例: prove it works）。[ガイド 08](../../docs/guide/08-principles.md)。

## プレイブック

スラッシュは無い。`/forge-mode` 内でタスク記述が選ぶ。例: babysit / shipping / session pickup / autopilot-stack / autopilot-full。一覧は [`forge-mode`](../forge-mode/SKILL.md) の Playbooks。[ガイド 06](../../docs/guide/06-verify-and-ship.md)。

## うまくいかないとき

| 症状 | 対処 |
|---|---|
| 数ターンでモードが薄れた | Custom Mode か、タスクごとに `/forge-mode` |
| 前タスクの続きと誤認 | 「new task」と明示 |
| モデル変更が効かない | `forge-models.mdc` は新チャットから |
| 並列が上書き | worktree 分離または cloud ワーカー |
| 夜間で進捗ゼロ | `/loop` は完了 predicate が必要（[ガイド 07](../../docs/guide/07-overnight.md)） |

[`references/prompting.md`](references/prompting.md)、[ガイド 10](../../docs/guide/10-recipes-and-pitfalls.md)。

## 返信

答えを先に。プロンプト例は 1 つまで（[`references/recipes.md`](references/recipes.md)）。根拠ファイルをリンク。

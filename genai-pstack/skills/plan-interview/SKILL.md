---
name: plan-interview
description: "計画や設計を容赦なくインタビューし、決定木の各分岐を解決して共有理解に到達する。実装・PRD 作成・データモデル確定の前にプランをストレステストしたいとき、エージェントに反論・プッシュバックが欲しいときに使用。/plan-interview、計画の穴洗い出しに使用。"
disable-model-invocation: true
---

# Plan interview

計画や設計を実装前にストレステストする。ユーザー向けエントリーポイント。

**grilling** スキルを実行する。本体のインタビュー技法は `grilling/SKILL.md` が所有する。

## いつ使う

- PRD や仕様を書く前
- **forge-mode** / **architect** に入る前（何を・なぜの意思決定）
- データモデルや API 形状を確定する前
- 複数の設計選択が相互依存しているとき
- エージェントに同意ではなく反論が欲しいとき
- `/forge-mode` の Intent gate が `blocked` と案内したとき

コードベースとの整合や ADR・用語集の作成が主目的なら **architect** や **forge-mode** を優先する。本スキルはコードベース不要の汎用インタビュー。

## forge-mode との関係

本スキル実行中は **grilling が勝つ。** never-block と Prototype プレイブックは使わない。

`/forge-mode` が既に起動しているチャットで本スキルを叩かれたら、Ship を中断し Align に切り替える。実装サブエージェントは spawn しない。途中の WIP は commit せず、必要なら **session-log**。

`disable-model-invocation: true` を維持する。forge の Intent gate が `blocked` のとき、親は本スキルを自己起動せず、ユーザーに `/plan-interview` を打たせる。

## やらないこと

- 合意前に Feature プレイブック・how・architect・実装へ進まない
- `decision-log` は任意。ゲートを Notion 依存にしない

## 終了時に必ず返す（Ship への手渡し）

ユーザーが合意を確認したら、次をチャットに出す。これがないと `/forge-mode` は Intent gate で止まる。

```
alignment: <1文。何を作るか / 何をやらないか>
用語: <あれば 単語=意味。なければ「なし」>
未確定: <Ship に持ち込まない残り。なければ「なし」>
```

次の一手の案内（ユーザーが選ぶ）:

- 技術設計 → `/architect` または `/forge-mode`（architect ステップ含む）
- 実装 → `/forge-mode alignment: <上と同じ1文>`
- 決定の記録 → **decision-log**（任意）

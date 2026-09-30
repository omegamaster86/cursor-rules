# omega ガイド

omega は **Align（何を・なぜ）** と **Ship（厳密な実装・検証）** を分け、Next.js / Supabase 規約と forge-mode プレイブックを一つにした Cursor ルールセットです。

マイクロマネージせず、**ゴール**と**完了の判定方法**を自分の言葉で渡す習慣を身につけるためのガイドです。

## 読む順（初回）

1. [セットアップ](./01-setup.md) — `omega-link`、Cloud、`/setup-forge`
2. [Align と Ship](./02-align-and-forge.md) — `/plan-interview` と `/forge-mode`、Intent gate
3. [理解する](./03-understand.md) — `/how`、`/why`、`/recall`
4. [設計する](./04-design.md) — `/architect`、`/multi-agent-candidates`、`/swarm`
5. [作って証明する](./05-build-and-verify.md) — プレイブック、`/verify-done`、`verify-*`
6. [PR と land](./06-ship-pr.md) — Babysit、Shipping、レビュー orchestrator
7. [離席・夜間](./07-overnight.md) — `decision-log`、Autopilot、Orchestrate
8. [原則で舵を取る](./08-principles.md) — `forge-mode/principles/` の 23 本
9. [自分用にする](./09-customize.md) — `forge-models.mdc`、スキル追加
10. [レシピと落とし穴](./10-recipes.md)

初回は上から順に。以降は各ページ単体で参照できます。

## これだけ覚える

```text
/plan-interview エクスポート時に重複行が出る。成功条件と非ゴールを先に固めたい。

/forge-mode 再現手順が分かった。直して /verify-done まで。
```

方向が空なら plan-interview。実装・調査・PR 運用は forge-mode がプレイブックを選び、必要なスキルをステップごとに呼びます。

次: [セットアップ](./01-setup.md)

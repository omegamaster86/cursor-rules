---
name: maintain-verification-skill
description: "プロジェクトの verify スキルと feature map を監査する。機能ごとにソース読みとライブ drive、実証済み修正は最大1 PR。/maintain-verification-skill、「verify スキルを監査して」に使用。"
disable-model-invocation: true
---

# Maintain a verification skill

`/create-verification-skill` が生成した（または同等の feature map を持つ）プロジェクトローカル検証スキルのメンテ。単位は機能。全文を一文ずつ検証しない。

対象が無い → 発明せず `/create-verification-skill` を案内して止まる。

## 成果

1 つ選び、名指しする。

- **clean** — 全 feature をソースとライブでカバー。直すものなし。ブランチも PR もなし。
- **changed** — 実証済みの doc / harness / map 修正を 1 PR。
- **blocked** — カバー未完了、または安全に直せない。何が止めたかを書く。

## 編集スコープ

検証スキル自身のディレクトリだけ（`SKILL.md`、`features/`、それが所有する harness）。**プロダクトコードは触らない。** map が記述する動作をアプリがもうしないなら、doc drift（map を直す）かプロダクト回帰（報告する。docs で隠さない）。

## パス

0. **Locate.** 通常 `.cursor/skills/verify-*/`。候補が複数ならどれか聞く。

1. **Index.** feature map README と sibling glob。欠け・余分・重複・死んだエントリを直す。

2. **Source wave.** feature ファイルごとに read-only サブエージェントを並列（`subagent_type: "forge-agent"`）。「このユーザー向け機能はどう動くか」をソースから説明し、drift 候補を引用付きで、ライブ検証レシピを1つ返す。子はアプリを drive しない、ファイルを編集しない。

3. **Reconcile.** 全 feature に summary があること。レシピを少ないアプリ状態にまとめる。最近の churn で map に無いユーザー面があれば、ソースパス付きでのみ missing と呼ぶ。

4. **Live pass.** ソースがきれいでも必須。coordinator が drive を所有。対象スキルの Launch に従う（サーバ/UI は長寿命 1 インスタンスを直列、短命 CLI は drive ごとに隔離）。全 feature を少なくとも1回。不変条件: (1) 驚くことが起きたあとは doctor してから再 drive、(2) これまでの証拠は cleanup 後も名指し場所に残る、(3) drive が始めた残り物はその drive の後に消す。doctor 失敗がスキル drift なら edit scope 内で直して1回だけ retry。到達不能は具体的な前提（auth、外部状態）付きで `verified-unreachable`。harness 修正はライブで再 drive してから ship。最終 teardown は最後の drive の後。証拠は残す。

5. **Triage.** ユーザー POV の誤り → doc。harness が drive できないがアプリは動く → harness。アプリが壊れている → プロダクトギャップとして報告し、この PR に入れない。

6. **Ship or stop.** changed: 変更ファイルを再読してから 1 PR。clean / blocked: PR なし、カバーを正直に報告。

run notes は scratch。commit しない。

---
name: omega-mode
model: inherit
description: 非自明な実装・調査のエントリ。omega-mode スキルのプレイブックと原則を適用し、genai のドメイン規約とレビューコマンドと連携する。
---

あなたは **omega-mode** のオーケストレータです。`/omega-mode` 起動時は `global.mdc` の通常フローより **本コマンドと omega-mode スキルが優先**します。

## 最初に必ず読む

1. `/.cursor/skills/omega-mode/SKILL.md`（**Principles** セクション含む全文）
2. `/.cursor/skills/omega-mode/SKILL.md` の **ルーティング** セクション
3. 適用する原則ごとに `/.cursor/skills/principle-*/SKILL.md` を leaf として全文読む

## 起動時の必須フロー

1. todo リストを開く。最初の項目は Principles インデックスを読むこと。
2. ユーザー依頼をプレイブックにマッチさせ、`/.cursor/skills/omega-mode/playbooks/` の該当ファイルのステップを verbatim でコピーする。
3. ステップが発火するたびにスキルまたはコマンドへルーティングする。
4. 返信は簡潔・検証済み・根拠付き（日本語可）。文体の細かい制約は設けない。

## 補足ルーティング

`omega-mode` スキルの **ルーティング** に加え、次も参照する。

| 状況 | 使うもの |
|------|----------|
| 変更の影響範囲 | `blast-radius` スキル |
| モデル設定 | `.cursor/rules/omega-models.mdc` を編集（行を削除するとスキル内デフォルトにフォールバック） |

## サブエージェント

- コード実装 delegate・プレイブック内ヘルパー: `subagent_type: "omega-agent"`
- `how` / `reflect` は各スキルが規定する `subagent_type` を尊重する
- デフォルト: `run_in_background: true`

## 実行環境

- 対象 PJ 内のみ。Fallow MCP / `fallow` CLI は使わない。
- UI / CLI の検証はブラウザ MCP または手動 verify。

## 軽い作業向けではない

typo 修正・1行変更・単純な質問には本コマンドを使わない。通常の Agent チャット（`global.mdc` のみ）で足りる。

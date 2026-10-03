---
name: product-design
description: "プロダクト設計ワークフロー: UXリサーチ、監査、ビジュアル探索、URLクローン、モック実装、デザインQA、プロトタイプ共有。product-design、プロトタイプ、画面監査、URLをクローン、モックを実装、デザインQA に使用。"
---

# Product Design（Cursor）

アイデア・URL・スクリーンショットから、レビュー可能なプロトタイプまでを扱うスキル群。エントリは [skills/index/SKILL.md](skills/index/SKILL.md)。

## 起動

- スキル `product-design` を読み込んだあと、ルーター [skills/index/SKILL.md](skills/index/SKILL.md) に従う。
- セットアップ・保存コンテキスト: [skills/user-context/SKILL.md](skills/user-context/SKILL.md)
- プレビューとブラウザ検証: [references/cursor-preview.md](references/cursor-preview.md)

## サブスキル

| スキル | 用途 |
| --- | --- |
| `user-context` | 保存済みプロダクト／デザイン参照の読み書き |
| `get-context` | 最小デザインブリーフの確定 |
| `research` | UX リサーチ |
| `audit` | フロー監査・critique |
| `ideate` | ビジュアル方向の3案 |
| `url-to-code` | ライブ URL のクローン |
| `image-to-code` | 選択モックの実装 |
| `design-qa` | 実装とソースの比較 QA |
| `share` | デプロイ・共有 URL |

## Cursor での前提

- **ブラウザ**: `cursor-ide-browser` MCP（`browser_navigate`, `browser_snapshot`, `browser_take_screenshot`）。詳細は [references/cursor-preview.md](references/cursor-preview.md)。
- **永続コンテキスト**: `~/.cursor/product-design/`（プロジェクトに `.cursor/product-design/user-context.md` がある場合はそちらを優先）。`PRODUCT_DESIGN_STATE_DIR` で上書き可。
- **画像生成**: セッションで `GenerateImage` 等が使えるときは ideate／アセット生成に利用。不可のときはユーザー提供画像を要求。
- **共有**: Vercel・GitHub Pages・既存 CI など、利用可能なデプロイ手段。OpenAI Sites 専用手順は [skills/share/SKILL.md](skills/share/SKILL.md) のフォールバックとしてのみ参照。

`.codex-plugin/` と各 `agents/openai.yaml` は上流 OpenAI プラグイン用の残骸。Cursor では無視する。

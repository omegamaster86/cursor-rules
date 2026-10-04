---
name: product-design
description: "プロダクト設計ワークフロー（Cursor 専用）: UXリサーチ、監査、ビジュアル探索、URLクローン、モック実装、デザインQA、プロトタイプ共有。product-design、プロトタイプ、画面監査、URLをクローン、モックを実装、デザインQA に使用。Codex CLI では使用しない。"
---

# Product Design（Cursor）

アイデア・ライブ URL・スクリーンショットから、レビュー可能なプロトタイプまでを扱う。**Cursor のみ**（`omega-link` → `.cursor/skills/product-design`）。**Codex CLI / `~/.codex/skills` 非対象。**

依頼はルーター [skills/index/SKILL.md](skills/index/SKILL.md) に従う。

## 起動

1. [skills/index/SKILL.md](skills/index/SKILL.md) でサブスキルを選ぶ。
2. 保存コンテキスト: [skills/user-context/SKILL.md](skills/user-context/SKILL.md)
3. プレビュー・ブラウザ検証: [references/cursor-preview.md](references/cursor-preview.md)

## ワークフロー例

| 目的 | スキル | 結果 |
| --- | --- | --- |
| 新規アイデアのプロトタイプ | `ideate` → `image-to-code` | 3 方向のビジュアル案 → 選択後に runnable プロトタイプ |
| ライブ画面の再現 | `url-to-code` | キャプチャに基づくローカルプロトタイプ |
| モック実装 | `image-to-code` | 選択デザインのインタラクティブ実装 |
| UX 監査 | `audit` | スクリーンショット付きの findings |
| 共有 | `share` | デプロイ URL |

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

## 実行時の必須

- **MCP**: `cursor-ide-browser`（プレビュー・キャプチャ）。任意で Figma MCP。
- **状態**: `.cursor/product-design/user-context.md` があれば優先。なければ `~/.cursor/product-design/`。`PRODUCT_DESIGN_STATE_DIR` で上書き可。
- **生成ラスタ**: ワークスペース `.cursor/assets/`（無ければ `mkdir -p`。[references/generated-image-assets.md](references/generated-image-assets.md)）。ImageGen 不可時はユーザー画像を要求。
- **共有**: Vercel・GitHub Pages・既存 CI など。OpenAI Sites のみ [skills/share/SKILL.md](skills/share/SKILL.md) フォールバック（テンプレ `.openai/hosting.json` 含む）。

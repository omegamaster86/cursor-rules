# Product Design（Cursor）

アイデア・ライブ URL・スクリーンショットから、レビュー可能なプロトタイプを作るスキル群。Cursor ではルートの [SKILL.md](SKILL.md) から入る。

**Codex CLI では使用しない。** omega 正本は Cursor 向けに移植済み。`~/.codex/skills` や Codex 用スキル同期に含めない。

## 使い方

チャットで例:

- `product-design スキルでセットアップを手伝って`
- `この URL をクローンしてプロトタイプにして`
- `このモックを実装して`

ルーティングは [skills/index/SKILL.md](skills/index/SKILL.md)。

## ワークフロー例

| 目的 | スキル | 結果 |
| --- | --- | --- |
| 新規アイデアのプロトタイプ | `ideate` → `image-to-code` | 3 方向のビジュアル案 → 選択後に runnable プロトタイプ |
| ライブ画面の再現 | `url-to-code` | キャプチャに基づくローカルプロトタイプ |
| モック実装 | `image-to-code` | 選択デザインのインタラクティブ実装 |
| UX 監査 | `audit` | スクリーンショット付きの findings |
| 共有 | `share` | デプロイ URL |

## Cursor 統合

| 機能 | 扱い |
| --- | --- |
| ブラウザ | cursor-ide-browser MCP（[references/cursor-preview.md](references/cursor-preview.md)） |
| 保存コンテキスト | `~/.cursor/product-design/` または `.cursor/product-design/` |
| 画像生成 | セッションの `GenerateImage` 等（ideate） |
| Figma | Figma MCP が接続されていれば利用 |

## レガシー（OpenAI Codex プラグイン）

`.codex-plugin/`、`agents/openai.yaml`、テンプレ内 `.openai/hosting.json` は上流 OpenAI Product Design プラグイン由来。Cursor 運用では必須ではない。Sites 専用ビルド手順は `share` スキル内のフォールバックとして残している。

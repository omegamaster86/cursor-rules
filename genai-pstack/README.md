# genai-pstack

genai（Next.js / Supabase ドメイン規約）と pstack（厳密エンジニアリングワークフロー）を統合した Cursor ルールセットの試作版です。

## 構成

```
genai-pstack/
├── commands/          # ユーザーが叩く入口
├── skills/            # ドメイン規約 + ワークフロー（フラット配置）
├── agents/            # omega-agent サブエージェント
└── rules/
    ├── global.mdc           # 通常モード（常時適用）
    └── omega-models.mdc # モデル設定テンプレート
```

## インストール（PJ へコピー）

対象プロジェクトの `.cursor/` にコピーします。

```bash
# 例: プロジェクトルートで
mkdir -p .cursor
cp -R /path/to/cursor-rules/genai-pstack/commands .cursor/
cp -R /path/to/cursor-rules/genai-pstack/skills .cursor/
cp -R /path/to/cursor-rules/genai-pstack/agents .cursor/
cp /path/to/cursor-rules/genai-pstack/rules/global.mdc .cursor/rules/
cp /path/to/cursor-rules/genai-pstack/rules/omega-models.mdc .cursor/rules/
```

`omega-agent` を Cursor が認識するには `agents/` を `.cursor/agents/` に置くか、プロジェクトの agents 設定に合わせてください。

## 使い方

| シーン | 使うもの |
|--------|----------|
| 軽い修正・質問 | 通常チャット（`global.mdc` のみ） |
| 本格的な実装・調査 | `/omega-mode` |
| ファイル調査 | `/file-brief` |
| 流用チェック | `/reuse-check` |
| リファクタ・削減チェック | `/refactor-check` |
| 完了前検証 | `/verify-done` |
| PR レビュー | `/review-orchestrator-triple-hybrid` |
| モデル設定 | `rules/omega-models.mdc` を編集 |

## モードの関係

- **通常モード**: `global.mdc` が適用。タスク分析・実行結果報告フォーマットあり。
- **omega-mode**: `/omega-mode` コマンド起動時、`commands/omega-mode.md` と `skills/omega-mode/` が `global.mdc` より優先。原則8本 + プレイブック + 検証重視。完了前検証は **`/verify-done`** が正本。検証・層配線は genai ドメインスキル、リファクタ調査は `/refactor-check` が正本。

コマンド（入口）とスキル（原則・プレイブック本体）はどちらも **omega-mode** という名前で統一しています。

## genai と pstack の統合方針

| 衝突 | 解決 |
|------|------|
| `typescript-best-practices` | 採用せず **`web-coding-standards`** を使用 |
| pstack `interrogate` | 未採用。**`/review-orchestrator-triple-hybrid`** コマンドを使用 |
| `poteto-agent` | **`omega-agent`** にリネーム |
| `cursor-team-kit`（deslop, control-*） | 未導入時は skip、手動 verify で代替 |

詳細は `skills/omega-mode/SKILL.md` の **ルーティング** セクションを参照。

## スキル一覧

`skills/README.md` を参照。

## 由来

- `genai/` — Next.js / Supabase コーディング規約
- `plugins-main/pstack/` — poteto のエンジニアリングワークフロー（日本語訳済み）

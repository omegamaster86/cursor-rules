# genai-pstack

genai（Next.js / Supabase ドメイン規約）と pstack（厳密エンジニアリングワークフロー）を統合した Cursor ルールセットの試作版です。

## 構成

```
genai-pstack/
├── commands/          # ユーザーが叩く入口
├── skills/            # ドメイン規約 + ワークフロー（フラット配置）
├── agents/            # forge-agent サブエージェント
└── rules/
    ├── global.mdc           # 通常モード（常時適用）
    ├── forge-models.mdc              # モデル設定テンプレート（Task runner の正）
    └── multi-agent-task-enforcement.mdc  # multi-agent の Task 3並列必須
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
cp /path/to/cursor-rules/genai-pstack/rules/forge-models.mdc .cursor/rules/
cp /path/to/cursor-rules/genai-pstack/rules/multi-agent-task-enforcement.mdc .cursor/rules/
```

`forge-agent` を Cursor が認識するには `agents/` を `.cursor/agents/` に置くか、プロジェクトの agents 設定に合わせてください。

## 使い方

| シーン | 使うもの |
|--------|----------|
| 軽い修正・質問 | 通常チャット（`global.mdc` のみ） |
| 本格的な実装・調査 | `/forge-mode`（プロダクト方向が未確定なら先に `/plan-interview`） |
| 計画・用語のすり合わせ | `/plan-interview` |
| ファイル調査 | `/file-brief` |
| 流用チェック | `/reuse-check` |
| リファクタ・削減チェック | `/refactor-check` |
| 完了前検証 | `/verify-done` |
| PJ の動作確認レシピ | `/create-verification-skill`（初回） / `/maintain-verification-skill`（更新） |
| PR レビュー | `/review-orchestrator-triple-hybrid` |
| モデル設定 | `rules/forge-models.mdc` を編集 |

## モードの関係

- **通常モード**: `global.mdc` が適用。タスク分析・実行結果報告フォーマットあり。
- **forge-mode**: `/forge-mode` コマンド起動時、`commands/forge-mode.md` と `skills/forge-mode/`（原則は `skills/forge-mode/principles/`）が `global.mdc` より優先。起動直後に **Intent gate**（Align vs Ship）。`blocked` ならプレイブックに入らず `/plan-interview` へ。原則14本 + プレイブック + 検証重視。完了前検証は **`/verify-done`** が正本。ユーザー操作の証明レシピは **`/create-verification-skill`**。検証・層配線は genai ドメインスキル、リファクタ調査は `/refactor-check` が正本。

コマンド（入口）とスキル（原則・プレイブック本体）はどちらも **forge-mode** という名前で統一しています。

## genai と pstack、mattpocock の統合方針

| 衝突 | 解決 |
|------|------|
| `typescript-best-practices` | 採用せず **`web-coding-standards`** を使用 |
| pstack `interrogate` | 未採用。**`/review-orchestrator-triple-hybrid`** コマンドを使用 |
| `poteto-agent` | **`forge-agent`** にリネーム |
| `cursor-team-kit`（deslop, control-*） | 未導入時は skip、手動 verify で代替 |
| grilling vs never-block | **Intent gate。** Align は `/plan-interview`、Ship は `/forge-mode`。同じターンで両方オンにしない |

詳細は `skills/forge-mode/SKILL.md` の **ルーティング** と **Intent gate** を参照。

## スキル一覧

`skills/README.md` を参照。

## 由来

- `genai/` — Next.js / Supabase コーディング規約
- `plugins-main/pstack/` — poteto のエンジニアリングワークフロー（日本語訳済み）

参考
https://github.com/mattpocock/skills/tree/main/skills 
https://github.com/cursor/plugins/tree/main/pstack 

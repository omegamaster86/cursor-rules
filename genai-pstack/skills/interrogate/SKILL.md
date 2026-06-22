---
name: interrogate
description: "敵対的レビュー・multi-model review。genai-pstack では review-orchestrator-triple-hybrid コマンドへ委譲する。"
disable-model-invocation: true
---

# Interrogate（genai-pstack 統合版）

**本リポジトリでは pstack 標準の interrogate パネルは使わない。** 代わりに genai の3レーン並列レビューを使う。

## 手順

1. レビュー対象の diff を特定する（`git diff <base>...HEAD` またはユーザー指定ファイル）。
2. **`/.cursor/commands/review-orchestrator-triple-hybrid.md`** の指示に従い、親エージェントとして3サブエージェントを並列起動する。
   - Codex 5.3（正しさ）
   - Sonnet 4.6（正しさ・クロスチェック）
   - Sonnet 4.6（品質・`deep-review-code-quality`）
3. 統合判定を受け取り、Must Fix / Quality Conditions を実装タスクに反映する。
4. 変更を自動適用しない。判定は人間または親エージェントが裁定する。

## 補足

- `nextjs-code-review` / `supabase-code-review` の準拠評価は orchestrator 内で参照される。
- 単体で `/interrogate` と呼ばれた場合も、上記コマンドと同じフローにルーティングする。

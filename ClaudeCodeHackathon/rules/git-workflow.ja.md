# Gitワークフロー

## コミットメッセージ形式

```
<type>: <description>

<optional body>
```

Types: feat, fix, refactor, docs, test, chore, perf, ci

Note: Attribution disabled globally via ~/.claude/settings.json.

## プルリクエストワークフロー

PR作成時:
1. 全コミット履歴を分析（最新コミットだけでなく）
2. `git diff [base-branch]...HEAD` で全変更を確認
3. 包括的なPRサマリを作成
4. TODO付きのテスト計画を含める
5. 新規ブランチの場合は `-u` 付きでpush

## 機能実装ワークフロー

1. **Plan First**
   - **planner** エージェントで実装計画を作成
   - 依存関係とリスクを特定
   - フェーズに分解

2. **TDD Approach**
   - **tdd-guide** エージェントを使用
   - テストを先に書く（RED）
   - 実装して通す（GREEN）
   - リファクタ（IMPROVE）
   - カバレッジ80%以上を確認

3. **Code Review**
   - コード記述後すぐに **code-reviewer** を使用
   - CRITICALとHIGHを解決
   - MEDIUMは可能なら修正

4. **Commit & Push**
   - 詳細なコミットメッセージ
   - Conventional Commitsに従う

---
description: "専用エージェントを使った包括的な PR レビュー"
argument-hint: "[review-aspects]"
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Task"]
---

# 包括的な PR レビュー

複数の専用エージェントを使って包括的なプルリクエストレビューを実行します。各エージェントはコード品質の異なる観点に注力します。

**レビュー観点（任意）:** "$ARGUMENTS"

## レビューワークフロー:

1. **レビュー範囲を決定**
   - `git status` を確認して変更ファイルを特定する
   - 引数を解析し、ユーザーが特定のレビュー観点を要求しているか確認する
   - デフォルト: 適用可能なレビューをすべて実行

2. **利用可能なレビュー観点:**

   - **comments** - コードコメントの正確性と保守性を分析
   - **tests** - テストカバレッジの品質と網羅性をレビュー
   - **errors** - サイレント障害がないかエラーハンドリングを確認
   - **types** - 型設計と不変条件を分析（新しい型が追加された場合）
   - **code** - プロジェクトガイドラインに沿った一般コードレビュー
   - **simplify** - 明確性と保守性のためにコードを単純化
   - **all** - 適用可能なレビューをすべて実行（デフォルト）

3. **変更ファイルを特定**
   - `git diff --name-only` を実行して変更ファイルを確認
   - PR が既に存在するか確認: `gh pr view`
   - ファイル種別を特定し、適用すべきレビューを判断

4. **適用するレビューを決定**

   変更内容に基づく:
   - **常に適用**: code-reviewer（全般品質）
   - **テストファイルが変更された場合**: pr-test-analyzer
   - **コメント/ドキュメントが追加された場合**: comment-analyzer
   - **エラーハンドリングが変更された場合**: silent-failure-hunter
   - **型が追加/変更された場合**: type-design-analyzer
   - **レビュー通過後**: code-simplifier（仕上げと洗練）

5. **レビューエージェントを起動**

   **順次アプローチ**（1 つずつ）:
   - 理解しやすく、対応しやすい
   - 次に進む前に各レポートが完結する
   - 対話的レビューに向いている

   **並列アプローチ**（ユーザーが要求可能）:
   - すべてのエージェントを同時起動
   - 包括レビューを高速化
   - 結果をまとめて取得

6. **結果を集約**

   エージェント完了後、次を要約:
   - **Critical Issues**（マージ前に必須修正）
   - **Important Issues**（修正推奨）
   - **Suggestions**（あると良い改善）
   - **Positive Observations**（良い点）

7. **アクションプランを提示**

   所見を次の形式で整理:
   ```markdown
   # PR Review Summary

   ## Critical Issues (X found)
   - [agent-name]: Issue description [file:line]

   ## Important Issues (X found)
   - [agent-name]: Issue description [file:line]

   ## Suggestions (X found)
   - [agent-name]: Suggestion [file:line]

   ## Strengths
   - What's well-done in this PR

   ## Recommended Action
   1. Fix critical issues first
   2. Address important issues
   3. Consider suggestions
   4. Re-run review after fixes
   ```

## 使用例:

**フルレビュー（デフォルト）:**
```
/pr-review-toolkit:review-pr
```

**特定観点のみ:**
```
/pr-review-toolkit:review-pr tests errors
# テストカバレッジとエラーハンドリングのみレビュー

/pr-review-toolkit:review-pr comments
# コードコメントのみレビュー

/pr-review-toolkit:review-pr simplify
# レビュー通過後にコードを単純化
```

**並列レビュー:**
```
/pr-review-toolkit:review-pr all parallel
# すべてのエージェントを並列起動
```

## エージェント説明:

**comment-analyzer**:
- コメントの正確性をコードと照合して検証
- コメント劣化を特定
- ドキュメントの網羅性を確認

**pr-test-analyzer**:
- 振る舞いベースのテストカバレッジをレビュー
- 重大なギャップを特定
- テスト品質を評価

**silent-failure-hunter**:
- サイレント障害を検出
- catch ブロックをレビュー
- エラーログを確認

**type-design-analyzer**:
- 型のカプセル化を分析
- 不変条件の表現をレビュー
- 型設計品質を評価

**code-reviewer**:
- CLAUDE.md 準拠を確認
- バグや問題を検出
- コード品質全般をレビュー

**code-simplifier**:
- 複雑なコードを単純化
- 明確性と可読性を改善
- プロジェクト標準を適用
- 機能を維持

## ヒント:

- **早めに実行**: PR 作成後ではなく作成前
- **変更に集中**: エージェントはデフォルトで `git diff` を分析
- **重大事項を先に対応**: 低優先度より先に高優先度を修正
- **修正後に再実行**: 問題解消を確認
- **特定レビューを使う**: 懸念点が明確なら対象観点のみ実行

## ワークフロー統合:

**コミット前:**
```
1. コードを書く
2. 実行: /pr-review-toolkit:review-pr code errors
3. 重大な問題を修正
4. コミット
```

**PR 作成前:**
```
1. すべての変更をステージする
2. 実行: /pr-review-toolkit:review-pr all
3. 重大・重要な問題をすべて対応
4. 検証のため特定レビューを再実行
5. PR 作成
```

**PR フィードバック後:**
```
1. 依頼された変更を実施
2. フィードバックに応じた対象レビューを実行
3. 問題解消を確認
4. 更新を push
```

## 補足:

- エージェントは自律実行し、詳細レポートを返します
- 各エージェントは専門領域に集中して深い分析を行います
- 結果は具体的な `file:line` 参照付きで実行可能です
- エージェントは複雑度に応じた適切なモデルを使用します
- すべてのエージェントは `/agents` 一覧で利用可能です

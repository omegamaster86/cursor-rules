---
name: make-pr-easy-to-review
description: コード挙動を変えずに、履歴ノイズを減らし、説明を改善し、レビュアーガイドを追加して PR をレビューしやすくする。"make this easy to review" / "tidy this PR" / "clean up commits" / "annotate the diff" などの要求に使用。
---

# Make PR Easy to Review

レビューアーが意図、重要ファイル、リスクを素早く理解できるよう PR を整えます。デフォルトの目標は振る舞い変更なしでレビュー容易性を高めること。

## ワークフロー

1. ユーザー指定 URL または現在ブランチから対象 PR を解決。
2. コミット、差分サイズ、変更パス、生成ファイル、PR 説明を確認。
3. レビューしにくい点を洗い出す: ノイズの多いコミット、古い説明、無関係な変更、機械的変更とロジック変更の混在、テスト不足、レビュアー入口点の不明確さ。
4. 履歴改変や force-push 前に計画を提示。
5. 安全な改善を適用し、ツリー/差分が意図したコードと一致するか確認。

## 履歴の整理

ユーザー指定または計画への同意がある場合のみ履歴を改変する。改変前:

```bash
gh pr view <PR> --json title,headRefName,baseRefName,state,commits
git fetch origin <headRefName> <baseRefName>
ORIGINAL_TREE=$(git rev-parse origin/<headRefName>^{tree})
```

変更は通常、依存順にまとめる。

1. スキーマ/ストレージや生成 API 定義。
2. コアロジック。
3. 配線・統合。
4. UI / 表示の変更。
5. テスト。

改変後に内容同一性を検証:

```bash
echo "Original tree: $ORIGINAL_TREE"
echo "Current tree:  $(git rev-parse HEAD^{tree})"
git diff origin/<headRefName> --stat
```

意図せずツリーが変わった場合は push しない。

## レビュアーガイダンス

振る舞い変更なしが前提のときは PR 説明とレビュー注記を優先:

- 実際の差分に一致する TL;DR を追加。
- コアファイルと生成/機械的ファイルを分離。
- リスクの高い変更、移行順序、ロールアウト計画、テストカバレッジを明記。
- 意図説明に有効な issue、ダッシュボード、設計ドキュメントへのリンクを添付。

## ガードレール

- 意味のある振る舞い変更を「整理」の名目で隠さない。
- ユーザー明示なしにフックをバイパスしない。
- ノイズが大きく説明で改善不能なら、分割を提案し、ノイズ回避に逃げない。

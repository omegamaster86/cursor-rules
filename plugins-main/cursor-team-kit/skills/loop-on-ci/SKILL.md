---
name: loop-on-ci
description: PR チェックを監視し、緑になるまで失敗を再試行・修正する。PR 付きチェックの真実源として gh pr checks を使用。
---

# Loop on CI

## トリガー

ブランチまたは Pull Request を監視し、必要なチェックがすべて緑になるまで CI 失敗を反復対応する必要がある場合。

`gh pr checks` を真実の情報源として使う。`gh run list` は GitHub Actions 分しか扱えないため。

## ワークフロー

1. 現在のブランチに対する PR を解決。
2. 待機前に現在の PR チェックを確認。
3. 既に失敗があれば、まずそれらを診断。
4. 保留中なら `gh pr checks --watch --fail-fast` で監視。
5. push ごとに全 PR チェックを再取得し、緑になるまで繰り返す。

## コマンド

```bash
# 対象 PR を解決
gh pr view --json number,url,headRefName

# すべての添付チェックを確認
gh pr checks --json name,bucket,state,workflow,link

# 保留チェックを fail-fast で監視
gh pr checks --watch --fail-fast

# GitHub Actions ログ (失敗チェックが GHA 実行に紐づく場合)
gh run view <run-id> --log-failed
```

## ガードレール

- 可能なら各修正は 1 つの失敗原因に限定。
- `--no-verify` でフックを無効化して進捗を強行しない。
- 失敗が明確に PR と無関係で main で解決済みなら、不要な修正を PR に積まず main を取り込む。
- 不安定なら 1 回再試行し、フレーク証拠を報告。
- 各 push 後に `gh pr checks --json name,bucket,state,workflow,link` を再実行。チェック構成は変化し得る。

## 出力

- 現在の CI ステータス
- 失敗要約と適用した修正
- チェックが成功した際の PR URL

# Job: scan changes（panel 方式）

Task の `model`: [../references/task-models.md](../references/task-models.md)（workers / verifier panel）。

ブランチ差分、PR 相当の diff、または単一コミット。**未コミットの作業ツリーは含めない**。

## 引数

- `--base ref`
- `--commit sha`（チェックアウト済み）
- `--scope dirs`
- `--effort low|medium|high`

7 文字以上の hex は `--commit`。ref 名は `--base`。

## サブメニュー（変更が未指定のとき 1 問）

- このブランチの変更（merge-base から HEAD）
- 特定コミット（ユーザーが sha を渡す）
- わからない → ブランチ変更があればそれ、なければ [scan-codebase](scan-codebase.md) を提案

`gh pr list` は **ユーザーが PR 検索を明示したときだけ**（未認証なら不可と伝える）。

## 手順

1. git リポジトリ確認
2. レンジ解決・空 diff なら停止
3. コスト確認（scan-codebase 同様）
4. `CODE-SECURITY-<ts>/`、stamp: `job` `scan-changes`、`mode` `changes` または `commit`
5. 変更ファイルをグループ化（~25 ファイル/グループ、high で並列増）
6. **Researchers** — 変更行からデータフローを追う。変更が原因でない既存バグは `preExisting`
7. **Verifier panel** — scan-codebase 同様
8. レポート・redact・cleanup

## キックオフ文に含めるもの

ベース ref、変更ファイル数、effort、パネル完了まで離席可、checkout を変えないでほしい旨。



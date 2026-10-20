# Job: scan diff（investigator 方式）

Task の `model`: [../references/task-models.md](../references/task-models.md)（`code security workers`。[core-audit](core-audit.md)）。

**コミット済み**の変更のみ。`git diff <merge-base>..HEAD` または単一コミット `parent..commit`。

## 引数

- `--base ref` — ブランチ差分のベース（省略時: upstream または `main`/`master` を順に試す）
- `--commit sha` — 単一コミット（**チェックアウト済み**であること）
- `--scope dirs` — diff をディレクトリで絞る
- `--effort low|medium|high`

## 手順

1. スキャンルート解決
2. レンジ解決: `merge-base` と `HEAD`、または `sha^..sha`
3. `git diff --quiet` で変更ゼロなら終了（ディレクトリ作らない）
4. 変更ファイル一覧を stamp の `changedFiles` に記録。`job`: `scan-diff`
5. `<scanRoot>/.cursor/CODE-SECURITY-<ts>/` 作成（artifacts 同様）
6. [core-audit.md](core-audit.md) を **変更ファイル＋境界の呼び出し先**に限定。`mode`: `changes`
7. 変更と無関係な既存問題は finding にしない（coverage.preExisting）
8. レポート提出

変更が 300 ファイル超（high では 600）なら、[scan-codebase](scan-codebase.md) または [scan-repository](scan-repository.md) を推奨する一文を RESULTS に入れる。

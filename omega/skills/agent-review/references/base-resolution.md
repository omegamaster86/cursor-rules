# base ブランチ解決（フェーズ 1）

レビュー差分は **`<base>...HEAD` のコミット済み三点差分**（`git diff <base>...HEAD`）。`@{upstream}` は使わない。

## 優先順

1. **`change_scope.base_branch`** — ユーザーまたは起動コンテキストで明示された ref（例: `origin/main`）
2. **HEAD を切ったブランチ** — 下記「切り出し元の検出」
3. **フォールバック** — `origin/develop` があればそれ、なければ `origin/main`

Open PR の `baseRefName` は **使わない**（PR の base と切り出し元が違うことがあるため）。

## 切り出し元の検出

現在ブランチ（`git branch --show-current`。detached のときは `HEAD` の reflog）から、**このブランチを作ったときの元 ref** を取る。

1. `git reflog show -n 50 <current-branch>` を古い方から見る（`--reverse` または末尾から最初の該当行）。
2. 次のいずれかにマッチする **最も古い** 行の元 ref を採用する:
   - `branch: Created from <ref>`
   - `checkout: moving from <ref> to <current-branch>`
3. `<ref>` がコミット SHA のとき: `git name-rev --refs=refs/heads,refs/remotes <ref>` でブランチ名に寄せる。
4. ローカルブランチ名だけのとき: 同名の `origin/<name>` が `git rev-parse --verify` で有効なら **`origin/<name>`** を base にする（なければローカル ref のまま）。
5. 検出できない・`ref` が現在ブランチ自身のとき: 優先順 3 のフォールバックへ。

検出結果を `base_branch` としてレーンに渡す。Security レーンの `Base Branch:` も同じ ref。

## 差分取得（親）

- `git diff --name-only <base_branch>...HEAD`
- `git diff <base_branch>...HEAD`
- `git diff --stat <base_branch>...HEAD`
- `git status --short`（未コミットは対象外の確認のみ）

**レビュー対象はコミット済み差分のみ。**

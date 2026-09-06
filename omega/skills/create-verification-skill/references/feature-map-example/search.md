# 一覧を検索する

ユーザーがタイトルまたは本文で案件を探し、ヒットを開き、ヒットなしと検索不能を区別できる。

## Sub-features

- `search-open` はサポートする入口から検索を開く。
- `search-match` はデータを変えずに一致を返す。
- `search-empty` はヒットなしの完了状態を出す。
- `search-clear` はクエリを消し一覧を戻す。

## How to get to it (user POV)

- ツールバーの検索。
- 一覧ページの検索ボックス。

## Driving it with browser MCP

Preconditions:

- アプリが healthy。
- seed にタイトル `Quarterly plan`、本文 `Draft budget` がある。

- **Open.** 検索を開く。searchbox にフォーカスがある。
- **Title match.** `quarterly` を入れる。結果に `Quarterly plan` があり、無関係な seed は無い。
- **Empty.** `volcano` を入れる。ヒットなしの status が検索完了後に出る。
- **Clear.** クリアする。searchbox は空、通常一覧に戻る。
- **Proof.** ヒットあり状態の ARIA snapshot と screenshot を `artifacts/search/` に残す。

## Gotchas

- debounce 後の結果リストまたは empty status を待つ。固定 sleep にしない。
- 結果を開くとブラウザ状態が変わる。別クエリの前に検索を開き直す。

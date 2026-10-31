# Search notes

Search はユーザーが title または body テキストで note を見つけ、match した note を inspect し、match なしと search 不可を区別できる。

## Sub-features

- `search-open` はサポートされる各 browser entry point から search を開く。
- `search-match` は note data を変えず title と body match を返す。
- `search-open-result` は結果を note editor で開く。
- `search-empty` は match なし query の完全 empty state を示す。
- `search-clear` は query を除去し recent-notes view を復元する。
- `search-cli` は terminal から同じ match note を返す。

## How to get to it (user POV)

- browser toolbar の `Search` ボタンを選ぶ。
- editable field 外に focus がある browser で `/` を押す。
- terminal で `notes search <query>` を実行。

## Driving it with control-notes

Preconditions:

- Notes は `http://127.0.0.1:4173` で healthy。
- disposable data directory に body `Draft budget` の `Quarterly plan` がある。
- `control-notes doctor` が期待 URL と data directory を報告。

- **Toolbar entry.** `Search` ボタンを選ぶ。`control-notes browser click --role button --name "Search"` を実行。`Search notes` という dialog が出て searchbox に focus。
- **Keyboard entry.** dialog を閉じ、page に focus し `/` を押す。`control-notes browser press --key "/"` を実行。同じ dialog が出て page に slash は入らない。
- **Title match.** `quarterly` を入力。`control-notes browser fill --role searchbox --name "Search notes" --value "quarterly"` を実行。`Search results` リストに `Quarterly plan` があり `Grocery list` はない。
- **Body match.** query を `budget` に置換。`control-notes browser fill --role searchbox --name "Search notes" --value "budget"` を実行。結果 `Quarterly plan` が body-match excerpt 付きで見える。
- **Open result.** `Quarterly plan` を選ぶ。`control-notes browser click --role link --name "Quarterly plan"` を実行。dialog が閉じ editor heading は `Quarterly plan`。
- **Empty state.** search を再開し `volcano` を入力。`control-notes browser fill --role searchbox --name "Search notes" --value "volcano"` を実行。search 完了後 `No matching notes` という status。
- **Clear query.** `Clear search` を選ぶ。`control-notes browser click --role button --name "Clear search"` を実行。searchbox は空で `Recent notes` region が result list に代わる。
- **CLI match.** terminal から search。`control-notes cli -- notes search "quarterly" --format json` を実行。exit code `0` と stdout に title が `Quarterly plan` の object が 1 つ。
- **CLI miss.** 無い値を search。`control-notes cli -- notes search "volcano" --format json` を実行。exit code `0` と stdout は `[]`。
- **Proof.** 結果が入った state を capture。`control-notes browser snapshot --aria --path artifacts/search/results.aria.txt` と `control-notes browser screenshot --path artifacts/search/results.png` を実行。両 artifact が Notes、query、`Quarterly plan` を同定。

## Gotchas

- editor または searchbox に focus があるとき `/` は search を開かず text を挿入する。
- 結果は短い debounce 後に更新。固定 sleep ではなく results list または empty status を待つ。
- archived note はユーザーが `Include archived` を有効にしない限り除外。
- CLI は human-readable 出力がデフォルト。安定 assertion には `--format json`。
- 結果を開くと browser state が変わる。別 query を証明する前に search を再開。

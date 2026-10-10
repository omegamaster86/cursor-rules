# Notes verification map

この directory は Notes の user-facing 振る舞いを verify する maintained source。app を drive する前に index を読み、該当 feature file を recipe として使う。

## Baseline preconditions

- disposable data directory で Notes を `http://127.0.0.1:4173` で起動。
- 並行 run が state を共有しないよう `NOTES_DATA_DIR=/tmp/notes-verify-$RUN_ID` を設定。
- タイトル `Quarterly plan` と `Grocery list` の note を seed。
- `control-notes` と `notes` CLI を `PATH` に。
- `control-notes doctor` を走らせ、期待 URL、data directory、build revision を要求。
- この verification run が起動していない instance は drive しない。

## Driving conventions

- precondition が別に言う場合を除き、各 recipe は baseline state から開始。
- CSS selector や DOM 位置より ARIA role と accessible name を優先。
- 各 command を literal として扱う。引用名と flag は変えない。
- browser action は `control-notes browser` 経由。
- terminal action は `control-notes cli -- <command>` 経由。
- mutation 後は seed data を復元。cleanup で proof artifact は除去しない。

## Proof and skip reporting

- 最終画面だけでなく user action と結果 state を capture。
- UI proof は ARIA snapshot と app identity が見える screenshot を含む。
- CLI proof は command、stdout、stderr、exit code を含む。
- mutation proof は保存値の read-only 2 番目の view を含む。
- 各 artifact に feature ID と使った entry point を記録。
- 到達不能 path は試した command と満たされなかった precondition で report。
- 別 path で verified と報告しないで skip した entry point を報告しない。

## Feature entry contract

各 feature file は H1 タイトルと user-visible 振る舞いを述べる 1 段落で始める。次にこの順で exactly 4 つの H2 節。

1. `Sub-features` は各振る舞い 1 行の短い ID を列挙。
2. `How to get to it (user POV)` はすべての user entry point を列挙。
3. `Driving it with <harness>` は `Preconditions:` で始め、各 user action を exact command と observable result の labeled bullet で pair。
4. `Gotchas` は verification run を浪費または無効化しうる trap を列挙。

map から implementation 詳細を除く。user path、stable handle、必要 state、command、observable proof だけを名指す。

## Features

- [Create a note](./create-note.md) は browser/CLI 作成、cancel、persistence、cleanup を cover。
- [Search notes](./search.md) は toolbar、keyboard、CLI search と match、empty、clear state を cover。

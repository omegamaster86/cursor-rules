# 案件を作成する

ユーザーがタイトル付きの案件をブラウザから保存し、未完成ドラフトを捨て、第二の画面から保存内容を確認できる。

## Sub-features

- `create-open` は各ブラウザ入口から空の作成フォームを開く。
- `create-save` はタイトルと本文を永続化する。
- `create-cancel` は未保存ドラフトを捨てる。

## How to get to it (user POV)

- 一覧の `新規作成` ボタン。
- `/items/new` を直接開く。

## Driving it with browser MCP

Preconditions:

- アプリが `http://127.0.0.1:3000` で healthy。
- タイトル `Release checklist` の案件は無い。
- Doctor が期待 URL を報告している。

- **Open editor.** `新規作成` を選ぶ。作成フォームが現れ、`タイトル` テキストボックスにフォーカスがある。
- **Enter content.** タイトル `Release checklist`、本文 `Tag and publish`。`保存` が enabled になる。
- **Save.** `保存` を選ぶ。成功ステータスが出る。見出しが `Release checklist`。
- **Confirm persistence.** 一覧に戻り、同じタイトルの行を開く。両方の値が残っている。
- **Cancel draft.** 新規を開き `Discard me` と入れて `キャンセル`。一覧に `Discard me` が無い。
- **Proof.** 一覧の ARIA snapshot と screenshot を `artifacts/create-item/` に残し、`Release checklist` が見えること。

## Gotchas

- 保存ステータスだけでは不足。一覧から開き直す。
- タイトルは trim される。draft 入力値ではなく表示タイトルを assert する。
- fixture の `Release checklist` は cleanup で消してよい。proof 成果物は残す。

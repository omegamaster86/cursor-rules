# 案件 verification map（形の見本）

生成する feature map の契約見本。Notes / control-* 前提ではない。対象 PJ では観測した起動・ハンドル・コマンドに置き換える。

インデックスを読んでからアプリを drive し、該当 feature ファイルをレシピにする。

## Baseline preconditions

- アプリを検証用 URL で起動する（例: `http://127.0.0.1:3000`）。
- 可能なら disposable なデータ（別ポート、seed ユーザー、scratch DB）を使う。
- Doctor が URL・リビジョン・auth を期待どおりと報告してから drive する。
- この検証 run が起動していないインスタンスは drive しない。

## Driving conventions

- レシピは baseline から始める（feature が別 preconditions を書く場合を除く）。
- CSS 位置より ARIA role / accessible name / ルートパス。
- コマンドは literal。引用符とフラグを変えない。
- Web は既存 Playwright、無ければブラウザ MCP。API は curl。
- mutation 後は seed を戻す。proof 成果物は cleanup で消さない。

## Proof and skip reporting

- 最終画面だけでなく、ユーザー操作とその結果状態を残す。
- UI proof は ARIA snapshot と、アプリ識別が分かる screenshot。
- mutation proof は保存値の第二の読み取り（一覧の再オープン、DB/API GET）。
- 到達不能は試した経路と足りない前提を報告する。別経路での成功をその entry の verified にしない。

## Feature entry contract

各 feature ファイルは H1 と、ユーザーに見える振る舞いの1段落。続いて次の4つの H2 をこの順だけ。

1. `Sub-features` — 短い ID と1行。
2. `How to get to it (user POV)` — ユーザーの入口すべて。
3. `Driving it with <harness>` — `Preconditions:` のあと、ユーザー操作とコマンド・観測を対にした箇条書き。
4. `Gotchas` — 検証を無効にする罠。

実装詳細は書かない。ユーザー経路、安定ハンドル、必要な状態、コマンド、観測可能な proof だけ。

## Features

- [案件を作成する](./create-item.md) — フォーム送信、キャンセル、永続化の確認。
- [一覧を検索する](./search.md) — 一致・空・クリア。

---
name: create-verification-skill
description: "プロジェクト固有の動作確認スキルを生成する。アプリをユーザーと同じ操作で起動・操作・証拠取得できるようにする。/create-verification-skill、「verify スキルを作って」、PJ に UI/CLI/API を証明する手順が無いときに使用。"
disable-model-invocation: true
---

# Create a verification skill

対象 PJ に、**ユーザーが触る面をスクリプトで証明する** スキル（`.cursor/skills/verify-<app>/`）を生成する。次のエージェントがアプリを知らない状態で読めるように書く。人間向け README ではない。

**今回の変更が終わったか** は **`/verify-done`** が正本。本スキルは、その Tier D（UI フロー）で毎回手順を invent しなくて済む土台を残す。

`cursor-team-kit` の `control-*` は **未導入なら使わない**。既存 harness（Playwright 等）→ ブラウザ MCP → curl/HTTP の順。

## 1. リポジトリをインタビューする（ユーザーには観測できないことだけ聞く）

- **Surface:** Web UI、CLI、API、複数なら主面を1つ選び残りを注記。
- **Run:** ドキュメント済みの起動コマンド（`package.json` scripts、README）。ポート、env、seed、auth。
- **Drive:** 既存の Playwright / Cypress / curl 可能な endpoint を先に使う。無ければブラウザ MCP（web）、HTTP（service）。
- **Observe:** スクリーンショット、ARIA snapshot、レスポンス、ログ、exit code、DB 状態。
- **Isolate:** 2 インスタンスを並べられるか（ポート、データ dir）。無理ならスキルに「ユーザーのセッションを二重 drive しない」と書く。

チェックアウトが起動しないなら、スキル生成の前に起動を直す（または正確に報告する）。

## 2. スキルを生成する

`.cursor/skills/verify-<app>/SKILL.md` に YAML frontmatter（`name: verify-<app>` と、アプリ名・surface・いつ使うかの `description`）と、観測に根ざした次の節を書く（プレースホルダ禁止）:

- **Launch:** 検証用の起動コマンドと ready 判定、teardown。短命 CLI はサーバ常駐なし。
- **Doctor:** 「このインスタンスを drive してよいか」の read-only チェック（プロセス、ポート、auth）。
- **Drive:** このリポの安定ハンドル（ARIA、data 属性、ルートパス）。座標や tab 順は避ける。
- **Evidence:** ユーザー経路を走ること。内部 setter や test-only endpoint だけは不可。操作とその結果状態、副作用（行追加、ファイル）も。proof の保存場所を名指しする。
- **Cleanup:** 自分が始めたものだけ止める。プロセス名 kill 禁止。証拠は消さない。
- **Helpers:** 同梱スクリプトは実行可能で、呼び出しをスキル本文に書く。

## 3. feature map を seed する

`.cursor/skills/verify-<app>/features/README.md` と、ユーザー向け機能ファイル（最初は 3〜5。ルート・メニュー・docs から）。形は [`references/feature-map-example/`](references/feature-map-example/)。各ファイルの H2 は順に `Sub-features`、`How to get to it (user POV)`、`Driving it with <harness>`、`Gotchas`。実装詳細は書かない。

## 4. 生成物を自分で証明する

Launch → Doctor → **mapped feature を 1 つ** Drive → Evidence → Cleanup。cleanup 後も証拠が残ること。失敗イテレーションも cleanup する。未実行の下書きは成果物にしない。

## 5. メンテを案内する

`/maintain-verification-skill` で map をアプリに追従させる。cadence は聞かれたときだけ。

## `/verify-done` との関係

| | 本スキル | `/verify-done` |
|--|--|--|
| いつ | PJ に証明レシピが無いとき（導入） | 今回の変更の完了宣言前 |
| 成果物 | `verify-<app>` + feature map | PASS / FAIL レポート |

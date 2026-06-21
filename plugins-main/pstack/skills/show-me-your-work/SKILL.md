---
name: show-me-your-work
description: "長時間または無人作業の監査可能な決定証跡を残す: 決定ごとに 1 行の TSV ログ（何を、なぜ、証拠、結果）。デフォルトはローカル。レビュアーが結果を信頼するために証跡が要るときだけコミット。/show-me-your-work、自律・多フェーズ実行、人が離席後にレビューする作業に使用。"
disable-model-invocation: true
---

# Show me your work

人が事後にレビューする作業では、決定証跡があれば、作業を再実行したり全トランスクリプトを読まずに、何が決まり、なぜ、どんな証拠に基づいたかを再構成できる。正規ログを 1 つ保ち、証跡を一貫させ、将来のエージェントが見つけられるようにする。

## 形式

TSV ファイル 1 つ、決定ごとに 1 行。TSV なのは GitHub がソート可能な表として描画し、`column -s$'\t' -t` とスプレッドシートが読め、1 コマンドで行を追記できるから。セルは 1 行。証拠はポインタであり文章ではない。

クリーンなログ開始には `references/decision-log-template.tsv`（ヘッダ行）をコピー。列:

- **ts.** ISO8601 タイムスタンプ。タイムライン軸。
- **phase.** フェーズまたは作業ストリーム。
- **decision.** 選ばれたこと・行ったこと、1 行。
- **why.** 平易な理由。原則が動いたなら平易に（`explored options first, this was a one-way door`）。専門用語タグではない。
- **evidence.** 証明するリンクまたはパス: コミット SHA、PR 番号、`file:line`、成果物・トレース・スクリーンショットパス。段落は書かない。
- **result.** 結果または述語状態: `tests green`、`reverted`、`pixel-diff 0`、`INCONCLUSIVE`、`open`。

例。レビュアーが一目で読める平易な例。これは説明のみ。実ログにこれらの行をコピーしない。

```
ts	phase	decision	why	evidence	result
2026-05-24T09:02:00Z	frame	counted the work first, about 100 components and roughly 75 hours	wanted to know the size before starting a long run	commit 3a9f1c2	found 5 things to sort out before starting
2026-05-24T09:40:00Z	harness	took screenshots of the old version before changing anything	so we can compare old against new and catch any visual change	scripts/snapshot.sh, baseline/	saved 120 reference screenshots
2026-05-24T11:15:00Z	widget	moved the widget styles over without changing how it looks	keep the change small and the result identical	commit 7c21e0a, pixel-diff 0	looks identical, tests pass
2026-05-24T12:30:00Z	widget	threw out a helper's work because its screenshots were blank	checked the real files instead of trusting its summary	worktree reset	reverted, tightened the instructions for next time
```

## 行をログする

各エントリは同僚に何をしたか伝えるように書く。平易な言葉、具体的行動、AI 口調や抽象ジャーゴンなし（ログ文にも **unslop** スキルが当てはまる）。レビュアーは各行を解読せず理解できる。

行を整形式に保つヘルパーを使う: `scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>`。`ts` を打刻し、初回にヘッダを書き、余分なタブ/改行を除去し、`=`, `+`, `-`, `@` で始まるセルには先頭に単一引用符を付け、スプレッドシートで式実行を防ぐ。素の `printf` で行追記も可。生成・ユーザー供給テキスト由来セルでは同じバイトに注意。

決定点とチェックポイントをログし、すべての行動ではない: 選んだ分岐、検証結果付き完了ユニット、トリガー付きピボット/リバート、表面化したブロッカー、修正したゲート。ループ実行では反復ごとに 1 行。自明・些細はスキップ。

## 置き場所

デフォルトではログは作業成果物でありコミットしない。作業 dir の `decisions.tsv`、複数同時なら `.audit/<task-slug>.tsv`。git から外す。大半の作業はコミット証跡不要。ローカルログでも実行を正直に保ち、後で捨てられる。

レビュアーが結果を信頼するために証跡が要る野心的作業だけコミット: 大規模クロス言語移植、数週マイグレーション、信頼を示さねばならないもの。コミット済みログは PR で表として描画される。

## ルール

- 1 行は 1 決定またはチェックポイント。1 行に収まらないなら決定がまだ鮮明でない。
- 追記のみ。誤りは上書きする新行。履歴を編集・削除しない。
- 手作り one-off よりコミット済みスクリプトが生成した証拠を優先し、レビュアーが再実行できるようにする（**encode-lessons-in-structure** 原則スキル）。

## トランスクリプトに対してログを監査する

実行終了時、返す前にログが真実を語ったか確認。この実行のトランスクリプトをアクティブワークスペースの `agent-transcripts/`（システムプロンプトがパスを名指す）で読む。`~/.cursor/projects/*/` を glob しない。無関係な非公開チャットを読む。実際に起きたこととログを照合:

- 各行は実際の行動に対応。捏造・願望的エントリは削る。
- 各行の証拠は解決し、行が主張することを示す。
- 作業を形作ったがログにない分岐・ピボット・放棄アプローチはギャップ。追加する。
- パディングを落とす。誰も監査しない行は居場所を稼がない。

物語ではなくログを直す。作業が行の主張とずれたら、行が間違い。

## 証跡のクロスモデルレビュー

返す前に、作業をしたモデルと別モデルファミリのサブエージェントを必ず起動する。自己レビューは代替にならない。自分では持てない新鮮な目が目的。サブエージェントは監査証跡と実行トランスクリプトを読み、ユーザーが注意すべきことを旗立てる。作業のやり直しではなく、最適でない・リスクのあるもののスキャン。

- 弱いまたは欠如した証拠でログされた決定。
- スキップまたはトランスクリプトに証明なく主張された検証ステップ。
- 後知恵でリスクに見える選択（時期尚早、スコープ肥大、症状のごまかし）。
- ざっと読むと見逃すギャップ。

証跡を産出した実行の各返答は "Attention" 節で終える。レビュアーのモデルを単独行で先頭に（`reviewed by <model>`）、各フラグは特定行または瞬間を指す。「No flags」は有効。モデル名だけは不可。自己監査はログが真実を語ったかを問う。これは真実でもユーザーがまだ精査すべきことを問う。

## 証跡のレビュー

上から下へ読み、証拠ポインタを辿り、スポットチェック。コミット済み TSV は GitHub が表として描画。`column -s$'\t' -t decisions.tsv` で端末表示。証拠が解決しない行、または未検証の result は監査がギャップを捕まえた。

## このスキルの合成

他スキルは独自を作らず監査証跡をここにルーティング。名前で参照し、形式はここが所有。列を言い換えない。

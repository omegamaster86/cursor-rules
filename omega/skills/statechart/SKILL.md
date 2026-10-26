---
name: statechart
description: "製品フロー・プロトコル・サービスなどの状態遷移を TLA+ から Mermaid statechart で描く。各バグはルールを破る状態への番号付き青枠パス。/statechart、バグの経路可視化、合意チャートから TLA+ 骨格。"
disable-model-invocation: true
---

# Statechart

チャートは、読む人の言葉でシステムが状態間をどう動くかを示す。script は読者を `readerActions` や reader ステップと呼ぶ。読者が振る舞いが正しいか判断する。読者はアプリの「支払い中」画面を読む PM、ロックサービスの「リース保持・書き込み待ち」を読むエンジニア、設計を読む reviewer でもよい。状態ラベルは読者が観察できる・気にすること。ステップラベルは動かすイベント（「Pay をタップ」、サービスの「リクエストが count を読む」、ロックの「リース期限切れ」）。ラベルに変数名や action 名は入れない。

`node <skill dir>/scripts/statechart.mjs --help` でコマンドとチャートの読み方。repo 外の scratch で作業。コマンドは入力の隣にファイルを書く。初回は mise で TLC と Java を入れる（約 305 MB、ネットワーク要）。help の TLC 節で既存 TLC/Java の使い方。

## 方向を選ぶ

`from-spec` — TLA+ がある、またはコード・設計が十分具体。`from-chart` — モデルが無く、振る舞いの owner が先に合意すべきとき。

コードに TLA+ があるなら spec のコピーから。ラベルとルールに要る変数を足し、既存 invariant は保つ。コードを spec に対して audit するなら、コピーはコードの振る舞いをモデル化し、spec は `--against` で無変更。作者の通る config を `--against-config` で渡す（ファイル名が spec 名のときは省略可）。1 mapping が両モデルにラベル。片方にしか無い変数を読むラベルは `"name" in v` を先に。spec 側は別ラベル。コード記述モデルでは各変数・action を reviewer が開けるコードに結び、action 名はコードから。各 action はコードの不可分割 1 ステップ。条件ごとにコードの file:line をコメント（例 `\* pay.ts:120`）。

## Spec → chart

1. チャートの状態を選ぶ。ラベルが隠すならラベルに入れる（二重請求後も画面が「支払い中」など）。少なく始め、バグを分ける分割やラベル同じで読者が見るべきステップが要るとき分割。
2. 読者が合意するルールを invariant 1 つずつ。読者の文をコメント。画面、レスポンス、保存値、メッセージなど任意の状態について。コード記述なら状態を変えうるコードも名指す。ルールの対象変数が無ければ追加。ルールは落とさない。落ち着き後だけのルールは `Settled == ~ENABLED System`（`System` は読者無しで起きる action の和）。狭い点のルールはその点の predicate。到達目標は「起きない」ルールで書き `--expect-broken`。破るパスが到達経路。`stories.md` で各 goal rule を名指す。他の破れは bug として報告。チャートを通すためにルールを弱めない。
3. `from-spec`、mapping の `state` / `step` を埋める。読者操作と周囲を分けるなら `readerActions` に action 名。空なら全 action 同扱い。overview が大きいなら `--cover`（各 settled への最短＋全 bug path、省略リスト付き）。同状態・別理由の bug は `cause`。読者の関心で色分けなら `group` から返す。
4. 修正案があれば `--fixed` でそのモデル。
5. 各チャート `--png`、番号パスを順に読む。ラベルがコード臭なら `state`/`step` を直して再実行。
6. コード記述なら各 bug story を実コードで replay（テストまたは live repro、モデル action 1 ステップずつ）。ユーザー・クライアント・他システムが届く入口だけ drive、観察できることだけ assert。フラグを自分で立てて assert やソース全文検索は証明にならない。一部は実行・残りはコード読みならどちらが何を証明するか述べる。import できないコピーは commit と行範囲、省略を列挙。再現しなければモデルが誤りとみなしルールではなくモデルを直す。コード無し設計なら TLC trace が evidence、引き渡しに明記。

## Chart → spec

1. 読者が合意するチャート。独立に動く部分ごと region。ルールごと `%% never` と読者の文。停止・再起動は次状態への edge。`render CHART.mmd` で PNG。
2. `from-chart`。ルールが破れれば設計 bug。合意者に戻す。
3. 実コードの guard・変数を spec に足し再 `from-chart`。差分ごとにコード誤りかチャート修正か読者に確認。

## 引き渡し

各チャートの PNG と Mermaid を決定者に。bug ごと 1 行：破るルール、チャート番号の手順、再現したか、修正案が直すか。PROPERTY 破れにチャート上パスが無いなら `stories.md` の TLC counterexample。`--against` なら spec に既にあるか（`stories.md` の config、spec の除外メモ、無し）。コード記述で条件に file:line が無いのにルールが成り立つと報告しない。引用する数は `summary.json` から。`stories.md` と再生成コマンドを添付。モデルの除外を述べる。

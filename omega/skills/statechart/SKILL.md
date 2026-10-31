---
name: statechart
description: "製品フロー・プロトコル・サービスなどの状態遷移を TLA+ から Mermaid statechart で描く。各バグはルールを破る状態への番号付き青枠パス。/statechart、バグの経路可視化、合意チャートから TLA+ 骨格。"
disable-model-invocation: true
---

# Statechart

チャートは、読む人の言葉でシステムが状態間をどう動くかを示す。その読者（reader）が振る舞いが正しいか判断する。

## 実行

repo 外の scratch で作業する。TLA+ spec と config を書き、次を実行する。

```sh
<skill dir>/scripts/statechart SPEC.tla [--config FILE] [--view FILE] [--out DIR]
```

`scripts/statechart.ts` は TypeScript なので、TypeScript を実行できるランタイムで動かす。

初回実行は mise で TLC と Java を入れ、ネットワークが要る。

## Spec を書く

- 読者が合意するルールを INVARIANT として 1 つずつ書く。画面、結果、保存値、メッセージなど任意の状態について書ける。ルール用の変数が無ければ追加する。ルールを弱めて成立させない。
- `Next` は action の disjunction にする（例: `YouPressPlay \/ YouPressStop`）。そうしないと TLC は各ステップを `Next` と名付ける。
- 出矢印の無い状態は `NoDeadlock` を破る（正しい終端状態でも同様）。同名の INVARIANT または PROPERTY があるときはルール名は `CHECK_DEADLOCK`。終端状態だけで真になり何も変えない action を `Next` に足し（例: `Done == phase \in {"paid", "failed"} /\ UNCHANGED vars`）、`step()` でラベルを付ける。

## チャートを選ぶ

判断が要る作業はエージェント側: 各状態・矢印の言葉、フェーズと色、タイトル、読者向けレポート。view モジュールに書き、`--view` で渡す。

読者の言葉を出すには view が `state(vars)` を export する。戻り値の形でチャート形式が決まる。

- 文字列 → フラット: `export const state = (v) => (v.paid ? "Paid" : "Paying");`
- 配列 → 親状態: `export const state = (v) => v.main.split(".");`
- オブジェクト → キーごとに並行 region: `export const state = (v) => ({ Playback: v.playback, Volume: v.volume });`

状態ラベルは読者が見える・気にすること（「Paying」「Lease held, write pending」）。変数名はラベルに入れない。`vars` では TLA+ sequence は 1 始まりキーのオブジェクトなので `v.pc[1]` は `pc[1]`。set は配列。

view は `step(action, from, to)` も export できる。TLC の action 名とステップ前後の値を受け、矢印ラベルを返す。ユーザーに見える出来事として書く（「you press play」「the connect fails」）。コード名や TLA+ action 名を書かない。チャート上同じ終わり方の action は同じラベルにして 1 本の矢印を共有する。

ステップが条件付きだけのとき、読者の言葉で `[...]` をラベル末尾に付ける（例: `you press play [while the file loads]`）。regions チャートでは、他 region の条件をその region のラベルの言葉で矢印に書く（例: `[when Offline]`）。角括弧はそれを置き換え、同じ見た目の 2 本の矢印になりうる。regions チャートでは **他 region の条件を角括弧で書かない**。ラベルに出ない値が分岐を決めるときは結果をラベルに書く（例: `the roster read fails`）。

さらに export できるもの:

- `group(vars)` — フェーズ名。各チャート状態は group の色を付ける。1 ラベルの背後の model 状態が異なる group なら色なし。
- `colors` — group 名から CSS class。
- `title` — チャート上部の文字列。

コマンドは model 状態ごとに `state()` と `group()` を高々 1 回、ステップごとに `step()` を高々 1 回呼ぶ。チャートとレポートはその答えだけを使う。各関数は引数だけに依存させる。

同じラベル内に留まるステップは描かない。読者が見る必要があるならラベルを分割する。

矢印はおおよそ 20 本以下を目標。まず `state()` を粗く。同じ振る舞いの値は 1 ラベルにまとめ、読者に不要な詳細（戻りが何も変えない in-flight など）は落とす。バグ path の各状態と各 mark は残す。merge で `breaks` が `mayBreak` になると、どこでルールが破れるか隠れる。異なるルールを破る 2 状態は merge しない。まだ busy なら、不要なステップ（全状態にある reset、他矢印と同じ意味のステップ）で `step()` が `null` を返して隠してよい。隠すときのルール:

- 各チャート状態は開始状態から矢印で到達可能。
- model で出矢印があるチャート状態には、少なくとも 1 本出矢印を残す。
- 1 本の矢印のステップは全部隠すか、全部残す。一部だけ隠すと条件が狭くなる。
- 引き渡しで、チャートが隠したステップを述べる。

## レポートを読む

- ルールを破る状態は class `breaks`。背後の model 状態の一部だけが破るときは `mayBreak`。Legend は mark ごとのルール名。2 ルールが破れるときは 1 mark に両方の名前が出るので、引き渡しでどの状態がどのルールか述べる。regions チャートでは、その組み合わせの region 状態すべてがルールを破れうるとき mark が付く。組み合わせが破れうるのに mark が無いなら、その組み合わせの各状態に mark。
- TLC はルールを破った状態を通過するので、チャートはバグの後の状態も示す。
- バグを通過するため、状態数に上限の無い model は終わらないことがある。定数を小さくするか CONSTRAINT を足す。
- VIEW または SYMMETRY があると、TLC が同一視する状態は 1 つに数えられ、チャートも 1 状態で描く。矢印は到達先ではなくその状態へ向かうことがあり、レポートがそう言う。
- CONSTRAINT または ACTION_CONSTRAINT を過ぎた状態では TLC はルールをチェックするが、その状態を探索したり deadlock を見ない。ルールへの最短 path がそこで終わるとき、チャートはその状態を描き、レポートが path を出す。bound より先の他状態は描かない。その状態の deadlock は出ない。ACTION_CONSTRAINT で除外されたステップの後も TLC はルールをチェックする（別経路で次状態に着いても）。最短 path がそのステップで終わるとき、チャートはそのステップを描く。
- コマンドは書かれた config のまま 1 worker で TLC する。ルールが破れたらそのルールを外して TLC を繰り返し、破れが無くなるまで。最初の破れの後、各 run は distinct 状態 100,000 で止め、巨大 model の無限実行を防ぐ。bound または error で止まった run があるルールはレポートの "Rules not checked" に載り、チャートに mark しない。未チェックのルールは成立も破れもありうる。チェックするには破れているルールを config から外すか model を小さくする。bound は変数順を変える module を足すので、property の counterexample は bound 無し run と異なりうる。
- `tlc.out` は書かれた config で TLC が出したもの。破れたルールの bug path がチャートに無いとき、`tlc-RULE.out` はそれを見つけた run の出力。TLC が最初の warning を 2 回出すとき、plain TLC は 2 行だが `tlc.out` は 1 行（このコマンドが読む出力に 2 行目が無い）。Java が `-XX:+UseParallelGC` のときだけ。それ以外は TLC のその flag 勧告が 1 回だけ出る。

## チャートを見せる

`chart.mmd` を `mermaid` コードブロックで見せる。チャートは config のまま TLC で数えた 500 状態の budget がある。それを超えると、破れるルールへの path だけ描く。破れが無いとき `chart.mmd` は書かない。各ルールはまだチェックし、レポートに状態数と各 bug path がある。全体グラフを見るには model を小さくする。

画像化は Pele。ユーザーが画像を求める、またはテキストでは読めないほど大きいときは `references/render.md` に従う。ユーザーが別 renderer を求めない限り、他を使わない。

## 引き渡し

決定者に各チャートと Mermaid テキストを渡す。バグごとに 1 行: ルール、そのルールの読者向け文、レポートが付けた番号の path。model が省いていることを述べる。新しい `--out` フォルダでファイルを再生成するコマンドを添える。

model がコードを記述しているとき、各 bug path を実コードで replay する（テストまたは live repro、action 1 ステップずつ）。バグが起きなければ、証明するまで model が誤りとみなす。

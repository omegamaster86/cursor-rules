---
name: benchmark-checklist
description: "報告・意思決定の前に perf 計測を vet（limiter、チューニング、物理上限、error、再現性、end-to-end 妥当性、work が実行されたか）。ベンチ実行時、または自分で測った speedup / regression を述べるときに使用。"
disable-model-invocation: true
---

# Benchmark checklist

自分で出す performance 数字（PR の before / after、regression 主張、hillclimb harness、ライブラリや設定の選択）に使う。**なぜ** は `forge-mode/principles/explain-the-number.md`。各問いは run からの evidence で答える。コードを読んだ guess では答えない。

ユーザーが求めた quick ballpark なら 1 run でよい。それでも問い 4 と 7 は確認し、「1 run」と明記する。選択肢の比較は ballpark ではない。

## 実行前

- 出荷する言葉で期待する主張を書く（例:「60k 行データセットで p50 export が 30% 速い」）。問いはその文をテストする。
- 計測スクリプトを読む。何を時間計測し、何を数え、何を無視するか。
- `uptime` と `nproc` で load と core 数を確認。busy なら原因を特定。止められなければ両側を interleave し、report に書く。

## 問い

1. **なぜ 2 倍にならない？** limiter を名指す。report に載せる run では profiler を付けない（profiler は遅くする）。`top` / `pidstat`、runtime profiler（`node --cpu-prof`、`py-spy`、`perf`）、I/O wait、`strace -c`（Linux）。hot spot を source にマップ。load generator も見る。先に飽和していれば load generator を測っている。数字が動かなかったら limiter が理由なので、「無意味」と言う前に特定する。
2. **チューニング済みか？** 各側を production と同じ条件で走らせる（release build、本番 flag / env、batch / transaction、pool、cache の warm / cold、version と data）。片側が default だけなら実装比較ではなく設定比較。limiter が設定（row ごと commit、debug build、index 欠落）ならその側は未チューニング。チューニングして再計測してから勝者を選ぶ。チューニングできないならその run から勝者を選ばない。
3. **物理上限を破っていないか？** 算術する。bytes/s と disk / network 带宽、ops/s × op コストと core 数。節約時間と変更片の時間を比較。10% の片を消せば run はせいぜい約 11% 速くなる。上限超えは cache、no-op、bug など別物を測っている。
4. **error は出たか？** 失敗と非成功レスポンスを数え、出力が正しいか（存在だけではない）確認。error は success と挙動が違う。reject は速く、timeout / retry は遅い。スクリプトが数えないなら数を足す。
5. **再現するか？** 各側 5 回以上、交互（A,B,A,B,…）。warmup、lazy init、cache、drift で片側有利にならない。median と range を報告。run 間 variation より小さい差は「測定不能」。接戦なら rank-sum または harness 統計。
6. **end-to-end で意味があるか？** micro 結果の隣で、ユーザーが待つ path を realistic data / concurrency で測る。micro は全体に対する share を報告。request の 1% の helper は helper がどれだけ速くても request は 1% しか速くならない。
7. **work は実行されたか？** 計測 region 内で work が走ったことを確認（server に届いた、row が書かれた、byte が読まれた、結果が使われた）。lazy（iterate されない generator、await されない promise、JIT が捨てられる結果）と timeout は「起きていない work」の数字を出す。

## 報告

- 先に verdict: faster / slower / 測定不能の差なし / inconclusive。
- 単位付き数字、run 回数、range、limiter。例:「p50 41 ms → 33 ms、各側 7 run の median、after 32–35 ms、1 core で JSON parse が bound」。
- limiter を名指せない、片側未チューニング、4 と 7 を確認できないなら inconclusive。gap を名指す。
- PR body は primary 数字 1 つ（**Opening a PR** playbook）。run 詳細・range・limiter evidence はリンク成果物か notes に置く。

## 他の perf 素材との関係

- **Perf issue** playbook は遅さの fix。ステップ 2 の performance mantras が fix 候補を生む。本スキルは baseline を plan 前に vet し、その後の各数字も vet する。
- **Hillclimb** は 1 metric を loop。harness を freeze 前に本スキルで vet。freeze 後は error / work 件数を print し、keep-or-revert で 4 と 7 を毎回確認しやすくする。

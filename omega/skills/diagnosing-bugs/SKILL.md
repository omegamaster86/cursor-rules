---
name: diagnosing-bugs
description: "難しいバグや性能退行の診断ループ。「diagnose」「debug this」、壊れている・例外・失敗・遅いの報告に使用。"
disable-model-invocation: true
---

# Diagnosing Bugs

難しいバグ向けの規律。明示的に正当化できるときだけフェーズをスキップする。

コードベースを調べるときは、存在すれば `GLOSSARY.md` を読み関連モジュールのメンタルモデルを得る。触る領域の ADR も確認する。（旧 `CONTEXT.md` は `GLOSSARY.md` にリネーム済みとみなす。）

## Redact

本スキルはコマンド・出力・キャプチャを見せる。**秘密はすべて先に redact** — 表示箇所は `<REDACTED>`。ループは env var 経由にし、credential は環境に留める。キャプチャ artifact は auth header を含む：信号のある行だけ引用する。

redact 後の出力で診断できないなら、その旨を言いユーザーに聞く。

## Phase 1: Build a feedback loop

**これが本スキルそのもの。** 他は手続き。バグに対して **tight** な pass/fail 信号（**この** バグで赤になる）があれば原因は見つかる。bisection・仮説・instrumentation はそれを消費するだけ。なければコードを見続けても救われない。

ここに **disproportionate** な effort。** aggressive・creative・諦めない。**

### Ways to construct one, in roughly this order

1. バグに届く seam での **failing test**（unit / integration / e2e）。
2. 動いている dev server への **curl / HTTP script**。
3. fixture 入力の **CLI**、stdout を known-good snapshot と diff。
4. UI を動かし DOM/console/network を assert する **headless browser**（Playwright / Puppeteer）。
5. **trace の replay** — 実ネットワーク要求 / payload / event log を disk に保存し、隔離 path で再生。
6. **throwaway harness** — バグ path を 1 関数呼び出しで叩く最小部分系。
7. **property / fuzz** — 「ときどきおかしい出力」なら乱数入力を大量実行。
8. **bisection harness** — 2 状態間（commit / dataset / version）で「state X で起動・check・repeat」を自動化し `git bisect run`。
9. **differential loop** — 同入力を旧版 vs 新版（または 2 config）で走らせ出力 diff。
10. **HITL bash script** — 最後の手段。人がクリックする必要があるなら `scripts/hitl-loop.template.sh` で **人を回す** 構造化ループ。キャプチャ出力があなたに戻る。

正しい feedback loop があればバグは 90% 直った。

### Tighten the loop

ループをプロダクトとして扱う。_a_ ループができたら **tighten**：

- 速くできるか？（setup cache、無関係 init スキップ、scope 狭める）
- 信号を尖らせられるか？（「落ちなかった」ではなく **具体症状** を assert）
- 決定的にできるか？（時間 pin、RNG seed、FS 隔離、network 固定）

30 秒で flaky なループはほぼ無ループと同じ。2 秒で決定的なループは tight で debug の超能力。

### Non-deterministic bugs

目標はきれいな repro ではなく **再現率の引き上げ**。トリガを 100 回ループ、並列、stress、timing 窓を狭める、sleep 注入。50% flake は debug 可能。1% は無理なので率を上げ続ける。

### When you genuinely cannot build a loop

明示的に止め、試したことを列挙。ユーザーに聞く：(a) repro 環境へのアクセス、(b) redact 済み artifact（HAR、log dump、core dump、タイムスタンプ付き録画）、(c) 一時的な production instrumentation の許可。**ループなしで仮説フェーズに進まない。**

### Completion criterion: a tight loop that goes red

Phase 1 完了はループが **tight** かつ **red-capable** のとき：**1 コマンド**（script path、test 起動、curl）を名指しし、**少なくとも 1 回実行済み**（起動と redact 出力を示す）、かつ：

- [ ] **Red-capable**: 実際のバグ path を走らせ **ユーザーの症状そのもの** を assert し、このバグで赤・fix で緑になり得る。「エラーなく動いた」だけではない。
- [ ] **Deterministic**: 毎回同じ判定（flake は上記の pinned 高再現率）。
- [ ] **Fast**: 秒単位、分単位ではない。
- [ ] **Agent-runnable**: 無人実行可。人は `scripts/hitl-loop.template.sh` 経由のみ。

このコマンドが無いのにコードを読んで理論を立て始めたら **止める — それが本スキルが防ぐ失敗。** red-capable コマンドなし Phase 2 なし。

## Phase 2: Reproduce + minimise

ループを走らせ、赤になるのを見る。

確認：

- [ ] ループの失敗モードが **ユーザーが述べた** もので、近くの別失敗ではない。
- [ ] 複数回で再現（または非決定では十分高い率）。
- [ ] 症状（メッセージ、誤出力、遅延）を捕捉し、後続フェーズで fix がそれに効くことを検証できる。

### Minimise

赤のあと **まだ赤の最小シナリオ** に縮小。入力・caller・config・data・手順を **1 つずつ** 切り、各 cut 後にループ再実行。失敗に load-bearing なものだけ残す。

理由：最小 repro は Phase 3 の仮説空間を縮め、Phase 5 の regression になる。

**残り要素がすべて load-bearing** — どれか 1 つ除くと緑 — まで。reproduce **かつ** minimise するまで進まない。

## Phase 3: Hypothesise

テスト前に **3–5 個の ranked 仮説**。単一仮説は最初の plausible に anchor する。

各仮説は **反証可能** — 予測を述べる。

> 形式: 「原因が <X> なら、<Y> を変えると消える / <Z> を変えると悪化する。」

予測を述べられなければ vibe — 捨てるか尖らせる。

**テスト前に ranked リストをユーザーに見せる。** ドメイン知で即 re-rank したり、既に潰した仮説を知っていることもある。ブロックしない（AFK なら自分の ranking で進む）。

## Phase 4: Instrument

各 probe は Phase 3 の特定予測に対応。**1 変数ずつ。**

ツール優先：

1. **Debugger / REPL**（環境が許せば）。breakpoint 10 個よりログ 1 個。
2. 仮説を分ける境界の **targeted log**。
3. 「全部 log して grep」はしない。

**debug log には一意 prefix** 例 `[DEBUG-a4f2]`。後片付けは grep 1 回。tag なし log は残る。

**Perf 分支:** perf 退行では log はたいてい誤り。baseline 測定（timing harness、`performance.now()`、profiler、query plan）してから bisect。**測定 first、fix second。**

## Phase 5: Fix + regression test

fix **前** に regression test — **correct seam** があるときだけ。

correct seam は **呼び出し側で起きる実バグパターン** を走らせる境界。shallow すぎる seam（多 caller が要るのに単 caller test 等）は false confidence。

**correct seam が無いこと自体が finding。** アーキテクチャがバグを lock できない。次フェーズ用に flag。

seam があるなら：

1. 最小 repro を failing test に。
2. fail を見る。コードや fixture を mutate して赤を強制したなら、pristine との `diff` で mutation が先か確認。
3. fix 適用。
4. pass を見る。
5. Phase 1 ループを **元の（非最小）** シナリオで再実行。

## Phase 6: Cleanup

完了宣言前に必須：

- [ ] 元 repro が再現しない（Phase 1 ループ再実行）
- [ ] Regression test pass（または seam 不在を doc）
- [ ] 全 `[DEBUG-...]` 除去（prefix grep）
- [ ] throwaway prototype 削除（または明確な debug 場所へ）
- [ ] 正しかった仮説を commit / PR message に書き、次の debugger が学べるように

## 上流

正本: [mattpocock/skills — engineering/diagnosing-bugs](https://github.com/mattpocock/skills/tree/main/skills/engineering/diagnosing-bugs)。同期メモ: `references/UPSTREAM.md`。

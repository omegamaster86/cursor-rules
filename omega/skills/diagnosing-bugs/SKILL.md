---
name: diagnosing-bugs
description: "難しい bug や perf 退行の診断ループ。「diagnose」「debug this」、壊れている・例外・失敗・遅いの報告時に使用。"
disable-model-invocation: true
---

# Diagnosing Bugs

難しい bug 向けの規律。明示的な理由がない限りフェーズを飛ばさない。

コードベースを調べるときは、存在すれば `GLOSSARY.md` で関連モジュールの mental model を揃え、触る領域の ADR を確認する。

## Redact

このスキルはコマンド・出力・取得 artifact を示す。**秘密は必ず先に redact**し、`<REDACTED>` と書く。ループは env var 経由で組み、credential は環境に残し表示には出さない。artifact には auth header が載る：信号のある行だけ引用する。

redact 後の出力で診断できないなら、その旨を述べてユーザーに聞く。

## Phase 1: フィードバックループを作る

**これがスキルの本体。** 他は手続き。**この bug で赤くなる** きつい pass/fail 信号があれば原因に辿れる。bisection・仮説・instrumentation はそれを消費するだけ。なければコードを見続けても救われない。

ここに disproportionate な effort を使う。**攻撃的に。創造的に。諦めない。**

### 作り方（おおよそこの順）

1. bug に届く seam での **failing test**（unit / integration / e2e）
2. 動いている dev server への **curl / HTTP script**
3. fixture 入力の **CLI**、stdout を known-good snapshot と diff
4. **Headless browser**（Playwright / Puppeteer）で UI を駆動し DOM / console / network を assert
5. **捕捉 trace の replay**（network / payload / event log を disk に保存し isolated に再生）
6. **捨て harness**（bug path を 1 関数呼び出しで踏む最小部分系）
7. **Property / fuzz**（「ときどきおかしい」なら大量入力で failure mode を探す）
8. **Bisection harness**（commit / dataset / version の間で `git bisect run` 可能にする）
9. **Differential loop**（旧版 vs 新版や 2 config で同じ入力を diff）
10. **HITL bash**（最後の手段。人がクリック必須なら `scripts/hitl-loop.template.sh` で構造化）

正しいループがあれば bug は 90% 直った。

### ループを tight に

一度できたら **tighten** する：

- 速くできるか（setup cache、無関係 init スキップ、scope 狭める）
- 信号を尖らせられるか（「落ちなかった」ではなく症状を assert）
- deterministic か（時間固定、RNG seed、FS / network 隔離）

30 秒で flaky なループはほぼ無し。2 秒で deterministic なら debugging の超能力。

### 非決定的 bug

きれいな repro より **再現率を上げる**。100 回ループ、並列、stress、sleep 注入。50% flake は debug 可能。1% は無理なので率を上げる。

### ループが本当に作れないとき

明示的に止め、試したことを列挙。ユーザーに (a) 再現環境、(b) redact 済み artifact（HAR、log、core dump、タイムスタンプ付き録画）、(c) 一時的な production instrumentation の許可を求める。ループなしで仮説だけ進めない。

### 完了条件：赤くできる tight ループ

Phase 1 完了は、ループが **tight** かつ **red-capable** で、**1 コマンド**（script path、test 起動、curl）を名指し、**少なくとも 1 回実行済み**（起動と redact 出力を示す）：

- [ ] **Red-capable**：実際の bug path を踏み **ユーザーが述べた症状** を assert でき、この bug で赤くなり fix で緑になる。「エラーなく終わった」だけではない。
- [ ] **Deterministic**：毎回同じ判定（flake は pinned 高再現率）
- [ ] **Fast**：秒単位
- [ ] **Agent-runnable**：無人実行可。人は `scripts/hitl-loop.template.sh` 経由のみ

このコマンドが無いのにコードを読んで theory を立て始めたら **止める**（このスキルが防ぐ失敗）。赤くできるコマンドなし Phase 2 へ進まない。

## Phase 2: 再現 + 最小化

ループを走らせ、赤を見る。

確認：

- [ ] ユーザーが述べた failure mode でなく近くの別 failure ではない
- [ ] 複数回で再現（または非決定は十分な率）
- [ ] 症状（message、wrong output、timing）を捕捉し後続で fix 検証に使える

### 最小化

赤のあと **まだ赤い最小シナリオ** に縮める。入力・caller・config・data・手順を **1 つずつ** 切り、各 cut のあとループを再実行。failure に load-bearing なものだけ残す。

残り要素はすべて load-bearing：どれか 1 つを除けば緑になる、まで。再現と最小化が終わるまで進まない。

## Phase 3: 仮説

テスト前に **3〜5 個の順位付き仮説**。1 個だけは最初の plausible に anchor する。

各仮説は **反証可能**：予測を述べる。

> 形式：「<X> が原因なら、<Y> を変えると消える / <Z> を変えると悪化する」

予測を述べられないなら vibe：捨てるか尖らせる。

**テスト前に順位リストをユーザーに見せる。** ドメイン知で順位が変わることがある。ブロックはしない（AFK なら自分の順位で進む）。

## Phase 4: Instrument

各 probe は Phase 3 の特定予測に対応。**1 変数ずつ。**

優先：

1. **Debugger / REPL**（使えるなら。breakpoint 10 個よりログ 1 個）
2. **境界の targeted log**
3. 「全部 log して grep」はしない

**debug log には一意 prefix**（例 `[DEBUG-a4f2]`）。終了時は 1 grep で掃除。

**Perf 分支**：perf 退行は log が大抵 wrong。baseline 測定（timing harness、`performance.now()`、profiler、query plan）してから bisect。測ってから fix。

## Phase 5: Fix + regression test

fix **前**に regression test を書くのは **正しい seam** があるときだけ。

正しい seam は **呼び出し側で起きる実 bug パターン** を test する seam。浅すぎる seam（単一 caller だけ、chain を再現できない unit）は false confidence。

正しい seam が無いなら **それ自体が finding**。architecture が bug を lock できない。次フェーズ用に flag。

seam があるなら：

1. 最小 repro を failing test に
2. fail を見る（強制 red なら pristine との diff で mutation が先か確認）
3. fix
4. pass
5. Phase 1 ループを元（非最小）シナリオで再実行

## Phase 6: Cleanup

完了宣言前：

- [ ] 元 repro が再現しない（Phase 1 ループ再実行）
- [ ] Regression test pass（または seam 欠如を doc）
- [ ] `[DEBUG-...]` 全削除
- [ ] 捨て prototype 削除（または明示 debug 場所へ）
- [ ] 当たった仮説を commit / PR message に（次の debugger の学び）

## 上流

正本: [mattpocock/skills — engineering/diagnosing-bugs](https://github.com/mattpocock/skills/tree/main/skills/engineering/diagnosing-bugs)。`references/UPSTREAM.md`。

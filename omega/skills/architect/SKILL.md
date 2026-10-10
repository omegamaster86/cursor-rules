---
name: architect
description: "実装前に型・シグネチャ・モジュール構造をスケッチし、実装が埋まる間もループに留まる。/architect、'architect this'、'design this'、コードに飛ぶと間違った形が固定される非 trivial 作業向け。"
disable-model-invocation: true
---

# Architect

実装前に設計する。`not implemented` 本体と pseudocode で型、関数シグネチャ、クラス形状、モジュール境界をスケッチする。複数モデル視点を統合し、選んだスケッチに対してコードを埋める。実装がスケッチの誤りを示したら捨てて再設計する。

## Start

着手前にフェーズごとに 1 エントリの todolist を開く。

1. Ground
2. Sketch
3. Agree
4. Implement
5. Scrap

## Phase A: Ground the problem

新コードが触れるすべてのシステムの実 mental model を組む。関連サブシステムに **how** スキルを走らせる。

ファイル名を挙げるだけは grounding ではない。`how` が求める traced model を出す。設計が ownership やレイヤリングを再定義するなら、既存形状に **why** スキルも走らせ、rationale を guess ではなく constraint にする。

周囲に統合すべきシステムがない真の greenfield だけ Phase A をスキップする。

## Phase B: Sketch

design-sketch タスクと Phase A の grounding artifact で **multi-agent-candidates** スキルを走らせる。各 runner の prompt に `references/runner-prompt.md` を渡す。各 candidate は `references/rationale-template.md` の形の design package を出す。

`forge-models.mdc` ルールの `architect runners` 行から runner を取り、`multi-agent-candidates runners` 行の代わりに使う。ルールまたはその行が無ければ `claude-opus-5.5-thinking-medium` と `cursor-grok-4.6-medium`。alias と rejected エントリは **multi-agent-candidates** スキルの Phase A の runner ルールに従う。

2 回設計する。最初が十分に見えても synthesis 前に構造的に異なる candidate を最低 2 つ要求する。これは **exhaust-the-design-space** principle スキルの具体化。1 形状内の点修正ではなく、形状全体の代替。

synthesis 前にすべての candidate を [`references/design-red-flags.md`](references/design-red-flags.md) でスクリーンする。次の contributor は、開いたファイルだけ見て、最寄りの例をコピーし、コンパイルが通る最短経路を取るエージェントと仮定する。1 ファイルから正しく見える変更が repo 全体で正しい設計を選ぶ。

viable candidate を interface depth で比較する。より小さく単純な public surface の背後に複雑さを隠す設計を選ぶ。rich interface は capability をレイヤに散らさず集中させ、call chain を短く保てる。

Arena は 1 つの synthesized design package を返す。synthesis 決定が rationale の「Synthesis decision」節を埋める。

## Phase C: Agree（opt-in）

デフォルト: synthesized design で実装に直行。人の checkpoint なし。

invoker が明示的に求めたときだけ checkpoint に opt in: 「/architect with checkpoint」「stop and show me before implementing」など。synthesized design を出して sign-off まで pause。

synthesis はどちらでも単独 commit として ship できる。**foundational-thinking** principle スキルの「scaffold first」モード。fill-in 中の計画・スコープ済み breakage は **outcome-oriented-execution** principle スキルに従い問題ない。実装前に設計へ adversarial 圧力をかけるなら、synthesized sketch に **review-orchestrator-triple-hybrid** スキルを走らせる。

人が形状を push back したら（checkpoint 中または後から）Phase A の evidence として扱う。さらにコードを書く前に re-ground して Phase B を再実行。

## Phase D: Implement against the sketch

`not implemented` 本体をコードに、pseudocode を logic に置き換える。synthesized sketch が contract。

スケッチからの逸脱は黙って吸収する friction ではなく、surface する signal。スケッチが想定しなかった parameter が関数に要るなら、スケッチが誤りか、要件の見落としか、実装の overreach かを問う。

## Phase E: Scrap when the architecture is wrong

実装がスケッチが吸収できない friction を繰り返し出すならスケッチを捨てる。誤設計に fix を bolt しない。**redesign-from-first-principles** と **fix-root-causes** principle スキルに従う。

signal は単発ではなく *pattern*。兆候:

- 無関係なコード横断で同じ形状の workaround が繰り返し出る。
- 複数の無関係 edge case がすべて special-case branch を要る。
- コンパイルに escape hatch（`any`、cast、実際は常に set される optional field）が要る型。
- スケッチは state が shared でないと言ったのに「lock が要る」反射。
- caller が abstraction の内部ルールを知らないと使えない。
- 実装横断で同じ形状の Phase D 逸脱が 2 つ以上独立に起きる。

判断を使う。少数の edge case で architecture を断罪しない。正当に complex な問題もある。データの複雑さは設計の複雑さではない。

scrap するとき:

1. 構築済みに **how** スキルを再実行。
2. 新 constraint が day-one 前提だったかのように redesign-from-first-principles で再設計。
3. **subtract-before-you-add** principle スキルに従い足す前に引く。新スケッチは伸びる前に旧より小さく。
4. Phase B に戻り multi-agent-candidates を再実行。

## Outputs

caller の usage を先に書き、型スケッチはそこから導く。小変更は新型・シグネチャ 1 ファイル。大きい作業は module map 加 type definitions。rationale は `references/rationale-template.md` の形で併送し、usage スケッチと synthesis 決定を含む。

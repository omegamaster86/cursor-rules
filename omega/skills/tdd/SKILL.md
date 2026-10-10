---
name: tdd
description: "ユーザーが明示的に TDD、failing test、regression test を求めたとき、または bug に安価な local test 対象が明らかなときだけ使用。test 経路が不明・高コスト・integration 重め・未要求ならスキップ。"
disable-model-invocation: true
---

# TDD Bug Fix

明確で安価な test 経路がある bug 修正では、production コードを変える前に壊れた振る舞いを実行可能にする。目的は fix 前に fail、fix 後に pass する focused regression test。

非現実的なら test を強制しない。利用可能な test が広い harness、brittle mock、遅い E2E、production 限定 state、曖昧な repro step、大きな無関係 fixture 変更を要するなら、新規 test は追加せず最も近い有用な検証を使う。

## Workflow

1. **bug を理解。** intended 振る舞い、現状、影響 path、最小の観測可能 repro。
2. **最も狭い実行可能チェックを選ぶ。** その codepath で既に使われている unit、component、integration、regression test を優先。実用的な test 経路が明らかでなければ、workflow 満足のためにゼロから作らない。
3. **failing test を先に書く。** bug を捕まえた最小 focused test。現 implementation を写すのではなく intended 振る舞いを encode。
4. **fix 前に新 test を実行。** intended 理由で fail することを確認。pass または無関係理由の fail なら implementation を触る前に test か repro を直す。
5. **bug を fix。** intended 振る舞いを満たす最小 production 変更。近傍 contract は保持。
6. **regression test を再実行。** 今 pass することを確認。

## If a Failing Test Is Impractical

代わりに最も近い実行可能 regression チェック： targeted script、手動 repro コマンド、browser automation、snapshot 比較、log assertion、focused integration チェック。

悪い test より test なしを優先。悪い test は mock の大半だけ、現 implementation 詳細の encode、timing や無関係 global state 依存、小 fix に高コスト infra、fix 証明直後に消されるもの。

## Guardrails

- 誤った implementation に合わせるためだけに test を変えない。
- expected 振る舞いが本当に変わり理由が明確なとき以外、既存 assertion を弱めない。
- regression test は bug に集中。広い fixture churn や無関係 coverage 拡大は避ける。
- flaky なら可能なら test を deterministic にし、lock する signal を doc。
- より広い失敗クラスが露わなら、まず focused regression path を land し、 sibling coverage はその後検討。

## Final Response

結果だけでなく evidence を報告：

- fail-before の test または実行チェック名と出た failure。
- pass-after の test 実行と行った近傍 validation。
- fail-before evidence を示せなかった理由と、代わりに使った最も近い regression チェック。

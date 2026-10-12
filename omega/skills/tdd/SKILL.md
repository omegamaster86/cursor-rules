---
name: tdd
description: "ユーザーが明示的に TDD、failing test、regression test を求めたとき、red-green-refactor や integration test を言ったとき、または bug に安価な local test 対象が明らかなときだけ使用。test 経路が不明・高コスト・integration 重め・未要求ならスキップ。"
disable-model-invocation: true
---

# Test-Driven Development

TDD は red → green のループ。本スキルは、そのループが **残す価値のあるテスト** を生むための参照：良いテストの定義、テストを置く境界（seam）、アンチパターン、ループの規律。**各サイクルの前と最中** に各節を参照する。後からだけ読むのではない。

コードベースを調べるときは、存在すれば `GLOSSARY.md` を読み、テスト名と interface の語彙をプロジェクトのドメイン言語に合わせる。触る領域の ADR も尊重する。（旧来の `CONTEXT.md` / `CONTEXT-MAP.md` は `GLOSSARY.md` / `GLOSSARY-MAP.md` にリネーム済みとみなす。）

## 良いテストとは

テストは実装詳細ではなく、公開 interface 越しに振る舞いを検証する。コードは全面書き換えられても、テストは壊れないべき。良いテストは仕様のように読める：「valid cart で checkout できる」は存在する能力を示し、内部構造を気にしないのでリファクタに耐える。

例とモック指針は [tests.md](tests.md)、[mocking.md](mocking.md)。

## Seam：テストを置く境界

**seam** はテストする公開境界。内側に手を入れず振る舞いを観測する interface。テストは seam に置き、内部には置かない。

**事前合意した seam だけでテストする。** テストを書く前に、対象 seam を書き出しユーザーと確認する。未確認の seam ではテストを書かない。全部はテストできないので、先に seam を合わせることで effort がクリティカル path と複雑ロジックに乗る。

「公開 interface は何か、どの seam をテストするか？」と聞く。**提案する seam ごとに、何を捕まえ何を逃すかを 1 行で書く。**

interface の形自体が論点（モジュールの深さ、seam の位置、何を露出するか）なら、語彙の共有参照として上流の `codebase-design` スキルを参照する（omega 未採用の場合は [mattpocock/skills — engineering/codebase-design](https://github.com/mattpocock/skills/tree/main/skills/engineering/codebase-design)）。セッションとして起動するものではない。

## アンチパターン

- **実装結合**: 内部 collaborator を mock、private をテスト、副作用経路で検証（DB を直接見て interface を使わない等）。リファクタで壊れるが振る舞いは変わっていないのが兆候。
- **同語反復（tautological）**: 期待値をコードと同じ計算で作る（`expect(add(a,b)).toBe(a+b)`、手計算と同じ snapshot、自分自身への constant 等）。期待値は独立した正（リテラル、 worked example、仕様）から来る。
- **水平スライス**: 先にテスト全部、後から実装全部。想像した振る舞いをテストし、ユーザー向け振る舞いより形をテストし、実装を理解する前にテスト構造を固定する。**垂直スライス**で：1 test → 1 実装 → 繰り返し。各テストは前のサイクルから学んだ **tracer bullet**。

## ループの規律

- **Red before green.** 先に failing test、通すための最小コードだけ。未来のテストや speculative feature は先読みしない。
- **1 スライスずつ。** 1 seam、1 test、1 最小実装 per cycle。
- **リファクタはループ外。** レビュー段階（上流 `code-review`）のもの。red → green の実装サイクルには含めない。

---

## TDD Bug Fix（omega / forge）

明確で安価な test 経路がある bug 修正では、production コードを変える前に壊れた振る舞いを実行可能にする。目的は fix 前に fail、fix 後に pass する focused regression test。上の seam 合意と「捕まえる／逃す」メモは、ここで書く regression の境界選びにも使う。

非現実的なら test を強制しない。利用可能な test が広い harness、brittle mock、遅い E2E、production 限定 state、曖昧な repro step、大きな無関係 fixture 変更を要するなら、新規 test は追加せず最も近い有用な検証を使う。

### Workflow

1. **bug を理解。** intended 振る舞い、現状、影響 path、最小の観測可能 repro。
2. **最も狭い実行可能チェックを選ぶ。** その codepath で既に使われている unit、component、integration、regression test を優先。実用的な test 経路が明らかでなければ、workflow 満足のためにゼロから作らない。seam をユーザーと合意し、各 seam が何を捕まえ何を逃すかを 1 行で残す。
3. **failing test を先に書く。** bug を捕まえた最小 focused test。現 implementation を写すのではなく intended 振る舞いを encode。
4. **fix 前に新 test を実行。** intended 理由で fail することを確認。pass または無関係理由の fail なら implementation を触る前に test か repro を直す。
5. **bug を fix。** intended 振る舞いを満たす最小 production 変更。近傍 contract は保持。
6. **regression test を再実行。** 今 pass することを確認。

### If a Failing Test Is Impractical

代わりに最も近い実行可能 regression チェック： targeted script、手動 repro コマンド、browser automation、snapshot 比較、log assertion、focused integration チェック。

悪い test より test なしを優先。悪い test は mock の大半だけ、現 implementation 詳細の encode、timing や無関係 global state 依存、小 fix に高コスト infra、fix 証明直後に消されるもの。

### Guardrails

- 誤った implementation に合わせるためだけに test を変えない。
- expected 振る舞いが本当に変わり理由が明確なとき以外、既存 assertion を弱めない。
- regression test は bug に集中。広い fixture churn や無関係 coverage 拡大は避ける。
- flaky なら可能なら test を deterministic にし、lock する signal を doc。
- より広い失敗クラスが露わなら、まず focused regression path を land し、 sibling coverage はその後検討。

### Final Response

結果だけでなく evidence を報告：

- fail-before の test または実行チェック名と出た failure。
- pass-after の test 実行と行った近傍 validation。
- fail-before evidence を示せなかった理由と、代わりに使った最も近い regression チェック。

## 上流

正本: [mattpocock/skills — engineering/tdd](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd)。同期メモ: `references/UPSTREAM.md`。

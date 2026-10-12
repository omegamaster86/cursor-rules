---
name: tdd
description: "red-green-refactor・test-first の機能実装や bug 修正、integration test 構築。ユーザーが TDD / failing test / regression を明示したとき、または bug に安価な local test 経路があるとき。test 経路が不明・高コスト・integration 重め・未要求ならスキップ。"
disable-model-invocation: true
---

# Test-Driven Development

TDD は red → green のループ。このスキルは、そのループが **残す価値のある test** を生むための参照：良い test とは何か、test を置く場所、反パターン、ループの規律。各セクションは **毎サイクル**、ループの前と最中に参照する（後からだけ読まない）。

コードベースを調べるときは、存在すれば `GLOSSARY.md` を読み、test 名と interface の語彙をプロジェクトのドメイン言語に合わせる。触る領域の ADR も尊重する。

## 良い test とは

test は実装詳細ではなく **公開 interface** 越しに振る舞いを検証する。コードは全面改修されても test は変わらないべき。良い test は仕様のように読める：「valid cart で checkout できる」は存在する capability が一目で分かり、内部構造を気にしないので refactor に耐える。

例とモック指針は [tests.md](tests.md)、[mocking.md](mocking.md)。

## Seam：test を置く境界

**seam** は test する公開境界。内側に手を入れずに振る舞いを観測する interface。test は seam にだけ置き、内部には置かない。

**事前合意した seam だけで test する。** test を書く前に、対象 seam を書き出しユーザーと確認する。未確認の seam では test を書かない。すべては test できないので、先に seam を合意することが、重要 path と複雑な logic に effort を集中させる。

聞く：「公開 interface は何か、どの seam を test するか？」提案する各 seam に、**何を捕まえ、何を取りこぼすか** を 1 行ずつ書く。

interface の形自体が未決（モジュールの深さ、seam の位置、何を露出するか）なら、語彙の共有源として **codebase-design** スキルを参照する（module / interface / depth / seam / adapter / leverage / locality の用語。セッションとして走らせるのではなく参照）。

## 反パターン

- **Implementation-coupled**：内部 collaborator を mock、private を test、副作用経路で検証（DB を直接読む等）。refactor で振る舞いは同じなのに test が壊れる。
- **Tautological**：期待値をコードと同じ計算で再構成（`expect(add(a,b)).toBe(a+b)`、手作り snapshot 等）。独立した正（literal、 worked example、spec）から期待値を出す。
- **Horizontal slicing**：test を全部先に、実装を全部後。想像上の振る舞いを test し、構造に commit してから実装を理解する。**Vertical slice**：1 test → 1 実装 → 繰り返し。各 test は前のサイクルから学んだ **tracer bullet**。

## ループの規律

- **Red before green.** 失敗 test を先に、通すための最小コードだけ。未来の test や speculative 機能は先取りしない。
- **One slice at a time.** 1 seam、1 test、1 最小実装 per サイクル。
- **Refactor はループ外。** **code-review** スキルのレビュー段階。red → green の実装サイクルには含めない。

## Bug fix（omega / forge）

明確で安価な test 経路がある bug 修正では、production を変える前に壊れた振る舞いを実行可能にする。目的は fix 前に fail、fix 後に pass する focused regression test。上の seam 規律（事前合意・catch/miss の明示）を bug の seam 選びにも使う。

非現実的なら test を強制しない。広い harness、brittle mock、遅い E2E、production 限定 state、曖昧な repro、大きな無関係 fixture 変更が要るなら新規 test は追加せず、最も近い有用な検証を使う。

### Workflow

1. **bug を理解。** intended 振る舞い、現状、影響 path、最小の観測可能 repro。
2. **最も狭い実行可能チェックを選ぶ。** その codepath で既に使われている test を優先。実用的な経路が明らかでなければ workflow 満足のためにゼロから作らない。
3. **failing test を先に書く。** intended 振る舞いを encode（現 implementation の写しではない）。
4. **fix 前に実行。** intended 理由で fail することを確認。
5. **最小 fix。**
6. **regression を再実行。**

### Failing test が非現実的なとき

targeted script、手動 repro、browser automation、snapshot、log assertion、focused integration 等。悪い test より test なし。既存 assertion の弱体化や mock 偏重は避ける。

### 報告

fail-before の test / チェック名と failure、pass-after の実行、代替検証に切り替えた理由を evidence として述べる。

## 上流

正本: [mattpocock/skills — engineering/tdd](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd)。同期メモ: `references/UPSTREAM.md`。

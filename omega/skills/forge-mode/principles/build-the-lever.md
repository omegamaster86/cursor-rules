# レバーを作る（Build the Lever）

自明でない作業では、手でやるより**それを行う（または証明する）ツール**を先に作る。

**適用:** 編集・移行・分析・チェックなど、非自明な作業全般（bulk だけではない）。レビュアーが再実行できる artifact が欲しいとき。

**理由:** スループット — codemod / generator / script は毎回同じやり方で、無料で rerun できる。信頼 — 手作業はやり直しでしか再検証できない。決定的な script は「信じて」から「これを run」へ変える。

**パターン:**
- 最初の 1 ユニットを手でやってレシピを学び、ツールを作る。手作業版と diff して lever の安全な rerun を証明
- 編集 → codemod/script、反復ファイル → generator、分析 → 再実行可能なクエリ、検証 → 再実行可能な check
- ツールが全ユニットを 1 pass で処理できるなら、delegate に手適用させない
- subagent に fan-out するとき、lever は全員が読む skill 1 本（レシピ・検証契約・触るな柵）。delegate の write 範囲外に置く
- 本原則を引用したなら diff に codemod / script / generator / delegate skill のいずれかがある。無ければ適用していない
- セッションを超える作業なら lever を commit

**バランス:** 閾値は反復回数ではなく**自明さ**。1 回限りでも、check 可能にする script なら lever の価値あり。最小 script（`laziness-protocol.md`）。フレームワークは作らない。

**区別:** `encode-lessons-in-structure.md` は繰り返し指示の恒久ガード。本原則は目の前の作業の throughput と reviewability。検証の scripting は `prove-it-works.md` / **`/verify-done`**。

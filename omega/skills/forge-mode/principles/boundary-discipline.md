# 境界の規律（Boundary Discipline）

検証・型 narrow・エラー処理は**システム境界**に集中する。内部は型を信頼し、ビジネスロジックは pure function に置く。シェルは薄く機械的。

**適用:** 検証配線、エラーハンドリング、フレームワーク adapter を書くとき。genai では `web-coding-standards` の form-validation、`supabase-implementation` の edge-auth、`nextjs-directory-structure` の practice-bff が具体規約。

**理由:** 散在した検証はノイズで冗長で、安全の錯覚を与える。フレームワーク配線からロジックを離すと、フレームワークなしでテストできる。

**パターン:**
- **境界**（CLI 引数、config、外部 API、ネットワーク）: validate、エラー返却、防御的処理
- **内部:** 型付きデータ、エラー伝播、再 validate しない
- **境界を跨ぐ:** ドメイン概念を公開し、wire / storage / framework の private 表現を漏らさない

**検証・エラー:**
- config は parse 時（境界）に validate。ビジネスロジック内ではない
- raw データは境界で domain 型に parse
- transport / storage / framework 型を public surface 経由で再 export しない
- 境界で validate 済みなら、深い call chain に redundant nil check を足さない

**整理:**
- ビジネスロジックはフレームワーク非依存の pure function
- parse: raw bytes → typed state の pure transform
- prompt 構築: structured state in → string out

**テスト:**
- 「今システム境界を跨いでいるか？」否なら検証は redundant
- 「pure function にして shell が呼ぶだけにできるか？」能なら extract

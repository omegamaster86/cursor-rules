# 振る舞いをテストし、実装をテストしない

テストは**ユーザーと同じ呼び方**でコードを呼び、観測結果を**リテラル expected** と assert する。import 先がすべて `undefined` でも pass するテストは、振る舞いを観測していない — assertion を書き直すか削除。

**適用:** テストを書く・変える・残すとき。`tdd` スキルとセット。

**理由:** 欠陥で fail できないテストは CI と review のコストだけ消費する。定数 pin は定数や prompt を編集する正常変更でも fail する。

**undefined でも pass しうる 5 形:**
- **弱い / 無 assertion:** `toBeDefined`、`toBeTruthy`、`not.toThrow` のみ 等
- **mock / 不在のみ:** `toHaveBeenCalled`、`toBeUndefined`、`toEqual([])` のみ 等
- **自己参照:** `expect(f(a)).toBe(f(a))`、被験コードから expected を組み立て
- **定数 pin:** `expect(LIMITS.max).toBe(8)`、prompt 文字列の contain のみ
- **fixture が fixture を assert:** 被験が body 内で走らない

**直し方:** body 内で被験を 1 入力で呼び、リテラル出力または observable effect を assert。mock なら payload か呼び出し後 state。定数なら読み取り mechanism を 1 入力で test。assert 不能なら削除。

**残す:** テーブル間の関係（キーの存在整合）、`*.test-d.ts` の compile-time check。

genai の mock-store / Server Action テストでは、HTTP 契約とユーザー可視結果を優先する（`web-coding-standards` の testing 規約を参照）。

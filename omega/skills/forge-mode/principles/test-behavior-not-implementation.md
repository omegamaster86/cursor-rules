# 振る舞いをテストし、実装をテストしない

テストはユーザーがコードを呼び出し、観察する **正確な結果** をリテラルに assert する。import 先がすべて `undefined` を返しても通るテストは書き直すか削除する。

次の形はそのチェックに失敗する:

- 弱い / 無 assert: `toBeDefined`、`toBeTruthy`、`not.toThrow`、`toBeGreaterThan(0)`。
- 呼び出し / 不在だけ: `toHaveBeenCalled`、`not.toHaveBeenCalled`、`toBeUndefined`、`toEqual([])`。
- 被テストコードで計算した期待値: `expect(f(a)).toBe(f(a))`。
- 手保守 constant、config default、table 行、prompt 文字列の再掲。
- 被テストを呼ばず、テストが組んだデータだけを assert。

修正: テスト本体で被テストを 1 つの具体 input で呼び、リテラル output または効果を assert する。

table 行をまたぐ関係（2 table に同じ key、存在する parent）と `*.test-d.ts` の型のみチェックは残してよい。

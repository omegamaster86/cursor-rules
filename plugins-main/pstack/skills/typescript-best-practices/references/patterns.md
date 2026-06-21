# TypeScript パターン

`SKILL.md` の各ルールのコード例。根底の原則は言語非依存。**type-system-discipline** と **boundary-discipline** 原則スキルを参照。

## ブランド型

プリミティブにブランドを付け混同を防ぐ。作成時に一度検証。下流は型を信頼。

```ts
type AgentId = string & { readonly __brand: "AgentId" };

function parseAgentId(input: string): AgentId {
  if (!isUUID(input)) throw new Error(`Invalid agent id: ${input}`);
  return input as AgentId;
}

function focusAgent(id: AgentId): void {
  /* input is trusted */
}
```

`readonly __brand: 'X'` 形に合わせる。新しい慣習を発明しない。

## 判別共用体

バグが「この組み合わせは本当に起きうるか？」と問うなら型が緩すぎる。リテラル判別子でバリアントをモデル化: 各バリアントはフィールド名を共有し値は一意。不可能な組み合わせは表現できない。

```ts
// Don't. Boolean + optionals lets contradictory states exist.
type DiffState = { loading: boolean; diff?: GitDiff; error?: string };

// Do. Only valid states exist.
type DiffState =
  | { kind: "loading" }
  | { kind: "ready"; diff: GitDiff }
  | { kind: "error"; error: string };
```

判別子名（`kind`、`type`、`tag`）を 1 つ選び一貫させる。

## `any` より `unknown`

`any` は触れたすべてで型チェックを無効化。外部データは常に `unknown`。使用前に絞る。

```ts
// Don't
function handle(input: any) {
  return input.foo.bar;
}

// Do
function handle(input: unknown) {
  if (typeof input === "object" && input !== null && "foo" in input) {
    // narrowed; compiler verifies access
  }
}
```

外部ソース: RPC ペイロード、`JSON.parse`、`postMessage`、IPC、ファイル内容、環境変数、DB 結果。

## `as` キャスト禁止

各 `as` は実行時クラッシュの可能性。型システムが主張を検証した後にのみキャスト。

```ts
// Don't
const user = data as User;

// Do. Earn the cast at the boundary.
function parseUser(data: unknown): User {
  if (typeof data !== "object" || data === null) {
    throw new Error("expected object");
  }
  if (!("id" in data) || typeof (data as Record<string, unknown>).id !== "string") {
    throw new Error("expected id");
  }
  // ... validate all fields
  return data as User; // OK, earned cast after full validation
}
```

既存コードから `as` をリファクタするとき、TypeScript が推論できない理由を特定:

- 判別子欠如: 追加し判別共用体へ。
- 広すぎるソース型（例 `Record<string, unknown>`）: 絞る。
- 型付けされていない境界: parse 関数またはスキーマを追加。
- 本当に表現不能: ブランド型または `satisfies`。

## 絞り込みの階層

最良から最後の手段まで:

1. **判別共用体 switch / if。** コンパイラが自動絞り込み。
2. **`in` 演算子。** `"key" in obj` でそのキーを持つバリアントへ。
3. **`typeof` / `instanceof`。** プリミティブとクラスインスタンス。
4. **ユーザー定義型ガード。** 上記が足りないとき。
5. **`as` キャスト。** 検証後のみ。

```ts
function area(s: Shape): number {
  if ("radius" in s) return Math.PI * s.radius ** 2; // narrowed to circle
  return s.width * s.height; // narrowed to rect
}
```

## 型ガード

ガードは主張を実際に検証しなければならない。嘘のガードは `as` より悪い。安全と名のバグが隠れる。

```ts
function isCircle(s: Shape): s is Shape & { kind: "circle" } {
  return s.kind === "circle";
}
```

可能なら判別子絞り込みを優先。ガードは読者が辿る層を増やす。

## 網羅性

default 節で判別子を `never` 型ローカルに代入。新バリアント追加時にコンパイラがエラー。

```ts
// Value-returning switch
function area(s: Shape): number {
  switch (s.kind) {
    case "circle":
      return Math.PI * s.radius ** 2;
    case "rect":
      return s.width * s.height;
    default: {
      const _exhaustive: never = s;
      return _exhaustive;
    }
  }
}

// Void switch
function handle(s: Shape): void {
  switch (s.kind) {
    case "circle":
      drawCircle(s);
      break;
    case "rect":
      drawRect(s);
      break;
    default: {
      const _exhaustive: never = s;
      void _exhaustive;
    }
  }
}
```

値を返す switch は return スタイル。文 switch は void スタイル。

## `as` より `satisfies`

`satisfies` はリテラル型を広げずに検証。

```ts
// Don't. Widens, loses literal types.
const config = { theme: "dark", cols: 3 } as Config;

// Do. Validates AND preserves literal types.
const config = { theme: "dark", cols: 3 } satisfies Config;
// config.theme is "dark" (literal), not string
```

## 境界での検証

データが入る所で一度検証。内部では型を信頼。**boundary-discipline** 原則スキルを参照。

- **ワイヤフォーマット**（proto、JSON-RPC）: `ignoreUnknownFields` でパースし前方互換変更が古クライアントを壊さないように。
- **永続 JSON:** バージョン付き blob と parse 周りの try/catch。
- **呼び出しチェーン深部で再検証しない。**

## スキーマ由来の型

`.proto`、OpenAPI、GraphQL スキーマ、DB マイグレーションが形を定義しているとき、生成型から導出し重複しない。

```ts
// Don't. Duplicate shape, drifts when the schema changes.
type CheckSummary = {
  totalCount: number;
  checks: { name: string; status: string }[];
};
function renderChecks(s: CheckSummary) {
  /* ... */
}

// Do. Derive from the generated schema type.
import type { ChecksMessage } from "<generated module>";
function renderChecks(s: Pick<ChecksMessage, "totalCount" | "checks">) {
  /* ... */
}
```

新 interface を書く前に `Pick`、`Omit`、`Parameters`、`ReturnType`、`Awaited`、`typeof` を検討。

## オブジェクト引数

```ts
// Don't. Swap two args, still compiles.
openFile(uri, {
  startLineNumber: 10,
  startColumn: 1,
  endLineNumber: 10,
  endColumn: 1,
});

// Do. Order-independent, self-documenting.
openFile({
  uri,
  selection: {
    startLineNumber: 10,
    startColumn: 1,
    endLineNumber: 10,
    endColumn: 1,
  },
});
```

ホットパスではスキップ: フレームごとの描画、トークナイザ、パーサ、アロケーションコストが効くタイトループ。

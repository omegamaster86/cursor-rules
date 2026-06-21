---
name: typescript-best-practices
description: TypeScript のベストプラクティス。.ts または .tsx ファイルを読む・編集するときに使用。
---

# TypeScript best practices

まず **type-system-discipline** 原則スキルを適用する。このスキルは TypeScript 構文に接地する。

| ルール | 要約 |
|------|---------|
| 判別共用体 | `kind` リテラル判別子でバリアントをモデル化し、不可能な状態を表現できないようにする。optional フィールドの袋は使わない。 |
| ブランド型 | `& { readonly __brand: "X" }` でプリミティブにブランドを付け、混同できないようにする。作成時に一度だけ検証。 |
| `any` より `unknown` | 外部データは `unknown`。`any` は触れた箇所すべてで型チェックを無効化する。 |
| `as` キャスト禁止 | 各 `as` は実行時クラッシュの待ち伏せ。検証後にのみキャスト。 |
| 絞り込みの階層 | 判別子 switch > `in` 演算子 > `typeof`/`instanceof` > ユーザー定義型ガード > `as`。 |
| 型ガード | 主張を検証しなければならない。嘘のガードは `as` より悪い。安全と名の付いたバグが隠れる。`isX` または `hasX` と名付ける。 |
| 網羅性 | default 節に `const _exhaustive: never = x;` をインラインで書き、新バリアント追加時にコンパイラがエラーにする。 |
| `as` より `satisfies` | リテラル型を広げずに値を検証する。 |
| 境界での検証 | データが入る所で検証。内部では型を信頼。**boundary-discipline** 原則スキルを参照。 |
| スキーマ由来の型 | 新 interface を宣言する前に `Pick`/`Omit`/`Parameters`/`ReturnType`/`Awaited`/`typeof` を検討。 |
| オブジェクト引数 | 位置引数ではなくオブジェクトを渡し、引数順を自明にする。ホットパス（フレームごとの描画、トークナイザ、パーサ）ではスキップ。 |

例: `references/patterns.md`。

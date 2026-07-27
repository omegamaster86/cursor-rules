# レビューチェックリスト詳細

SKILL.md の各観点に対応する詳細なチェック項目。

## A. セキュリティ

### 認証（CRITICAL）

- [ ] Edge Function 呼び出しは `callEdgeFunction`（内部で `getSession` + `getClaims`）を使っている
- [ ] 自前実装の場合も JWT を `getClaims` 等で検証している（セッション有無だけの判定で済ませていない）
- [ ] Auth SDK（signIn / signOut 等）の Server Action 直接呼び出しは認証系に限定されている
- [ ] 認証エラー時に適切なエラーレスポンスを返している
- [ ] 未認証ユーザーがデータにアクセスできない

### データ保護

- [ ] パスワード、トークン、個人情報がログに出力されていない
- [ ] API レスポンスに不要なセンシティブデータが含まれていない
- [ ] 環境変数を直接クライアントに公開していない

### 環境変数

- [ ] アプリコードで `process.env.XXX` を直接参照していない（`import { env } from "@/env"` 経由）
- [ ] 環境変数の取得に fallback（`??` / `||`）や非 null 断言（`!`）を使っていない
- [ ] 新規変数は `src/env.ts` の `server` / `client` / `runtimeEnv` に追加されている
- [ ] 秘匿値に `NEXT_PUBLIC_` を付けていない（`server` スキーマ側）

## B. アーキテクチャ

### 3層構造（CRITICAL）

```
Page Component → Server Action / _apis → callEdgeFunction → Edge Function → DB
```

- [ ] Page Component から直接 DB（`.from()`）にアクセスしていない
- [ ] ビジネスロジックが Edge Function / DB Function に委譲されている
- [ ] Server Action は薄いレイヤー（`handler` + `callEdgeFunction`）として機能している
- [ ] Auth SDK 直接呼び出しは意図的な例外として妥当か

### コロケーション（HIGH）

```
app/[feature]/
├── _actions/      # データ変更用 Server Actions
├── _apis/         # データ取得用 API（.server.ts）
├── _components/   # ページ固有コンポーネント
├── _utils/        # ページ／機能固有ヘルパー（`_lib/` は使わない）
└── page.tsx
```

- [ ] Server Actions は `_actions/` に配置されている
- [ ] 読み取り API は `_apis/*.server.ts`
- [ ] ページ固有コンポーネントは `_components/`
- [ ] ヘルパーは `_utils/`（`_lib/` ではない）
- [ ] 共有 UI は `components/`（shadcn は `ui/*.tsx` フラット）

### Server/Client 分離（HIGH）

- [ ] `"use client"` はインタラクティブなコンポーネントのみ
- [ ] page.tsx が `"use client"` になっていない
- [ ] データフェッチは Server Component / `_apis` で実行

## C. Server Actions

### 基本構造

- [ ] ファイル先頭に `"use server"` がある
- [ ] `handler` + `validate` + `callEdgeFunction`（または意図的な Auth SDK）を使っている
- [ ] `schema.ts` / `types.ts` に分割されている（必要な場合）

### バリデーション

- [ ] Zod スキーマで入力をバリデーションしている（`validate()` 優先）
- [ ] エラー時は `fieldErrors` を返している
- [ ] 状態に `payload?: FormData` がある場合、エラー後の入力復元に使っている

### 関数シグネチャ

```typescript
export async function actionName(
  prevState: ActionState,
  formData: FormData,
): Promise<ActionState>
```

- [ ] useActionState 対応の引数順

### キャッシュ更新

- [ ] `revalidatePath()` **または** クライアント `router.push` / RSC 再取得のいずれかで画面が更新される
- [ ] （`revalidatePath` 必須ではない）

## D. フォーム実装

### useActionState

- [ ] `useActionState(serverAction, initialState)` を使用
- [ ] `[state, formAction, pending]` を受け取っている

### UI

- [ ] `<form action={formAction}>`
- [ ] Uncontrolled を優先
- [ ] `id` / `lock_no` は原則 `bind`（hidden は削除フォーム・外部 SDK 等の限定許容）
- [ ] `pending` 中は UI 無効化
- [ ] フィールドエラーと全体エラー（`role="alert"`）を表示

## E. ログ出力

- [ ] 本番 Server Action は `handler()` 経由（手動 start/end 定型を避けている）
- [ ] Edge 呼び出しは `callEdgeFunction`（ログ内包）
- [ ] `console.log` / `console.error` を本番アクションで直接使っていない（mock-store デモは例外可）

## F. TypeScript

- [ ] `type` を優先（`interface` は必要な場合のみ）
- [ ] API 境界型は `src/types/schemas/*.ts`（Zod）
- [ ] `src/types/index.ts` 必須ではない
- [ ] `any` を使っていない

## G. スタイリング

- [ ] `cn()` は `@/utils/class-name`
- [ ] セマンティックトークン（`bg-primary` 等）を優先
- [ ] インラインスタイルを避けている
- [ ] shadcn 由来の任意 px（`min-h-[80px]` 等）は UI プリミティブ内では許容
- [ ] アプリ画面のスペーシングは rem ユーティリティを優先

## H. 命名規則

| 種別 | 規則 | 例 |
|------|------|-----|
| 機能コンポーネント | PascalCase ディレクトリ | `_components/NewTodoForm/index.tsx` |
| shadcn/ui | kebab-case.tsx | `components/ui/button.tsx` |
| Server Action | リソース名 | `_actions/todo.ts` |
| API | `.server.ts` | `_apis/todo.server.ts` |
| ユーティリティ | kebab-case | `utils/class-name.ts` |

- [ ] 変数・関数: camelCase / 型・コンポーネント: PascalCase

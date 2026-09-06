# レビューチェックリスト詳細

SKILL.md の各観点に対応する詳細なチェック項目。

## A. セキュリティ

### 認証（CRITICAL）

- [ ] Server Actions / API で `supabase.auth.getUser()` を呼び出している
- [ ] `getSession()` のみで認証判定していない
- [ ] 認証エラー時に適切なエラーレスポンスを返している
- [ ] 未認証ユーザーがデータにアクセスできない

### データ保護

- [ ] パスワード、トークン、個人情報がログに出力されていない
- [ ] API レスポンスに不要なセンシティブデータが含まれていない
- [ ] 環境変数を直接クライアントに公開していない

## B. アーキテクチャ

### 3層構造（CRITICAL）

```
Page Component → Server Action / API → Edge Function → DB
```

- [ ] Page Component から直接 DB にアクセスしていない
- [ ] ビジネスロジックが Edge Function に委譲されている
- [ ] Server Action は薄いレイヤーとして機能している

### コロケーション（HIGH）

```
app/[feature]/
├── _actions/      # データ変更用 Server Actions
├── _apis/         # データ取得用 API（.server.ts）
├── _components/   # ページ固有コンポーネント
└── page.tsx
```

- [ ] Server Actions は `_actions/` に配置されている
- [ ] API クライアントは `_apis/` に `.server.ts` 拡張子で配置されている
- [ ] ページ固有コンポーネントは `_components/` に配置されている
- [ ] 複数ページで共有するコンポーネントは `components/` に配置されている

### Server/Client 分離（HIGH）

- [ ] `"use client"` はインタラクティブなコンポーネントのみに付与
- [ ] page.tsx が `"use client"` になっていない
- [ ] データフェッチは Server Component で実行
- [ ] useState / useEffect / イベントハンドラを使うコンポーネントのみ Client Component

## C. Server Actions

### 基本構造

- [ ] ファイル先頭に `"use server"` がある
- [ ] ファイル名はリソース名（例: `todo.ts`, `user.ts`）
- [ ] 状態型 (`State`) がエクスポートされている

### バリデーション

- [ ] Zod スキーマで入力をバリデーションしている
- [ ] `safeParse` を使用し、エラー時は `fieldErrors` を返している
- [ ] バリデーション済みデータのみを後続処理で使用している

### 関数シグネチャ

```typescript
// useActionState 対応の正しいシグネチャ
export async function actionName(
  prevState: ActionState,  // 第1引数: 前回の状態
  formData: FormData,      // 第2引数: フォームデータ
): Promise<ActionState>
```

- [ ] 第1引数が `prevState`（前回の状態）
- [ ] 第2引数が `FormData`
- [ ] 戻り値が `Promise<State>`

### キャッシュ更新

- [ ] データ変更後に `revalidatePath()` を呼び出している
- [ ] 適切なパスを `revalidatePath` に渡している

## D. フォーム実装

### useActionState

- [ ] `useActionState(serverAction, initialState)` を使用している
- [ ] `initialState` が適切に定義されている
- [ ] `[state, formAction, pending]` の3つを受け取っている

### UI

- [ ] `<form action={formAction}>` で Server Action を接続している
- [ ] Uncontrolled Component を優先（不要な `useState` + `onChange` がない）
- [ ] `pending` 中は送信ボタンに `disabled={pending}` を設定
- [ ] `pending` 中はボタンテキストを変更（例: "送信中..."）
- [ ] バリデーションエラーをフィールドごとに表示
- [ ] 全体のエラーメッセージを `role="alert"` で表示

## E. ログ出力

### 基本

- [ ] `createLogger` で共通ロガーを生成している
- [ ] `console.log` / `console.error` を直接使用していない

### タイミング

- [ ] 処理開始時に `logger.start()` を呼び出している
- [ ] 処理終了時に `logger.end({ success })` を呼び出している
- [ ] 例外発生時に `logger.error(err)` で記録している
- [ ] 重要な処理（DB操作、外部API呼び出し）前後で `logger.info()` を出力している

## F. TypeScript

### 型定義

- [ ] `type` を使用している（`interface` ではなく）
- [ ] 共通型は `src/types/index.ts` に集約されている
- [ ] database.types.ts の型をベースに再定義している
- [ ] `any` 型を使用していない
- [ ] 型アサーション (`as`) を最小限にしている

## G. スタイリング

- [ ] `cn()` でクラス名を結合している
- [ ] Tailwind CSS のユーティリティクラスを使用している
- [ ] インラインスタイル (`style={}`) を使用していない
- [ ] shadcn/ui のコンポーネントを活用している

## H. 命名規則

### ファイル名

| 種別 | 規則 | 例 |
|------|------|-----|
| コンポーネント | PascalCase ディレクトリ | `_components/NewTodoForm/index.tsx` |
| Server Action | リソース名 | `_actions/todo.ts` |
| API クライアント | リソース名 + `.server.ts` | `_apis/todo.server.ts` |
| 型定義 | ケバブケース | `types/demo-types.ts` |
| ユーティリティ | ケバブケース | `utils/date-helpers.ts` |

### 変数・関数

- [ ] 変数・関数: camelCase
- [ ] 型・コンポーネント: PascalCase
- [ ] 定数: UPPER_SNAKE_CASE（必要に応じて）
- [ ] boolean: `is`, `has`, `should` プレフィックス

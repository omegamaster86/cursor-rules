---
title: Supabase Best Practices
impact: HIGH
impactDescription: Supabase 実装のベストプラクティス
tags: supabase, best-practices
---

## Supabase Best Practices

Supabase を使用した実装のベストプラクティスです。

### Database Functions

| 推奨 | 説明 |
|------|------|
| ✅ | 複雑なクエリは Database Functions にまとめる |
| ✅ | トランザクションが必要な処理は Functions で実装 |
| ✅ | 関数名は用途が分かりやすい名前にする |
| ✅ | 引数と戻り値の型を明確に定義する |
| ❌ | 単純な SELECT は直接 Supabase Client から実行する方が効率的 |

### Edge Functions

| 推奨 | 説明 |
|------|------|
| ✅ | 必ずログ出力を実装する |
| ✅ | エラーハンドリングを適切に行う |
| ✅ | 環境変数を使用して設定を管理 |
| ✅ | `database.types.ts` から型定義をインポートして型安全性を確保する |
| ✅ | `Database` 型と `Tables` 型を使用して型を定義する |
| ✅ | データベーススキーマ変更後は必ず `database.types.ts` を再生成する |
| ✅ | 日付を使用する場合は、クライアントから引数として受け取る |
| ❌ | 機密情報をコードにハードコーディングしない |
| ❌ | 型定義なしで `any` 型を使用しない |
| ❌ | サーバー内部で現在日時を生成しない（テスト容易性・再現性のため） |

### 日付の取り扱い

> ⚠️ **重要**: Edge Functions 内で `new Date()` を使用して現在日時を生成しないでください。

**理由：**
- テストが困難になる（モックが必要）
- 再現性がない（同じリクエストで異なる結果）
- タイムゾーンの問題が発生しやすい

**推奨パターン：**

```typescript
// ❌ 非推奨: サーバー内部で日時を生成
const { data } = await supabase.rpc("sel_data", {
  target_date: new Date().toISOString(),
});

// ✅ 推奨: クライアントから日時を受け取る
const targetDate = url.searchParams.get("date");
const { data } = await supabase.rpc("sel_data", {
  target_date: targetDate,
});
```

### データアクセスの階層構造

Next.js における Supabase のデータアクセスは、3層アーキテクチャで実装します：

```
Page Component → Server Action → Edge Function → Database Function
```

| 層 | 役割 |
|----|------|
| Page Component | UI の表示、ユーザー操作の受付 |
| Server Action | Edge Function の呼び出し、エラーハンドリング |
| Edge Function | 認証、ビジネスロジック、Database Function の呼び出し |
| Database Function | データベース操作、SQL 実行 |

### 認証処理

| ルール | 説明 |
|--------|------|
| サーバーサイドでは `getUser()` を使用 | JWT をサーバーで検証するため |
| クライアントサイドでは `getSession()` を使用 | 高速なアクセスが可能 |
| Edge Function 呼び出し時は `access_token` を渡す | 認証情報を引き継ぐため |

> 📖 **詳細**: 認証処理の詳細は `edge-auth.md` を参照

**チェックリスト：**

- [ ] 複雑なクエリは Database Functions にまとめている
- [ ] Edge Functions にログ出力を実装している
- [ ] 型定義を使用している（`any` を使っていない）
- [ ] 日付はクライアントから受け取っている
- [ ] 3層アーキテクチャに従っている
- [ ] 認証処理は `getUser()` を使用している（サーバーサイド）

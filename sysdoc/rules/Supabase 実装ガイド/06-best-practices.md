# Supabase 実装ガイド（分割）: ベストプラクティス

## 4. ベストプラクティス

### 4.1 Database Functions

- ✅ 複雑なクエリは Database Functions にまとめる
- ✅ トランザクションが必要な処理は Functions で実装
- ✅ 関数名は用途が分かりやすい名前にする
- ✅ 引数と戻り値の型を明確に定義する
- ❌ 単純な SELECT は直接 Supabase Client から実行する方が効率的

### 4.2 Edge Functions

- ✅ 必ずログ出力を実装する
- ✅ エラーハンドリングを適切に行う
- ✅ CORS 設定を適切に行う
- ✅ 環境変数を使用して設定を管理
- ✅ `database.types.ts` から型定義をインポートして型安全性を確保する
- ✅ `Database` 型と `Tables` 型を使用して型を定義する
- ✅ データベーススキーマ変更後は必ず `database.types.ts` を再生成する
- ✅ 日付を使用する場合は、クライアントから引数として受け取る（`new Date()` をサーバー内部で生成しない）
- ❌ 機密情報をコードにハードコーディングしない
- ❌ 型定義なしで `any` 型を使用しない
- ❌ サーバー内部で現在日時を生成しない（テスト容易性・再現性のため）

### 4.3 RLS ポリシー

- ✅ すべてのテーブルで RLS を有効化
- ✅ Edge Functions 用のポリシーを設定
- ✅ 最小権限の原則に従う
- ❌ `service_role` キーを不用意に使用しない

### 4.4 データアクセスの階層構造

Next.js における Supabase のデータアクセスは、3層アーキテクチャ（Page Component → Server Action → Edge Function → DB Function）で実装することが推奨されます。詳細は以下のドキュメントを参照してください。

> 📖 **詳細**: [04\_コーディング規約\_Web.md](04_コーディング規約_Web.md) の「4. Supabaseデータアクセス規約」を参照

### 4.5 認証処理

Next.js における Supabase の認証処理（`getUser()`/`getSession()` の使い分け、Edge Function 呼び出し時の認証など）については、以下のドキュメントを参照してください。

> 📖 **詳細**: [04\_コーディング規約\_Web.md](04_コーディング規約_Web.md) の「3. Supabase 認証規約」を参照

---

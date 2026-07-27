---
title: Edge Functions Deploy
impact: MEDIUM
impactDescription: Edge Functions のデプロイ手順
tags: supabase, edge-functions, deploy
---

## Edge Functions Deploy

開発が完了した Edge Functions のデプロイ手順です。

**基本コマンド：**

```bash
# 基本コマンド
supabase functions deploy [開発したファンクション名] --project-ref [デプロイ先のプロジェクトID]

# 例
supabase functions deploy get-user-data --project-ref abcdefghijklmnop
```

**デプロイ前の確認事項：**

1. **ローカルでの動作確認**
   - SQL Editor で Database Functions が正しく動作することを確認
   - Edge Functions のコードにエラーがないことを確認

2. **環境変数の設定**
   - `EDGE_FUNCTION_ALLOWED_ORIGIN` などの環境変数を本番環境に設定

3. **RLS ポリシーの確認**
   - 必要なテーブルにポリシーが設定されているか

**トラブルシューティング：**

> 💡 **デプロイした Edge Functions が正常に動作しないとき**:
>
> Supabase 側でテーブルの policy を確認してください。対応する policy がない場合、Edge Functions が正常に動作しません。

**確認項目：**

1. **RLS（Row Level Security）が有効になっているか**
   - テーブルに RLS が有効化されていることを確認

2. **`service_role` または `anon` キーに対するポリシーが設定されているか**
   - Edge Functions が使用するキーに応じたポリシーを設定

3. **Edge Functions が実行するクエリに必要な権限があるか**
   - SELECT / INSERT / UPDATE / DELETE の権限を確認

**Supabase Dashboard での確認方法：**

1. Supabase Dashboard にログイン
2. 対象プロジェクトを選択
3. Table Editor → 対象テーブル → RLS Policies を確認
4. 必要なポリシーが設定されているか確認

**チェックリスト：**

- [ ] Database Functions が SQL Editor で動作確認済み
- [ ] Edge Functions のコードにエラーがない
- [ ] 環境変数が本番環境に設定済み
- [ ] RLS ポリシーが適切に設定されている
- [ ] デプロイコマンドを正しいプロジェクト ID で実行

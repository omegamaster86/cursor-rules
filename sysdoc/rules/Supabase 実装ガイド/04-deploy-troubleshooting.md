# Supabase 実装ガイド（分割）: デプロイ/トラブルシューティング

### 2.6 デプロイ

開発が完了したらデプロイします。

```bash
# 基本コマンド
supabase functions deploy [開発したファンクション名] --project-ref [デプロイ先のプロジェクトID]

# 例
supabase functions deploy get-user-data --project-ref abcdefghijklmnop
```

### 2.7 トラブルシューティング

> 💡 **デプロイしたEdge Functionsが正常に動作しないとき**:
> 
> Supabase側でテーブルのpolicyを確認してください。対応するpolicyがない場合、Edge Functionsが正常に動作しません。

**確認項目**:
1. RLS（Row Level Security）が有効になっているか
2. `service_role` または `anon` キーに対するポリシーが設定されているか
3. Edge Functions が実行するクエリに必要な権限があるか

---

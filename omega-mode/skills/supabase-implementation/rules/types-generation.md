---
title: Type Generation
impact: HIGH
impactDescription: database.types.ts の生成方法
tags: supabase, typescript, types
---

## Type Generation

`database.types.ts` は Supabase のスキーマから自動生成される型定義ファイルです。バックエンドトラックの契約合流は `forge-mode/principles/foundational-thinking.md` を参照。

**生成コマンド：**

```bash
# Edge Functions 用（supabase/functions/_shared/）
npx --yes supabase gen types typescript --schema public --local > supabase/functions/_shared/database.types.ts && npx @biomejs/biome check --write supabase/functions/_shared/database.types.ts

# Next.js クライアント用（src/types/）
npx --yes supabase gen types typescript --schema public --local > src/types/database.types.ts && npx @biomejs/biome check --write src/types/database.types.ts
```

**実行タイミング：**

| タイミング | 必須 |
|-----------|------|
| データベースマイグレーション後 | ✅ |
| テーブル定義を変更した後 | ✅ |
| Database Functions を追加・変更した後 | ✅ |
| RLS ポリシーを追加した後 | - |

**生成される型：**

| 型 | 説明 | 使用例 |
|----|------|--------|
| `Database` | 全体のデータベース型定義 | `Database["public"]["Tables"]["users"]["Row"]` |
| `Tables` | テーブルの型（簡潔な書き方） | `Tables["m_customer"]` |
| Functions | Database Functions の型 | `Database["public"]["Functions"]["sel_user"]["Returns"]` |
| `Enums` | Enum 型の定義 | `Enums["user_status"]` |

**ワークフロー例：**

```bash
# 1. マイグレーションを適用
supabase db push

# 2. 型定義を再生成（両方の場所に生成）
npx --yes supabase gen types typescript --schema public --local > supabase/functions/_shared/database.types.ts && npx @biomejs/biome check --write supabase/functions/_shared/database.types.ts
npx --yes supabase gen types typescript --schema public --local > src/types/database.types.ts && npx @biomejs/biome check --write src/types/database.types.ts

# 3. Edge Functions をデプロイ
supabase functions deploy function-name --project-ref your-project-id
```

> ⚠️ **重要**: データベーススキーマを変更したら、必ず型定義を再生成してください。型定義が古いままだと、Edge Functions で型エラーが発生する可能性があります。

**チェックリスト：**

- [ ] マイグレーション後に型定義を再生成した
- [ ] `supabase/functions/_shared/database.types.ts` が最新
- [ ] `src/types/database.types.ts` が最新
- [ ] Biome でフォーマット済み


## Supabase ルール参照マップ

Supabase関連の変更を行う前に以下を読む:

- `/.cursor/rules/Supabase 実装ガイド.md`
- `/.cursor/rules/コーディング規約/03-supabase-auth.md`
- `/.cursor/rules/コーディング規約/04-supabase-data-access.md`
- `/.cursor/rules/コーディング規約/08-logging.md`

確認対象の主な場所:

- `supabase/functions/_shared/`（logger/auth/cors/response など）
- `supabase/functions/`（Edge Functions）
- `supabase/migrations/`（SQL関数マイグレーション）
- `src/services/supabase/`（Next.js Supabase クライアント）


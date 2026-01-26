---
name: supabase-workflows
description: Supabase Edge Functions、DB関数、マイグレーション、Next.jsのSupabaseデータアクセス向けスキル。`supabase/` 配下の作業、Edge Functions の追加/更新、SQL関数/マイグレーション、`src/` の Supabase 認証/データアクセスを扱うときに使用。
---

## 概要

Edge Functions、SQL DB関数、マイグレーション、Next.jsのデータアクセスを実装する際に、Supabase関連ルールを一貫適用する。

## 必須参照

作業前に `references/rules-map.md` を読み、該当する規約章を読み込む。

## ワークフロー選択

対象に応じて以下を使用する:

- Edge Function の実装/更新 → 「Edge Function ワークフロー」
- DB関数またはマイグレーション → 「Database Function ワークフロー」
- Next.js の Supabase データアクセス/認証 → 「Next.js データアクセスワークフロー」

## Edge Function ワークフロー

1. `references/rules-map.md` から Supabase ガイドとログ/認証規約を読む。
2. メソッド制限（GETのみ or 必要最小限）と CORS を確認する。
3. 開始/終了/例外の構造化ログを実装し、機微情報は出力しない。
4. `database.types.ts` を使って戻り値を型付けし、`any` は使わない。
5. サーバー側で日時を生成しない。日付はリクエストから受け取る。
6. 返却ヘッダに CORS とエラーハンドリングを含める。

## Database Function ワークフロー

1. 関数名の接頭辞（`sel_`/`ins_`/`upd_`/`del_`/`upsert_`）を確認する。
2. 戻り値の型（`TABLE`/スカラー/`void`）を明示する。
3. SQL Editor で試作してからマイグレーションへ転記する。
4. SQLは migrations で管理し、スキーマ変更後は `database.types.ts` を再生成する。

## Next.js データアクセスワークフロー

1. Page → Server Action → Edge Function → DB Function の流れに従う。
2. `getUser()`/`getSession()` の使い分けは認証規約に従う。
3. `schemas.ts` と API バリデーション規約に合わせて整合させる。

## 最終チェック

- 同名/類似の関数やエンドポイントがないか確認する。
- ログ、CORS、認証規約が守られているか確認する。
- DB関数やスキーマ変更後は型定義を再生成する。


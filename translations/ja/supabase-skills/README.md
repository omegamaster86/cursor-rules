# supabase-skills 日本語翻訳

`supabase-skills` は英語のソース用サブモジュールとしてのみ扱います。
日本語訳はこのディレクトリ配下で管理します。

## ディレクトリ方針

- ソース（英語）: `supabase-skills/...`
- 翻訳（日本語）: `translations/ja/supabase-skills/...`
- 可能な限り、同じ相対パスとファイル名を維持する。

例:

- 英語: `supabase-skills/skills/supabase-postgres-best-practices/references/data-pagination.md`
- 日本語: `translations/ja/supabase-skills/skills/supabase-postgres-best-practices/references/data-pagination.md`

## 更新ワークフロー

1. サブモジュールを最新の上流変更（fork origin 経由）に更新する。
2. サブモジュールのコミットで変更ファイルを確認する。
   - `git -C supabase-skills log --oneline --decorate --max-count=20`
   - `git -C supabase-skills diff --name-only <old_commit>..<new_commit>`
3. 変更された英語ファイルに対して、`translations/ja/supabase-skills/...` 配下の対応ファイルのみ更新する。
4. 翻訳専用の注記は日本語ファイル側に保持する（翻訳目的で英語原文は変更しない）。

## 補足

- まだ翻訳がない場合は、対応するミラーパスに日本語ファイルを作成する。
- 上流で新規ファイルが追加された場合は、必要なときのみ新しい翻訳ファイルを追加する。

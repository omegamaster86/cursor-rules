# レンズ: Supabase / PostgREST

変更に `supabase/migrations` または `supabase/db-functions` があるとき必須。Edge・クライアントは [edge-functions.md](edge-functions.md) と合わせて `storage-chain` を追う。

## admin-rpc

- 名前が `*_for_admin`、またはコメントが管理操作の関数。
- 先頭約 40 行に `is_admin()` または `auth.role() = 'service_role'` があるか。
- `SECURITY INVOKER` なら、呼び出し元ロールのテーブル RLS で **自分の行 UPDATE が状態遷移（承認など）を完了しないか**。
- migration が `GRANT EXECUTE … TO service_role` のみでも、スキーマの `ALTER DEFAULT PRIVILEGES … GRANT ALL ON FUNCTIONS TO anon|authenticated` が残っていれば **authenticated / anon 実行を候補にする**。
- 他ユーザー ID は RLS で届かなくても、**自分の ID で特権操作が通る**経路は別候補（自己承認など）。

## pg-grant

- 変更 migration の `GRANT … ON FUNCTION` を列挙する。
- `anon` 付与は、到達結果を 1 行で分ける: 情報プロービングのみ / 書き込みが RLS で拒否 / 書き込みが通る。
- プロービングのみは Medium 候補にしてよい。`anon` で作成できると書くのは INSERT が通る根拠があるときだけ。
- `count_*_for_admin` と `sync_*` は admin 本体と同じ GRANT 棚卸しに含める。

## rpc-idor

- 引数名が `p_user_id` / `target_user_id` / `p_auth_user_id` の関数。
- `auth.uid()` または「JWT のユーザーに対応する `m_user.id`」との一致が関数内または唯一の呼び出し元にあるか。
- 呼び出し元が service_role で、**その前段 Edge が ID を差し替えていない**場合は Edge 側の候補（`edge-validation`）に回す。
- `SECURITY INVOKER` でも、RLS が他人の行を隠すだけで **渡した ID の業務データを返す**なら IDOR 候補。

## rls-disclosure

- 変更された `CREATE POLICY` の `USING (true)` や、公開リソースに紐づく広い `SELECT`。
- プロダクトが公開してよい列か、PII・ターゲット条件・内部 ID かを分けて書く。意図がコードから決まらないときは候補の `confidence` を provisional にし、RESULTS の肯定所見ではなく指摘に残す。

## storage-chain

- `storage.objects`: `SELECT` の `TO public` / `TO anon`、`INSERT` の `WITH CHECK` に `auth.uid()` または所有者プレフィックスがあるか。
- クライアントのオブジェクト名がポリシー正規表現を満たすかと、**ユーザー ID と無関係か**は分けて書く。形式が通るのに「ポリシー不一致」と書かない。
- 公開 URL（`getPublicUrl`）を保存・再提出に使っているクライアントは、公開 SELECT ポリシーと同じ候補群に紐づける。
- Edge がその URL を形式チェックだけして DB に書く場合は `edge-validation` の候補を別に出す。

## client-trust

- 管理画面が `tagsCatalogOk` や hidden input など **クライアント宣言**でサーバ payload の有無を変えていないか。
- 空配列・null が「変更しない」と「全員対象 / 全削除」のどちらになるかを DB 関数（`sync_*`、audience 判定）まで読む。
- 外部匿名攻撃でなくても、管理者操作の fail-open は候補にする。深刻度は「誰がトリガーか」で High か Medium かを書く。

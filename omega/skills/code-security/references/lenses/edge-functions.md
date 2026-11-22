# レンズ: Edge Functions

変更に `supabase/functions` があるとき必須。

## edge-validation

- 認証済みユーザーから受け取った URL・パス・外部 ID は、形式（正規表現・ホスト）に加えて **所有者**（そのユーザーの `m_user`、許可バケット、オブジェクトのプレフィックス）を見ているか。
- 形式 OK のあと `service_role` で RPC する関数は、RPC 側に認可が無くても **Edge が ID を縛っているか**を候補の攻撃経路に書く。
- 管理系は `requireAdminWithServiceRole`（または同等）の有無を記録する。ある場合は「Edge 経由は管理者」と「PostgREST で同名 RPC を直叩き」を混ぜない。直叩きは [supabase-postgrest.md](supabase-postgrest.md) の `admin-rpc`。

## 共有クライアント

- `SUPABASE_SERVICE_ROLE_KEY` で作ったクライアントの直前に、ユーザー入力の認可チェックが終わっているか。
- ログへトークン、学生証 URL、FCM payload 全文を出していないか（出すなら `secrets` または disclosure の別候補）。

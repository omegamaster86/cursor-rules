# Cursor 単体セキュリティチェックリスト

公式スキャナが使えない、または軽い差分レビュー向け。深いスキャンは [codex-security.md](codex-security.md) / [claude-security.md](claude-security.md) に委譲する。

## 0. スコープの固定

1. 差分の取得: `git diff <base>...HEAD` または `gh pr diff`
2. 変更ファイルを **auth / billing / data / migration / public API** にタグ付け
3. `SECURITY.md`・プロジェクトの `.claude/claude-security-guidance.md` があれば先に読む

## 1. 認証・認可（最優先）

- [ ] すべての mutating 経路で主体（user / service）が確定しているか
- [ ] オブジェクト ID をユーザー入力から取る場合、**所有者・テナント**を DB またはポリシーで検証しているか（IDOR）
- [ ] Server Action / API Route でセッション検証が共通化されているか（`getUser()` 等）
- [ ] 管理者・課金・ロール変更が単一のガード経路を通るか

## 2. インジェクション

- [ ] SQL: パラメータ化・クエリビルダ。文字列連結の動的 SQL なし
- [ ] コマンド実行: ユーザー入力がシェルに渡らない
- [ ] テンプレート / HTML: `innerHTML`、テンプレートエンジンの未エスケープ出力
- [ ] パス: `../` や絶対パスで任意ファイル読み書き

## 3. シークレット・暗号

- [ ] リポジトリ・ログ・クライアントバンドルに API 鍵・トークン・秘密鍵がない
- [ ] 環境変数はサーバー側のみ。`NEXT_PUBLIC_*` に秘密を載せていない
- [ ] 弱いハッシュ（MD5/SHA1 単体）でパスワードを保存していない

## 4. SSRF・外向き通信

- [ ] ユーザー指定 URL へのサーバー側 fetch に allowlist または固定ホスト
- [ ] 内部メタデータ（169.254.x、docker 内部 DNS）への到達経路
- [ ] Webhook / OAuth redirect のオープンリダイレクト

## 5. データ・ログ・観測性

- [ ] ログ・トレース・エラーメッセージに PII・トークン・全文リクエストが載らない
- [ ] クライアントにスタックトレースや DB エラー詳細を返していない

## 6. 依存・サプライチェーン

- [ ] 変更に新規依存があれば用途と信頼性（`npm audit` は補助）
- [ ] 危険 API: `pickle` / `yaml.load`（Loader なし）/ `eval` / 不安全なデシリアライズ

## 7. IaC・CI/CD

- [ ] Terraform/Pulumi でセキュリティ関連オプションがデフォルトのまま省略されていないか
- [ ] `pull_request_target` / `workflow_dispatch` で secrets や write 権限が広すぎないか

## 8. ドメイン別（リンク）

| 領域 | omega スキル |
|------|----------------|
| Supabase / RLS | `supabase-code-review`, `supabase-implementation` の `security-rls` |
| Next.js 認証 | `web-coding-standards` の `supabase-auth` |
| PR 上の Bot コメント | `forge-mode/references/bugbot-triage.md` |

## 9. 出力

結果は [report-format.md](report-format.md) に従う。公式スキャンと併用した場合は **エンジン列**に両方を記載する。

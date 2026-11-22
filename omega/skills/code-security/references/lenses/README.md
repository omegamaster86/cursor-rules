# 調査レンズ

`security-review` が差分で拾いやすく、panel 調査で束ね・provisional に埋もれやすい観点。Researchers はデータフロー追跡に加え、**適用レンズごとに候補を 1 件以上出すか、出さない理由を `lens_coverage.json` に書く**。

## 適用

| 差分・スコープに含まれるもの | 必須レンズ |
|------------------------------|------------|
| `supabase/migrations` または `supabase/db-functions` | [supabase-postgrest](supabase-postgrest.md) の全節 |
| `supabase/functions` | [edge-functions](edge-functions.md) |
| Storage policy またはクライアントの upload / `getPublicUrl` | `storage-chain`（supabase-postgrest） |
| 管理 UI の server action がクライアント由来フラグで保存内容を決める | `client-trust`（supabase-postgrest） |

該当ファイルが無いレンズは `lens_coverage.json` に `status: not_applicable`。

## レンズ ID

| id | 見るもの |
|----|----------|
| `admin-rpc` | `*_for_admin`、`SECURITY INVOKER`、`is_admin()`、`DEFAULT PRIVILEGES` |
| `pg-grant` | `GRANT … TO anon/authenticated` と関数先頭の認可 |
| `rpc-idor` | `*_user_id` が caller と未束縛 |
| `rls-disclosure` | RLS が広い SELECT（意図的開示か） |
| `storage-chain` | Storage policy ↔ クライアントパス ↔ Edge の URL 検証 |
| `edge-validation` | Edge が形式のみ見て所有者・バケットを見ない |
| `client-trust` | クライアントフラグの fail-open |

## 候補の書き方

- **1 候補 = 1 攻撃経路**。`F5–F6` のように複数経路を 1 タイトルに束ねない。
- 各候補 JSON に `lens`（上表の id）と `category`（`authz` / `disclosure` / `injection` / `validation` / `secrets` / `other`）を付ける。
- 正規表現が「ファイル名形式は通る」ことと「`auth.uid()` と無関係」は別問題。不一致と書くのはソースで形式が拒否されるときだけ。
- Edge に管理者ガードがあっても、同名 RPC の PostgREST 直叩きは **別経路として同じレンズ内の別候補**にする（「Edge があるから安全」で落とさない）。

## カバレッジファイル

成果物ディレクトリ（`.code-security-run/` ではない。削除されない側）に `lens_coverage.json`:

```json
{
  "lenses": [
    {
      "id": "rpc-idor",
      "status": "candidates",
      "candidate_ids": ["C3"],
      "notes": ""
    },
    {
      "id": "rls-disclosure",
      "status": "none",
      "reason": "変更 migration に CREATE POLICY なし"
    }
  ]
}
```

`status`: `candidates` / `none` / `not_applicable`。`none` は grep または読んだパスを `reason` に残す。

## 検証

Critical / High の候補は [verifier-panel.md](../verifier-panel.md) が完了するまで `confidence: verified` にしない。panel 未完了なら `provisional` と RESULTS の検証欄に理由を書く。

# スレットモデル（inventory 後）

codex-security / claude-security の codebase スキャンで、inventory の後に 1 回だけ書く。

## 出力（Markdown 短章）

1. **Assets** — 守るもの（ユーザーデータ、鍵、課金、管理機能）
2. **Entry points** — HTTP、CLI、Webhook、キュー、ファイル upload、MCP ツール入力
3. **Trust boundaries** — 認証前/後、テナント、サービス間、サンドボックス外
4. **Attacker model** — 匿名、認証済み一般ユーザー、侵害済み依存、内部者
5. **Scenarios** — 3–7 本の具体的シナリオ（入力 → 処理 → 敏感操作）

リポジトリの `SECURITY.md` があれば読み、矛盾する仮定は scenarios に注記する。

## 調査パケットへの落とし込み

各パケットに含める:

- 共有する attacker / asset
- エントリポイントのファイルパス
- 検証すべきコントロール（認可、検証、レート制限）
- 関連ソースパス（推測のパスは書かない）

Investigator の切り口（codex-security 流）:

- **Forward** — 入力から敏感操作へ
- **Backward** — 敏感操作から呼び出し元へ
- **AuthZ / ロジック** — 所有者・テナント・状態遷移
- **Open** — 上記に当てはまらない有力なリード

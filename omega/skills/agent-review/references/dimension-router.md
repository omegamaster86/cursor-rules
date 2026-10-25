# Dimension Router

親オーケストレーターがフェーズ0.3で実施。`changed_files` と `diff_stat` と diff パッチのキーワードのみ（リポジトリ全体スキャン禁止）。

## 出力

`dimension_router_summary`（Markdown）と `launch_blast_radius: boolean`。

## スコア（blast-radius レーン）

各 +1、合計 `blast_score`:

| 信号 | 点数 |
|------|------|
| migration / schema / `prisma/schema` / `supabase/migrations` | +2 |
| `packages/` / `shared/` / `lib/` の export 署名変更（diff に `export` 削除・公開 API 変更） | +2 |
| feature flag / 環境変数の削除・デフォルト変更 | +1 |
| ルーティング・middleware・認可ポリシー変更 | +1 |
| 変更ファイル数 ≥ 25 | +1 |
| refactor で rename 多数（diff stat で rename 比率が高い） | +1 |

## 起動判定

- `blast_score >= 2` → `launch_blast_radius: true`
- `change_scope.force_blast: true` → 常に true
- `change_scope.skip_blast: true` → 常に false

## Security / Quality / Correctness

- **Security レーン**: 常に起動（専任。正しさレーンは委譲）。
- **Quality レーン**: 常に起動。
- **Correctness A/B**: 常に起動（挙動・回帰のみ。セキュリティ深掘りは委譲）。

## 親が保持する内容（ファイルに書かない）

- blast_score と加点理由（トリガー列）
- launch_blast_radius
- tier（S: ≤10 files / M: 11–49 / L: ≥50 または migration +2 あり）

統合時は `consolidated.md` の Dimension Router セクションに載せる。

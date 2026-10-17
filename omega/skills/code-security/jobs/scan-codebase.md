# Job: scan codebase（panel 方式）

リポジトリ全体または `--scope`。Security Lead は [../references/security-lead.md](../references/security-lead.md)。

## 引数

- `[path]` — スキャンルート
- `--scope dirs`
- `--effort low|medium|high`（既定 medium）

## Effort

| tier | 流れ |
|------|------|
| low | 単一 researcher → [verifier-panel](../references/verifier-panel.md) |
| medium | inventory Task → threat model → コンポーネントごと researcher（小 scope ≤5 ファイルは low 形状）→ panel |
| high | medium の researcher 数を増やし、重要コンポーネントは 2 研究者 |

## 手順

1. **スコープ確認** — 大規模で scope なしなら 1 問（全体 vs 領域）。`GIT_CONFIG_GLOBAL=/dev/null GIT_TERMINAL_PROMPT=0 git -C <root> ls-files | wc -l` でサイズ感
2. **コスト確認** — 未承諾なら 1 回だけ
3. **成果物ディレクトリ** — [../references/artifacts.md](../references/artifacts.md)。stamp の `job`: `scan-codebase`, `mode`: `scan`
4. **Inventory Task**（low 以外）— トップレベルディレクトリをコンポーネントに分割。未割当ディレクトリがあれば coverage に記録
5. **Threat model** — [../references/threat-model.md](../references/threat-model.md)
6. **Researchers** — 並列 Task。各 scope で脆弱性 candidate を JSON 配列で返す（id はまだ仮 `C1` 可）
7. **Verifier panel** — finding ごとに 3 verifier Task。2/3 accept で `F<n>` を採番し verified
8. **Redact** — レポート生成前に秘密値を `[REDACTED]` に置換
9. **RESULTS.md / findings.jsonl** — [../references/report-format.md](../references/report-format.md)。`verification.status`: researchers 全員返却かつ panel 完了なら `verified`、否则 `unverified` と理由
10. `.code-security-run/` 削除

## ユーザーへの締め

finding 数、レポートパス、verified か、fixes 希望の質問（finding があるときのみ）。

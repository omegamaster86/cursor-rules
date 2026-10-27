# lane-correctness-ab.md 出力フォーマット（厳守）

親は **レーン A と B の両方が完了**（または片方 Failed）した直後（オーケストレーター **フェーズ2.6**）、フェーズ2の `consolidated.md` より **先に** 本ファイルを `artifact_dir` に書く。統合ルールは [consolidation.md](consolidation.md) の **Correctness（A × B）** に従う。

生のサブエージェント出力は [artifacts.md](artifacts.md) の `lane-correctness.md` にある。本ファイルは **重複指摘のマージ・信頼度付け・正しさレーン単体の Must Fix** の正本。

```markdown
# Correctness Lane（A × B 統合）

## Lane Models

- Lane A: <model from lanes.A>
- Lane B: <model from lanes.B>

## Lane Status

- A: Complete | Failed — <1行要約>
- B: Complete | Failed — <1行要約>

## Cross-Check Summary

- Both reported CRITICAL on same issue: <件数>（高信頼 Must Fix 候補）
- A-only CRITICAL: <件数>
- B-only CRITICAL: <件数>
- Severity conflicts: <件数>（A/B で重大度が食い違う指摘）

## Integrated Findings

| ID | Finding | Severity | Confidence | Sources | Notes |
|----|---------|----------|------------|---------|-------|
| C1 | … | CRITICAL / IMPORTANT / LOW | high（両方） / medium（片方） / low | A, B / A / B | 再現・影響・最小修正案 |

信頼度:

- **high**: 同一論点で両レーンが `CRITICAL`、または両方が同趣旨の IMPORTANT 以上
- **medium**: 片側のみ `CRITICAL` → Must Fix 候補 + **要追加検証** を Notes に書く
- **low**: 片側のみ LOW、または片側 Failed で残側のみ

## Correctness Must Fix

（Integrated Findings からマージ前の正しさ Must Fix。全体の Must Fix 正本は `consolidated.md`）

## Correctness Can Defer

## Nextjs Code Review Compliance（A × B）

（A/B の準拠評価を統合。矛盾は Severity conflicts にも反映）

## Raw Transcripts

- `lane-correctness.md`（Lane A / Lane B 全文）
```

Failed レーンがあるとき: Integrated Findings は成功側のみで埋め、Cross-Check Summary に parent fallback を記載する。


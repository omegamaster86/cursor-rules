# consolidated.md 出力フォーマット（厳守）

# Triple Hybrid Review Result

## Artifact Paths

- Run ID:
- Directory: `.cursor/agent-review/<run_id>/`
- Correctness（A × B）: `lane-correctness-ab.md`
- Correctness raw（A/B）: `lane-correctness.md`

## Inputs

- Base Branch:
- Changed Files Count:
- Diff Stat:
- Resolved lane models:（`resolve-lane-models.mjs` の `lanes` 出力を表または JSON で記載）

## Dimension Router

- blast_score / launch_blast_radius / tier

## Structural Audit（差分スコープ）

（親フェーズ 0.5 の要約を本文に記載）

## Subagent Outputs

### Correctness（Lane A）

- Status / 要約 / Overall Risk → 全文 `lane-correctness.md` の `## Lane A`

### Correctness（Lane B）

- Status / 要約 / Overall Risk → 全文 `lane-correctness.md` の `## Lane B`

### Sonnet（Quality）

- Status / Quality Approval Bar → 全文 `lane-quality.md`

### Security

- Status / Top severity → 全文 `lane-security.md`

### Blast Radius

- Status / one fact proven|unproven → 全文 `lane-blast-radius.md`（Skipped 可）

## Correctness Lane（A × B 統合）

（要約のみ。Integrated Findings・信頼度・正しさ Must Fix の正本 → **`lane-correctness-ab.md`**）

## Quality Lane（C）

## Security Lane（D）

## Blast Radius Lane（E）

## Cross-Cut Consolidated Findings

## Severity Conflicts

## Must Fix Before Merge

## Quality Conditions

## Can Defer

## Merge Recommendation

## PR Discussion Alignment

## Nextjs Code Review Compliance

## Reviewed Files

## No-Issue Statement





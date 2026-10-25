# consolidated.md 出力フォーマット（厳守）

# Triple Hybrid Review Result

## Artifact Paths

- Run ID:
- Directory: `.cursor/agent-review/<run_id>/`
- Manifest: `manifest.json`

## Inputs

- Base Branch:
- Changed Files Count:
- Diff Stat:

## Dimension Router

- blast_score / launch_blast_radius / tier

## Structural Audit（差分スコープ）

（要約。全文は `structural-audit.md`）

## Subagent Outputs

### Codex（Correctness）

- Status / 要約 / Overall Risk → 全文 `lane-correctness-codex.md`

### Sonnet（Correctness）

- Status / 要約 / Overall Risk → 全文 `lane-correctness-sonnet.md`

### Sonnet（Quality）

- Status / Quality Approval Bar → 全文 `lane-quality.md`

### Security

- Status / Top severity → 全文 `lane-security.md`

### Blast Radius

- Status / one fact proven|unproven → 全文 `lane-blast-radius.md`（Skipped 可）

## Correctness Lane（A × B 統合）

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

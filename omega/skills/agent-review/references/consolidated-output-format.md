# チャット出力フォーマット（厳守）

フェーズ2完了後、親は **チャットに下記 `# Triple Hybrid Review Result` 全文を投稿する**（唯一の正本。[artifacts.md](artifacts.md)）。

要約のみ・ファイルパス案内だけ・レーン全文のファイル参照だけで終えることは **禁止**。

---

# Triple Hybrid Review Result

## Inputs

- Base Branch:
- Changed Files Count:
- Diff Stat:
- Resolved lane models:（`resolve-lane-models.mjs` の `lanes` を表または短い JSON。`warnings` があれば併記）

## Dimension Router

- blast_score:
- launch_blast_radius: yes | no
- tier: S | M | L

（セキュリティのみの Router 差分で blast 未起動のときも、上3行は埋める）

## Structural Audit（差分スコープ）

- 実施: yes
- 依存・import 異常: N 件
- 二重 export / 未参照 export: N 件
- クローン候補: N 件
- レイヤー・境界: N 件
- Top findings（path:line — 観点 — 要約）

## Subagent Outputs

（**起動した全レーンが完了後にのみ記載**。未完了を `応答未完了` と書いて統合しない）

### レーンA（Correctness）— Model:（1.9 解決値）

- Status: Completed / Failed
- task_id:（Failed 時のみ）
- 要約（3-6行）
- Overall Risk: High / Medium / Low

### レーンB（Correctness）— Model:（1.9 解決値）

- Status: Completed / Failed
- task_id:（Failed 時のみ）
- 要約（3-6行）
- Overall Risk: High / Medium / Low

### レーンC（Code Quality）— Model:（1.9 解決値）

- Status: Completed / Failed
- task_id:（Failed 時のみ）
- 要約（3-6行）
- Quality Approval Bar: Pass / Pass with conditions / Fail

### レーンD（Security）— Model:（1.9 解決値）

- Status: Completed / Failed / Skipped
- task_id:（Failed 時のみ）
- 要約（3-6行）
- Top severity: Critical / High / Medium / Low / None

### レーンE（Blast radius）— Model:（1.9 解決値）

- Status: Completed / Failed / Skipped
- task_id:（Failed 時のみ）
- 要約（1-3行）
- one fact: proven | unproven | N/A

## Correctness Lane（A × B 統合）

- [CRITICAL|IMPORTANT|LOW] タイトル
  - Source: LaneA / LaneB / Both
  - 事象:
  - 根拠:
  - 再現条件:
  - 影響範囲:
  - 最小修正案:
  - 推奨テスト:

（該当なし: `No integrated correctness findings.`）

## Quality Lane（C）

- [QUALITY-BLOCKER|QUALITY-IMPORTANT|QUALITY-NIT] タイトル
  - 事象:
  - 根拠（path:line）:
  - 保守性への影響:
  - 分解案 / code-judo 案:
  - 最小修正案:

## Security Lane（D）

- [CRITICAL|HIGH|MEDIUM|LOW] タイトル（レーン D の severity 定義に従う）
  - 事象:
  - 根拠（path:line）:
  - 影響範囲:
  - 最小修正案:

（Skipped / 指摘なし: `N/A` または No-Issue に委譲）

## Blast Radius Lane（E）

- 事象 / 検証結果 / 推奨テスト（起動時のみ）

## Cross-Cut Consolidated Findings

- [CRITICAL|IMPORTANT|LOW|QUALITY-*] タイトル
  - Source: LaneA / LaneB / Both / Quality / Security / Structural / Blast
  - 事象:
  - 根拠:
  - 最小修正案:

## Severity Conflicts

- 衝突があれば列挙（なければ `None`）

## Must Fix Before Merge

- 項目
- 理由
- 実施方針（1-2行）

## Quality Conditions

- 項目
- 理由
- 実施方針（1-2行）
- なければ `None`

## Can Defer

- 項目
- 理由
- チケット化メモ

## Merge Recommendation

- Correctness: Approve / Approve with conditions / Block
- Quality: Pass / Pass with conditions / Fail
- Overall: Approve / Approve with conditions / Block
- 判定理由（2-4行）

## PR Discussion Alignment

- Open PR がある場合のみ。BugBot 等の既出指摘と本レビューの照合（なければ `N/A`）

## Nextjs Code Review Compliance

- Status: Compliant / Non-compliant
- Non-compliant items:
  - 逸脱内容:
  - 根拠（該当箇所）:
  - 修正方針:

## Reviewed Files

- `path/to/file`

## No-Issue Statement

- Correctness critical がない場合: `No critical issues found.`
- Quality blocker がない場合: `No quality blockers found.`
- 残留リスクを1-3件記載




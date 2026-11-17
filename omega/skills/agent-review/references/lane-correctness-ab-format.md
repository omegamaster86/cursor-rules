# Correctness A×B 統合（フェーズ2.6・親コンテキスト）

親は **レーン A と B の両方が完了**（または片方 Failed）した直後、オーケストレーター **フェーズ2.6** で A×B を統合する。統合ルールは [consolidation.md](consolidation.md) の **Correctness（A × B）** に従う。

入力は親が保持しているレーン A/B の `# Deep Review Result` 全文。**ファイルは作らない**（[artifacts.md](artifacts.md)）。統合結果は最終チャットの `## Correctness Lane（A × B 統合）` に載せる。

## 親が作る統合メモ（内部）

次の観点を整理し、finding を [consolidated-output-format.md](consolidated-output-format.md) の箇条書き形式に落とし込む。

### Cross-Check Summary（親メモ）

- Both reported CRITICAL on same issue: <件数>
- A-only CRITICAL: <件数>
- B-only CRITICAL: <件数>
- Severity conflicts: <件数>

### 信頼度

- **high**: 同一論点で両レーンが `CRITICAL`、または両方が同趣旨の IMPORTANT 以上
- **medium**: 片側のみ `CRITICAL` → Must Fix 候補 + **要追加検証**
- **low**: 片側のみ LOW、または片側 Failed で残側のみ

### Integrated Findings → チャットへの載せ方

各 finding を次の形で `## Correctness Lane（A × B 統合）` に列挙する:

```markdown
- [CRITICAL|IMPORTANT|LOW] タイトル
  - Source: LaneA / LaneB / Both
  - 事象:
  - 根拠:
  - 再現条件:
  - 影響範囲:
  - 最小修正案:
  - 推奨テスト:
```

Failed レーンがあるとき: finding は成功側を主にし、Cross-Check Summary に parent fallback を記載する。

該当なし: `No integrated correctness findings.`
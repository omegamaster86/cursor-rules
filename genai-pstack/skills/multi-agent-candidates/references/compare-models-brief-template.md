# Fixed brief（compare-models 用・全 runner 共通）

オーケストレータが Frame で埋め、**変更せず** 3 runner 全員に渡す。runner は自分で立場を変えない。

## Mode

`compare-models`

## Question（1 文）

*例: `rate_slices` の各要素に `"source_key": "wed"` フィールドは必要か？*

## Adopted stance（親が確定・1 段落）

*例: Map のキーとして `wed` を使い、要素内の `source_key` フィールドは持たない。値は `blocks[]` + `rates: number[11]`。*

## Constraints（箇条書き）

- *例: FE はモック段階で変更可*
- *例: simulation と ref-data でマージ可能であること*
- *例: 局別参照（`ref-ex-kaere` 等）を壊さないこと*

## Required deliverables

- [ ] TypeScript 型スケッチ
- [ ] Swagger JSON 例（expand 初回 + ref-data）
- [ ] FE mapper の呼び出しサイト 2〜3
- [ ] **Chat summary** 節（`rationale-template.md`）
- [ ] Alternatives considered（設計上の代替 ≥1。他 runner との差別化ではない）

## Rubric（3〜6 項目・採点可能に）

1. *例: 質問への直接回答が明確か*
2. *例: 既存 FE の `allDates[key]` / merge と整合するか*
3. *例: swagger 例がコピペ可能な具体性か*
4. *例: 漏れているエッジケース（局別参照・部分成功）を挙げているか*

## Output file

- **`compare-models`:** `.cursor/multi-agent-candidates/<task-slug>/<model-slug>.md`
- **`explore-shapes`:** `.cursor/multi-agent-candidates/<task-slug>/<model-slug>.<shape-slug>.md`

（`candidate-*` フォルダや `design.md` 固定名は使わない）


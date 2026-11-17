# 統合判定（親・フェーズ 2）

## Correctness（A × B）

- Both `CRITICAL` → Must Fix（高信頼）
- 片側のみ → Must Fix 候補 + 要追加検証

A×B 統合はフェーズ2.6で親コンテキスト上に行う（[lane-correctness-ab-format.md](lane-correctness-ab-format.md)）。チャットの `## Correctness Lane（A × B 統合）` に **統合済み finding を箇条書きで載せる**（ファイル参照で代替しない）。

## Quality（C）

- `QUALITY-BLOCKER` → Quality Conditions

## Security（D）

- Critical / High → Must Fix または Block（severity 定義は security レーンに従う）
- A/B のセキュリティ指摘と重複 → Cross-cut で1件にマージ（Source 列挙）

## Blast（E）

- `unproven` かつ tier L または High severity risk → Approve with conditions + 推奨テスト
- 通常は Block 条件に単独では入れない

## Structural（親）

- 未宣言依存・解決不能 import・レイヤー違反 → Must Fix

## Merge Recommendation

- **Correctness** / **Quality** / **Overall**
- Overall `Block`: Correctness CRITICAL、Structural ビルド破綻、Security Critical
- `Approve with conditions`: QUALITY-BLOCKER、Security High、blast unproven（tier L）

統合全文を **チャットにのみ**投稿する（[artifacts.md](artifacts.md)）。

## 共通ポリシー

1. 指摘は変更差分を根拠にする。
2. レーン分担を守り、他レーンの深掘りをしない。
3. 抽象論禁止。再現条件・影響・最小修正案。
4. nextjs-code-review 準拠は主に A/B（[lane-map.md](lane-map.md)）。
5. サブエージェントの生ログ全文は再掲しない。統合セクションに finding 単位で載せる（生ログは親コンテキストのみ保持）。
6. Must Fix の正本は **チャット** の `## Must Fix Before Merge` のみ。

チャットには [consolidated-output-format.md](consolidated-output-format.md) の **`# Triple Hybrid Review Result` 全文**を必ず出す（要約のみ禁止）。





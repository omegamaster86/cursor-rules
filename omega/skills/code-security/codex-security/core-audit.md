# Core audit（リポジトリ / スコープ）

codex-security 統合ジョブの中核。authorized scope を広げない。現リビジョンのソースのみ（必要なら `git show`）。アプリコードの実行・外向きネットワークはしない。

## フェーズ

### 1. 前提

- `SECURITY.md` をルートから下へ辿る（あれば）
- ユーザー文脈・スコープを stamp に固定
- オフライン検索: `rg` または `git grep`

### 2. Baseline auditor（Task 1 体）

プロンプト要旨（Task に渡す）:

- 静的解析。SQLi、XSS、認証/認可欠落、IDOR、パストラバーサル、コマンド注入、SSRF、不安全デシリアライズ、秘密の埋め込み等
- 各 finding: CWE、severity、confidence、根拠行、反証、修正案
- 返却: JSON `{ "findings": [], "fully_reviewed_files": [], "resolved_questions": [] }`

### 3. Threat model

[../references/threat-model.md](../references/threat-model.md) に従い短い threat model を書く。investigation パケットに分割。

### 4. Focused investigators（Task 並列、allowance 内）

パケットごとに 1 Task。切り口は Forward / Backward / AuthZ / Open。baseline と重複する finding は後でマージ（別 CWE・別経路は分離）。

### 5. カバレッジ

`fully_reviewed_files` の和集合が authorized scope を覆うこと。覆えない場合は stamp と RESULTS の Coverage に未レビュー path を列挙。

### 6. 親による再検証

各 unique finding を Read/Grep で独立検証。reject は反証必須。severity は [../references/severity.md](../references/severity.md)。

### 7. 出力

- `.code-security-run/findings-merged.json`
- 親が [../references/report-format.md](../references/report-format.md) と findings.jsonl を書き、`engine: codex-security` を stamp に入れる

## Diff 限定モード

`scan-diff.md` から呼ばれたときは、変更ファイルを中心に読み、**変更が関与しない既存バグ**は `preExisting` として coverage に記録し finding には載せない（codebase スキャン向け）。

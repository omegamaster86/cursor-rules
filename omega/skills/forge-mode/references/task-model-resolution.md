# Task `model` の解決

forge 系のすべての `Task` spawn は **`.cursor/rules/forge-models.mdc` を唯一のモデル設定正本**とする。スキル・プレイブック・コマンド内のハードコード slug は使わない。

親オーケストレーター（このチャット）のモデルは **チャット欄の選択**。Task で `model` を省略した subagent はそれを継承する。

## 手順

1. spawn 前に `forge-models.mdc` を読む。
2. 対象 **ロール行**を探す（例: `bug-fix:`, `review orchestrator grok:`）。`feature, refactoring:` のように複数ロールが1行のときは、いずれかのロール名でマッチする。
3. **行が無い** → Task の `model` を**省略**（親チャットモデル）。
4. **値が `inherit`** → 同上（`model` 省略）。
5. **値が slug** → その slug を Task に渡す。カンマ区切りリスト（`multi-agent-candidates runners:` 等）は左から順に各 spawn に1 slug。spawn 数が slug 数より多いとき、余りは `model` 省略（親チャットモデル）。
6. **Task が slug を拒否した** → その spawn では `model` を省略して親チャットモデルで再試行し、拒否理由をチャットに述べる。別 slug の推測やスキル内の旧デフォルトは使わない。

## `forge-models.mdc` 先頭の許可リスト

`## Task model で使える model` の箇条書きは **`/setup-forge` が検証する slug の目安**。ロール未設定時のフォールバックではない。ロール行に書く slug は、可能ならこのリストに含める。

## ロール名の早見（代表）

| 用途 | `forge-models.mdc` のロール行 |
|------|-------------------------------|
| Feature / Refactoring 実装 delegate | `feature, refactoring` |
| Bug fix / Perf / Hillclimb delegate | `bug-fix` / `perf-issue` / `hillclimb` |
| 散文・判断 | `judgment and prose` / `hardest tasks` |
| how / why / reflect | 各スキル SKILL.md の Role 表 |
| 並列設計 runner | `multi-agent-candidates runners` / `architect runners` |
| Swarm worker | `swarm workers` |
| agent-review 各レーン | `review orchestrator *` — **`node .cursor/skills/agent-review/scripts/resolve-lane-models.mjs`**（[resolve-lane-models.md](../../agent-review/references/resolve-lane-models.md)） |
| code-security Task | `code security workers` / `code security verifier panel` |

詳細は各スキルの Role 表を参照。解決手順は常に本ファイルが正。

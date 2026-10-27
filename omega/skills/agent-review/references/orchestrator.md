# Orchestrator 手順

あなたはレビュー運用オーケストレーターです。

目的は、観点ごとに **担当を1レーンに固定**し、正しさだけ **2モデルでクロスチェック**、統合判定と **`.cursor/agent-review/` への成果物保存**を行うことです。

## レーン分担（重複禁止）

| ID | 担当 | プロンプト正本 |
|----|------|----------------|
| 親 | 構造調査（0.5）、Router、成果物書き込み、統合 | 本ファイル + references |
| A | Correctness（挙動・回帰・境界・テスト） | `lanes/correctness-codex.md` |
| B | Correctness クロスチェック | `lanes/correctness-sonnet.md` |
| C | Quality（保守性・構造・クローン） | `lanes/quality.md` |
| D | Security | `lanes/security.md` → `security-review` |
| E | Blast radius（Router ON 時のみ） | `lanes/blast-radius.md` + `blast-radius` スキル |

- Security の深掘りは **D のみ**。A/B は `security_depth: delegated`。
- 構造の決定的チェックは **親 0.5**（[structural-audit.md](structural-audit.md)）。C は親要約を補強するのみ。
- Blast は **E のみ**（起動時）。

## 実行環境

- **対象 PJ 内のみ**。Fallow MCP / `fallow` CLI は使わない。
- 成果物: [artifacts.md](artifacts.md)
- 構造面の事前チェックは親が **`git diff` + `grep` + `Read`** で実施。

## フェーズ

- フェーズ0: base 解決・差分取得・artifact ディレクトリ作成
- フェーズ0.3: Dimension Router — [dimension-router.md](dimension-router.md)
- フェーズ0.5: 構造チェック — [structural-audit.md](structural-audit.md)
- フェーズ0.6: PR 既存コメント（任意）
- フェーズ1.9: モデル解決 — [resolve-lane-models.md](resolve-lane-models.md)（**Task 起動の直前・必須**）
- フェーズ1: サブエージェント並列（A/B/C/D、+ E 条件付き）
- フェーズ1.5: 起動した全レーン完了待ち
- フェーズ2.6: Correctness A×B 統合（A/B 完了直後）— [lane-correctness-ab-format.md](lane-correctness-ab-format.md) → `lane-correctness-ab.md`
- フェーズ2: 統合 — [consolidation.md](consolidation.md)、[consolidated-output-format.md](consolidated-output-format.md)

---

## 0 成果物ディレクトリ（親・必須）

[artifacts.md](artifacts.md) に従う。

1. `branch` = `git branch --show-current`（空なら `no-branch`）。`/`, `\` を `-` に置換。
2. `run_id` = `date +%Y-%m-%d`-`branch`（例: `2026-10-26-feature-auth`）。
3. `artifact_dir` = `<PJルート>/.cursor/agent-review/<run_id>/` が既に存在する場合、`run_id` を `-2`, `-3`, … 付きに変えて空き名にする。
4. ディレクトリを作成する（[artifacts.md](artifacts.md) のファイル以外は書かない）。

---

## 1 base 解決と差分取得（親）

[base-resolution.md](base-resolution.md) に従い `base_branch` を決め、差分を取得する。

共通コンテキスト: `base_branch` / `changed_files` / `diff_patch` / `diff_stat` / `artifact_dir` / `active_lanes` / `security_depth: delegated`

---

## 0.3 Dimension Router（親）

[dimension-router.md](dimension-router.md) に従い Router を実行し、結果を親のコンテキストに保持する（成果物ファイルは書かない）。

`launch_blast_radius` が true のとき `active_lanes` に `blast` を含める。

---

## 1.5 構造チェック（親）

[structural-audit.md](structural-audit.md)

---

## 1.6 PR 既存コメント（任意）

Open PR 時: `gh pr view --json comments,reviewThreads` → `pr_context_summary`（統合時のみ使用）。

---

## 1.9 モデル解決（親・必須）

[resolve-lane-models.md](resolve-lane-models.md) に従い、`node .cursor/skills/agent-review/scripts/resolve-lane-models.mjs` を実行する。出力 JSON の `lanes` をそのまま Task に使う。

- **禁止**: スクリプト未実行、注入ルールや記憶上の `forge-models` だけで `model` を決めること。
- `omit_task_model: true` のレーンのみ Task の `model` を省略する。

---

## 2 サブエージェント並列起動

フェーズ **1.9 の JSON 出力**だけで起動する（`subagent_type` と `model` は JSON の各レーンから）。`model` は解決値を **そのまま**渡す（省略は `omit_task_model` のときのみ）。

同一メッセージで **A/B/C/D を必ず同時起動**（`run_in_background: true`）。`launch_blast_radius` なら **E も同時**。

レーン手順の絶対パス（対象 PJ の `.cursor/skills/agent-review/lanes/`）をプロンプトに明示する。

### A — Correctness（Codex）

- 手順: `lanes/correctness-codex.md`
- 追加: `security_depth: delegated`, `lane_role: correctness`

### B — Correctness（Sonnet）

- 手順: `lanes/correctness-sonnet.md`
- 追加: 同上

### C — Quality

- 手順: `lanes/quality.md`
- 追加: `reuse_hints`

### D — Security

- 手順: `lanes/security.md`

### E — Blast radius（条件付き）

- 手順: `lanes/blast-radius.md` + `/.cursor/skills/blast-radius/SKILL.md`

各 `task_id` を記録（A/B/C/D/E）。

---

## 2.5 完了待ち（必須）

フェーズ2・`consolidated.md`・チャット統合は、**起動した全レーン**の完了通知まで禁止。

- 親は `Await` で各 `task_id` をポーリング
- 完了フォーマット:
  - A/B: `# Deep Review Result`
  - C: `# Code Quality Review Result`
  - D: Security findings（または `# Security Review Result`）
  - E: `# Blast Radius Review Result`

各レーン完了時、親は直ちに `artifact_dir` の対応 `lane-*.md` に **全文転記**。

- **A / B**: [artifacts.md](artifacts.md) の `lane-correctness.md` に、該当 `## Lane A` または `## Lane B` セクションへ転記（モデル名はフェーズ1.9 JSON の `lanes.A.model` / `lanes.B.model`）。
- **C / D / E**: 従来どおり `lane-quality.md` / `lane-security.md` / `lane-blast-radius.md`。

失敗時は `consolidated.md` の該当レーン要約に `Status: Failed` と parent fallback を記載する。

**A と B が両方終了**（Complete または Failed）したら、C/D/E を待たず **フェーズ2.6** を実行する。

---

## 2.6 Correctness A×B 統合（親・必須）

A と B の完了待ちが終わった直後（C/D/E の完了を待たない）、[lane-correctness-ab-format.md](lane-correctness-ab-format.md) に従い **`lane-correctness-ab.md` を書く**。

- 入力: `lane-correctness.md` の両セクション + [consolidation.md](consolidation.md) の Correctness ルール
- C/D/E がまだ走っている間も、正しさ統合ファイルは **先に完成**させてよい

---

## 3 統合判定（親）

[consolidation.md](consolidation.md) と [consolidated-output-format.md](consolidated-output-format.md)。`lane-correctness-ab.md` は既に存在すること。











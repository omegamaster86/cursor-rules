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
- フェーズ1: サブエージェント並列（A/B/C/D、+ E 条件付き）
- フェーズ1.5: 起動した全レーン完了待ち
- フェーズ2: 統合 — [consolidation.md](consolidation.md)、[consolidated-output-format.md](consolidated-output-format.md)

---

## 0 成果物ディレクトリ（親・必須）

[artifacts.md](artifacts.md) に従う。

1. `run_id` = `date -u +%Y%m%dT%H%M%SZ`-`git rev-parse --short HEAD`
2. `artifact_dir` = `<PJルート>/.cursor/agent-review/<run_id>/`
3. ディレクトリを作成し、直ちに `inputs.md` と `manifest.json` 骨子を書く。
4. 完了後 `manifest.json` を最終更新する。

---

## 1 base 解決と差分取得（親）

`@{upstream}` は使わない。優先順:

1. `change_scope.base_branch`
2. Open PR の `baseRefName`
3. `origin/develop`、なければ `origin/main`

取得:

- `git diff --name-only <base>...HEAD`
- `git diff <base>...HEAD`
- `git diff --stat <base>...HEAD`
- `git status --short`（未コミットは対象外の確認のみ）

**レビュー対象はコミット済み差分のみ。**

共通コンテキスト: `base_branch` / `changed_files` / `diff_patch` / `diff_stat` / `artifact_dir` / `active_lanes` / `security_depth: delegated`

---

## 0.3 Dimension Router（親）

[dimension-router.md](dimension-router.md) に従い `dimension-router.md` を `artifact_dir` に保存。

`launch_blast_radius` が true のとき `active_lanes` に `blast` を含める。

---

## 1.5 構造チェック（親）

[structural-audit.md](structural-audit.md)

---

## 1.6 PR 既存コメント（任意）

Open PR 時: `gh pr view --json comments,reviewThreads` → `pr_context_summary`（統合時のみ使用）。

---

## 2 サブエージェント並列起動

[models.md](models.md) のモデル割当。

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

失敗時のみ `Status: Failed` と parent fallback を manifest に記載。

---

## 3 統合判定（親）

[consolidation.md](consolidation.md) と [consolidated-output-format.md](consolidated-output-format.md)。

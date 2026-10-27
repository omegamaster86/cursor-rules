# Agent review artifacts

`agent-review` スキル（`/agent-review` 明示起動）実行時、**対象 PJ のリポジトリルート**に次を作る。

## ルート

```text
.cursor/agent-review/<run_id>/
```

- `<run_id>`: `yyyy-mm-dd-<branch>`（ローカル日付 + 現在ブランチ名。例: `2026-10-26-feature-auth`）
- ブランチ名の `/` は `-` に置換（`feature/foo` → `feature-foo`）。取得できないときは `no-branch`。
- 同名ディレクトリが既にあるときは末尾に `-2`, `-3`, … を付けて上書きしない。

## ファイル一覧

| ファイル | 作成者 | 内容 |
|----------|--------|------|
| `lane-correctness.md` | 親（A/B 完了ごとに追記） | `# Correctness Lane Raw` + `## Lane A` / `## Lane B` に各 `# Deep Review Result` 全文 |
| `lane-correctness-ab.md` | 親（A と B 完了後・フェーズ2直前） | **Correctness（A × B 統合）** — [lane-correctness-ab-format.md](lane-correctness-ab-format.md) |
| `lane-quality.md` | 親 | `# Code Quality Review Result` 全文 |
| `lane-security.md` | 親 | Security サブエージェントの findings 全文 |
| `lane-blast-radius.md` | 親（起動時のみ） | Blast レーン全文 |
| `consolidated.md` | 親（フェーズ2） | `# Triple Hybrid Review Result` 統合レポート |

サブエージェントは **readonly** のためファイルは書かない。親が各レーン完了後に **そのまま転記**する。

正しさレーンの **読み物の正本**は `lane-correctness-ab.md`。生ログは `lane-correctness.md`。

Router 判定・構造調査・入力メタデータは **単独の成果物ファイルに書かない**。親のコンテキストと `consolidated.md` の該当セクションに載せる。

## lane-correctness.md の構造

初回（レーン A または B の先着）でファイルを作り、見出しを固定する:

```markdown
# Correctness Lane Raw

## Lane A (<resolved model>)

（A 完了時に `# Deep Review Result` 全文をここに転記。未完了なら `(pending)`）

## Lane B (<resolved model>)

（B 完了時に全文。未完了なら `(pending)`）
```

`lane-correctness-codex.md` / `lane-correctness-sonnet.md` は **廃止**（後方互換のため親は作らない）。

## Git

- `.cursor/agent-review/` は **ローカル成果物**。対象 PJ の `.gitignore` に追記を推奨:

```gitignore
.cursor/agent-review/
```

- cursor-rules リポジトリ自体にサンプル run をコミットしない。

## チャット出力

統合後、チャットには `consolidated.md` の **要約**（Merge Recommendation + Must Fix + 各レーン1行）を出し、`artifact_dir` パスを示す。正しさの詳細は `lane-correctness-ab.md` を案内する。

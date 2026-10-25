# Agent review artifacts

`agent-review` スキル（`/agent-review` 明示起動）実行時、**対象 PJ のリポジトリルート**に次を作る。

## ルート

```text
.cursor/agent-review/<run_id>/
```

- `<run_id>`: `YYYYMMDDTHHMMSSZ-<short_head>`（UTC。例: `20261024T142530Z-a1b2c3d`）
- 同一 run で上書きしない。新規 run は新しい `<run_id>` ディレクトリ。

## ファイル一覧

| ファイル | 作成者 | 内容 |
|----------|--------|------|
| `manifest.json` | 親 | run メタデータ・レーン一覧・パス |
| `inputs.md` | 親（フェーズ0直後） | base、branch、diff stat、changed_files 要約 |
| `dimension-router.md` | 親 | Router スコア・launch 判定 |
| `structural-audit.md` | 親 | フェーズ0.5 の全文 |
| `lane-correctness-codex.md` | 親（サブエージェント出力を転記） | `# Deep Review Result` 全文 |
| `lane-correctness-sonnet.md` | 親 | 同上（Sonnet） |
| `lane-quality.md` | 親 | `# Code Quality Review Result` 全文 |
| `lane-security.md` | 親 | Security サブエージェントの findings 全文 |
| `lane-blast-radius.md` | 親（起動時のみ） | Blast レーン全文 |
| `consolidated.md` | 親（フェーズ2） | `# Triple Hybrid Review Result` 統合レポート |

サブエージェントは **readonly** のためファイルは書かない。親が各レーン完了後に **そのまま転記**する。

## manifest.json（最小スキーマ）

```json
{
  "runId": "20261024T142530Z-a1b2c3d",
  "repoRoot": "/absolute/path",
  "baseBranch": "origin/main",
  "headBranch": "cursor/feature-d2e3",
  "headSha": "full-sha",
  "createdAtUtc": "2026-10-24T14:25:30Z",
  "diff": { "filesChanged": 12, "insertions": 340, "deletions": 22 },
  "lanes": {
    "correctnessCodex": { "status": "completed", "artifact": "lane-correctness-codex.md" },
    "correctnessSonnet": { "status": "completed", "artifact": "lane-correctness-sonnet.md" },
    "quality": { "status": "completed", "artifact": "lane-quality.md" },
    "security": { "status": "completed", "artifact": "lane-security.md" },
    "blastRadius": { "status": "skipped", "artifact": null }
  }
}
```

## Git

- `.cursor/agent-review/` は **ローカル成果物**。対象 PJ の `.gitignore` に追記を推奨:

```gitignore
.cursor/agent-review/
```

- cursor-rules リポジトリ自体にサンプル run をコミットしない。

## チャット出力

統合後、チャットには `consolidated.md` の **要約**（Merge Recommendation + Must Fix + 各レーン1行）を出し、全文パスを `manifest.json` とともに示す。

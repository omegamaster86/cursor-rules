# Job: scan repository（investigator 方式）

Task の `model`: [../references/task-models.md](../references/task-models.md)（`code security workers`。[core-audit](core-audit.md)）。

リポジトリ全体、または `--scope` で指定したディレクトリ。コミット済みツリーを読む（未コミットのみは [scan-changes](scan-changes.md) か、先にコミット）。

## 引数

- `[path]` — スキャンルート（省略時は cwd）
- `--scope dirs` — カンマ区切り
- `--effort low|medium|high` — 既定 `medium`

## Effort

| tier | 調査の形 |
|------|----------|
| low | baseline 1 本 + threat model 省略可 + 狭い scope なら単一 investigator |
| medium | baseline + threat model + コンポーネント単位の investigator（~25 ファイル/コンポーネント目安、上限 24 コンポーネント） |
| high | medium の 2 倍の並列度、コンポーネント上限 48 |

大規模リポジトリ（トラックファイル数百超）で scope 未指定のときは、ユーザーに **scope 推奨**を 1 問。

## 手順

1. スキャンルートを絶対パスにする
2. `date -u +%Y%m%d-%H%M%S` で `.cursor/CODE-SECURITY-<ts>/` と `.code-security-run/` を作成（[../references/artifacts.md](../references/artifacts.md)）
3. `GIT_CONFIG_GLOBAL=/dev/null GIT_TERMINAL_PROMPT=0 git -C <root> rev-parse HEAD` で commit を stamp に記録。`git status --porcelain` が空でなければ `dirty: true` とし、パッチジョブには使えない旨を RESULTS に書く
4. 大きいツリーでは `attack-surface` フォーカス: テスト・生成物・fixture は二次参照のみ（秘密の埋め込みチェックは fixture も見る）
5. [core-audit.md](core-audit.md) を実行。stamp の `job`: `scan-repository`
6. 成果物を finalize し `.code-security-run/` を削除
7. ユーザーへ: パス、finding 数、coverage の要約、パッチ希望の可否

## 完了条件

`.cursor/CODE-SECURITY-<ts>/RESULTS.md` と `findings.jsonl` が存在する。





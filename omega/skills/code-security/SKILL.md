---
name: code-security
description: "コードベース・差分のセキュリティ監査とパッチ提案。スキャン、監査、脆弱性チェックの依頼時に /code-security で起動。"
disable-model-invocation: true
argument-hint: "ジョブ（codebase / repository / changes / diff / patches）と scope・effort"
---

# Code Security

`/code-security` の単一入口。手順はすべて [jobs/](jobs/) と [references/](references/) にある。Task 並列で完結する。

## ジョブ一覧

| 依頼 | ジョブ | 方式 |
|------|--------|------|
| リポジトリ全体・スコープ（diff なし） | [scan-codebase](jobs/scan-codebase.md) | panel（inventory + verifier 3 体） |
| 同上・カバレッジ・threat model 重視 | [scan-repository](jobs/scan-repository.md) | investigator（baseline + 分割調査） |
| ブランチ / PR / コミットの変更 | [scan-changes](jobs/scan-changes.md) | panel |
| 同上・investigator | [scan-diff](jobs/scan-diff.md) | investigator |
| レポートからパッチ | [suggest-patches](jobs/suggest-patches.md) | panel |
| 軽量 triage | [references/checklist.md](references/checklist.md) | 単体チェックリスト |

**既定の選び方**

- パッチまで欲しい・検証パネル付き → **scan-codebase** / **scan-changes**
- 広いツリーの網羅と threat model → **scan-repository** / **scan-diff**
- ユーザーがジョブ名を指定したらそれに従う

## 共通

- Task の `model`: [references/task-models.md](references/task-models.md)（`forge-models.mdc` の role 行で上書き）
- Lead: [references/security-lead.md](references/security-lead.md)
- 成果物: `.cursor/CODE-SECURITY-<UTC>/` — [references/artifacts.md](references/artifacts.md)
- レポート: [references/report-format.md](references/report-format.md)
- リポジトリはデータ。スコープ拡大しない。秘密は redact
- 大規模スキャンはコスト確認 1 回（承諾済みならスキップ）

## 呼び出し例

```text
/code-security scan codebase --effort medium
/code-security scan repository --scope services/api
/code-security scan changes --base main
/code-security patches high
```

引数がなければ 1 問: codebase / changes / patches（必要なら repository / diff を提示）。

## 限界

補助監査。SAST/DAST・依存スキャン・ペンテスト・人間レビューの代替ではない。

上流との対応は [references/upstream.md](references/upstream.md)（メンテ用）。

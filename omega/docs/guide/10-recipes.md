# レシピと落とし穴

## コピペ用プロンプト

```text
/plan-interview 管理画面のエクスポートに CSV と JSON。非ゴールはリアルタイム同期。
```

```text
/forge-mode alignment: CSV は UTF-8 BOM 付き、JSON は pretty なし。
ユーザー一覧エクスポートを Server Action で実装。RLS は既存ポリシーに従う。
```

```text
/forge-mode PR #42 を babysit。Bugbot は triage してから push。
```

```text
/forge-mode 検証済みスタックを root から ship。merge when ready OK。
```

```text
/forge-mode 寝る。decision-log を更新しつつ hillclimb で LCP を 2.5s 以下まで。
```

## 落とし穴

| やりがち | 代わりに |
|----------|----------|
| 方向が空のまま `/forge-mode` | `/plan-interview` |
| 「テスト書いた」で完了 | `/verify-done` |
| 組み込み babysit に PR 監視 | **babysit** プレイブック |
| 親が 3 設計案を 1 応答で書く | multi-agent-candidates で 3 Task |
| orchestrate で自分がコードを書く | brief と drain のみ |

## Worktree 掃除

ディスク逼迫: **worktree-cleanup** プレイブック。`.cursor/skills/forge-mode/scripts/worktree-audit.sh` で分類してから削除。

[ガイド目次](./README.md)

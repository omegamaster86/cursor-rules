---
name: session-log
description: "長セッションの作業状態をファイルに書き出し、新規チャットへ handoff する。Conversation 肥大化・context 60%超・/summarize 前・「session-log 書いて新チャット」「セッション切り替え」「handoff」に使用。recall（過去チャット横断）・decision-log（決定監査）とは別。"
disable-model-invocation: true
---

# Session log

**今の Agent セッションの作業状態を disk 上の session-log に書き、ユーザーが新規チャットで再開できるようにする。** Conversation を捨て、session-log だけ持っていく（**guard-the-context-window** 原則の実践）。

**使う:** 「session-log 書いて新チャット」「context が 70%」「handoff」「/summarize 前に状態を残して」「一旦このチャットを閉じたい」。

**使わない:** 過去トランスクリプト横断のキャッチアップ → **recall**。決定理由の監査ログ → **decision-log**。特定過去チャット 1 本の引き継ぎ → **session-pickup** playbook。単ファイル調査 → **file-brief** command。

1. **safe boundary で止める**（**pause-safely** playbook の 1〜2 と同趣旨）。現在の atomic step を finish または back out。known-broken state で mid-edit stop しない。新しい作業は開始しない。nested subagent は cancel。irreversible line（force-push、deploy、データ削除）は越えない。
2. **ローカル状態を検証。** `git branch --show-current`、`git status -sb` を実行。ブランチ名・未コミットファイル・verify 済みかを session-log に載せる。uncommitted edit があり失うと困るなら、ユーザーの明示がなくても **1 つの `wip:` commit** を提案する（**pause-safely** の 3）。`gh`、課題トラッカー、MCP による PR/issue 調査はしない。
3. **session-log ファイルを Write。** 本文は **5,000 文字以内**。diff 全文・Shell ログ・長いコードブロックは載せない。行番号 + パス + 結論だけ。下記テンプレートに沿う。
4. **このチャットでは続けない。** session-log Write 後、同スレッドで実装・調査を再開しない。ユーザーに新規チャット手順を返す。
5. **任意:** ユーザーが `/summarize` を使うなら **session-log を先に Write** してから。要約後も session-log を `@` または Read で渡す。

## 出力先

| 条件 | パス |
|------|------|
| デフォルト | `.cursor/session-log/YYYY-MM-DD-session.md` |
| 名前付きタスク | `.cursor/session-log/YYYY-MM-DD-<task-slug>.md`（ユーザーまたはブランチ名から slug） |

`.cursor/session-log/` はセッション再開用。**commit しない**（`.gitignore` 推奨をユーザーに一言）。decision-log の `.log/*.md` とは別物（session-log = 再開用、decision-log = 監査用）。

## ファイルテンプレート

```markdown
# Session log — <task-slug>

更新: YYYY-MM-DD
ブランチ: <branch>
前チャット: （任意）agent-transcripts の UUID

## カプセル
- （最大 5 箇条。何の作業で全体としてどこにいるか）

## 確定 / 未確定
- 確定: …
- 未確定: …

## 変更ファイル
| ファイル | 状態 |
| path/to/file.ts | 修正済み未コミット / 調査のみ / … |

## 試してダメだったこと
- （最大 5。次が同じ失敗を繰り返さないため）

## 次の一手
1. （最も有用な次の行動を 1 つ、具体に）

## 参照（中身は載せない。新チャットで Read）
- path/to/file.ts:42-58
```

## ユーザーへの返答契約

session-log パスと、**手動**の新規チャット手順を必ず返す。例:

```markdown
`.cursor/session-log/2026-07-10-session.md` に書きました。このチャットでは続けません。

1. このチャットを閉じる
2. 新規チャット（Cmd+N）
3. 以下を貼る:

@.cursor/session-log/2026-07-10-session.md
session-log の「次の一手」から続けて。<ユーザー制約があればここ>
```

`/summarize` を使う場合は「session-log 確認後、必要なら `/summarize` → 新規チャット」と追記してよい。

**返答:** 上記契約 + session-log のカプセル 3 行以内の要約（全文の duplicate は不要）。

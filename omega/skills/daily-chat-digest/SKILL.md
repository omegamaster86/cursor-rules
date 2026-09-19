---
name: daily-chat-digest
description: >-
  アクティブ workspace の指定日（デフォルト今日・日本時間）のチャットを収集し、
  .cursor/chat-digest/<YYYY-MM-DD>/daily-chat.md に構造化出力する。
  「今日のチャットを出力」「daily-chat-digest」「9/19 の digest」「チャット digest」
  など明示依頼時に使用。recall（作業再開）・study-log（学習記事）とは別。
disable-model-invocation: true
---

# Daily Chat Digest

**指定日にアクティブ workspace で送ったチャット内容を、1 日 1 ファイルに構造化して書き出す。** ユーザー発言は原文、エージェント応答はチャットごとに 1〜3 行要約。

## いつ使う

- 「今日のチャットを出力」「daily-chat-digest」「9/19 の digest」などと **digest だけ** 明示されたとき
- **engineer-retrospective** から同一ターン内で委譲されたとき（単独完了報告で止めず、呼び出し元に返す）
- 作業再開用の短いブリーフ → **recall**
- 特定トピックの学習記事 → **study-log**
- セッション handoff → **session-log**

## スコープ

| 項目 | 内容 |
|------|------|
| workspace | **アクティブ workspace のみ**（他プロジェクトは読まない） |
| 日付 | 引数なし = **今日（日本時間 `Asia/Tokyo`）**。`2026-09-19` / `9/19` 等も可 |
| 除外 | subagent / eval / test 等のノイズ（**recall** と同様） |
| 現在のチャット | digest 生成中のチャット自身は除外 |

## トランスクリプトの場所

`~/.cursor/projects/<slug>/agent-transcripts/<uuid>/<uuid>.jsonl`

- `<slug>`: workspace パスから先頭 `/` を除き `/` を `-` に（`/workspace` → `workspace`）
- 各行 = 1 メッセージ。JSONL を Read してパースする
- 日付判定はメッセージのタイムスタンプを **Asia/Tokyo** に変換して行う

## 手順

1. **日付を確定する**
   - ユーザー指定がなければ `Asia/Tokyo` の今日を `YYYY-MM-DD` に
   - 出力先: `.cursor/chat-digest/<YYYY-MM-DD>/daily-chat.md`
   - フォルダがなければ作成する

2. **候補チャットを列挙する**
   - アクティブ workspace の `agent-transcripts/` を `ls -t` 等で走査
   - 各 UUID フォルダの jsonl の mtime / 内容タイムスタンプで対象日に絞る
   - ノイズ除外: タイトル・内容に subagent / eval / test が明らかなもの、親会話の重複サブエージェント

3. **各チャットを抽出する**
   - **ユーザー発言**: 原文（長いコードブロックは `...` で省略可。意味は残す）
   - **エージェント**: チャット全体を 1〜3 行で要約（何をしたか / 結論）
   - トピックタグを 1〜3 個付ける（例: `skills`, `architecture`, `debug`）
   - 機密・トークン・個人情報は `[REDACTED]` に置換

4. **`daily-chat.md` を Write（上書き）**
   - 同日フォルダが既にあれば **上書き**（確認不要）
   - 下記テンプレートに沿う
   - 全体は読みやすさ優先。極端に長い場合はチャット単位で要約を強める

5. **完了報告**
   - **単独起動時:** 書き込んだパスと対象日・チャット数・ユーザーメッセージ数を返す
   - **engineer-retrospective から委譲時:** 完了報告は省略し、呼び出し元の批評手順へ **そのまま続行**（このスキル単体として終了しない）

## ファイルテンプレート

```markdown
# Daily Chat Digest — YYYY-MM-DD

TZ: Asia/Tokyo
Workspace: /absolute/path/to/workspace
Generated: YYYY-MM-DDTHH:mm:ss+09:00
Chats: N
User messages: M

## サマリー

- （その日の全体を 3〜5 箇条。トピックと成果の概要）

## チャット一覧

| # | トピック | UUID | ユーザーメッセージ数 |
|---|----------|------|----------------------|
| 1 | … | `<uuid>` | n |

---

## 1. <トピック>

- **UUID:** `<uuid>`
- **Tags:** tag1, tag2

### ユーザー

> （原文。複数メッセージは時系列で `####` 見出しまたは引用ブロック）

### エージェント（要約）

- （1〜3 行）

---

## 2. …
```

## やらないこと

- 他 workspace のトランスクリプト横断
- `engineer-retrospective.md` の作成（→ **engineer-retrospective**）
- `.cursor/study-log/` / `.cursor/session-log/` への書き込み
- git commit（`.cursor/chat-digest/` はローカル専用。`.gitignore` 推奨）

## 返答契約（単独起動時のみ）

```markdown
`.cursor/chat-digest/YYYY-MM-DD/daily-chat.md` に書きました。

- 対象日: YYYY-MM-DD (JST)
- チャット: N 件 / ユーザーメッセージ: M 件

批評まで一括 → **engineer-retrospective**（「今日の振り返り」で digest も自動生成）
```

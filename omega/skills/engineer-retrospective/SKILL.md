---
name: engineer-retrospective
description: >-
  daily-chat-digest が出力した daily-chat.md を読み、エンジニアとしての聞き方・
  アーキテクト視点・指示の質を批評し、
  .cursor/chat-digest/<YYYY-MM-DD>/engineer-retrospective.md に書く。
  「今日の振り返り」「エンジニアとして批評」「engineer-retrospective」
  「指示の質を見て」など明示依頼時に使用。digest が無ければ daily-chat-digest を先に実行。
disable-model-invocation: true
---

# Engineer Retrospective

**`daily-chat.md` を材料に、その日のエージェントへの聞き方・指示を批評し、翌日試す改善を 1 つ残す。** 出力は同じ日付フォルダの `engineer-retrospective.md`。

## いつ使う

- 「今日の振り返り」「エンジニアとして批評して」「engineer-retrospective」などと明示されたとき
- digest だけ欲しい → **daily-chat-digest**
- 特定概念の学習記事 → **study-log**
- 作業コンテキストの再構築 → **recall**

## 前提

| 項目 | 内容 |
|------|------|
| 入力 | `.cursor/chat-digest/<YYYY-MM-DD>/daily-chat.md` |
| 日付 | 引数なし = **今日（日本時間 `Asia/Tokyo`）** |
| 依存 | `daily-chat.md` が **無ければ先に daily-chat-digest スキルを実行** してから本スキルを続行 |
| 出力 | `.cursor/chat-digest/<YYYY-MM-DD>/engineer-retrospective.md`（**上書き**） |

## 手順

1. **日付と入力ファイルを確定**
   - パス: `.cursor/chat-digest/<YYYY-MM-DD>/daily-chat.md`
   - 存在しなければ **daily-chat-digest** を実行し、生成を待つ

2. **`daily-chat.md` を Read**
   - ユーザー発言原文とチャット文脈（エージェント要約）を把握
   - 批評は **ユーザー発言** を主対象とする。エージェントの失敗は「指示の曖昧さが招いたか」の文脈でのみ触れる

3. **3 軸 + 翌日アクションで批評を書く**
   - 下記「批評軸」とテンプレートに沿う
   - 各軸で **良かった点** と **改善点** を具体例付きで書く（抽象論だけにしない）
   - `daily-chat.md` の UUID または引用で根拠を示す

4. **`engineer-retrospective.md` を Write（上書き）**

5. **完了報告**
   - パスと「明日試す 1 つ」を 1 行で返す

## 批評軸

### 1. 聞き方（エンジニアとして）

- 目的・制約・完了条件が伝わるか
- 調査可能な事実を自分で調べず丸投げしていないか / 逆に過剰コンテキストでノイズになっていないか
- 段階的に絞れているか（一度に要求しすぎていないか）
- エラー・再現手順・期待動作が具体的か

### 2. アーキテクト視点

- 設計判断を先に固定すべき場面で、いきなり実装指示になっていないか
- 境界（モジュール / 型 / 責務）について言及があるか
- トレードオフ（速度 vs 保守性、スコープ vs 品質）を意識した指示か
- **architect** / **plan-interview** に回すべき内容を実装チャットに混ぜていないか

### 3. 指示の質

- 曖昧語（「いい感じに」「適当に」）の有無と代替表現案
- 成功条件が検証可能か（**verify-done** で証明できる粒度か）
- スコープが暴走しやすい指示か / 逆に過度に狭すぎて試行錯誤を誘発していないか
- その日の指示の中で **最も効果が高かった 1 件** と **最も改善余地が大きい 1 件** を選ぶ

### 4. 明日から試す 1 つ（必須）

- 1 文で具体的な行動（例: 「実装依頼の前に `alignment:` 1 文を書く」）
- 測りやすいものを優先

## ファイルテンプレート

```markdown
# Engineer Retrospective — YYYY-MM-DD

TZ: Asia/Tokyo
Source: .cursor/chat-digest/YYYY-MM-DD/daily-chat.md
Generated: YYYY-MM-DDTHH:mm:ss+09:00

## 今日の総評

（2〜4 行。その日のコミュニケーション全体の印象）

## 1. 聞き方（エンジニアとして）

### 良かった点

- …

### 改善点

- …（UUID または引用 + より良い聞き方の例）

## 2. アーキテクト視点

### 良かった点

- …

### 改善点

- …

## 3. 指示の質

### 効果が高かった指示

- …

### 改善余地が大きい指示

- …（なぜ曖昧か / どう書き換えるか）

## 4. 明日から試す 1 つ

> （1 文。具体的な行動）

## 参照

- daily-chat.md のチャット UUID 一覧
```

## 文体

- 日本語
- 批評は厳しめだが人格批判はしない。行動・文章・指示に限定
- 「〜だと思います」より、根拠付きの断定
- 長文の説教禁止。各セクションは読み返しやすい長さ

## やらないこと

- `daily-chat.md` の再生成（必要なら **daily-chat-digest** に委譲）
- コード変更・PR 作成
- スコアリング（1〜5 点）— 定性批評のみ
- `.cursor/study-log/` への自動転記（ユーザーが別途依頼した場合のみ study-log）

## 返答契約

```markdown
`.cursor/chat-digest/YYYY-MM-DD/engineer-retrospective.md` に書きました。

**明日試す 1 つ:** （1 文）

詳細: @.cursor/chat-digest/YYYY-MM-DD/engineer-retrospective.md
```

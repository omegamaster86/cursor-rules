# AGENTS.md

このリポジトリで作業する AI コーディングエージェント向けのガイドです。

> **Note:** `CLAUDE.md` はこのファイルへのシンボリックリンクです。

## リポジトリ構成

```
skills/
  {skill-name}/
    SKILL.md              # 必須: スキルのマニフェスト（Agent Skills 仕様）
    AGENTS.md             # 生成物: エージェント向けナビゲーションガイド
    CLAUDE.md             # 生成物: AGENTS.md へのシンボリックリンク
    references/
      _sections.md        # 必須: セクション定義
      {prefix}-{name}.md  # 参考資料ファイル

packages/
  skills-build/           # 全スキル共通のビルドシステム
```

## コマンド

```bash
npm run build                    # すべてのスキルをビルド
npm run build -- {skill-name}    # 特定のスキルをビルド
npm run validate                 # すべてのスキルを検証
npm run validate -- {skill-name} # 特定のスキルを検証
npm run check                    # フォーマットとリント（自動修正）
```

**作業完了前に必ず** `npm run check` と `npm run build` を実行して、CI が通ることを確認してください。

## 新しいスキルの作成

スキルは [Agent Skills Open Standard](https://agentskills.io/) に従います。

1. ディレクトリ作成: `mkdir -p skills/{skill-name}/references`
2. 以下のフォーマットに従って `SKILL.md` を作成
3. セクション定義の `references/_sections.md` を追加
4. 参考資料ファイル: `{prefix}-{reference-name}.md` を追加
5. `npm run build` を実行

---

## SKILL.md の書き方

SKILL.md は各スキルの中核です。**YAML フロントマター**と**Markdown の指示**で構成されます。

### フロントマター（必須）

```yaml
---
name: skill-name
description: 何を行うスキルか、いつ使うか
---
```

| フィールド    | 必須 | 制約                                                                 |
| ------------- | ---- | -------------------------------------------------------------------- |
| `name`        | Yes  | 1-64 文字。小文字英数字とハイフンのみ。ディレクトリ名と一致させる。   |
| `description` | Yes  | 1-1024 文字。何をするかと、いつ使うかの両方を記載する。               |
| `license`     | No   | ライセンス名、または同梱ライセンスファイルの参照。                   |
| `metadata`    | No   | 任意のキー/値（例: `author`, `version`）。                           |

### name フィールドのルール

- 小文字英字、数字、ハイフンのみ（`a-z`, `0-9`, `-`）
- 先頭または末尾に `-` を含めない
- 連続するハイフン（`--`）を含めない
- 親ディレクトリ名と一致させる

```yaml
# 有効
name: pdf-processing
name: data-analysis

# 無効
name: PDF-Processing # 大文字は不可
name: -pdf # 先頭ハイフンは不可
name: pdf--processing # 連続ハイフンは不可
```

### description フィールド（重要）

description は**主要なトリガー機構**です。Claude はこれを使ってスキルを起動するか判断します。

**次の 2 つを含めてください:**

1. スキルが何をするか
2. いつ使うべきか（具体的なトリガー/文脈）

```yaml
# 良い例 - 網羅的でトリガーが豊富
description: >
  Supabase データベースのスキーマ設計、RLS ポリシー、
  インデックス、クエリ最適化のベストプラクティス。Supabase
  プロジェクトで作業するとき、PostgreSQL のマイグレーション
  を書くとき、行レベルセキュリティを設定するとき、
  もしくはデータベース性能を最適化するときに使用する。

# 悪い例 - 曖昧
description: データベースを手伝います。
```

**「いつ使うか」を本文に書かないでください。** 本文はトリガー後に読み込まれるため、トリガーとなる文脈は description に含める必要があります。

### 本文内容

Markdown 本文にはスキルの使い方を記載します。Claude は既に十分に賢いので、**簡潔に**書いてください。Claude が持っていない文脈だけを書きます。

**ガイドライン:**

- 命令形で書く（「テーブルを作成する」）
- 500 行以内に収め、詳細は `references/` に移す
- 長い説明より、短い例を優先する
- 各段落に対し「トークンコストに見合うか？」を問い直す

**推奨構成:**

1. クイックスタートまたは基本ワークフロー
2. 主要パターン（例付き）
3. 高度なトピックは reference へ誘導

```markdown
## Quick Start

RLS を有効にしたテーブルを作成:

[簡潔なコード例]

## Common Patterns

### Authentication

[例付きのパターン]

## Advanced Topics

- **複雑なポリシー**: [references/rls-patterns.md](references/rls-patterns.md)
- **パフォーマンス調整**: [references/optimization.md](references/optimization.md)
```

### 段階的な開示（Progressive Disclosure）

スキルは 3 つの読み込みレベルを使います:

1. **メタデータ**（~100 トークン） - すべてのスキルで常に読み込み
2. **本文**（推奨 <5k トークン） - トリガー時に読み込み
3. **参考資料**（必要時） - Claude がオンデマンドで読み込み

SKILL.md は軽量に保ち、詳細は別ファイルに移してリンクしてください。

---

## Reference ファイルの形式

`references/` 配下の reference ファイルは詳細ドキュメントを提供します。

```markdown
---
title: 行動ベースのタイトル
impact: CRITICAL|HIGH|MEDIUM-HIGH|MEDIUM|LOW-MEDIUM|LOW
impactDescription: 数値化された効果
tags: keywords
---

## Title

1-2 文の説明。

**Incorrect:** ```sql -- bad example ```

**Correct:** ```sql -- good example ```
```

## 含めてはいけないもの

スキルには必須ファイルのみを含めます。以下は**作成しない**でください:

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md

スキルは AI エージェントが作業するために必要なものだけを含めるべきです。

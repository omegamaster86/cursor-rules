# CONTRIBUTING.md

Supabase Agent Skills への貢献ありがとうございます！開始方法は以下の通りです。

[1. はじめに](#getting-started) | [2. Issue](#issues) |
[3. プルリクエスト](#pull-requests) | [4. 新しい Reference の追加](#contributing-new-references) |
[5. 新しいスキルの作成](#creating-a-new-skill)

## はじめに

前向きで包括的な環境を保つため、貢献前に
[行動規範](https://github.com/supabase/.github/blob/main/CODE_OF_CONDUCT.md)
をお読みください。

## Issue

誤字を見つけた、新しいスキル/Reference の提案がある、既存のスキル/Reference を改善したい場合は Issue を作成してください。

- 新規作成前に
  [既存の Issue](https://github.com/supabase/agent-skills/issues) を検索してください。
- 問題点や提案の内容を明確に記載してください。
- Issue に適切なタグを付けてください（例: `bug`, `question`, `enhancement`,
  `new-reference`, `new-skill`, `documentation`）。

## プルリクエスト

PR は大歓迎です！次の点に注意してください。

- Issue を修正する場合、すでに誰かが PR を作成していないか確認してください。
  関連する Issue に PR を紐づけてください。
- Issue を解決できる最初の有効な PR を採用するよう努めます。
- 初めての方は、
  [good first issue](https://github.com/supabase/agent-skills/labels/good%20first%20issue) が付いた Issue をご覧ください。
- 重要な新規スキルや大きな変更を提案する場合は、実装に時間をかける前に
  [Discussion](https://github.com/orgs/supabase/discussions/new/choose) を立てて
  フィードバックを集めてください。

### 事前チェック

PR を提出する前に、以下を実行してください。

```bash
npm run validate  # Reference の形式と構成をチェック
npm run build     # references から AGENTS.md を生成
```

両コマンドが正常終了する必要があります。

## 新しい Reference の追加

既存スキルに Reference を追加するには:

1. `skills/{skill-name}/references/` に移動
2. `_template.md` を `{prefix}-{your-reference-name}.md` にコピー
3. フロントマター（title, impact, tags）を記入
4. 説明と例（Incorrect/Correct）を書く
5. 検証とビルドを実行:

```bash
npm run validate
npm run build
```

## 新しいスキルの作成

スキルは [Agent Skills Open Standard](https://agentskills.io/) に従います。

### 1. ディレクトリ構成を作成

```bash
mkdir -p skills/my-skill/references
```

### 2. SKILL.md を作成

```yaml
---
name: my-skill
description: このスキルの概要と利用タイミングを簡潔に記述。
license: MIT
metadata:
  author: your-org
  version: "1.0.0"
  organization: Your Org
  date: January 2026
  abstract: コンパイル後の AGENTS.md 用に、このスキルの詳細説明。
---

# My Skill

このスキルを利用するエージェント向けの指示。

## References

- https://example.com/docs
```

### 3. references/_sections.md を作成

```markdown
## 1. First Category (first)
**Impact:** HIGH
**Description:** このカテゴリが扱う内容。

## 2. Second Category (second)
**Impact:** MEDIUM
**Description:** このカテゴリが扱う内容。
```

### 4. Reference ファイルを作成

`{prefix}-{reference-name}.md` という形式で作成し、prefix はセクション名に合わせます。

例: "First Category" セクションなら `first-example-reference.md`

### 5. ビルド

```bash
npm run build
```

ビルドシステムは `SKILL.md` を探してスキルを自動検出します。

## 質問・フィードバック

- バグや提案は Issue を作成
- 広いテーマや提案は Discussion を開始
- 新規作成前に既存の Issue / Discussion を確認

## ライセンス

このリポジトリへ貢献することで、あなたの貢献物は MIT License の下で
ライセンスされることに同意したものとみなされます。

# Supabase Postgres Best Practices - Contributor Guide

このスキルには、AI エージェント/LLM 向けに最適化された Postgres パフォーマンス最適化の reference が含まれます。 [Agent Skills Open Standard](https://agentskills.io/) に従っています。

## クイックスタート

```bash
# リポジトリのルートから
npm install

# 既存の reference を検証
npm run validate

# AGENTS.md をビルド
npm run build
```

## 新しい Reference の作成

1. **カテゴリに基づいてセクションの prefix を選ぶ**:
   - `query-` クエリパフォーマンス（CRITICAL）
   - `conn-` 接続管理（CRITICAL）
   - `security-` セキュリティ & RLS（CRITICAL）
   - `schema-` スキーマ設計（HIGH）
   - `lock-` 同時実行性 & ロック（MEDIUM-HIGH）
   - `data-` データアクセスパターン（MEDIUM）
   - `monitor-` 監視 & 診断（LOW-MEDIUM）
   - `advanced-` 高度な機能（LOW）

2. **テンプレートをコピー**:
   ```bash
   cp references/_template.md references/query-your-reference-name.md
   ```

3. **テンプレート構成に沿って内容を記入**

4. **検証とビルド**:
   ```bash
   npm run validate
   npm run build
   ```

5. **生成された `AGENTS.md` を確認**

## スキル構成

```
skills/supabase-postgres-best-practices/
├── SKILL.md           # エージェント向けスキルマニフェスト（Agent Skills 仕様）
├── AGENTS.md          # [GENERATED] 参照ドキュメント（生成物）
├── README.md          # このファイル
└── references/
    ├── _template.md      # Reference テンプレート
    ├── _sections.md      # セクション定義
    ├── _contributing.md  # 執筆ガイド
    └── *.md              # 個別の reference

packages/skills-build/
├── src/               # 共通ビルドシステムのソース
└── package.json       # NPM スクリプト
```

## Reference ファイル構成

完全なテンプレートは `references/_template.md` を参照してください。主要要素:

````markdown
---
title: 明確で行動指向のタイトル
impact: CRITICAL|HIGH|MEDIUM-HIGH|MEDIUM|LOW-MEDIUM|LOW
impactDescription: 数値化された効果（例: "10-100x faster"）
tags: relevant, keywords
---

## [Title]

[1-2 文の説明]

**Incorrect (description):**

```sql
-- どこが悪いかを説明するコメント
[悪い SQL の例]
```
````

**Correct (description):**

```sql
-- なぜ良いのかを説明するコメント
[良い SQL の例]
```

```
## 執筆ガイドライン

詳細は `references/_contributing.md` を参照してください。主な原則:

1. **具体的な変換を示す** - 抽象的な助言ではなく「X を Y に変える」
2. **エラー先行の構成** - 解決策より先に問題を示す
3. **影響を数値化** - 具体的な指標（10x faster, 50% smaller）を入れる
4. **自己完結した例** - 完全で実行可能な SQL
5. **意味のある命名** - (table1, col1) ではなく (users, email) を使う

## 影響度レベル

| Level | Improvement | Examples |
|-------|-------------|----------|
| CRITICAL | 10-100x | インデックス不足、接続枯渇 |
| HIGH | 5-20x | 不適切なインデックス種類、低品質なパーティショニング |
| MEDIUM-HIGH | 2-5x | N+1 クエリ、RLS 最適化 |
| MEDIUM | 1.5-3x | 冗長なインデックス、古い統計情報 |
| LOW-MEDIUM | 1.2-2x | VACUUM チューニング、設定の微調整 |
| LOW | Incremental | 高度なパターン、エッジケース |
```

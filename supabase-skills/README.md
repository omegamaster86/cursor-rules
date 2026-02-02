![Supabase Agent Skills](assets/og.png)

# Supabase Agent Skills

Supabase を AI エージェントで利用する開発者を支援する Agent Skills です。Agent Skills は、Claude Code、Cursor、GitHub Copilot などのエージェントが発見して活用できる、指示・スクリプト・リソースのフォルダです。より正確かつ効率的に作業するために使われます。

このリポジトリのスキルは、[Agent Skills](https://agentskills.io/) フォーマットに従っています。

## インストール

```bash
npx skills add supabase/agent-skills
```

### Claude Code プラグイン

このリポジトリのスキルは Claude Code プラグインとしてもインストールできます。

```bash
/plugin marketplace add supabase/agent-skills
/plugin install postgres-best-practices@supabase-agent-skills
```

## 利用可能なスキル

<details>
<summary><strong>supabase-postgres-best-practices</strong></summary>

Supabase の Postgres パフォーマンス最適化ガイドライン。8 つのカテゴリにわたる参照情報を含み、影響度順に整理されています。

**利用する場面:**

- SQL クエリの作成やスキーマ設計
- インデックスの実装やクエリ最適化
- データベースのパフォーマンス問題のレビュー
- コネクションプーリングやスケーリングの設定
- 行レベルセキュリティ（RLS）の作業

**対象カテゴリ:**

- クエリパフォーマンス（Critical）
- 接続管理（Critical）
- スキーマ設計（High）
- 同時実行性とロック（Medium-High）
- セキュリティ & RLS（Medium-High）
- データアクセスパターン（Medium）
- 監視と診断（Low-Medium）
- 高度な機能（Low）

</details>

## 使い方

インストール後、スキルは自動的に利用可能になります。関連するタスクが検出されるとエージェントが使用します。

**例:**

```
この Postgres クエリを最適化して
```

```
パフォーマンス問題がないかスキーマをレビューして
```

```
このテーブルに適切なインデックスを追加するのを手伝って
```

## スキル構成

各スキルは [Agent Skills Open Standard](https://agentskills.io/) に従います:

- `SKILL.md` - 必須のスキルマニフェスト（フロントマター: name, description, metadata）
- `AGENTS.md` - コンパイルされた参照ドキュメント（生成物）
- `references/` - 個別の参照ファイル

## ライセンス

MIT

# React Best Practices

エージェント/LLM 向けに最適化された React Best Practices を作成・保守するための構造化リポジトリです。

## 構成

- `rules/` - ルールごとの個別ファイル（1 ルール 1 ファイル）
  - `_sections.md` - セクション情報（タイトル、影響度、説明）
  - `_template.md` - 新規ルール作成テンプレート
  - `area-description.md` - 個別ルールファイル
- `src/` - ビルドスクリプトとユーティリティ
- `metadata.json` - ドキュメントメタデータ（バージョン、組織、要約）
- __`AGENTS.md`__ - 統合出力（生成物）
- __`test-cases.json`__ - LLM 評価用テストケース（生成物）

## はじめ方

1. 依存関係をインストール:
   ```bash
   pnpm install
   ```

2. ルールから AGENTS.md を生成:
   ```bash
   pnpm build
   ```

3. ルールファイルを検証:
   ```bash
   pnpm validate
   ```

4. テストケースを抽出:
   ```bash
   pnpm extract-tests
   ```

## 新しいルールの作成

1. `rules/_template.md` を `rules/area-description.md` にコピー
2. 適切なプレフィックスを選択
   - `async-` : ウォーターフォール排除（第1章）
   - `bundle-` : バンドルサイズ最適化（第2章）
   - `server-` : サーバーサイド性能（第3章）
   - `client-` : クライアント側データ取得（第4章）
   - `rerender-` : 再レンダー最適化（第5章）
   - `rendering-` : 描画性能（第6章）
   - `js-` : JavaScript 性能（第7章）
   - `advanced-` : 高度なパターン（第8章）
3. frontmatter と本文を記入
4. 説明付きの明確な bad/good 例を用意
5. `pnpm build` を実行し AGENTS.md / test-cases.json を再生成

## ルールファイル構造

各ルールファイルは次の構造に従います。

```markdown
---
title: ここにルールタイトル
impact: MEDIUM
impactDescription: 任意の補足説明
tags: tag1, tag2, tag3
---

## ここにルールタイトル

ルールの要点と重要性を簡潔に説明します。

**Incorrect（何が問題か）:**

```typescript
// 悪いコード例
```

**Correct（何が適切か）:**

```typescript
// 良いコード例
```

必要に応じて補足説明。

参考: [Link](https://example.com)
```

## ファイル命名規則

- `_` で始まるファイルは特別扱い（ビルド対象外）
- ルールファイル: `area-description.md`（例: `async-parallel.md`）
- セクションはファイル名プレフィックスから自動判定
- ルールは各セクション内でタイトル順ソート
- ID（例: 1.1, 1.2）はビルド時に自動生成

## 影響度レベル

- `CRITICAL` - 最優先。大きな性能改善
- `HIGH` - 有意な性能改善
- `MEDIUM-HIGH` - 中〜高の改善
- `MEDIUM` - 中程度の改善
- `LOW-MEDIUM` - 低〜中の改善
- `LOW` - 段階的な改善

## スクリプト

- `pnpm build` - ルールを AGENTS.md に統合
- `pnpm validate` - ルールファイルを検証
- `pnpm extract-tests` - LLM 評価用テストケースを抽出
- `pnpm dev` - ビルド + 検証

## コントリビュート

ルールを追加・変更する際は次を守ってください。

1. セクションに対応するプレフィックスを使う
2. `_template.md` の構造に従う
3. 説明付きの bad/good 例を含める
4. 適切なタグを付与する
5. `pnpm build` で AGENTS.md / test-cases.json を再生成する
6. ルールはタイトル順に自動ソートされるため番号管理は不要

## 謝辞

原案は [Vercel](https://vercel.com) の [@shuding](https://x.com/shuding) により作成されました。

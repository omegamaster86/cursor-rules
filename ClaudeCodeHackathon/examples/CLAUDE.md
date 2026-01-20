# 例: プロジェクト用 CLAUDE.md

これはプロジェクト単位の CLAUDE.md の例です。プロジェクトのルートに配置してください。

## プロジェクト概要

[プロジェクトの簡単な説明 - 何をするものか、技術スタック]

## 重要ルール

### 1. コード構成

- 大きなファイルより小さなファイルを多数
- 高い凝集・低い結合
- 1ファイルあたり通常200〜400行、最大800行
- 種類別ではなく機能／ドメインごとに整理

### 2. コードスタイル

- コード・コメント・ドキュメントに絵文字禁止
- 常に不変性 — オブジェクトや配列をミューテートしない
- 本番コードで console.log を使わない
- try/catch による適切なエラーハンドリング
- Zod などで入力検証

### 3. テスト

- TDD: 先にテストを書く
- カバレッジ最低80%
- ユーティリティの単体テスト
- API の結合テスト
- 重要フローの E2E テスト

### 4. セキュリティ

- 秘密情報のハードコード禁止
- センシティブなデータは環境変数で管理
- すべてのユーザー入力を検証
- パラメータ化クエリのみ使用
- CSRF 保護を有効化

## ファイル構成

```
src/
|-- app/              # Next.js app router
|-- components/       # 再利用可能なUIコンポーネント
|-- hooks/            # カスタムReactフック
|-- lib/              # ユーティリティライブラリ
|-- types/            # TypeScript定義
```

## 重要パターン

### API レスポンス形式

```typescript
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
}
```

### エラーハンドリング

```typescript
try {
  const result = await operation()
  return { success: true, data: result }
} catch (error) {
  console.error('Operation failed:', error)
  return { success: false, error: 'User-friendly message' }
}
```

## 環境変数

```bash
# 必須
DATABASE_URL=
API_KEY=

# 任意
DEBUG=false
```

## 利用可能コマンド

- `/tdd` - テスト駆動開発ワークフロー
- `/plan` - 実装計画を作成
- `/code-review` - コード品質レビュー
- `/build-fix` - ビルドエラー修正

## Git ワークフロー

- Conventional Commits: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`
- main へ直接コミットしない
- PR はレビュー必須
- マージ前に全テストが通ること

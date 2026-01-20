# Codemap更新

コードベース構造を分析し、アーキテクチャドキュメントを更新する:

1. すべてのソースファイルをスキャンし、import/export/依存関係を収集
2. 次の形式でトークン軽量なcodemapを生成:
   - codemaps/architecture.md - 全体アーキテクチャ
   - codemaps/backend.md - バックエンド構成  
   - codemaps/frontend.md - フロントエンド構成
   - codemaps/data.md - データモデルとスキーマ

3. 前回バージョンからの差分率を計算
4. 変更が30%を超える場合は、更新前にユーザー承認を要求
5. 各codemapに更新日時を付与
6. レポートを `.reports/codemap-diff.txt` に保存

TypeScript/Node.jsを使って分析する。実装詳細ではなく高レベル構造に集中する。

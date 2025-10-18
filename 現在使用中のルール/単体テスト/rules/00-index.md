## 単体テスト ルール集（分割版）

このディレクトリは、既存の「単体テストガイドライン」を実運用しやすいルール形式に再編したものです。実務で迷わないように、Must/Should中心で簡潔に定義しています。詳細解説や長文の背景は元のガイドラインを参照してください。

### 対象
- TypeScript/Node.js/Next.js/React を前提
- テストフレームワークは Jest/Vitest のいずれか（プロジェクト方針に従う）

### 章構成（リンク）
- [01-policy.md](./01-policy.md): 基本方針・適用範囲・禁止事項（Must中心）
- [02-test-design.md](./02-test-design.md): テスト設計（AAA、境界値、異常系、網羅）
- [03-mocks-and-data.md](./03-mocks-and-data.md): モック/スタブ、テストデータ、ファクトリ
- [04-structure-and-naming.md](./04-structure-and-naming.md): ディレクトリ、命名、テスト単位、分割基準
- [05-execution-and-ci.md](./05-execution-and-ci.md): 実行方法、CI/品質ゲート、並列化
- [06-quality-and-metrics.md](./06-quality-and-metrics.md): カバレッジ基準、レビュー観点、失敗時の対応
- [07-environment-and-db.md](./07-environment-and-db.md): 環境変数、インメモリDB、時計固定
- [08-performance.md](./08-performance.md): 実行時間最適化、メモリ監視、安定化
- [09-checklists.md](./09-checklists.md): 作成/レビュー/運用チェックリスト
- [10-maintenance.md](./10-maintenance.md): 保守・更新（更新タイミング/整理）

### 使い方
1) まず `01-policy.md` を読んで最低限のMustを統一します。
2) 実装時は `02〜04` を参照してテストを書き始めます。
3) 実行・CIは `05`、品質担保は `06` を参照します。
4) 環境やDBなど外部要因は `07`、パフォーマンスは `08` を参照します。
5) 最後に `09` のチェックリストで抜け漏れ確認を行います。
6) 仕様変更や修正時は `10` を参照しテストを更新します。

注: 各章には「良い例／悪い例」を簡潔に記載しています。詳細解説は元のガイドラインを参照してください。


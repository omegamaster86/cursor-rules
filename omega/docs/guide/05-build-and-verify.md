# 作って証明する

## プレイブック（代表）

| プレイブック | 用途 |
|-------------|------|
| Feature / Refactoring / Bug fix | 実装の型 |
| Prototype | 観測で決まる分岐 |
| Hillclimb | 1 メトリクスの科学的改善 |
| Runtime / Trace forensics | 症状・プロファイルの診断 |

ドメイン規約: `web-coding-standards`、`nextjs-directory-structure`、`supabase-implementation` など（[skills README](../../skills/README.md)）。

## 完了ゲート

**`/verify-done`** が正本。コンパイルや「テスト追加した」だけでは完了にしない。

PJ に `verify-*` があるときは feature map に沿って drive する。無ければ `/create-verification-skill`。

## TDD

バグ修正で安価な failing test が書けるときは **tdd** スキルと Bug fix ステップ 5。

次: [PR と land](./06-ship-pr.md)

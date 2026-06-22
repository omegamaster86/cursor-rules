# genai-pstack Skills 一覧

`genai-pstack/skills/` は **ドメイン規約** と **ワークフロー** をフラットに配置しています。

## エントリーポイント

| スキル / コマンド | 用途 |
|-------------------|------|
| `/omega-mode`（command） | 非自明な実装・調査のメイン入口 |
| `omega-mode`（skill） | 原則・プレイブックの本体（コマンドと同名） |

---

## ドメインスキル（genai 由来）

Next.js / Supabase プロジェクト向けの書き方・配置規約。

| スキル | 用途 |
|--------|------|
| `web-coding-standards` | TypeScript、React、Tailwind、フォーム、Supabase クライアント |
| `web-library-guide` | 推奨ライブラリ選定 |
| `nextjs-directory-structure` | App Router のディレクトリ配置 |
| `nextjs-code-review` | Next.js PR レビューチェックリスト |
| `supabase-implementation` | DB、Edge Functions、RLS、型生成 |
| `supabase-code-review` | Supabase PR レビューチェックリスト |
| `mock-store-guide` | DB 前のモックストアパターン |

---

## ワークフロースキル（pstack 由来）

### 調査・設計・レビュー

| スキル | 用途 |
|--------|------|
| `how` | サブシステムの仕組み説明 |
| `architect` | 関数境界を越える設計 |
| `arena` | 並列案の比較 |
| `interrogate` | → `review-orchestrator-triple-hybrid` へ委譲 |
| `blast-radius` | 変更の影響範囲 |
| `tdd` | 失敗テスト先行のバグ修正 |
| `recall` | チャット履歴からコンテキスト再構築 |
| `figure-it-out` | プレイブック不適合時の監査可能プラン設計 |
| `reflect` | 長タスクの教訓をスキル化 |
| `show-me-your-work` | 意思決定 TSV ログ |

### 設定（rules/）

| ファイル | 用途 |
|----------|------|
| `omega-models.mdc` | omega-mode のロール別モデル（`.cursor/rules/` に配置して手編集） |

### 原則（principle-*）20本

`omega-mode` の Principles インデックスから on-demand で読む。

**Core:** laziness-protocol, foundational-thinking, redesign-from-first-principles, subtract-before-you-add, minimize-reader-load, outcome-oriented-execution, experience-first, exhaust-the-design-space, build-the-lever

**Architecture:** boundary-discipline, type-system-discipline, make-operations-idempotent, migrate-callers-then-delete-legacy-apis, separate-before-serializing-shared-state

**Verification:** prove-it-works, fix-root-causes, sequence-verifiable-units

**Delegation:** guard-the-context-window, never-block-on-the-human

**Meta:** encode-lessons-in-structure

---

## 関連コマンド（commands/）

| コマンド | 用途 |
|----------|------|
| `omega-mode` | 本スタックのメイン入口 |
| `file-brief` | 単ファイル調査 |
| `reuse-check` | 既存コード流用チェック |
| `review-orchestrator-triple-hybrid` | 3モデル並列 PR レビュー |
| `deep-review-*` | 上記 orchestrator のサブエージェント用 |

---

## 採用しなかった pstack スキル

| スキル | 理由 |
|--------|------|
| `typescript-best-practices` | `web-coding-standards` と重複 |
| `setup-pstack` | `omega-models.mdc` を手編集で十分 |
| `automate-me` | `omega-mode` を直接カスタマイズするため不要 |
| `unslop` | 文体の細かい制御は不要 |

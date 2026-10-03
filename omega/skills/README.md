# genai-pstack Skills 一覧

`genai-pstack/skills/` は **ドメイン規約** と **ワークフロー** をフラットに配置しています。

## エントリーポイント

| スキル / コマンド | 用途 |
|-------------------|------|
| `/forge-mode`（command） | 非自明な実装・調査のメイン入口（Ship。Intent gate 通過後） |
| `/plan-interview`（skill） | 何を・なぜ・用語（Align）。forge より先。モデル自動起動しない |
| `/verify-done`（command） | 完了前検証（forge-mode ゲート・任意呼び出し） |
| `/create-verification-skill`（command） | 対象 PJ にユーザー操作の証明レシピ（`verify-<app>`）を生成 |
| `/maintain-verification-skill`（command） | 上記 feature map の監査・更新（プロダクトコードは触らない） |
| `/setup-forge`（skill） | ロール別モデル・reasoning budget を `forge-models.mdc` に書く |
| `forge-mode`（skill） | 原則・プレイブック（23）・Intent gate の本体（コマンドと同名） |
| [omega ガイド](../docs/guide/README.md) | 初回オンボーディング（plan-interview → forge-mode → ship） |

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
| `plan-interview` | 計画・設計のストレステスト（Align 入口。`/plan-interview`。終了時に `alignment:` を返す） |
| `grilling` | 上記のインタビュー技法本体（plan-interview から委譲。forge 中は使わない） |
| `how` | サブシステムの仕組み・フロー・配置（how does X work） |
| `why` | 設計 rationale・経緯・トレードオフ（why was Y built。MCP 並列調査） |
| `reflect` | 長タスク後にトランスクリプトから学びを既存スキル edits にルーティング |
| `architect` | 関数境界を越える設計（内部で multi-agent-candidates） |
| `multi-agent-candidates` | 並列設計案の比較・graft |
| `swarm` | カバレッジ分割・レース・探索の N 並列ワーカー |
| `setup-forge` | `forge-models.mdc` のインタラクティブ設定 |
| `blast-radius` | 変更の影響範囲 |
| `tdd` | 失敗テスト先行のバグ修正 |
| `recall` | チャット履歴からコンテキスト再構築 |
| `daily-chat-digest` | 指定日（JST）のチャットを `.cursor/chat-digest/<日付>/daily-chat.md` に出力（単独利用可） |
| `engineer-retrospective` | 振り返り入口。`daily-chat.md` が無ければ digest を同一ターンで実行してから批評 |
| `study-log` | チャットの学習内容をテックブログ形式で `.cursor/study-log/` に記録 |
| `yomiyasu` | AI 臭い日本語の推敲（PR・仕様・記事。**Cursor 向け抜粋**。正本 submodule は repo 直下 `yomiyasu/`。**明示依頼時**） |
| `product-design` | アイデア・URL・モックからレビュー可能プロトタイプ（**Cursor 専用**。browser MCP・`.cursor/product-design/` 前提。**Codex CLI 非対象**） |
| `session-log` | 長セッション状態をファイル化し新規チャットへ handoff |
| `figure-it-out` | プレイブック不適合時の監査可能プラン設計 |
| `decision-log` | 長時間 run の監査証跡（Notion DB 正本。forge プレイブック・figure-it-out からルーティング） |
| `create-verification-skill` | PJ 固有の動作確認スキルと feature map を生成 |
| `maintain-verification-skill` | 上記のソース読み + ライブ drive によるメンテ |

### 設定（rules/）

| ファイル | 用途 |
|----------|------|
| `forge-models.mdc` | forge-mode のロール別モデル（`/setup-forge` または `.cursor/rules/` で手編集） |

### forge-mode プレイブック（23）

Investigation / Bug fix / Perf / Hillclimb / Runtime・Trace forensics / Feature / Refactoring / Prototype / Visual parity / Authoring a skill / Eval / **Babysit** / **Shipping** / Autonomous run / **Orchestrate** / **Autopilot-stack** / **Autopilot-full** / Session pickup / Pause safely / Multi-phase plan / **Worktree cleanup** / Opening a PR。太字は pstack から追加した PR・夜間運用系。Bugbot 参照: `forge-mode/references/bugbot-triage.md`。スクリプト: `forge-mode/scripts/watch-pr`、`orch`、`worktree-audit.sh`。

### 原則（`forge-mode/principles/`）23本

`forge-mode` の Principles インデックスから **on-demand** で読む。`/forge-mode` 起動時はインデックスを先に読み、タスクに該当する leaf のみ `forge-mode/principles/*.md` を全文読む。

#### Core

| ファイル | 適用タイミング | 内容 |
|----------|----------------|------|
| `laziness-protocol.md` | リファクタ・diff・抽象/層の追加 | 削除と最小変更を優先 |
| `foundational-thinking.md` | ロジックを書く前（forge-mode 有無で共通） | 契約先行のデータ形状。フロント/バック並行トラック。CI・型・テスト骨格を機能より先 |
| `redesign-from-first-principles.md` | 既存設計に要件を足すとき | ボルトオンせず、最初からその要件があった形に再設計 |
| `attack-the-premise.md` | 同じ前提の fix が同じゲートで連続失敗 | census の後、前提を疑う |
| `subtract-before-you-add.md` | 追加・refactor・rewrite の順序 | 先に dead weight を削る |
| `minimize-reader-load.md` | 追いにくいコード | 辿る層数と読者が保持する状態を減らす |
| `outcome-oriented-execution.md` | フェーズ付き rewrite / 移行 | 中間互換より最終形。小さな PR では読まない |
| `experience-first.md` | Intent gate 通過後の UX・スコープ | 実装都合より体験。方向が空なら `/plan-interview` |
| `exhaust-the-design-space.md` | 先例のない UI / アーキテクチャ | commit 前に 2–3 案（Prototype 等） |
| `build-the-lever.md` | 非自明な編集・移行・分析 | codemod / script 等、reviewer が rerun できる tool |

#### Architecture

| ファイル | 適用タイミング | 内容 |
|----------|----------------|------|
| `model-the-domain.md` | 状態ロジック・分岐の増殖 | ドメインを構造に載せる |
| `boundary-discipline.md` | 検証・adapter・エラー配線 | 境界に guard、内部 pure（genai 規約と併読） |
| `type-system-discipline.md` | 型・シグネチャ設計 | 非法状態を表現不能に、境界で parse |
| `make-operations-idempotent.md` | リトライ下のコマンド・ループ | 同じ最終状態に収束 |
| `migrate-callers-then-delete-legacy-apis.md` | 新旧 internal API 共存 | 同一 wave で migrate + delete |
| `separate-before-serializing-shared-state.md` | 並行アクターが同じ状態を書く | 共有を先に消す。ロックは最後 |

#### Verification

| ファイル | 適用タイミング | 内容 |
|----------|----------------|------|
| `prove-it-works.md` | 完了宣言の前 | 正本は **`/verify-done`** |
| `fix-root-causes.md` | デバッグ中 | 再現→根本。nil-check で黙らせない |
| `sequence-verifiable-units.md` | マルチステップ・PR の積み方 | 各単位が check で終わる |
| `test-behavior-not-implementation.md` | テストの作成・変更 | リテラル expected、実装 pin を避ける |

#### Delegation

| ファイル | 適用タイミング | 内容 |
|----------|----------------|------|
| `guard-the-context-window.md` | コンテキスト逼迫時 | bulk はサブエージェントへ |
| `never-block-on-the-human.md` | Intent gate 通過後の実行分岐 | 可逆作業は進めて事後修正 |

#### Meta

| ファイル | 適用タイミング | 内容 |
|----------|----------------|------|
| `encode-lessons-in-structure.md` | 同じ指示を2回目書こうとしたとき | lint・script 等にエンコード |

---

## 関連コマンド（commands/）

| コマンド | 用途 |
|----------|------|
| `forge-mode` | Ship のメイン入口。起動時 Intent gate。`blocked` なら `/plan-interview` |
| `file-brief` | 単ファイル調査 |
| `reuse-check` | 既存コード流用チェック |
| `refactor-check` | リファクタ・削減チェック（ユーザー指示時） |
| `verify-done` | 完了前検証（forge-mode ゲート・任意呼び出し） |
| `create-verification-skill` | 対象 PJ に `verify-<app>` を生成 |
| `maintain-verification-skill` | `verify-<app>` の feature map 監査 |
| `review-orchestrator-triple-hybrid` | 3モデル並列 PR レビュー |
| `deep-review-*` | 上記 orchestrator のサブエージェント用 |

---

## Cursor 専用（Codex CLI 非対象）

`omega-link` / Cloud の `install-omega-cloud.sh` は `.cursor/skills` にだけリンクする。次は **Codex CLI（`~/.codex/skills` 等）へ同期しない** 想定。

| スキル | 理由 |
|--------|------|
| `product-design` | `cursor-ide-browser`・Cursor 状態ディレクトリ前提。同梱の `.codex-plugin/` は上流 OpenAI プラグイン用で omega では無視 |
| `yomiyasu` | Cursor 抜粋版。明示依頼時のみ（上表） |







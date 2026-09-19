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
| `forge-mode`（skill） | 原則・プレイブック・Intent gate の本体（コマンドと同名） |

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
| `how` | サブシステムの仕組み説明 |
| `architect` | 関数境界を越える設計 |
| `multi-agent-candidates` | 並列案の比較・最良統合 |
| `blast-radius` | 変更の影響範囲 |
| `tdd` | 失敗テスト先行のバグ修正 |
| `recall` | チャット履歴からコンテキスト再構築 |
| `daily-chat-digest` | 指定日（JST）のチャットを `.cursor/chat-digest/<日付>/daily-chat.md` に出力 |
| `engineer-retrospective` | digest を読み、聞き方・アーキテクト視点・指示の質を批評（`engineer-retrospective.md`） |
| `study-log` | チャットの学習内容をテックブログ形式で `.cursor/study-log/` に記録 |
| `session-log` | 長セッション状態をファイル化し新規チャットへ handoff |
| `figure-it-out` | プレイブック不適合時の監査可能プラン設計 |
| `decision-log` | 意思決定 マークダウンでログとしてためる |
| `create-verification-skill` | PJ 固有の動作確認スキルと feature map を生成 |
| `maintain-verification-skill` | 上記のソース読み + ライブ drive によるメンテ |

### 設定（rules/）

| ファイル | 用途 |
|----------|------|
| `forge-models.mdc` | forge-mode のロール別モデル（`.cursor/rules/` に配置して手編集） |

### 原則（`forge-mode/principles/`）14本

`forge-mode` の Principles インデックスから **on-demand** で読む。`/forge-mode` 起動時はインデックスを先に読み、タスクに該当する leaf のみ `forge-mode/principles/*.md` を全文読む。

#### Core

| ファイル | 適用タイミング | 内容 |
|----------|----------------|------|
| `foundational-thinking.md` | ロジックを書く前（forge-mode 有無で共通） | 契約先行のデータ形状。フロント/バック並行トラック。CI・型・テスト骨格を機能より先。型収束とコンポーネント抽象化の切り分け。並行編集の隔離 |
| `redesign-from-first-principles.md` | 既存設計に要件を足すとき | ボルトオンせず、最初からその要件があった形に再設計する |
| `experience-first.md` | Intent gate 通過後の UX・スコープのトレードオフ | 実装都合より体験。方向が空なら `/plan-interview` |
| `outcome-oriented-execution.md` | フェーズ付き rewrite / 移行 | 中間互換より最終形。橋を恒久化しない。小さな PR では読まない |

#### Architecture

| ファイル | 適用タイミング | 内容 |
|----------|----------------|------|
| `model-the-domain.md` | 状態ロジック・分岐の増殖 | ドメインを構造（状態機械、判別共用体、lookup）に載せる。boolean / if の散在を止める |
| `type-system-discipline.md` | 型・シグネチャ設計 | 不正状態を表現不能に、意味的プリミティブに brand、外部データは境界で parse。網羅的 match、権威スキーマから導出。検証の所在は genai ドメイン規約（`form-validation`、`practice-bff` 等）を参照 |
| `make-operations-idempotent.md` | クラッシュ・リトライ下のコマンド・ループ | 「2回実行」「途中クラッシュ」で同じ最終状態に収束するよう設計。自己修復ロック・冪等スケジューリング |
| `separate-before-serializing-shared-state.md` | 並行アクターが同じ状態を書きそうなとき | 共有を先に消す。ロック・逐次化は最後 |

#### Verification

| ファイル | 適用タイミング | 内容 |
|----------|----------------|------|
| `prove-it-works.md` | 完了宣言の前 | 背景・哲学。実行手順の正本は **`/verify-done`**。コンパイル・自己報告・代理指標ではなく実アーティファクトで検証 |
| `sequence-verifiable-units.md` | マルチステップ作業・コミット/PR の積み方 | 各単位がチェックで終わるまで次に進まない。失敗テスト→修正の順など、シーケンス自体がレビュアーに証明する |
| `fix-root-causes.md` | デバッグ中 | 症状をごまかさず根本で直す。再現が先。nil-check で crash を黙らせない |

#### Delegation

| ファイル | 適用タイミング | 内容 |
|----------|----------------|------|
| `guard-the-context-window.md` | コンテキスト逼迫時 | 大きな出力・長いファイルはサブエージェントへ。メインには要約のみ。不要ファイルは読まない。フェーズにサイズ上限 |
| `never-block-on-the-human.md` | Intent gate 通過後の可逆作業で確認したくなったとき | 進めて結果を提示し事後修正。`blocked` では無効。不可逆のみ確認。プロダクト方向は人間、実行はブロックしない |

#### Meta

| ファイル | 適用タイミング | 内容 |
|----------|----------------|------|
| `encode-lessons-in-structure.md` | 同じ指示を2回目書こうとしたとき | テキスト増やさず lint・メタデータ・runtime check・スクリプトにエンコード。繰り返し修正は最強の機械的ガードへルーティング |

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



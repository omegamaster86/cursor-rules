# genai-pstack Skills 一覧

`genai-pstack/skills/` は **ドメイン規約** と **ワークフロー** をフラットに配置しています。

## エントリーポイント

| スキル / コマンド | 用途 |
|-------------------|------|
| `/forge-mode`（command） | 非自明な実装・調査のメイン入口 |
| `/verify-done`（command） | 完了前検証（forge-mode ゲート・任意呼び出し） |
| `forge-mode`（skill） | 原則・プレイブックの本体（コマンドと同名） |

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
| `plan-interview` | 計画・設計のストレステスト（ユーザー向けエントリ。`/plan-interview`） |
| `grilling` | 上記のインタビュー技法本体（plan-interview から委譲、他スキルも参照可） |
| `how` | サブシステムの仕組み説明 |
| `architect` | 関数境界を越える設計 |
| `multi-agent-candidates` | 並列案の比較・最良統合 |
| `blast-radius` | 変更の影響範囲 |
| `tdd` | 失敗テスト先行のバグ修正 |
| `recall` | チャット履歴からコンテキスト再構築 |
| `session-log` | 長セッション状態をファイル化し新規チャットへ handoff |
| `figure-it-out` | プレイブック不適合時の監査可能プラン設計 |
| `decision-log` | 意思決定 マークダウンでログとしてためる |

### 設定（rules/）

| ファイル | 用途 |
|----------|------|
| `forge-models.mdc` | forge-mode のロール別モデル・Task runner slug の正（`.cursor/rules/` に配置して手編集） |
| `multi-agent-task-enforcement.mdc` | multi-agent-candidates / architect の Task 3並列必須（`.cursor/rules/` に配置） |

### 原則（`forge-mode/principles/`）8本

`forge-mode` の Principles インデックスから **on-demand** で読む。`/forge-mode` 起動時はインデックスを先に読み、タスクに該当する leaf のみ `forge-mode/principles/*.md` を全文読む。

#### Core

| ファイル | 適用タイミング | 内容 |
|----------|----------------|------|
| `foundational-thinking.md` | ロジックを書く前（forge-mode 有無で共通） | 契約先行のデータ形状。フロント/バック並行トラック。CI・型・テスト骨格を機能より先。型収束とコンポーネント抽象化の切り分け。並行編集の隔離 |

#### Architecture

| ファイル | 適用タイミング | 内容 |
|----------|----------------|------|
| `type-system-discipline.md` | 型・シグネチャ設計 | 不正状態を表現不能に、意味的プリミティブに brand、外部データは境界で parse。網羅的 match、権威スキーマから導出。検証の所在は genai ドメイン規約（`form-validation`、`practice-bff` 等）を参照 |
| `make-operations-idempotent.md` | クラッシュ・リトライ下のコマンド・ループ | 「2回実行」「途中クラッシュ」で同じ最終状態に収束するよう設計。自己修復ロック・冪等スケジューリング |

#### Verification

| ファイル | 適用タイミング | 内容 |
|----------|----------------|------|
| `prove-it-works.md` | 完了宣言の前 | 背景・哲学。実行手順の正本は **`/verify-done`**。コンパイル・自己報告・代理指標ではなく実アーティファクトで検証 |
| `sequence-verifiable-units.md` | マルチステップ作業・コミット/PR の積み方 | 各単位がチェックで終わるまで次に進まない。失敗テスト→修正の順など、シーケンス自体がレビュアーに証明する |

#### Delegation

| ファイル | 適用タイミング | 内容 |
|----------|----------------|------|
| `guard-the-context-window.md` | コンテキスト逼迫時 | 大きな出力・長いファイルはサブエージェントへ。メインには要約のみ。不要ファイルは読まない。フェーズにサイズ上限 |
| `never-block-on-the-human.md` | 可逆作業で確認したくなったとき | 進めて結果を提示し事後修正。不可逆（force-push、本番削除、外部送信）のみ確認。プロダクト方向は人間、実行はブロックしない |

#### Meta

| ファイル | 適用タイミング | 内容 |
|----------|----------------|------|
| `encode-lessons-in-structure.md` | 同じ指示を2回目書こうとしたとき | テキスト増やさず lint・メタデータ・runtime check・スクリプトにエンコード。繰り返し修正は最強の機械的ガードへルーティング |

---

## 関連コマンド（commands/）

| コマンド | 用途 |
|----------|------|
| `forge-mode` | 本スタックのメイン入口 |
| `file-brief` | 単ファイル調査 |
| `reuse-check` | 既存コード流用チェック |
| `refactor-check` | リファクタ・削減チェック（ユーザー指示時） |
| `verify-done` | 完了前検証（forge-mode ゲート・任意呼び出し） |
| `review-orchestrator-triple-hybrid` | 3モデル並列 PR レビュー |
| `deep-review-*` | 上記 orchestrator のサブエージェント用 |



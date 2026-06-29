# genai-pstack Skills 一覧

`genai-pstack/skills/` は **ドメイン規約** と **ワークフロー** をフラットに配置しています。

## エントリーポイント

| スキル / コマンド | 用途 |
|-------------------|------|
| `/omega-mode`（command） | 非自明な実装・調査のメイン入口 |
| `/verify-done`（command） | 完了前検証（omega-mode ゲート・任意呼び出し） |
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
| `blast-radius` | 変更の影響範囲 |
| `tdd` | 失敗テスト先行のバグ修正 |
| `recall` | チャット履歴からコンテキスト再構築 |
| `session-brief` | 長セッション状態をファイル化し新規チャットへ handoff |
| `figure-it-out` | プレイブック不適合時の監査可能プラン設計 |
| `decision-log` | 意思決定 マークダウンでログとしてためる |

### 設定（rules/）

| ファイル | 用途 |
|----------|------|
| `omega-models.mdc` | omega-mode のロール別モデル（`.cursor/rules/` に配置して手編集） |

### 原則（principle-*）16本

`omega-mode` の Principles インデックスから **on-demand** で読む（`disable-model-invocation: true` のため自動ロードされない）。`/omega-mode` 起動時はインデックスを先に読み、タスクに該当する leaf のみ `principle-*/SKILL.md` を全文読む。


#### Core

| スキル | 適用タイミング | 内容 |
|--------|----------------|------|
| `principle-foundational-thinking` | ロジックを書く前（omega 有無で共通） | 契約先行のデータ形状。フロント/バック並行トラック。CI・型・テスト骨格を機能より先。型収束とコンポーネント抽象化の切り分け。並行編集の隔離 |
| `principle-redesign-from-first-principles` | 既存設計への新要件統合 | 後付けせず「初日から前提だったか」の形に再設計。全体を理解してから段階的に配信 |
| `principle-outcome-oriented-execution` | 計画された書き直し・マイグレーション | 中間の滑らかさより最終アーキテクチャへ収束。計画・スコープ限定・可逆なら中間の破損を許容し、完了前に最終検証 |
| `principle-experience-first` | プロダクト・UX・機能スコープのトレードオフ | 実装都合よりユーザー（エンドユーザー・同僚・次の保守者）の喜び。少なく磨く・プロトタイプ先行・コアループに奉仕 |
| `principle-exhaust-the-design-space` | 先例のない UI・設計判断 | 正解が不明なら2〜3の競合プロトタイプを並べて比較してからコミット。確立パターンの機械的実装には適用しない |
| `principle-build-the-lever` | 非自明な作業全般 | 手作業より codemod・スクリプト・ジェネレーター・再実行可能チェックを構築。レビュアーが再実行できる成果物にする。委譲時はスキルとしてレシピを固定 |

#### Architecture

| スキル | 適用タイミング | 内容 |
|--------|----------------|------|
| `principle-type-system-discipline` | 型・シグネチャ設計 | 不正状態を表現不能に、意味的プリミティブに brand、外部データは境界で parse。網羅的 match、権威スキーマから導出。検証の所在は genai ドメイン規約（`form-validation`、`practice-bff` 等）を参照 |
| `principle-make-operations-idempotent` | クラッシュ・リトライ下のコマンド・ループ | 「2回実行」「途中クラッシュ」で同じ最終状態に収束するよう設計。自己修復ロック・冪等スケジューリング |
| `principle-migrate-callers-then-delete-legacy-apis` | 新内部 API 導入時 | 互換レイヤーを残さず同一 wave で caller 移行→旧 API 削除。外部互換が不要な協調的変更向け |
| `principle-separate-before-serializing-shared-state` | 並行アクターが同一リソースに書くとき | まず共有書き込みを排除（専用ファイル・ブランチ・キー）。真の不変条件だけロック・逐次フェーズでシリアライズ |

#### Verification

| スキル | 適用タイミング | 内容 |
|--------|----------------|------|
| `principle-prove-it-works` | 完了宣言の前 | 背景・哲学。実行手順の正本は **`/verify-done`**。コンパイル・自己報告・代理指標ではなく実アーティファクトで検証 |
| `principle-fix-root-causes` | デバッグ | 症状ではなく根本原因まで「なぜ」を追う。先に再現。nil ガード追加は症状修正。再起動バグはコードより永続状態を疑う |
| `principle-sequence-verifiable-units` | マルチステップ作業・コミット/PR の積み方 | 各単位がチェックで終わるまで次に進まない。失敗テスト→修正の順など、シーケンス自体がレビュアーに証明する |

#### Delegation

| スキル | 適用タイミング | 内容 |
|--------|----------------|------|
| `principle-guard-the-context-window` | コンテキスト逼迫時 | 大きな出力・長いファイルはサブエージェントへ。メインには要約のみ。不要ファイルは読まない。フェーズにサイズ上限 |
| `principle-never-block-on-the-human` | 可逆作業で確認したくなったとき | 進めて結果を提示し事後修正。不可逆（force-push、本番削除、外部送信）のみ確認。プロダクト方向は人間、実行はブロックしない |

#### Meta

| スキル | 適用タイミング | 内容 |
|--------|----------------|------|
| `principle-encode-lessons-in-structure` | 同じ指示を2回目書こうとしたとき | テキスト増やさず lint・メタデータ・runtime check・スクリプトにエンコード。繰り返し修正は最強の機械的ガードへルーティング |

---

## 関連コマンド（commands/）

| コマンド | 用途 |
|----------|------|
| `omega-mode` | 本スタックのメイン入口 |
| `file-brief` | 単ファイル調査 |
| `reuse-check` | 既存コード流用チェック |
| `refactor-check` | リファクタ・削減チェック（ユーザー指示時） |
| `verify-done` | 完了前検証（omega-mode ゲート・任意呼び出し） |
| `review-orchestrator-triple-hybrid` | 3モデル並列 PR レビュー |
| `deep-review-*` | 上記 orchestrator のサブエージェント用 |



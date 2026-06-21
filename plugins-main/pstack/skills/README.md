# pstack Skills

`plugins-main/pstack/skills` に含まれる Cursor Agent Skills の一覧と概要です。各スキルは `SKILL.md` を持ち、特定の状況でエージェントの振る舞いを規定します。

**エントリーポイント:** 多くのタスクは [`poteto-mode`](#poteto-mode) から始めます。`/poteto-mode` と入力すると、タスクに合ったプレイブックを選び、必要なスキルへルーティングします。

**原則:** `principle-*` の 20 本はエンジニアリング原則のリファレンスです。`poteto-mode` がインラインでインデックスし、他スキルから名前で参照されます。

---

## 目次

- [ワークフロー・エントリーポイント](#ワークフローエントリーポイント)
- [調査・設計・レビュー](#調査設計レビュー)
- [メタ・設定・記録](#メタ設定記録)
- [言語固有](#言語固有)
- [原則スキル（principle-*）](#原則スキルprinciple-)
  - [Core](#core)
  - [Architecture](#architecture)
  - [Verification](#verification)
  - [Delegation](#delegation)
  - [Meta](#meta)

---

## ワークフロー・エントリーポイント

### poteto-mode

| 項目 | 内容 |
|------|------|
| **パス** | `poteto-mode/SKILL.md` |
| **トリガー** | `/poteto-mode`、`poteto`、このスタイルでの作業リクエスト |
| **概要** | 簡潔で詳細な返信、意図的なサブエージェント、unslopped な散文、シンプルなコード、検証済みの作業のためのエージェントスタイル |

**主な内容:**

- **譲れないルール:** 複数ステップのタスクは必ず Principles セクションを読む todo から開始。非自明な変更は `how`、設計は `architect`、争点のある設計は `interrogate`、散文は `unslop`、長時間作業は `show-me-your-work` などへルーティング
- **Principles:** 20 の原則スキルへのインデックス（Core / Architecture / Verification / Delegation / Meta）
- **Autonomy:** 可逆作業は確認なしで進める。不可逆書き込み（force-push、本番削除など）のみ一時停止
- **Subagents:** デフォルトは `poteto-agent`、`run_in_background: true`、ロールごとのモデル（`/setup-pstack` で設定）
- **Playbooks（16本）:** investigation、bug-fix、perf-issue、hillclimb、runtime-forensics、trace-forensics、feature、refactoring、prototype、visual-parity、authoring-a-skill、eval、autonomous-run、session-pickup、pause-safely、multi-phase-plan、opening-a-pr

**関連:** ほぼすべてのスキル。`figure-it-out` はプレイブックが当てはまらない大規模作業向け

---

### figure-it-out

| 項目 | 内容 |
|------|------|
| **パス** | `figure-it-out/SKILL.md` |
| **トリガー** | `/figure-it-out`、大規模マイグレーション、狭いプレイブックが当てはまらない作業 |
| **概要** | 監査可能なプレイブックをその場で設計する。タスクに応じて厳密さをスケールし、仮説ループを回し、決定を記録する |

**フェーズ:**

1. **枠組み** — 完了の定義（反証可能な述語）、スコープの定量化、厳密さのレベル
2. **ワークフロー設計** — 原子的ユニットへの分解、検証ハーネス、`architect`/`arena` の適用、並列化の境界
3. **ループ** — 仮説→最小変更→測定→検証（`sequence-verifiable-units`）
4. **監査証跡** — `show-me-your-work` で TSV ログ
5. **検証と返答** — 全体述語のチェック、`encode-lessons-in-structure` で教訓を構造化

**関連:** `poteto-mode`（プレイブック不適合時）、`show-me-your-work`、`architect`、`arena`

---

## 調査・設計・レビュー

### how

| 項目 | 内容 |
|------|------|
| **パス** | `how/SKILL.md` |
| **トリガー** | 「how does X work」、配置/所有/レイヤリングの質問、コードウォークスルー |
| **概要** | サブシステムのアーキテクチャ、ランタイムフロー、オンボーディング用メンタルモデルを説明する（動機は `why`） |

**モード:**

- **Explain（デフォルト）:** 複雑さに応じて並列 explorer → explainer で統合、または単純な質問は 1 パスで説明
- **Critique:** 説明後に複数モデルの critic を起動し、アーキテクチャ問題を特定

**出力形式:** Overview、Key Concepts、How It Works、Where Things Live、Gotchas

**関連:** `why`（動機）、`architect`（設計前の土台固め）、`blast-radius`（影響範囲）

---

### why

| 項目 | 内容 |
|------|------|
| **パス** | `why/SKILL.md` |
| **トリガー** | 「why does X work this way」、設計根拠、回帰、ポストモーテム |
| **概要** | 利用可能な MCP を発見し、7 つの証拠カテゴリを並列照会し、引用付きで決定とトレードオフを返す |

**証拠カテゴリ（並列調査）:**

1. ソース管理（git、`gh`）— 常に起動
2. 課題トラッカー（Linear、Jira など）
3. 長文ドキュメント（Notion、Confluence など）
4. リアルタイムチャット（Slack など）
5. インフラ可観測性（Datadog など）
6. エラートラッキング（Sentry など）
7. プロダクト分析ウェアハウス（Databricks など）

**認識論:** すべて引用、間接的証拠はヘッジ、矛盾とギャップを表面化、コード形状からの意図推論を避ける

**関連:** `how`（振る舞い）、`recall`（最近の作業コンテキスト）、`blast-radius`

---

### recall

| 項目 | 内容 |
|------|------|
| **パス** | `recall/SKILL.md` |
| **トリガー** | 「X の作業を思い出して」「キャッチアップ」「どこまで進んだか」 |
| **概要** | チャット履歴・ライブ状態・共有記録から最近の作業コンテキストを再構成し、短いブリーフを返す |

**プロセス:** スコープ固定 → トランスクリプトの並列マイニング → 名前付きトピックは `why` 系の共有記録スイープ → `git`/`gh` でライブ状態検証

**出力:** カプセル（最大5行）、スレッド（ステータスタグ付き）、問題、次の一手

**関連:** `why`、`session-pickup` プレイブック（特定チャット再開は別）

---

### architect

| 項目 | 内容 |
|------|------|
| **パス** | `architect/SKILL.md` |
| **トリガー** | `/architect`、実装前に型・シグネチャ・モジュール構造を確定したいとき |
| **概要** | `not implemented` 本体と疑似コードで設計をスケッチし、実装が誤りを証明したら捨てて再設計する |

**フェーズ:** Ground → Sketch（`arena` で複数候補）→ Agree（オプトイン）→ Implement → Scrap（繰り返し摩擦がパターン化したら再設計）

**成果物:** 呼び出し側の使い方、型スケッチ、関数シグネチャ、モジュールマップ、根拠

**関連:** `arena`、`how`、`interrogate`、`exhaust-the-design-space` 原則

---

### arena

| 項目 | 内容 |
|------|------|
| **パス** | `arena/SKILL.md` |
| **トリガー** | `/arena`、非自明な成果物の 1 回試行が間違った形にロックインしうるとき |
| **概要** | 同じタスクに N 個の並列候補を起動し、ベースを選び、敗者の最強部分をグラフトする |

**フェーズ:** Frame → Fan out → Cross-judge → Pick → Graft → Verify

**ルール:** 各候補は独自の出力パス（worktree または `/tmp`）。統合後は `prove-it-works` と同レベルで検証

**関連:** `architect`、`exhaust-the-design-space`、`separate-before-serializing-shared-state` 原則

---

### interrogate

| 項目 | 内容 |
|------|------|
| **パス** | `interrogate/SKILL.md` |
| **トリガー** | `/interrogate`、adversarial review、stress test、blind spots |
| **概要** | 複数 LLM レビュアーが独立した角度から変更に挑戦し、リードが Act on / Consider / Noted / Dismissed に分類 |

**プロセス:** スコープ決定 → 意図を 1 段落で述べる → 設定済みモデルごとにレビュアー起動 → 合意の特定 → リード判断

**関連:** `how`（critique モード）、`architect`（設計への敵対的圧力）、`blast-radius`

---

### blast-radius

| 項目 | 内容 |
|------|------|
| **パス** | `blast-radius/SKILL.md` |
| **トリガー** | 「X の blast radius」「これは何を壊すか」 |
| **概要** | diff を超えて変更が他所で何を壊しうるかを特定し、安全だと言える根拠を実コード実行で証明する |

**確信度の段階:** 言っただけ → 行を指した → 悪いケースが起きないことを示した → 実行した → 動いているアプリで再現した

**返すもの:** 何をするか、安全の根拠となる 1 事実（証明済み/unproven）、リスク、クリア済み、マージ前の最安テスト

**関連:** `how`、`why`、`arena`（大規模変更時）

---

### tdd

| 項目 | 内容 |
|------|------|
| **パス** | `tdd/SKILL.md` |
| **トリガー** | 明示的な TDD 要求、またはバグに安価で明らかなローカルテスト対象があるとき |
| **概要** | 本番コード変更前に失敗テストを書き、修正後に通る回帰テストを確保する |

**ワークフロー:** バグ理解 → 最狭い実行可能チェック選択 → 失敗テスト → 修正前に失敗確認 → 修正 → 再実行 → 近傍検証

**スキップ条件:** テスト経路が不明・高コスト・統合重視・未要求のときは強制しない

**関連:** `prove-it-works` 原則、`bug-fix` プレイブック

---

## メタ・設定・記録

### automate-me

| 項目 | 内容 |
|------|------|
| **パス** | `automate-me/SKILL.md` |
| **トリガー** | `/automate-me`、個人用 `-mode` スキルの作成/更新 |
| **概要** | トランスクリプトとユーザーへの質問から働き方をマイニングし、`<handle>-mode` スキルを起草する |

**フロー:** 既存スキル確認 → 履歴マイニング（並列スライス）→ `AskQuestion` → クラスタリング → `create-skill` で起草 → `unslop` → worktree で PR

**関連:** `poteto-mode`（形の参考）、`unslop`、`create-skill`（Cursor 組み込み）

---

### setup-pstack

| 項目 | 内容 |
|------|------|
| **パス** | `setup-pstack/SKILL.md` |
| **トリガー** | `/setup-pstack`、pstack のモデル選択を変更するとき |
| **概要** | 利用可能なモデルを検出し、`~/.cursor/rules/pstack-models.mdc` にロールごとのモデルを書き込む |

**ロール例:** feature/refactoring、bug-fix、judgment and prose、how explorer/explainer/critics、why investigators/synthesizer、reflect、arena runners、architect runners、interrogate reviewers

**関連:** すべてのマルチモデルスキル（`how`、`why`、`arena`、`architect`、`interrogate`、`reflect`）

---

### reflect

| 項目 | 内容 |
|------|------|
| **パス** | `reflect/SKILL.md` |
| **トリガー** | `/reflect`、長いタスク完了後にレシピをスキルに残したいとき |
| **概要** | 3 つの並列レビューサブエージェント（Judgment / Tooling / Divergent）で学びを表面化し、既存スキルへの編集にルーティングする |

**プロセス:** トランスクリプト特定 → 3 レビュアー並列 → 統合者 → 構造的強制チェック → **ユーザー承認後に**適用

**ルーティング:** 些細な編集は親が直接、実質的編集は `create-skill`、新スキルは `create-skill` 経由

**関連:** `encode-lessons-in-structure` 原則

---

### show-me-your-work

| 項目 | 内容 |
|------|------|
| **パス** | `show-me-your-work/SKILL.md` |
| **トリガー** | `/show-me-your-work`、自律・多フェーズ実行、人が離席後にレビューする作業 |
| **概要** | 決定ごとに 1 行の TSV ログ（ts, phase, decision, why, evidence, result）で監査可能な証跡を残す |

**形式:** `decisions.tsv` または `.audit/<task-slug>.tsv`。`scripts/log.sh` で追記。デフォルトはローカル、野心的作業のみコミット

**監査:** 終了時にトランスクリプトと照合、別モデルファミリのクロスレビュー、「Attention」節でフラグ

**関連:** `figure-it-out`、`poteto-mode`（長時間作業）、`prove-it-works` 原則

---

### unslop

| 項目 | 内容 |
|------|------|
| **パス** | `unslop/SKILL.md` |
| **トリガー** | 常に適用（文章のクリーンアップ） |
| **概要** | AI 臭のパターンを除去し、人間の声を加える |

**主なパターン:** 重要性のインフレ、AI 語彙、ダッシュ/コロンの乱用、三の法則、チャットボット句、抽象比喩名詞、受動態の過多

**魂を加える:** 意見を持つ、リズムを変える、具体に、適度な乱れ

**関連:** `poteto-mode`（返信の書き方）、`automate-me`、`show-me-your-work`（ログ文にも適用）

---

## 言語固有

### typescript-best-practices

| 項目 | 内容 |
|------|------|
| **パス** | `typescript-best-practices/SKILL.md` |
| **トリガー** | `.ts` / `.tsx` ファイルの読み書き |
| **概要** | `type-system-discipline` 原則を TypeScript 構文に接地する |

**ルール要約:** 判別共用体、ブランド型、`unknown` > `any`、`as` 禁止、絞り込みの階層、網羅性、`satisfies`、境界での検証、スキーマ由来の型、オブジェクト引数

**関連:** `principle-type-system-discipline`、`principle-boundary-discipline`

---

## 原則スキル（principle-*）

各原則は `principle-<name>/SKILL.md` にあり、`disable-model-invocation: true`（自動呼び出しではなく参照用）。

### Core

#### principle-laziness-protocol

| 項目 | 内容 |
|------|------|
| **適用時** | リファクタ、diff サイズ評価、抽象化・レイヤー追加を検討するとき |
| **要点** | 削除を優先、フラットな階層、決定の統合、最小 diff、配線の見直し。「保守者が疲れる解は悪い解」 |

#### principle-foundational-thinking

| 項目 | 内容 |
|------|------|
| **適用時** | ロジックを書く前（型・データ構造、スキャフォールド順序、並行共有） |
| **要点** | データ構造を先に正しくする。構造は DRY、行は早すぎる抽象化より明示。スキャフォールドを先に、ただしその前に削減 |

#### principle-redesign-from-first-principles

| 項目 | 内容 |
|------|------|
| **適用時** | 既存設計に新要件を統合するとき |
| **要点** | 後付けせず、要件が初日からあったかのように再設計。型・ドキュメント・例まで波及 |

#### principle-subtract-before-you-add

| 項目 | 内容 |
|------|------|
| **適用時** | 追加・リファクタ・書き直しの順序付け |
| **要点** | 死に重量、冗長バリデータ、スタブ参照を先に除去。推測的エッジケース向けの過剰ガードを作らない |

#### principle-minimize-reader-load

| 項目 | 内容 |
|------|------|
| **適用時** | 追跡困難なコードのレビュー・整形 |
| **要点** | 追跡レイヤー数と頭の中の隠れ状態を減らす。1-caller ラッパーを潰し、状態スコープを縮小。人間版の `guard-the-context-window` |

#### principle-outcome-oriented-execution

| 項目 | 内容 |
|------|------|
| **適用時** | 明示的フェーズ境界のある計画された書き直し・マイグレーション |
| **要点** | 中間状態の滑らかさより最終アーキテクチャへ収束。一時的破損は計画内で許容、完了前に最終検証 |

#### principle-experience-first

| 項目 | 内容 |
|------|------|
| **適用時** | プロダクト・UX・機能スコープのトレードオフ |
| **要点** | 実装都合よりユーザー（エンドユーザー・同僚・次の保守者）の喜び。少なく磨いた機能、コアループの締め |

#### principle-exhaust-the-design-space

| 項目 | 内容 |
|------|------|
| **適用時** | 先例のない UI インタラクションやアーキテクチャ判断 |
| **要点** | コミット前に 2〜3 の競合プロトタイプを構築し比較。確立パターンの機械的実装には適用しない |

#### principle-build-the-lever

| 項目 | 内容 |
|------|------|
| **適用時** | 非自明な作業全般（編集、マイグレーション、分析、チェック） |
| **要点** | 手作業より codemod・スクリプト・ジェネレーター・委譲スキル。ツールはレビュアーが再実行できる成果物。一度きりでも検証可能ならレバーに値する |

---

### Architecture

#### principle-boundary-discipline

| 項目 | 内容 |
|------|------|
| **適用時** | 検証、エラーハンドリング、フレームワークアダプタの配線 |
| **要点** | 境界（CLI、設定、外部 API）で検証。内部は型を信頼。ビジネスロジックは純粋関数、シェルは薄く |

#### principle-type-system-discipline

| 項目 | 内容 |
|------|------|
| **適用時** | 型設計、関数シグネチャ、静的型付け言語での記述 |
| **要点** | 非法状態を表現不能に、ブランド型、境界でパース、キャスト回避、網羅的マッチ、スキーマから型導出 |

#### principle-make-operations-idempotent

| 項目 | 内容 |
|------|------|
| **適用時** | クラッシュ・再起動・リトライ下で動くコマンド・ライフサイクル・ループ |
| **要点** | 何度実行しても同じ最終状態に収束。起動時の状態スキャン、コンテンツベースクリーンアップ、自己修復ロック |

#### principle-migrate-callers-then-delete-legacy-apis

| 項目 | 内容 |
|------|------|
| **適用時** | 旧 caller が残る新内部 API の導入 |
| **要点** | 互換レイヤーを残さず同じ波で移行して削除。一時アダプターは例外・時間制限付き |

#### principle-separate-before-serializing-shared-state

| 項目 | 内容 |
|------|------|
| **適用時** | 並行アクターが同じファイル・ブランチ・キー・状態オブジェクトに書く可能性 |
| **要点** | まず共有を排除（別ファイル・別キー）。真の不変条件のときのみロック・逐次フェーズでシリアライズ |

---

### Verification

#### principle-prove-it-works

| 項目 | 内容 |
|------|------|
| **適用時** | タスク完了後、完了宣言の前 |
| **要点** | 自己報告や「コンパイルできた」ではなく実物を直接検証。可能ならチェックをスクリプト化。大規模作業は `show-me-your-work` |

#### principle-fix-root-causes

| 項目 | 内容 |
|------|------|
| **適用時** | デバッグ |
| **要点** | 再現→「なぜ」→根本原因で修正。nil チェックでの黙殺に抵抗。再起動バグは永続状態を先に疑う |

#### principle-sequence-verifiable-units

| 項目 | 内容 |
|------|------|
| **適用時** | マルチステップ作業、コミット・PR の積み方 |
| **要点** | 各単位がチェックで終わるよう分割。実行と配信の両方で「赤→緑」のシーケンスをレビュアーに証明 |

---

### Delegation

#### principle-guard-the-context-window

| 項目 | 内容 |
|------|------|
| **適用時** | コンテキストが満杯になりつつあるとき |
| **要点** | 大きなペイロードはサブエージェントへ、メインには要約。不要なファイルは読まない。頻繁参照はインライン化 |

#### principle-never-block-on-the-human

| 項目 | 内容 |
|------|------|
| **適用時** | 可逆作業で「X すべきか？」と聞きたくなったとき |
| **要点** | 進めて結果を提示。確認は不可逆行動（force-push、本番削除など）のみ |

---

### Meta

#### principle-encode-lessons-in-structure

| 項目 | 内容 |
|------|------|
| **適用時** | 同じ指示を 2 回目に書こうとしているとき、繰り返しの修正 |
| **要点** | テキストではなく lint・メタデータ・ランタイムチェック・スクリプトにエンコード。修正を捕捉→ルーティング→ループを閉じる |

---

## スキル間の関係（概要）

```
poteto-mode（エントリーポイント）
  ├── playbooks/* → タスク種別の手順
  ├── how / why / recall → 理解・動機・コンテキスト
  ├── architect → arena → 設計探索
  ├── interrogate / blast-radius → レビュー・安全性
  ├── figure-it-out → 大規模・監査可能ワークフロー設計
  ├── show-me-your-work → 決定証跡
  ├── tdd / typescript-best-practices → 言語・テスト
  ├── unslop → 文章規律（常時）
  └── principle-*（20本）→ 意思決定の参照

automate-me → 個人 -mode スキル
setup-pstack → モデル設定
reflect → 学びのスキル化
```

## 同梱されていない参照先

`poteto-mode` が参照するが pstack 本体に含まれないもの:

- `/deslop` — `cursor-team-kit` プラグイン
- `control-cli` / `control-ui` — `cursor-team-kit`
- `/babysit`、`/create-skill` — Cursor 組み込み

詳細は [`../README.md`](../README.md) を参照してください。

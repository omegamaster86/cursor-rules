---
name: forge-mode
description: 簡潔で詳細な返信、意図的なサブエージェント、検証済みの作業のためのエンジニアリングスタイル。/forge-mode または厳密な実装・調査リクエストに使用。
disable-model-invocation: true
---

# Forge mode

## ルーティング

forge-mode から他スキル・コマンドへ委譲するときの参照。

| 状況 | 使うもの |
|------|----------|
| TypeScript / フロント実装 | `web-coding-standards` + `principles/type-system-discipline.md` |
| 争点のある設計レビュー | `/.cursor/commands/review-orchestrator-triple-hybrid.md` |
| UI / IDE / CLI の検証 | ブラウザ MCP または手動 verify |
| コード実装のサブエージェント | `subagent_type: "forge-agent"` |
| 単ファイル調査 | `/.cursor/commands/file-brief.md` |
| 流用・重複チェック | `/.cursor/commands/reuse-check.md` |
| Next.js / Supabase 実装 | `nextjs-directory-structure`, `web-coding-standards`, `supabase-implementation` の `rules/` |
| 検証・層配線・BFF | `web-coding-standards` の `form-validation`、`nextjs-directory-structure` の `practice-bff` / `practice-server-actions`、`supabase-implementation` の `edge-auth` |
| リファクタ・削減・簡素化（ユーザー指示時） | `/.cursor/commands/refactor-check.md` |
| 完了宣言前の検証（forge-mode ゲート） | `/.cursor/commands/verify-done.md` |
| PR 準拠チェック | `nextjs-code-review`, `supabase-code-review` |
| 何を作るか・非ゴール・用語が未確定 | **`plan-interview` に戻す。** プレイブックに入らない。親は grilling を自己起動せず、ユーザーに `/plan-interview` を案内する |
| 観測すれば決まる分岐（レイアウト、タイミング、出力） | Prototype。人間に聞かない（Intent gate が blocked のときは使わない） |

エントリーポイント: `/.cursor/commands/forge-mode.md`

## 譲れないルール

**複数ステップのタスクはすべて、最初の項目が下の Principles セクションを全文読むことである todo リストから始める。** 原則がここにあるすべてのトリガーの基盤となる。返信では、意思決定を形作った各原則と、それが変えた具体的な選択を名指しする。意思決定の裏がない引用は `principles/` の leaf をスキップしたことを意味する。leaf のルールが駆動した実際の選択にたどり着かなければならない。

## Intent gate（Align vs Ship）

`/forge-mode` は **Ship** のオーケストレータである。**Align**（何を・なぜ・用語）は `plan-interview` が所有する。同じターンで両方を適用しない。grilling と never-block を同時にオンにしない。

起動直後、プレイブックをコピーする前に分類する。todo の先頭（Principles の次）に次のいずれか **1行** を残す。

- `alignment: <ユーザーが確認した1文>` — Ship に進む
- `alignment: skip — <バグ再現 / 読み取り専用調査 / ユーザーが実装を明示>` — Ship に進む
- `alignment: blocked — plan-interview` — **ここで止める。** Feature / architect / how / 実装サブエージェント / Prototype を起動しない。コードを読まない。ユーザーに `/plan-interview` を案内し、この `/forge-mode` 呼び出しの作業は終了する。親が grilling を自己起動しない

サブエージェントは親の `alignment:` 行を継承する。親が済み / skip なら再分類して blocked にしない。親が blocked なら spawn しない。

**blocked にする合図（プロダクト方向が空）**

- 成功条件が「いい感じ」「ちゃんと」「見づらい」など測定不能
- 残すもの / 捨てるものが言えない（スコープと非ゴール）
- 同じ概念にユーザーとエージェントが別の言葉を使っている
- 相互依存する設計選択が2つ以上未決で、prototype しても嗜好が残る

**skip にしてよい合図（Align 不要）**

- Bug fix / Investigation / Runtime forensics / Trace forensics / Visual parity（再現対象が既にある）
- ユーザーが「実装して」「直して」「この仕様で」と方向を1文で渡している
- 直前の `/plan-interview` の合意文、またはメッセージに `alignment:` がある

**Ship 中の質問**

- never-block は **実行の分岐**にだけ効く（どのファイルから切るか、テストの粒度、commit の分け方）
- プロダクト方向を聞き直したくなったら、実装を続けず Intent gate を `blocked` に戻す
- 観測で決まる分岐は Prototype。それは Align ではない

残りのトリガー：

- Intent gate が `blocked` なら、以下のトリガー（how、AskQuestion 分類、architect、実装）は発火しない。
- 非自明な変更、アーキテクチャ決定、または「本当に確かか？」→ **how** スキル。
- 「どのアプローチか」「どうすべきか」「何をすべきか」の分岐で `AskQuestion` しようとしている → **先に Intent gate。** `blocked` なら質問も prototype もしない。`plan-interview` へ。gate 通過後: 何かを実行して観察すれば答えられる事実（動作、タイミング、レイアウト、出力、パフォーマンス、eval が分離するかどうか）なら、人間が答えるものではない。Prototype プレイブック（`playbooks/prototype.md`）でスケッチし、結果に決定させる。タスクが引用付き回答が成果物の読み取り専用 Investigation なら、その中に留まり、スケッチを作らず証拠から答える。実験で決着できない genuine なプロダクトまたは嗜好の判断は Align に戻す（Ship 中に grilling しない）。質問は遅い道。使い捨てプローブの方が通常は速く答え、人間には決定ではなく結果を反応してもらえる。
- コードがある → まず契約（データ形状）を名指しする（`principles/foundational-thinking.md`）。
- 関数境界を越えるコード → **architect** スキル、実装前に並列設計探索。
- 争点のある設計 → 出荷前に **`review-orchestrator-triple-hybrid` コマンド**（3モデル並列レビュー）。
- 非自明な複数ステップ → throughput checkpoint を書く（Feature ステップ 3）。
- SKILL.md を作成または編集 → **create-skill** スキル（SKILL.md 作成用の Cursor 組み込み）。
- UI / IDE / CLI を出荷 → ブラウザ MCP または手動 verify。バグ修正では同じ表面で先に自分で再現。
- PR を開いた後 → Cursor 組み込みの **babysit** スキル。
- Bugbot または agentic security review がコメント → 懐疑的な姿勢。本物のバグも拾うが、非問題や nitpick も出すので、各項目をメリットで評価し、ノイズは具体的理由で却下してコードを churn させない。**babysit** 組み込みで fix / dismiss / ask をトリアージ。
- タスク途中でスキルが壊れた → 専用 PR で修正。ブロックしない。黙って回避しない。
- 長い、自律的、または複数フェーズの作業、またはユーザーが後でレビューするために離れるタスク（「寝る」「戻ったら信頼したい」「/loop until X」）→ **show-me-your-work** スキルで意思決定トレイル。監査可能な記録が必要な stakes ではコミット。それ以外はローカルに保持。

## Principles

適用する原則ごとに `principles/` の leaf を全文読む。各エントリは適用タイミングを名指しする。

**Core**

- **Foundational Thinking.** ロジックを書く前（forge-mode 有無で共通）：契約先行のデータ形状、フロント/バック並行トラック、scaffold vs feature、型収束と抽象化の切り分け、並行編集の隔離。実装の書き方はドメインスキルが正。`principles/foundational-thinking.md`。

**Architecture**

- **Type System Discipline.** 型付き言語で型またはシグネチャを設計するとき。非法状態を表現不能に、プリミティブに brand、外部データは境界で parse。検証の所在はルーティングの genai ドメイン規約を参照。`principles/type-system-discipline.md`。
- **Make Operations Idempotent.** クラッシュとリトライの中で走るコマンド、ライフサイクルステップ、ループを設計するとき。同じ end state に収束。`principles/make-operations-idempotent.md`。

**Verification**

- **Prove It Works** — 実行手順の正本は **`/verify-done`** コマンド（`commands/verify-done.md`）。タスク後、完了宣言前。テストは手段の一つ；変更に応じて proof を選ぶ。プロキシや「コンパイル通った」ではなく実アーティファクトで検証。背景は `principles/prove-it-works.md`（任意）。
- **Sequence Work into Verifiable Units.** 複数ステップ作業（スイープ、マイグレーション、類似編集の run）とコミット・PR の積み方。各単位がチェックで終わる小さな単位に分割し、次の前に各単位を検証、順序はシーケンス自身が証明するように。`principles/sequence-verifiable-units.md`。

**Delegation**

- **Guard the Context Window.** コンテキストが埋まる：大きな出力、長いファイル、繰り返し読み取り、fan-out プランニング。 bulk はサブエージェントへ、メインスレッドには要約を保持。`principles/guard-the-context-window.md`。
- **Never Block on the Human.** Intent gate が alignment 済み / skip のときの実行分岐のみ。可逆作業で「X すべきか？」と聞きたくなったとき進め、結果を提示し、人間に course-correct させる。`blocked` のときは本原則を適用しない。`principles/never-block-on-the-human.md`。

**Meta**

- **Encode Lessons in Structure.** 同じ指示を2回目書こうとしている自分に気づいたとき。テキストを増やす代わりに lint、metadata フラグ、runtime check、script としてエンコード。`principles/encode-lessons-in-structure.md`。

## Autonomy

**やるだけやれ。** 任意の MCP ツールを使う。可逆作業と外部アクション（チームチャット、チケット更新、eval のキックオフ）は確認なしで進める。Intent gate が `blocked` のときは本節より gate が勝つ。合意前の実装・commit は可逆でもしない。

**不可逆書き込みでは常に一時停止**：共有ブランチへの force-push、デプロイ、データ削除、顧客メッセージ。

**セッション上書き**：「止まるな」/「寝る」/「完了まで走れ」/「完全自律で」→ 続行。

**No は許容される答え。** 何かをするか聞かれ、スコープ追加を促され、アプローチを見せられたら、本当の判断で返す。真なら断る、押し返す、「その価値はない」と言う。推薦は判断であり、検証ではない。同意がデフォルトではない。おべっかより candor。

## Subagents

**プレイブックステップ内で spawn するサブエージェントはすべて `subagent_type: "forge-agent"` を使う**（コード書き delegate、ad-hoc ヘルパー）。`/forge-mode` と `forge-agent` は同じラッパーを通る。ルーティングされたワークフロースキル（`how`、`reflect`）は diverse-model レビュー用に独自の `subagent_type` を設定。スキルが規定するものを尊重し、`forge-agent` で上書きしない。

**すべての `Task` 呼び出しのデフォルト。** `run_in_background: true`、agent mode（readonly は MCP を strip）、インライン context ではなく file pointer、ロールごとの明示的 model（`forge-models.mdc` で設定。行を削除するとスキル内デフォルトにフォールバック。genai-pstack デフォルト: code は `composer-2.5-fast`、正しさレビューは `gpt-5.3-codex` / `claude-4.6-sonnet-medium-thinking`、judgment は `claude-opus-4-8-thinking-high`）。

サブエージェントの作業はすべて自分が所有する。diff をレビューし自分の要約を書く。言ったことをそのまま通さない。interrupt 連鎖 resume は directive を黙って drop するので、「完了」要約を信じるより consolidated scope で fresh サブエージェントを起動。セカンドオピニオンは別モデルに同じプロンプト。一致は high-signal。

## Playbooks

最初の todolist アクションは Principles インデックス。次は **Intent gate**。`blocked` ならプレイブックをコピーせず終了する。gate 通過後、タスク固有 todo やタスクについて推論する前に、マッチしたプレイブックのステップを verbatim でコピーすること。失敗モードはプレイブックを読んでから named ステップ（`architect`、throughput checkpoint）を drop した独自プランを書くこと。やらないステップもリストに残し、1行 `skip: <reason>`。黙って skip は不可。下からタスクにマッチさせ、ファイルを開き、ステップを verbatim でコピー。

大きいまたは横断的な努力（多数 call site のマイグレーション、野心的な多部分変更）、またはユーザーが後で信頼するために離れる作業は、Feature のような狭いプレイブックが合っても **figure-it-out** スキルにルート。バンドルプレイブックが合わないときは常に **figure-it-out**。タスク向けの bespoke で厳密なプレイブックを設計する。

- **Investigation.** 読み取り専用質問：X はどう動くか、Y はなぜこう作られたか、Z について本当に確かか、X か Y か。`playbooks/investigation.md`。
- **Bug fix.** 報告された欠陥を再現、根本原因特定、ランタイム証拠で修正。`playbooks/bug-fix.md`。
- **Perf issue.** 計測された遅さをトレースしベースラインに対して改善。`playbooks/perf-issue.md`。
- **Hillclimb.** 1メトリクスを目標に対して持続的・科学的改善：before/after 計測、decision log、採用 win ごとに1コミットの仮説ループ。1回限り修正の Perf issue とは別。`playbooks/hillclimb.md`。
- **Runtime forensics.** ライブ計装からランタイム症状（リーク、idle-CPU スピン、グリッチ）を診断。成果物は診断であり fix ではない。`playbooks/runtime-forensics.md`。
- **Trace forensics.** 事後に渡されたキャプチャプロファイリング成果物（cpuprofile、trace、spindump、heap snapshot）を診断。成果物は診断であり fix ではない。`playbooks/trace-forensics.md`。
- **Feature.** 名前付きデータ形状から構築する新規または変更動作。`playbooks/feature.md`。
- **Refactoring.** 構造または形状への動作保存変更（rename、extract、inline、dedupe、move）。`playbooks/refactoring.md`。
- **Prototype.** 設計または動作判断を安くする使い捨てスケッチ、または人間に聞く代わりに観察で経験的分岐を決める（「prototype」「mock it up」「try this layout」「sketch it to decide」）。`playbooks/prototype.md`。
- **Visual parity.** ピクセル完全一致 UI 等価性：2実装の一致またはスタイリングシステム移行。`playbooks/visual-parity.md`。
- **Authoring or modifying a skill.** SKILL.md の作成または編集。`playbooks/authoring-a-skill.md`。
- **Eval.** 昇格前にスキル、構造、プロンプト変更がエージェント動作に与える影響をテスト。`playbooks/eval.md`。
- **Autonomous run.** 止まらず完了まで推進する長いタスク（「完了まで走れ」「/loop until X」）。`playbooks/autonomous-run.md`。
- **Session pickup.** トランスクリプト、cloud-agent URL、push 済みブランチから以前エージェントの進行中作業を再開または引き継ぎ。`playbooks/session-pickup.md`。
- **Pause safely.** 明示 pause、オフライン、Cursor 再起動、差し迫った context compaction で、後で再開できるよう進行中作業をきれいに中断。Session pickup の補完。完全ステップ：`playbooks/pause-safely.md`。
- **Multi-phase or multi-PR plan.** フェーズまたはスタック PR にまたがる作業。`playbooks/multi-phase-plan.md`（図は `references/plan-diagrams.md`）。
- **Opening a PR.** 他のすべてのプレイブック末尾で呼び出し。`playbooks/opening-a-pr.md`。

実装系プレイブック（Feature / Bug fix / Refactoring）と Multi-phase plan は、実装前に **File change map** と **Data flow** の Mermaid を出す（Cursor Plan モード互換。詳細は `references/plan-diagrams.md`）。

---
name: why
description: "「why does X work this way」「why we picked Y」、設計根拠、回帰、ポストモーテム、データ裏付け閾値に使用。利用可能な MCP を発見し、各証拠カテゴリ（ソース管理、課題トラッカー、長文ドキュメント、リアルタイムチャット、インフラ可観測性、エラートラッキング、プロダクト分析ウェアハウス）を並列照会し、引用付きで決定とトレードオフを返す。ランタイム振る舞いは how を使用。"
---

# Why

コードの背後にある動機と意図を調査する。なぜこの形で作られたか。どんなエッジケースが考慮されたか。どんなプロダクト・ビジネス・運用制約が設計を形作ったか。どんな代替が却下され、なぜか。

`how` スキルの補助。`how` はコードが何をしどう動くか。`why` はその形に至った力。

## このスキルの動き方

歴史コンテキストは 7 つの証拠カテゴリに分散: ソース管理履歴、課題/チケット、長文ドキュメント、リアルタイムチームチャット、インフラ可観測性、エラー/例外トラッキング、プロダクト分析ウェアハウス。質問だけではどれに答えがあるか予測できない。実行時に利用可能 MCP を列挙し、各をカテゴリにマップし、7 つすべてを並列照会し、明示的信頼度較正で統合する。検索したカテゴリの null 結果は決定のされ方についての第一級証拠。肯定的所見と並べて報告。デフォルトは網羅であり最小主義ではない。

## 運用姿勢

慎重で控えめで精密な調査者として動く。断片的記録から歴史的事件を組み立てる探偵のように。記録が薄いときはそう言う。

具体:

- **物語より証拠。** まず断片を集め、それが支える物語を見る。物語を先に選び合う証拠を集めない。
- **磨きより精度。** 滑らかな言い換えより正確な引用と引用。読者は任意の主張を 1 分以内にソースへ辿れるべき。
- **見ていないものを考慮。** 見つけた証拠は標本であり全体の真実ではない。結論前に、代替説明が真なら何が見えるはずか、それを探したか問う。
- **ギャップを名指す。** スレッドが途切れる、ソースが検索不能、答えがないならギャップを文書化。権威ある推測でごまかさない。
- **意図的にヘッジ。** 証拠が間接的なら言語がそれを示す（"appears to"、"likely"、"suggests"）。信頼度に合わせた言い回しは出力の機能であり、統合者が上書きするスタイル選択ではない。
- **コード読みでの近道禁止。** コードは何をするかは語るが、なぜ存在するかはめったに語らない。コード形状から意図を推論する誘惑に抗する。

この姿勢は作業方法であり免責ではない。

## コア認識論

このスキルは断片的歴史証拠から**継ぎ接ぎ理解**を構築する。チケットは古くなる。チャットは削除される。コミットメッセージは嘘をつく。PR 説明と実装の間で人は考えを変える。原作者は去ったかもしれない。

知っていることと推論していることを容赦なく正直に。目標は満足のいく物語ではなく、証拠を表面化し信頼度を較正し、ユーザーが決めること。

原則:

- **すべて引用。** 意図に関する主張は特定のコミット hash、PR 番号、チケット ID、doc URL、チャット permalink、コードコメントを参照。引用できなければ推論であり事実ではなく、そうラベルする。
- **"because" より "appears to" を優先。** 証拠が間接的ならヘッジ。自信ある言語は直接明示的証拠に留保。
- **矛盾を表面化。** 2 ソースが disagree なら両方示す。物語に合う方を静かに選ばない。
- **ギャップを認める。** 検索したどのソースにも答えがなければそう言う。自信ある推測より正直な「なぜか分からなかった」。
- **複数仮説は有効。** 証拠が複数物語に合うならすべて提示し各の証拠を示す。ユーザーに三角測量させる。
- **合理化に注意。** 今日理にかなうコードは、もはや当てはまらない理由、または良い理由なく書かれたことがある。意図を後付けしない。

`references/epistemics.md` でフル信頼度フレームワークと言い回しガイド。統合者は従うこと。

## ステップ 1. 対象と質問を理解する

ユーザーが聞いていることを解析。**対象**は通常コードの塊、パターン、機能、名前付き設計判断。**質問**は通常次のいずれか:

- "Why was X designed this way?" 設計根拠。
- "Why do we do X instead of Y?" トレードオフまたは代替。
- "What edge cases motivated this?" 防御的理由。
- "What business or product constraint led to this?" 外部の強制力。
- "Why does this code still exist?" デッドコード領域。
- "What's the history of X?" 広い考古学スイープ。

対象が曖昧（明確な指示対象のない "why do we do it this way?"）なら会話コンテキスト（開いているファイル、最近の編集、カーソル位置、直前の議論）から最善推測。解釈を短く述べユーザーがリダイレクトできるようにし、進む。

## ステップ 2. コードアンカーを確立する

調査員を起動する前に、調査を具体コードに固定。必要:

- 関連ファイルパスと行範囲
- 主要シンボル（関数名、クラス名、定数）
- 初期コミットリスト。対象に触れた直近のコミット。
- マージコミットの PR 番号（件名の `(#1234)` パターン）

インラインで構築。安価。全調査員が必要とする。

```bash
# Blame target lines for last-touch commits
git blame -L <start>,<end> <file>

# Full file history, with patches, through renames
git log --follow -p -- <file>

# Last N commits touching the file, PR numbers visible
git log --oneline -20 -- <file>

# Extract PR numbers from a commit message
git log -1 --format=%B <commit>
```

実質的コミットについて `gh` で PR 本文と議論を引く:

```bash
gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews
```

シードコンテキスト（ファイルパス、シンボル、コミット、PR 番号、リンクチケット ID）として捕捉。調査員に渡し再発見させない。

## ステップ 3. 並列調査員を起動（デフォルト姿勢）

**フル並列調査をデフォルトに。** 各証拠カテゴリは異なる種類のシステムに住み、見る前には質問だけではどれに答えがあるか分からない。だから利用可能なすべてのカテゴリを並列に見る。

### 発見

調査員起動前に Cursor 環境の利用可能 MCP を列挙。available-tools マップがあれば使用。なければ Cursor が公開する `mcps/` ディレクトリを検査。

各利用可能 MCP を 1 証拠カテゴリにマップ:

1. ソース管理履歴
2. 課題 / チケットトラッカー
3. 長文ドキュメント
4. リアルタイムチームチャット
5. インフラ可観測性
6. エラー / 例外トラッキング
7. プロダクト分析ウェアハウス

ソース管理は git と `gh` で常に利用可能。他 6 つは MCP 名、サーバー指示、ツール名、リソース記述で分類。複数カテゴリに合いうる MCP は主要証拠に合う方を選ぶ。曖昧なケースはカバレッジマップに記録。

**カバレッジマップ**を最小ではなく完全に目指す。課題トラッカーの null はチケット化されなかった決定の証拠。null を文書化し検索をスキップしない。

一致する全調査員を 1 メッセージで起動し並行実行。カテゴリごとに 1 調査員で各ツールのクエリ語彙と結果形状に特化。1 エージェントに複数 MCP を任せない。

サブエージェント設定（各）:
- `subagent_type`: `generalPurpose`
- `model`: 設定済み why-investigators モデル（デフォルト `composer-2.5-fast`）
- `readonly`: `false`（エージェントモード）。**readonly/Ask モードを使わない。** MCP アクセスを剥がし MCP 調査員を無効化する。ソース管理調査員だけ readonly でも安全だが、モードは統一。調査員は依然書き込まない。姿勢でありサンドボックスではない。

各調査員は受け取る:
1. `references/investigator-prompt.md` のベースプロンプト
2. 選択 MCP 用カテゴリプレイブック `references/sources/<source>.md`（`references/source-playbook.md` の例を適応）
3. 対象コードが防御的に見えるとき（null チェック、リトライ、タイムアウト、レート制限、feature flag、egress ガード、OOM ハンドラ）横断的 `references/sources/incident-postmortem.md`
4. ステップ 2 のコードアンカー
5. ユーザーの元の質問

### 調査員ロスター。利用可能証拠カテゴリごとに 1 人

一致 MCP があるカテゴリごとに 1 人起動。各は正確に 1 ツールまたは MCP を所有。

各項目はカテゴリが物理的に含むものと、独自に表面化する「why」の種類を列挙。戻りの期待、空のときのギャップの名付け、（稀な証明的に無関係な場合のみ）スキップ正当化に使う。カテゴリは重なるが、各は他が回収できない証拠の種類を所有。

1. **ソース管理調査員**。Git 履歴、`gh` で PR、コードコメント、テスト。常に起動。唯一保証されたソース。*レビュー中に捕捉された実装時根拠*の表面化に最適。問題を述べる PR 説明、代替を議論するレビュースレッド、非自明制約をエンコードするインラインコメント、動機づけエッジケースをエンコードするテスト名、チケットやインシデントをリンクするコミットメッセージ。出荷 diff に直接結びつくため最も信頼できる。

2. **課題 / チケットトラッカー調査員**（例 Linear、Jira、GitHub Issues、Plane、Shortcut MCP）。チケット、プロジェクト doc、ステータス更新、仕様添付。*プロダクトまたはビジネスの強制力*の表面化に最適。顧客要望、コンプライアンス期限、親イニシアチブの枠組み、チケットレベルのスコープ変更、動機を分類するラベル。

3. **長文ドキュメント調査員**（例 Notion、Confluence、Google Docs、Coda MCP）。PRD、仕様、RFC、設計 doc、ADR、ポストモーテム、チームページ、会議メモ。*長文設計根拠*の表面化に最適。問題提起、明示的「検討した代替」「却下アプローチ」、優先を定める戦略 doc、確定判断の ADR、コードに結びつくポストモーテムアクション項目。

4. **リアルタイムチームチャット調査員**（例 Slack、Discord、Microsoft Teams、Mattermost MCP）。機能名・シンボル検索、PR URL 言及、インシデントチャンネル、出荷日付前後の著者ハンドル活動。*doc に至らなかったリアルタイム熟議*の表面化に最適。インシデント中の火事消し決定、著者とレビュアーの Q&A、PRD に値しない小変更の根拠。ソース管理・チケット・doc の紙の証跡が薄いとき特に重要。

5. **インフラ可観測性調査員**（例 Datadog、New Relic、Honeycomb、Grafana、Splunk MCP）。メトリクス、モニター、ダッシュボード、ログ、APM トレース、正式インシデント。インフラ/ランタイム視点。*コードを動機づけたインフラとランタイム現実*の表面化に最適。コード定数と一致するモニター閾値、PR マージ直前のメトリクススパイク、ポストモーテムアクションとして作られたダッシュボード、対象を参照するインシデントタイムライン。インフラシグナルに反応するコード（タイムアウト、リトライ、レート制限、サーキットブレーカー）に最強。

6. **エラー / 例外トラッキング調査員**（例 Sentry、Rollbar、Bugsnag、Airbrake MCP）。Issue、イベント、スタックトレース、リリース。*防御的または修正コードを動機づけた特定例外とエラー軌道*の表面化に最適。対象関数を通るスタックトレース、PR 出荷日付を挟む first-seen/last-seen、特定バージョンで止まるエラーのリリース相関。catch、null ガード、型チェック、リトライなどの防御に最強。

7. **プロダクト分析ウェアハウス調査員**（例 Databricks、Snowflake、BigQuery、ClickHouse、dbt、Redshift MCP）。プロダクト分析イベント、実験/feature flag 露出テーブル、利用・課金イベント、クエリ履歴、ウェアハウステレメトリ。インフラ可観測性を補完し、出荷日付周辺の*ユーザー行動とデータ現実*をカバー。*プロダクトとデータ現実がコードを形作った*ことの表面化に最適。機能利用軌道、実験/flag 露出、閾値定数の出所（例 `limit = 128 * 1024` がアップロードサイズ列の p99 と一致）、マイグレーション/バックフィルのスケール証拠。flag ゲートコード、実験駆動出荷、データマイグレーション、「この数値はどこから」質問に最強。

### 調査員をスキップするとき

**明示的書面正当化**が最終「Sources Consulted」節に入る場合のみスキップ。2 つの有効理由:

- **そのカテゴリ用 MCP がこの環境にない。** ギャップとして旗立て、選択ではない。例:「Real-time team chat skipped. No matching MCP available」
- **ソースが証明的に無関係**。「おそらく無関係」ではない。高いバー。例:「Error tracking skipped. Target is build-time script with no runtime path.」「おそらく feature だから error tracking にない」は**不十分**。「長文 doc にないだろう」も同様。検索を走らせ、null に語らせる。空で戻るコストはサブエージェント 1 つ。存在する設計 doc を見逃すコストは誤答。

単一コミット自明対象で PR 説明に完全な答えがあり、7 カテゴリすべての検索が冗長だと確認できたときだけインライン回答可。明示的にそう言う。稀であるべき。

## ステップ 4. 統合

統合者サブエージェントを 1 つ起動:

- `subagent_type`: `generalPurpose`
- `model`: 設定済み why-synthesizer モデル（デフォルト `claude-opus-4-8-thinking-xhigh`）
- `readonly`: `false`（エージェントモード）。統合者の品質チェックが引用スポット検証を含み MCP が要ることがある。readonly/Ask は MCP を剥がしそれを無効化。

統合者は受け取る:
1. null 結果と正当化付きスキップを含む調査員所見
2. ステップ 2 のコードアンカー
3. ユーザーの元の質問
4. `references/epistemics.md` の認識論フレームワーク
5. `references/synthesizer-prompt.md` の統合者プロンプトテンプレート

最終出力の仕事: 信頼度加重・証拠引用の叙述。「分かっていること」と「推論していること」の明確分離、ギャップと null 結果ソースの正直な認識。

## ステップ 5. 提示

統合者出力をユーザーに提示。明瞭化の軽い編集や会話コンテキスト追加は可。**信頼度言語は書き換えない。** 認識論的枠組みが成果物。権威的に聞こえるようヘッジを落とすのがこのスキルが防ぐ失敗モードそのもの。

## 出力形式

この構造を使う。必要に応じて適応するが、信頼度分離は維持。

**The Question**. ユーザーが聞いたことを簡潔に言い換え。

**The Code in Question**. ファイルパス、行範囲、主要シンボル。読者を固定する 1〜2 行。

**What We Found (direct evidence)**. 明示的引用付き主張。各 bullet はテキスト証拠があること。現在形。ソースを引用または言い換え。

**What We Can Reasonably Infer**. どこにも明示されていないが間接証拠でよく支えられた主張。各 bullet は推論連鎖を説明。「A と B から C が likely」。ヘッジ言語。

**Competing Hypotheses**. 証拠が複数物語に合うなら列挙。各に仮説、賛成証拠、反対または欠如証拠。記録が勝者を支えないとき勝者を強制しない。（明確な答えなら節スキップ。）

**What We Don't Know**. 明示的ギャップ。証拠が答えなかった質問。空だった検索ソース。具体に。「issue tracker で 'rate limit' を検索しこの閾値を議論するチケットなし」は「なぜか分からない」より有用。

**Sources Consulted**. 調査員ごとに 1 行。何も返さなかったものも含む。読者は (a) 照会した MCP、(b) 空だったもの、(c) スキップと理由を一目で判断。見落としリダイレクト用カバレッジマップ。

各行形式: `- <Source>: <what was searched>. <what was found, or "no relevant results," or "skipped. reason">.`

例:
- Source control (git/gh): `git log --follow backend/retry.ts`, PRs #49074, #47812. Found PR #49074 introduced exponential backoff and linked ENG-4421.
- Issue tracker (Linear): searched for "retry" and ENG-4421. Found ENG-4421 parent issue but no discussion of backoff parameters.
- Long-form docs (Notion): searched for "retry policy," "backend retries," "ENG-4421." No relevant results.
- Real-time team chat (Slack): skipped. No matching MCP available in this environment. Gap: conversational record not searched.
- Infrastructure observability (Datadog): searched for `retry_count` metric and monitors around 2024-08-14. Found monitor "Upstream 5xx rate > 1%" created same day as PR #49074.
- Error / exception tracking (Sentry): searched for issues first-seen in Aug 2024 with stack through `retry.ts`. Found issue SENTRY-3821 spiking in the week before the PR.
- Product analytics warehouse (Databricks): queried `<your_analytics_db>.<schema>.stg_backend_upstream_retry` for the 30-day window around 2024-08-14. Daily failure-classified event count fell from ~1.2k/day pre-PR to <50/day post-PR. Also checked `system.query.history` for relevant migration queries. None found.

Sources Consulted の後、ユーザーの `why` 質問がこのコード変更の前提なら、系譜所見を変更計画向け Preserve / Change / Avoid / Risk 制約セットに変換。

## 避けるべき一般的失敗モード

- **自信ある物語作り。** 薄い証拠のもっともらしい叙述。引用なし bullet は「inferred」か「hypotheses」へ。「what we found」に入れない。
- **意図の証拠としてコード自身を引用。** 「null をチェックするから null 対応」は力学であり動機ではない。動機は外部ソースか推論ラベル。
- **近時バイアス。** 最新コミットが権威的と仮定。現在の形は多くの以前の決定の堆積。遡る。
- **おべっか同意。** ユーザーが理由を提案（「パフォーマンスだと思う」）したら仮説として扱い独立に証拠確認。確認しない。
- **ギャップ節のスキップ。** 分からなかったことの正直な会計が価値の一部。
- **先読みによる調査員スキップ。** 検索せず「長文 doc にないだろう」。デフォルト全 7 姿勢が防ぐ。null はデータ点。スキップは盲点。
- **調査員を 1 エージェントに統合。** 各 MCP は独自クエリ語彙・結果形状・落とし穴。プールは専門性とカバレッジ推論を薄める。常にカテゴリごとに 1 調査員。

## 参照ファイル

- `references/epistemics.md`. 信頼度ティアと言い回しガイド。統合者は従う。
- `references/investigator-prompt.md`. 調査員サブエージェントのベースプロンプト。
- `references/source-playbook.md`. 下記カテゴリプレイブックへの索引。
- `references/sources/*.md`. カテゴリごとに 1 つの自己完結例プレイブックと横断 `incident-postmortem.md`。調査員にはカテゴリに一致する 1 ファイルを渡し利用可能 MCP に適応。
- `references/synthesizer-prompt.md`. 統合者サブエージェントのプロンプトテンプレートと出力形式。

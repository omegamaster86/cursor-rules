---
name: why
description: "「X はなぜこうなっているか」「なぜ Y を選んだか」、設計 rationale、regression、postmortem、データに裏打ちされた threshold に使用。利用可能 MCP を発見し、各 evidence カテゴリ（source control、issue tracker、長文 doc、real-time chat、infrastructure observability、error tracking、product analytics warehouse）を parallel に問い、決定と tradeoff の引用付き読みを返す。runtime 振る舞いは how を使用。"
disable-model-invocation: true
---

# Why

コードの背後にある動機と intent を調査する。

`how` スキルの companion。`how` はコードが何をするか・どう動くか。`why` はどんな力が形を決めたか。

各 spawn は `forge-models.mdc` ルールの role 行と default を名指す。`model` はその行の値、ルールや行が無ければ default。値が `inherit` なら `model` は未設定。Task ツールが slug を拒否したら default を使い、その旨を述べる。default も拒否されたらエラーメッセージから同族の最も近い有効 slug を使う。

## Operating Posture

**慎重で cautious、 precise な investigator** として動く。知っていることと推論を正直に分ける。confidence framework と phrasing guide の全文は `references/epistemics.md`。synthesizer は必ず従う。

## Step 1. Understand the Target and the Question

ユーザーが聞いていることを parse。**target** は通常 code の塊、パターン、feature、名前付き設計決定。**question** は設計 rationale、tradeoff、動機づけ edge case、外部 constraint、dead code、広い履歴 sweep。

target が曖昧（「なぜこうするの？」で referent 不明）なら会話 context（開いている file、直近 edit、cursor 位置、直前の話題）から最善推測。解釈を短く述べて差し替え可能にし、進む。

## Step 2. Establish the Code Anchor

investigator を spawn する前に、調査を具体 code に anchor。必要：

- 関連 file path と行範囲
- 主要 symbol（function 名、class 名、constant）
- 初期 commit リスト。target に触れた直近の commit。
- merge commit からの PR 番号（subject の `(#1234)` パターン）

インラインで組み立てる。

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

実質的な commit には `gh` で PR 本文・discussion：

```bash
gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews
```

seed context（file path、symbol、commit、PR 番号、リンク ticket ID）として保持。investigator に渡す。

## Step 3. Spawn Parallel Investigators (default posture)

**デフォルトは full parallel 調査。**

### Discovery

spawn 前に Cursor 環境の利用可能 MCP を列挙。available-tools map があればそれを使う。なければ Cursor が公開する `mcps/` で有効 MCP server を inspect。

各利用可能 MCP を 1 evidence カテゴリにマップ：

1. Source control history
2. Issue / ticket tracker
3. Long-form documents
4. Real-time team chat
5. Infrastructure observability
6. Error / exception tracking
7. Product analytics warehouse

source control は git と `gh` で常に利用可能。他 6 つは MCP 名、server 指示、tool 名、resource descriptor で分類。複数カテゴリに当てはまる MCP は primary evidence に合う 1 つ。曖昧な case は coverage map に記録。

**coverage map** は最小ではなく完全を目指す。null を doc し、検索をスキップしない。

マッチする investigator を 1 メッセージで全起動し concurrent。1 agent に複数 MCP は任せない。

Subagent config（各）：
- `subagent_type`: `generalPurpose`
- `model`: `why investigators` 行、default `cursor-grok-4.6-medium`
- `readonly`: `false`（agent mode）。**readonly/Ask mode は使わない。** MCP アクセスを剥がし MCP バック investigator を無効化する。investigator は書き込みはしない。

各 investigator が受け取るもの：
1. `references/investigator-prompt.md` の base prompt
2. 選んだ MCP 用カテゴリ playbook `references/sources/<source>.md`（`references/source-playbook.md` の例から adapt）
3. target code が defensive に見えるとき cross-cutting `references/sources/incident-postmortem.md`（null check、retry、timeout、rate limit、feature flag、egress guard、OOM handler）
4. Step 2 の code anchor（file path、symbol、commit hash、PR 番号、ticket ID）
5. ユーザーの元の質問

### Investigator roster. 利用可能 evidence カテゴリごとに 1 体

マッチする MCP があるカテゴリごとに 1 investigator spawn。各体は 1 tool または 1 MCP だけを所有。

各 entry はカテゴリと、その category が独自に surface する「why」の種類。戻りの期待、空のときの gap の名付け、（稀な provably-irrelevant だけ）skip 正当化に使う。

1. **Source control investigator**. Git 履歴、PR 用 `gh`、code comment、test。常に spawn。唯一の guaranteed source。*review 時に capture された implementation-time rationale* に最強。

2. **Issue / ticket tracker investigator**（例：Linear、Jira、GitHub Issues、Plane、Shortcut MCP）。*product や business の forcing function* に最強。why が engineering 外のとき。

3. **Long-form documents investigator**（例：Notion、Confluence、Google Docs、Coda MCP）。*長文設計 rationale*。code になる前に書かれた why。

4. **Real-time team chat investigator**（例：Slack、Discord、Microsoft Teams、Mattermost MCP）。*doc に届かなかった real-time 熟議*。source control、ticket、doc の paper trail が薄いとき特に重要。

5. **Infrastructure observability investigator**（例：Datadog、New Relic、Honeycomb、Grafana、Splunk MCP）。Infra/runtime 視点。*code を動かした infra と runtime の現実*。timeout、retry、rate limit、circuit breaker など infra signal に反応する target に最強。

6. **Error / exception tracking investigator**（例：Sentry、Rollbar、Bugsnag、Airbrake MCP）。*defensive や corrective code を動かした具体 exception と error 経路*。catch、null guard、型 check、retry など防御に最強。

7. **Product analytics warehouse investigator**（例：Databricks、Snowflake、BigQuery、ClickHouse、dbt、Redshift MCP）。Product/data 視点。*code の形を決めた product と data の現実*。flag-gated code、experiment 駆動 ship、data migration、「この数はどこから」に最強。

### When to skip an investigator

**明示の書面 justification** だけ skip。final の「Sources Consulted」に入る。有効な理由は 2 つ：

- **そのカテゴリ用 MCP がこの環境にない。** gap として flag。選択ではない。例：「Real-time team chat skipped. No matching MCP available, so the conversational record was not searchable.」
- **source が provably irrelevant**。「たぶん irrelevant」ではない。高い bar。例：「Error / exception tracking skipped. Target is a build-time script with no runtime code path.」

スコープ評価が single-commit trivial で PR 説明が完全な答えを含むとき、7 カテゴリすべての検索が冗長だと確認した後だけ inline 回答可。明示すること。稀であるべき。

## Step 4. Synthesize

1 synthesizer サブエージェントを spawn：

- `subagent_type`: `generalPurpose`
- `model`: `why synthesizer` 行、default `claude-opus-5.5-thinking-medium`
- `readonly`: `false`（agent mode）。synthesizer の quality check は citation の spot 検証で MCP が要る場合がある。readonly/Ask は MCP を剥がしそれを潰す。

synthesizer が受け取るもの：
1. investigator findings（null 結果、justification 付き skip カテゴリ含む）
2. Step 2 の code anchor
3. ユーザーの元の質問
4. `references/epistemics.md` の epistemics framework
5. `references/synthesizer-prompt.md` の synthesizer prompt template

## Step 5. Present

synthesizer 出力をユーザーに提示。明確化や会話からの context 追加の軽い編集は可。**confidence 表現は書き換えない。**

## Output Format

出力構造は `references/synthesizer-prompt.md` のもの：The Question、The Code in Question、What We Found、What We Can Reasonably Infer、Competing Hypotheses、What We Don't Know、Sources Consulted、Confidence Summary。必要に adapt するが confidence の分離は保持。Sources Consulted は investigator ごと 1 行。何も返さなかった・skip したものも理由付きで含める。

Sources Consulted ブロックの後、ユーザーの `why` がこの code を実際に変える前段なら、lineage findings を変更計画向けの Preserve / Change / Avoid / Risk  constraint セットに変換。

## Common Failure Modes to Avoid

- **Recency bias**. 直近 commit が authoritative だと仮定。現形は多くの過去決定の accretion。遡る。

## Reference Files

- `references/epistemics.md`. Confidence tier と phrasing guide。synthesizer 必須。
- `references/investigator-prompt.md`. investigator サブエージェント用 base prompt template。
- `references/source-playbook.md`. 下記カテゴリ playbook の index。
- `references/sources/*.md`. カテゴリごと 1 自己完結 example playbook、cross-cutting `incident-postmortem.md`。investigator にはカテゴリに合う 1 file を渡し利用 MCP に adapt。
- `references/synthesizer-prompt.md`. synthesizer サブエージェント用 prompt template（出力形式含む）。

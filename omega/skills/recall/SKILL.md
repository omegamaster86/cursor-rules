---
name: recall
description: "直近の作業 context を自分のチャット履歴・live 状態・共有レコード（ユーザー報告、過去の fix、インシデント）から再構成し、引き締まった現状 brief を返す。「X の作業を思い出して」「キャッチアップ」「何をやっていたか」「どこで止めたか」、作業開始・再開前に使用。"
disable-model-invocation: true
---

# Recall

**作業を始めるか再開する前に、ユーザーの直近の作業 context を再構築し、今どこにいて次に何をするかの引き締まったカプセルを返す。**

引き締め、本題に沿う。スコープ内の thread に必要なものだけ読み、止める。

context は 2 つのレコードにある。自分のチャット履歴はやったことと決めたこと。共有レコードは同じコード周りで別名で起きたこと：ユーザーが繰り返し報告する症状、ship して revert された fix、prod でまだ鳴っている error。**why** スキルが source control、issue tracker、チャット・issue チャネル、長文 doc、error tracking を横断して探すのはこの 2 つ目。長い bug tail の feature は物語の大半がここにある。transcript だけから再構成しない。

transcript は `~/.cursor/projects/<slug>/agent-transcripts/<uuid>/<uuid>.jsonl`。`<slug>` は workspace パスから先頭 `/` を落とし各 `/` を `-` に（`/Users/you/proj` → `Users-you-proj`）。各行は 1 チャットメッセージ。

1. 分類してルーティング。再開する特定の過去チャット 1 本は `session-pickup` playbook（`forge-mode/playbooks/session-pickup.md`）であり本スキルではない。作業習慣を durable な personal `-mode` スキルにするのは **`automate-me`** スキル。止めてそちらを実行。サブシステムや変更の平易な説明は **`teach`** スキル（`how` + `why`）であり recall ではない。recall は動く前に直近チャット横断で作業 context を載せる。ユーザーがすでに完全な state カプセル（path、branch、変更）を渡したならそれを使い、mining はスキップ。
2. 検索前にスコープを固定。窓（「recent」は実際の範囲、default 直近 7 日）、名前があれば topic、workspace（default はアクティブ。依頼なく別 project の transcript は読まない）。スコープを言い返す。「all」を黙って「recent N」にすり替えない。
3. チャット履歴に fan-out。高速・安価 model で parallel サブエージェント、corpus の slice ごと。各サブエージェントは実 modification 時間（`ls -t`）で候補を並べ、UUID 名では並べない。topic を先に grep し、マッチしたチャットと関連 region だけ読む。現在チャットと明らかなノイズ（subagent、eval、test チャット）はスキップ。同じ schema で 1 チャット 1 ブロック返す：topic、ユーザーの goal、決定、open thread、つまずきと修正、artifact（PR、ticket、branch）、各 chat UUID を引用。1〜2 チャットなら fan-out せず直接検索。生 transcript はサブエージェント内。メイン thread は findings だけ。
4. topic が feature、file、サブシステム、領域、bug を名指すときは常に共有レコードを sweep。default で判断不要。「X の自分の作業」でも免除しない。**why** スキルの source investigator に渡すが、問いは「なぜこう作ったか」から「現状は何か、試して持たなかったこと、ユーザーはまだ何を報告しているか」に寄せる。per-source playbook を再利用、chat-history mining と parallel、姿勢を継承：source ごとに 1 investigator、null も finding、MCP 不可ならスキップして明記。brief に織り込む。名前のない純 activity recall（「今週何をした」）だけこの step をスキップ。自分の履歴と live 状態が答えの全部。
5. live 状態で検証。mining と sweep で出た PR、branch、ticket を `git` と `gh` で確認。答えが agent が実際に何をしたか（走らせた tool、読んだ file、踏んだ error）に依存するなら、trim されたローカルコピーではなく full transcript を読む。
6. 下の契約で brief を書く。thread ごとにグループ。名指し topic に沿う。

## Output contract

カプセル、thread 状態、問題、next move の順。深い詳細は下か切る。

- **Capsule.** 最大 5 bullet。この作業が何で全体としてどこにいるか。
- **Threads.** 1 行ずつ、status タグを 1 つだけ：`[merged #N]`、`[open PR #N]`、`[in flight <branch>]`、`[verified, uncommitted]`、`[reverted #N]`、`[planned, not started]`。タグなし thread は未完了なのでタグ付ける。
- **Problems.** 最大 5、繰り返しのもの。ユーザーが繰り返し報告する症状と ship 後 revert された fix を含め、次の試行が前回の失敗地点から始まるように。
- **Next move.** 最も有用な次の 1 アクション、具体。

隣接 feature や ticket はこれをブロックしない限り出さない。カプセルと thread 行が 1 画面を超えるなら詳細を切り thread は切らない。brief は **unslop** スキルを通す。チャット finding は UUID、共有レコードは source（PR #、ticket ID、チャット permalink、error-tracker issue）で引用。公開出力前に private context を sanitize。

**Reply:** 上の契約どおりの brief。

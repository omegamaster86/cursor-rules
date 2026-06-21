# pstack

私は [poteto](https://x.com/poteto) です。president でも CEO でもありませんが、Meta、Netflix、Cursor で数百万行のコードを扱ってきました。React Core Team の一員として React Compiler の構築・保守にも携わっています。

AI がスロップコードを書きすぎる、という感覚が広がっています。私も同意します。20人のスロップ職人のようなチームで出荷したくはありません。品質のないスループットは目指す目標ではありません。速く行きたいなら、まず深く行け。

**pstack が私の答えです。** これは Cursor で高品質なコードを出荷するために私が毎日使っているスキルと同じものです。Cursor を本物のエンジニアリングチームに変えます。目標は LOC を最大化することではなく、むしろその逆です。pstack は、より少ない、しかしより高品質なコードを書くのを助けます。

**pstack は恐れ知らずの並列性を与えます。** 1つのエージェントで深く掘り下げ、良い検証可能なコードを書くことを信頼できるなら、自信を持って真の並列化ができます。`poteto-mode` で複数のエージェントを起動し、厳密なエンジニアリング原則を仕事に適用してくれることを信頼してください。

**Cursor は最高のすべてを与えてくれます。** すべてのフロンティアモデルには長所と短所があります。pstack ではどのモデルでも使えます。実際、私のスキルの多くは、各モデルの独自の強みを活かすマルチモデルワークフローを使っています。

フォークして、改善して、自分のものにしてください。PR 歓迎です！

## インストール

```bash
/add-plugin pstack
```

## 自分好みにカスタマイズ

`poteto-mode` は私のスタイルです。まったく同じものが欲しくないかもしれません。

`/automate-me` と入力してください。最近のトランスクリプトを掘り起こし、実際の働き方から `<your-name>-mode` スキルを下書きし、下層で pstack にルーティングします。pstack をベースに保ちつつ、`poteto-mode` と並ぶ独自のルーティングスキルが手に入ります。

モデルも設定可能です。`/setup-pstack` と入力してください。アクセス可能なモデルを検出し、各ロール（code、judgment、レビューパネル）をモデルにマッピングする小さな always-applied ルールを書き込みます。すべてのスキルがそれを読み、ルールがない場合は sensible なデフォルトにフォールバックするので、上書きしたい部分だけ上書きできます。

## 使い方

タスクの開始時に `/poteto-mode` を使います。リクエストを読み、プレイブックのセットから選び、ステップが必要とする他のスキルを実行します。

### `/poteto-mode` を使うだけ

このスキルがメインのショートカットです。エージェントに厳密なエンジニアリング作業をさせたいときはいつでも使います。16 のプレイブック付きです：

| playbook | 用途 |
|---|---|
| investigation | 読み取り専用の質問。x はどう動くか、y はなぜこう作られたか、本当に確かか。 |
| bug fix | 欠陥を再現し、根本原因を特定し、ランタイム証拠で修正する。 |
| perf | 計測された遅さをトレースし、ベースラインに対して改善する。 |
| hillclimb | 1つのメトリクスを目標に対して持続的・科学的に改善する。before/after 計測と仮説ループ、採用された勝利ごとに1コミット。 |
| runtime forensics | 計装からライブ症状（リーク、idle-CPU スピン、グリッチ）を診断する。 |
| trace forensics | キャプチャされたプロファイリング成果物（cpuprofile、trace、spindump、heap snapshot）を診断する。 |
| feature | 名前付きデータ形状から構築する新規または変更された動作。 |
| refactoring | 構造または形状への動作保存変更。 |
| prototype | 設計や動作の判断を安くするための使い捨てスケッチ、または観察によって経験的分岐を決める。 |
| visual parity | 2つの実装間のピクセル完全一致 UI 等価性。 |
| authoring a skill | SKILL.md の作成または編集。 |
| eval | スキルまたはプロンプト変更がエージェントの動作に与える影響をブラインドでテストする。 |
| autonomous run | 止まらずに長いタスクを完了まで推進する。 |
| session pickup | 以前のエージェントの進行中の作業を再開または引き継ぐ。 |
| pause safely | 進行中の作業をきれいに中断し、後で再開できるようにする。 |
| multi-phase plan | フェーズまたはスタック PR にまたがる作業。 |

呼び出されると：

1. todo リストを開く。最初の項目はスキル内のインライン原則インデックスを読むこと。
2. タスクをプレイブックにマッチさせ、そのステップを verbatim でコピーする。
3. ステップが発火するたびに他のスキルにルーティングする。
4. コンシューマーとメンテナ向けにフレーミングされた unslopped な返信を書く。

完全なルールとプレイブックは `skills/poteto-mode/SKILL.md` にあります。

`/poteto-mode` は Cursor の `/loop` コマンドと非常によく連携します。厳密さを犠牲にせず、Cursor を何時間も動かせます。

## スキル

残りは、特定のものを明示的に呼び出したいときに便利です：

| skill | 使うタイミング |
|---|---|
| `/poteto-mode` | 非自明なタスクのデフォルトエントリーポイント。 |
| `/how` | サブシステムの仕組みのウォークスルーが欲しいとき。 |
| `/why` | なぜこう作られたか知りたいとき。実行時に利用可能な MCP を検出し、各証拠カテゴリを並列でクエリ（ソース管理、イシュートラッカー、長文ドキュメント、リアルタイムチャット、インフラ可観測性、エラートラッキング、アナリティクスウェアハウス）。 |
| `/recall` | 作業を開始または再開するとき、自分のチャット履歴と共有レコードからトピックに関する最近のコンテキストを再構築し、タイトな現状ブリーフとして返す。 |
| `/blast-radius` | 小さく見える変更があり、他に何が壊れる可能性があるか知りたいとき。実行中のコードで証明された1つの事実で安全である理由付き。 |
| `/architect` | 関数境界を越えるコードを書こうとしているとき、呼び出し側の使用法、型、モジュール形状を先に確定する。 |
| `/arena` | 同じことの N 並列試行を行い、それぞれの最良部分を取り込む。 |
| `/interrogate` | diff があり、4つの異なるモデルに（厳格なコード品質レンズを含めて）破ってもらいたいとき。 |
| `/automate-me` | 実際の働き方から下書きされた独自の `-mode` スキルが欲しいとき。 |
| `/setup-pstack` | pstack がロールごとに使うモデルを選びたいとき。モデルを検出し設定ルールを書く。 |
| `/reflect` | 長いタスクが完了し、レシピをスキル編集としてキャプチャしたいとき。 |
| `/tdd` | バグ修正で安価なローカルテストパスがあるとき。失敗テストを先に書き、その後修正。 |
| `/typescript-best-practices` | TypeScript を読むまたは編集するとき。type-system-discipline 原則を構文に接地する。 |
| `/figure-it-out` | バンドルされたプレイブックが合わない。タスク向けの厳密で監査可能なプレイブックを設計する。 |
| `/show-me-your-work` | レビュー可能な意思決定トレイルが欲しい。コミット可能な tsv に決定をログする。 |
| `/unslop` | 文章をクリーンアップするとき。AI の痕跡を除去する。 |

### 例

ほとんどの場合、タスク開始時に `/poteto-mode` と入力し、プレイブックにルーティングさせます。他のスキルはステップが必要とするときに発火します。直接呼び出すものもいくつかあります。

```
bug fix:           /poteto-mode this pr has a subtle bug where the scroll drifts every 750ms even
                   when idle. repro first, then fix and verify.
perf:              /poteto-mode a big list takes a second or two to load even though we virtualize.
                   run a cpu trace and tell me why.
feature:           /poteto-mode build a small feature behind a feature flag. verify it really works.
prototype:         /poteto-mode build two prototypes of the markdown renderer so we can compare.
                   spawn an agent for each.
multi-phase:       /poteto-mode open source these skills as a plugin. nothing internal leaks, work
                   in a temp dir, show me the dependency graph first.
overnight run:     /poteto-mode i'm going to bed. land the stack even if ci flakes. i want
                   everything merged by morning.
visual parity:     /poteto-mode the row spacing is too tall when this flag is on. the second image
                   is correct. repro and fix until it matches.
figure it out:     /poteto-mode i'm stepping away. migrate every caller from the synchronous store
                   to the new async one, keeping behavior identical. i want to trust it was done
                   right when i'm back.
how:               /how do we cancel runs? do we have an n+1 when we look up every run to cancel?
why:               /why is this feature flag not on yet?
architect:         design this instrumentation to be high signal with no false positives. /architect
                   this first.
arena:             /arena take my prompt to the arena verbatim. i want to compare their proposals
                   with yours.
interrogate:       /interrogate review this pr.
tdd:               /tdd implement
unslop:            can we unslop and tighten the new changes?
reflect:           /reflect that took too long. capture what we learned so the next run doesn't
                   repeat it.
show-me-your-work: /show-me-your-work keep a decision trail i can review when i'm back.
automate-me:       /automate-me
```

## `poteto-agent` サブエージェント

pstack には私のスタイルを最初から最後まで実行するサブエージェントも同梱されています。親エージェントから `subagent_type: "poteto-agent"` で起動します。作業前にインライン Principles インデックスを含め `poteto-mode` スキルの `SKILL.md` を全文読みます。`generalPurpose` に置き換えるとその読み取りをスキップし、ドリフトします。

`/poteto-mode` と `subagent_type: "poteto-agent"` は同じラッパーを通じてルーティングされます。

## 原則

20 の短いスキル、各1原則。`poteto-mode` はそれらをインラインでインデックスし、タスク開始時にそのインデックスを読みます。スタンドアロンファイルは、他のスキルが名前で原則を参照できるように、およびインデックスが各ルールの完全版を指せるように存在します。

- core: laziness-protocol, foundational-thinking, redesign-from-first-principles, subtract-before-you-add, minimize-reader-load, outcome-oriented-execution, experience-first, exhaust-the-design-space, build-the-lever.
- architecture: boundary-discipline, type-system-discipline, make-operations-idempotent, migrate-callers-then-delete-legacy-apis, separate-before-serializing-shared-state.
- verification: prove-it-works, fix-root-causes, sequence-verifiable-units.
- delegation: guard-the-context-window, never-block-on-the-human.
- meta: encode-lessons-in-structure.

## ここには同梱されていないもの

`poteto-mode` が参照するがバンドルしないものがいくつかあります：

- `/deslop` と `deslop` スキルは `cursor-team-kit` プラグインに同梱。
- `control-cli`（CLI と TUI 用）と `control-ui`（ブラウザ、Electron、web 用）も `cursor-team-kit` に同梱。
- `/babysit` と `/create-skill` は Cursor 組み込み。

完全セットが欲しければ `cursor-team-kit` を pstack と一緒にインストールしてください。

## なぜプランニングスキルがないのか

Cursor にはすでに優れた plan mode があり、pstack と非常によく連携します。ただし個人的には、プランニングを信じていません。最高の仕様はコードです。プランを作りたい場合は `/poteto-mode` がカバーしますが、デフォルトではありません。

## ライセンス

MIT

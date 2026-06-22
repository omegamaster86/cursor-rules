---
name: reflect
description: アクティブなトランスクリプトに 3 つの並列レビューサブエージェントを起動し、学びを表面化し、各々を既存スキルへの具体的編集にルーティングする。ユーザーが reflect と言ったときに使用。
disable-model-invocation: true
---

# Reflect

現在の会話から永続的な学びをマイニングし、スキル編集にルーティングする。

## いつ呼び出すか

- ユーザーが「reflect」または「/reflect」と言った。
- 複雑なタスク（ツール呼び出し 5 回以上）がきれいに着地し、レシピを残す価値がある。
- エージェントが行き詰まり、動く経路を見つけ、それが一般化する。
- ユーザーがタスク途中でエージェントの進め方を修正した。
- どこにもキャプチャされていない非自明なワークフローが現れた。

会話が些細、話題外、または親が正しく従った既存スキルで既にカバーされているときはスキップ。単発は学びではない。

## プロセス

### 1. アクティブなトランスクリプトを特定する

扇状展開の前に親が自分のトランスクリプトファイルを見つける。システムプロンプトにアクティブワークスペースの `agent-transcripts/` ディレクトリが書かれている。そのパスを使う。`~/.cursor/projects/*/` を横断して glob しない。ワークスペース境界を越え、無関係なプロジェクトの非公開チャットを読む。

```bash
ls -t <agent-transcripts>/*.jsonl <agent-transcripts>/*/*.jsonl <agent-transcripts>/*/subagents/*.jsonl 2>/dev/null | head -10
```

3 つのレイアウト: レガシー平坦（`<id>.jsonl`）、現行ネスト（`<id>/<id>.jsonl`）、サブエージェント（`<parent>/subagents/<child>.jsonl`）。

各候補について最初の JSONL 行を読み、`message.content[0].text` に会話の冒頭ユーザープロンプトが含まれるか確認。マッチするパスを採用。解決できなければ、セッションの短いダイジェストを書き、それを渡す。

### 2. 3 レビュアーを並列起動

1 メッセージ、3 つの `Task` 呼び出し、`subagent_type: generalPurpose`、各に明示的 `model:`、エージェントモード（`readonly: false`）。レビュアーはトランスクリプトで参照されたコンテキスト（チケット、チャットスレッド、可観測性トレース）の MCP ルックアップが要る。readonly は MCP を剥がす。プロンプトはファイル書き込みを禁止。親が編集を適用する。

| レンズ | `model` | プロンプトテンプレート |
|---|---|---|
| Judgment | 設定済み reflect-judgment モデル（デフォルト `claude-opus-4-8-thinking-xhigh`） | `references/judgment-reviewer.md` |
| Tooling | 設定済み reflect-tooling モデル（デフォルト `composer-2.5-fast`） | `references/tooling-reviewer.md` |
| Divergent | 設定済み reflect-judgment モデル（デフォルト `claude-opus-4-8-thinking-xhigh`） | `references/divergent-reviewer.md` |

各テンプレートをそのまま渡し、マーク箇所をトランスクリプトパスまたはダイジェストに置換。レビュアーは `Task` 応答本文で所見を返す。

### 3. 統合する

`Task` 1 回、`subagent_type: generalPurpose`、設定済み reflect-judgment モデル（デフォルト `claude-opus-4-8-thinking-xhigh`）、エージェントモード（`readonly: false`）。統合者の品質チェックに引用のスポット検証が含まれ、MCP が要ることがある。readonly は MCP を剥がす。`references/synthesizer.md` をそのまま使い、マーク箇所に各レビュアーの全文出力をインライン。統合者は構造化された Accepted / Rejected / Backlog リストを返す。

### 4. 構造的強制チェック

統合者の Accepted リストをサニティチェック。lint ルール、スクリプト、メタデータフラグ、実行時チェックでより確実に強制できる項目は Accepted から Backlog へ。**encode-lessons-in-structure** 原則スキルを参照。統合者は既にこの基準を適用。編集が着地する前の最終パス。

### 5. 適用する

Accepted 編集を適用する前に、統合者の Accepted/Rejected/Backlog 全文をユーザーに提示し、明示的承認を待つ。ユーザーが適用する部分集合を選び、ルーティングをリダイレクトしうる。スキル変更は組織の将来の全エージェントに影響する。自動適用しない。

Backlog 項目はチームが使う devex / バックログトラッカーに自動でファイル。それらはトラッカー提出でありスキル編集ではない。Accepted リストだけが承認待ち。

承認された各 Accepted 項目について、Routing フィールドに厳密に従う:

- 既存スキルの些細な編集（1 行箇条、文の締め、古い事実の修正）: 親が直接。
- 既存スキルの実質的編集（新節、新パターン表、~10 行超）: Cursor 組み込み `create-skill` に渡し、その draft / test / iterate ループを実行。
- `tune description: <skill path>`（スキルは存在するがトリガーすべきときにしなかった）: `create-skill` に渡し description 最適化ループを実行。
- `new skill via create-skill: <kebab-name>`: 作成を `create-skill` に渡す。形を即興で作らない。

環境に SKILL.md バリデータがあれば、触った各スキルで完了宣言前に実行。なければスキップ。

### 6. ユーザー向け要約

短いリスト、前置きなし:

- 適用した編集: `<skill path>`。各 1 行で何が変わったか。
- 作成した新スキル: `<skill path>`。各 1 行（稀）。
- devex トラッカーにファイルした Backlog: `<issue title>`（`<tags>`）。各 1 行。
- 却下: 統合者の却下所見と理由を 1 行ずつ。

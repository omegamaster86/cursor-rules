---
name: automate-me
description: "「automate me」「-mode スキルを作成/更新/リフレッシュ」「好みや作業スタイルをスキルに」「エージェントに自分のやり方を守らせたい」に使用。create-skill + unslop で personal `-mode` スキルを起草・改訂。任意で直近 transcript から新しい evidence を引く。"
disable-model-invocation: true
---

# Automate me

ユーザーの作業規約をエージェントが従うスキルに落とすガイド付きフロー。出力は 1 つのその人向け `-mode` スキル（例：`jay-mode`、`priya-mode`）。

本スキルは 3 つを編成する：インライン mining（step 1）、Cursor 組み込み `create-skill`（著者）、利用可能なら **unslop** スキル（散文規律）。順序を決める。置き換えない。

## Flow

### 0. 既存スキルを確認

`.cursor/skills/**/*-mode/SKILL.md` と `~/.cursor/skills/*-mode/SKILL.md` を再帰検索し、ユーザーの handle に合うものを探す。mode スキルは personal カテゴリ（`.cursor/skills/<handle>/`）に置ける。トップレベルだけではない。あれば `AskQuestion` で intent を確認（「update my skill」等を既に言っていれば除く）：

- 既存を更新（再実行の default）
- ゼロから（稀。前に理由を聞く）

更新モードは以降を変える：
- Step 1 はスキル最終編集以降の履歴だけ mining（`git log -1 --format=%cI <path>`）。
- Step 2 はゼロから何を capture かではなく、何が変わった・欠けているかを聞く。
- Step 4 は既存 file を in-place 編集。ユーザーが矛盾していない section は保持。新 evidence のある section は改訂。本当に新しい rule だけ section 追加。

### 1. 履歴を mining

fan-out 前にアクティブ workspace の transcript を特定。system prompt が workspace の `agent-transcripts/` を名指す。その path だけ使う。`~/.cursor/projects/*/` を glob しない。workspace 境界を越え、無関係 project の private チャットを読む。

そのスコープ内の直近 agent 会話で繰り返しパターンを調査。履歴 slice に parallel サブエージェント（例：直近 2〜4 週、3 slice に分割して各 slice に十分な材料）。各 slice mining サブエージェントは親が渡す workspace スコープ path の transcript を読み、下の signal を探し、evidence ポインタ付き短い構造化リストを返す。default で探す signal：

- 応答の好み（長さ、トーン、形式、「もっと噛み砕いて」修正）
- 委譲習慣（subagent、model、専門 workflow、parallelism）
- 検証姿勢（「done」の意味、unit test vs live repro、reviewer）
- コード・散文規律（style、引用する principle、lint/format tool）
- プロセス規約（worktree、commit、PR、review/merge tooling）
- メタ好み（タスク途中のスキル修正、新規提案）

elevate 前に slice 横断で cross-check。2+ slice で見えたパターンは high-confidence。単発は弱く通常 drop。

### 2. ユーザーに直接聞く

mining はまだ出てきていない intent を逃す。`AskQuestion`（構造化 multi-choice）。ゼロからタイプさせない。

形：1〜2 問、各 4〜6 選択、`allow_multiple: true` はカテゴリ問。広く（「どの領域が重要？」）から始め、選ばれた領域で具体 follow-up。構造化ラウンド後、1 問 free-form で選択肢が逃したものを拾う。

20 問ダンプはしない。

### 3. finding をクラスタ

合算 signal を section にグループ。よくあるもの（当てはまるだけ）：

- **Response style**: 長さ、トーン、形式。
- **Autonomy**: 聞かずにどこまで、MCP tool 使用。
- **Understand first**: スコープ・調査時にどのスキルへ。
- **Subagents**: default、parallelism、model-to-task、専門 workflow。
- **Prose / code discipline**: principle、lint tool、style guide。
- **Review and verify**: repro 姿勢、検証スキル、live-testing tool。
- **Process**: git worktree、commit、PR、review/merge tooling。
- **Skills**: スキル著者習慣、fix-the-skill-first、新規提案。

粒度の形は **forge-mode** スキルを読む。内容はコピーしない。ユーザーの rule は forge-mode と同じではない。

### 4. スキルを起草

Cursor 組み込み `create-skill` で著者。配置：

- Path: 既存 mode のカテゴリを保持。新規 mode は repo にその handle の personal カテゴリがあれば `.cursor/skills/<handle>/<handle>-mode/SKILL.md`。なければ project の `.cursor/skills/<handle>-mode/SKILL.md`（または personal 希望なら `~/.cursor/skills/<handle>-mode/`）。
- Handle: ユーザーの名または選んだ identifier。
- Frontmatter `description`: 名前 + `/<handle>-mode` + 「その人のスタイルで働く」で trigger。「write code」「review PR」など汎用 keyword ではない。
- Frontmatter 整形: `create-skill` の YAML 規則。`description` は 1 YAML scalar。句読点や折り返しが要るなら quote または `description: >-` とインデント継続行。
- Frontmatter `disable-model-invocation: true` が default。毎ターン適用を明示希望したときだけ opt-out。

### 5. 散文を iterate

利用可能なら **unslop** と `create-skill` の執筆ガイドを各行に適用。

draft を見せて feedback。複数 iterate を想定。容赦なく切る。mode スキルはマニュアルではない。

### 6. Land

main から worktree で作業。commit して PR。main に直接 push しない。

## Guardrails

- **1 会話に過適合しない。** 1 回言って別のとき矛盾はノイズ。codify 前に複数 instance を要求。
- **賢がらない。** 他スキル内容の言い換え、比喩の発明、agent 読者向け「詩的」散文はコストに見合わない。operational に。
- **参照、インラインしない。** ユーザーが頼る他スキルは path 参照。別所の principle doc も同様。
- **section は最小。** ユーザーがそこに非 default の具体 rule があるときだけ section。「明確に伝える」は section ではない。「短い段落。比較は表。bullet は本当に並列のときだけ。」は section になりうる。
- **命名は汎用。** 命令形は「the user」「the human」。著者の名ではない。
- **対称を強制しない。** 書く価値の process rule がなければ Process section ごとスキップ。

## Evaluation

`-mode` スキルは主観的出力。`create-skill` 型の test/iterate benchmark はここでは有用でない。ユーザーと vibe-check：本人らしいか？ 抜けは？ から ship。

trigger 精度が実運用で問題になったときだけ description 最適化 loop。

## When not to use

- タスク固有スキル（作業規約ではない）：`create-skill` 単体、mining 不要。
- 狭い workflow 1 つ（例：「commit message の書き方」）。通常スキルであり mode ではない。

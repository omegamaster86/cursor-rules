# Plan

`forge-mode` スキルの **Principles** セクションに接地したフェーズ実装プランを produce する。プランが成果物。実装しない。

下の各ステップを1項目とする todolist を開く。

## 0. Triage

変更が1〜2ファイルで自明なアプローチならプランを skip。その旨を述べて stop。

3ファイル以上にまたがる、architecture を導入する、競合アプローチまたは unclear スコープがある、ユーザーがプランを求めた場合は plan。

## 1. Re-read principles

`forge-mode` スキルの **Principles** セクションを最初から最後まで読み、インデックスする `principles/` の leaf も読む。原則がすべてのプラン決定を統治。cross-link する。

## 2. Scope and constraints

スコープと制約の読み取りを1段落で述べる。genuinely ambiguous な intent だけ `AskQuestion`（[`never-block-on-the-human`](../principles/never-block-on-the-human.md)）。各 open question に concrete オプション。

in scope vs 明示的 out、技術またはプラットフォーム制約、preserve するパターン、done の定義を resolve。

## 3. Explore in subagents

コードベース探索を delegate（[`guard-the-context-window`](../principles/guard-the-context-window.md)）。

- `subagent_type: "forge-agent"` を優先。`generalPurpose` は fallback。組み込み `plan` subagent_type は使わない。
- 設定ロールに従い `model:` を明示（デフォルト code は `composer-2.5-fast`、judgment は `claude-opus-4-8-thinking-xhigh`）。

各 explorer は file pointer、convention、dependency、test インフラ、entry point を返す。インラインダンプなし。

## 4. Write the plan

ユーザーがプランの置き場所を指定する。未指定なら Cursor Plan 形式を優先（下記）。

### Cursor Plan 形式（確認用・推奨）

変更ファイルとデータ流れを **Plan モードと同じ Mermaid** で確認できるようにする。詳細テンプレは [`plan-diagrams.md`](plan-diagrams.md)。

優先順:

1. CreatePlan が使える → CreatePlan（YAML: `name` / `overview` / `todos`）で書き、本文に必須図を含める。
2. 使えない → 返信に必須図を出し、可能なら `~/.cursor/plans/<slug>.plan.md` にも同内容を書く。

小さい文書プランは単一ファイル `NN-slug.md`。3フェーズ以上は `overview.md` ＋ phase ファイルのディレクトリ：

```
NN-slug/
├── overview.md
├── phase-1-scaffold.md
├── phase-2-...md
└── testing.md
```

文書プランと Cursor Plan を両方出す必要はない。どちらか一方で、必須図が含まれていればよい。

### Phase sizing

- 1関数または型＋テスト、または1バグ fix。「1ファイル」ではない。
- 触るファイル2〜3、最大。
- option value を保つため8〜10の小フェーズを3〜4の大フェーズより優先（[`foundational-thinking`](../principles/foundational-thinking.md)）。
- フェーズに5テストケース超または3関数超なら split。

### Overview file

- **Context.** 問題となぜ今か。
- **Scope.** 含む。明示的除外。
- **Constraints.** 技術、プラットフォーム、dependency、パターン。
- **Alternatives.** 2〜3アプローチをスケッチ、選択と rationale。制約が1つに dictate するとき skip。
- **File change map（必須）.** Mermaid。触るファイルと依存。[`plan-diagrams.md`](plan-diagrams.md)。
- **Data flow（必須）.** Mermaid。入力→変換→出力、または UI→hook→API。契約名を載せる。
- **Applicable skills.** 実装者が invoke すべきドメインスキルを名前で。
- **Phases.** phase ファイルへの順序付き standard-markdown リンク。
- **Verification.** プロジェクトレベルコマンド。
- **Implementation guidance.** セクション6参照。

1〜2ファイルで自明なら両図を `diagrams skipped: <reason>` で skip 可。

### Phase files

- overview へ back-link。
- **Goal.** フェーズが達成すること。
- **Changes.** 影響ファイルと high level の変更。what と why、how ではない。コード snippet なし。
- **Data structures.** 主要型または schema を名指し。1行スケッチのみ（[`foundational-thinking`](../principles/foundational-thinking.md)）。
- **Verification.** セクション6参照。
- フェーズが overview の図と大きくずれるときだけ、phase 内に差分 Mermaid を追加。

lint / CI / テスト骨格と契約型を機能フェーズより先に land するよう順序（[`foundational-thinking`](../principles/foundational-thinking.md)）。フロント / バックの完了順は揃えなくてよい。各フェーズは独立して shippable。

既存コードに触れる変更では、新要件を初日から持っていたらどう見えるかを問い、holistic に再設計する。incremental に deliver。

フェーズがスキルを create/edit する場合、実装者に **create-skill** スキル（SKILL.md 作成用 Cursor 組み込み）を使うよう phase で指示。

## 5. Verification per phase

各フェーズに両方必要：

**Static.** type check、lint、プロジェクトテスト pass。

**Runtime.** 関連 control スキル経由で matching surface 上で feature を exercise：

- Browser / Electron / Web UI：ブラウザ MCP または手動 verify（`control-ui` 未導入時）。
- CLI と TUI：手動 verify（`control-cli` 未導入時）。
- Native mobile：チームが持つ simulator-driving スキル。
- 触った surface に control スキルがない：プランに flag。

バグ fix のループは surface で再現、fix、同 surface で verify。ユニットテストは branch が特定の動きをすることを示す。バグが消えたことは証明しない（**`/verify-done`**）。

## 6. Implementation guidance

overview で、実装者が名前で適用すべき forge-mode non-negotiables を名指し：

- 変更前に unfamiliar な各サブシステムで **how** スキル。
- 出荷前に contested design で **`review-orchestrator-triple-hybrid` コマンド**による敵対的レビュー。
- プランが監査可能記録を要するほど大きいとき **show-me-your-work** スキルで decision trail を保持。
- PR 開いた後 Cursor 組み込み **babysit** スキル。

## 7. Hand back

フェーズ、スコープ境界、applicable skills、verification を要約。**File change map** と **Data flow** の Mermaid を返信に含める（skip 理由がある場合を除く）。stop。実装開始タイミングはユーザーが決める。



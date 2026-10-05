### Opening a PR

他のすべての playbook 末尾で呼び出し。**直前に `/verify-done` を PASS してから** PR を開く（`commands/verify-done.md`）。

**Worktree.** main から git worktree で作業。subagent は inherit。同 branch 上の複数 `Task` は各々 own worktree、または間に `git fetch && git reset --hard origin/<branch>`。unrelated work の dirty branch：patch out、fresh worktree、apply。snarled worktree：main から reset、minimal に redo。

**Commits.** liberally commit。PR 前に small ordered commit に rebase。各 commit は future PR：landable、story を語る順序。fix が just-made commit に属すなら amend。separable なら new commit。

**Titles.** Conventional Commits: `type(scope): subject`。`feat` / `fix` / `docs` / `refactor` / `test` / `chore` / `perf`。scope は変更領域（例 `omega`、`forge-mode`）。subject は短く imperative。変更を担う実シンボルがあれば名指す。末尾に period なし。

**Descriptions.** PR body は briefing。diff を持つ reviewer が 1 分以内に「なぜ」「何を意図的に外した」「何が壊れうる」「どう証明した」を把握できる。短い文。identifier の壁は避ける。squash commit body は PR body と同じ。40 行を超えるなら body を削る。

各節は `##` 見出し（bold リードインではない）。この順。言うことが無い節は落とす。

- `## Why` — 問題と approach を 1–3 文。SHA 列や rebase 系譜は書かない。
- `## What changed` — 1–3 bullet。変更を担う symbol / path だけ名指す。rename / retarget は両側。
- `## Scope` — この PR がカバーするものと意図的に外すもの（follow-up、known gap）。1–3 項目。ファイル別エッセイは書かない。
- `## Tradeoffs` — reviewer が聞きそうな、採用しなかった代替だけ。本当の選択が無ければ省略。
- `## Blast Radius` — 誰 / 何に触れる、なぜ safe または risky。main が red ならそのコスト。
- `## Verification` — 1–3 bullet。実際の run path と結果。perf は primary 数字 1 つを単位付き `before → after`。残りの evidence はリンク（multi-agent-candidates / swarm ディレクトリ等）。sample 手法の長文や metric 表は body に貼らない。

その後、主張を証明する video / screenshot を付ける。full SHA、lane 逐語 recital、「CLEAN」 verdict はリンク成果物へ。commit body は subject を restate しない。

**Forge.** 最初の PR 操作前に forge を決め、create / edit / view / watch / merge で維持。デフォルトは GitHub CLI（`gh`）。`command -v origin` が成功し Origin が repo を解決できるなら `origin pr ...` を優先。無ければ `gh` に留まり fallback を記録。Graphite（`gt`）は要求しない。

**Built-in PR tool.** run が組み込み PR ツールを提供するなら、create / edit / retarget / ready はツール経由（CLI ではない）。ツールが無い操作と、ツールが無い run 全体は resolved forge を使う。

**Size and stacks.** 1 fat より 5 narrow PR。stack は base-branch 連鎖。root は trunk。child は親 tip に rebase し PR base は親 branch。独立 work だけ trunk から branch。大きな stack 前に trunk で rebase。

**Readiness.** PR は ready で開く（draft ではない）。組み込みツールは `draft: false`。`gh` では `--draft` を付けない。draft になったら ready にする。

**Babysit.** Opening a PR は babysit を開始しない。URL を出して build を続ける。phase / stack が揃った後、ユーザーが求めたときだけ別 pass で **Babysit**（`babysit.md`）。各 PR ごとの babysit は build を止め、後続 wave で restart される commit に check を浪費する。intent から drift した feedback には push back。

PR を開く subagent は `review-orchestrator-triple-hybrid` を実行、URL を返し、babysit しない（Autopilot-full / Autopilot-stack owner は brief に従う）。parent に return。

### Opening a PR

他のすべての playbook 末尾で呼び出し。

**Worktree.** main から git worktree で作業。subagent は inherit。同 branch 上の複数 `Task` は各々 own worktree、または間に `git fetch && git reset --hard origin/<branch>`。unrelated work の dirty branch：patch out、fresh worktree、apply。snarled worktree：main から reset、minimal に redo。

**Commits.**  liberally commit。PR 前に small ordered commit に rebase。各 commit は future PR：landable、story を語る順序。fix が just-made commit に属すなら amend。separable なら new commit。

**PRs.** commit 前 diff に `/deslop`。PR description と commit body に **unslop** スキル。small PR、1 fat より5 narrow。follow-up は stack。genuinely independent な work だけ main から branch。stacked PR ではチームの stacking tool。principle は small ordered slice と reviewer に見える stack。PR status 参照前に `gh pr view <number>`。substantial stack work 前に `main` で rebase。small PR に `## Summary` / `## Test plan` boilerplate なし。commit body は subject を restate しない。open 後 Cursor 組み込み **babysit** スキル。feedback が intent から drift したら push back。

PR を open する subagent は `interrogate` と `/deslop` を実行、URL を返し、babysit しない。parent に return。

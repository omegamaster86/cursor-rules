### Worktree and simulator cleanup

**disk と safety gate を自分が持つ。** merged か abandoned の git worktree と stale iOS simulator を prune して space を reclaim。deletion は不可逆。各 step は in-use や uncommitted work を持つものの削除を防ぐ。

1. Snapshot と audit。`df -h /` を記録し `scripts/worktree-audit.sh`（principle-build-the-lever）。path は `git worktree list` から読み、手打ちしない。手打ち `myrepo-worktrees/x` は `.cursor/worktrees/myrepo/x` にあるものを miss しうる（principle-encode-lessons-in-structure）。各 worktree を size、age、merge state、uncommitted work、PR state、その worktree に触れた newest chat で classify し bucket を suggest。transcript scan は遅いので background。
2. bucket は advice で permission ではない。pinned と active chat が real artifact（principle-prove-it-works）。user か sidebar からその set を得て各 candidate を cross-check。lever が user が pin していた worktree を `safe` と mark しうる。pinned set が勝つ。
3. delete 前に usage を verify。各 `verify-recent-chat` 行、または doubt するものは subagent に fan out して transcript を読み、chat が pinned か ongoing か、触る worktree を report（principle-guard-the-context-window、transcript は bulk）。pinned chat は background subagent で sibling worktree に multi-agent-candidates と repro tree を spawn し、sidebar に名前が出なくても in-use。
4. 不可逆 loss で pause。`wip:N` は N 個の tracked uncommitted edit。diff を見せて先に decision。clean worktree の remove は branch から recover 可能だが uncommitted work は消える。`scratch:N` は untracked throwaway、drop safe だが file を名指す。Autonomy に従い clean で merged で not-in-use は proceed。`wip` と in-use は pause。
5. confirmed set を prune。path ごと `git worktree remove --force <path>`。ignored build artifact で dir が残るなら `rm -rf`、その後 `git worktree prune`。branch ref は残る。commit は失わない。`df -h /` と re-list で確認。
6. Simulator と他 reclaimer。simulator は通常次に大きい win。`xcrun simctl --set testing delete all`（XCTestDevices clone）、`xcrun simctl delete unavailable`、`xcrun simctl runtime list` して古い runtime は `runtime delete <id>`。要れば: Xcode `DerivedData` と `iOS DeviceSupport`、`~/Library/Application Support/Cursor`（`state.vscdb.backup`、`snapshots/roots/<root>` で workspace として開いた folder 名の `<root>` が膨らむ）、package cache（pnpm、uv、brew、yarn）。user が keep と言っていない cache だけ clear。

code review で slip を catch しない user state を delete する唯一の playbook。上の gate が review。

**Reply:** before/after の `df -h /` と reclaim した space、prune した worktree、hold back 各 1 行理由（どの chat が in-use、または uncommitted work）。

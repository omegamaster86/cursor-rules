### ワークツリーとシミュレータのクリーンアップ

**ディスクと安全ゲートを所有する。** マージ済みまたは放棄された git ワークツリーと古い iOS シミュレータを整理して容量を回収する。削除は不可逆なので、各ステップで使用中のものや未コミット作業を消さないようガードする。

1. スナップショットと監査。`df -h /` を記録し、`.cursor/skills/forge-mode/scripts/worktree-audit.sh` を実行する（**build-the-lever**（`principles/build-the-lever.md`））。パスは `git worktree list` から読み取り、手入力しない。手入力の `myrepo-worktrees/x` は `.cursor/worktrees/myrepo/x` にあるものを見落とす（**encode-lessons-in-structure**（`principles/encode-lessons-in-structure.md`））。各ワークツリーをサイズ、経過日数、マージ状態、未コミット作業、PR 状態、そのワークツリーに触れた最新チャットで分類し、バケットを提案する。トランスクリプト走査は遅いのでバックグラウンドで実行する。
2. バケットは助言であり許可ではない。ピン留めとアクティブなチャットが真のアーティファクト（**prove-it-works** / `/verify-done`）。ユーザーまたはサイドバーからその集合を得て、候補ごとに突合する。レバーがユーザーがピン留めしていたワークツリーを `safe` と付けたことがあるので、ピン留め集合が優先する。
3. 削除前に使用状況を確認する。`verify-recent-chat` の各行、または疑うものすべてについて、サブエージェントを扇状に立ててトランスクリプトを読み、チャットがピン留めまたは進行中か、どのワークツリーに触れるか報告させる（**guard-the-context-window**（`principles/guard-the-context-window.md`）、トランスクリプトは bulk）。ピン留めチャットはバックグラウンドサブエージェント経由で兄弟ワークツリーへ並行ワークツリーを spawn し、サイドバーに名前が出なくても使用中である。
4. 不可逆な損失で pause。`wip:N` は N 件の tracked 未コミット編集。diff を示し先に判断を得る。クリーンなワークツリーの削除はブランチから復元可能だが、未コミット作業は消える。`scratch:N` は untracked の捨て物で削除してよいが、ファイル名を示す。Autonomy に従い、clean かつ merged かつ not-in-use は proceed。`wip` と in-use は pause。
5. 確認済み集合を prune。パスごとに `git worktree remove --force <path>`。ignored な build artifact でディレクトリが残るなら `rm -rf` し、続けて `git worktree prune`。ブランチ ref は残るので commit は失われない。`df -h /` で再確認し、一覧を取り直す。
6. シミュレータとその他の回収。シミュレータは通常次に大きい win。`xcrun simctl --set testing delete all`（XCTestDevices の clone）、`xcrun simctl delete unavailable`、古い runtime には `xcrun simctl runtime list` のあと `runtime delete <id>`。必要ならさらに: Xcode の `DerivedData` と `iOS DeviceSupport`、`~/Library/Application Support/Cursor`（`state.vscdb.backup`、ワークスペースとして開いたフォルダ名の `<root>` がある `snapshots/roots/<root>` は膨らむ）、パッケージキャッシュ（pnpm、uv、brew、yarn）。ユーザーが残すと言っていないキャッシュだけ消す。

これは slip をコードレビューで防げない、ユーザー状態を削除する唯一の playbook なので、上記ゲートがレビューになる。

**Reply:** 前後の `df -h /` と回収した容量、prune したワークツリー、保留したものごとの一行理由（どのチャットが in-use か、または未コミット作業）。

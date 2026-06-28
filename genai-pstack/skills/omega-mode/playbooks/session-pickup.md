### Session pickup

**resume point を所有する。以前の trail を読み、やり直さない。** 「take over this」「resume this conversation」「continue from <transcript path>」「you're taking over」「pick up where X left off」、cloud-agent URL handoff、続行すべき push 済みブランチ向け。

pickup は継承。以前のエージェントがコード読み、repro 実行、設計選択のコストをすでに払った。やり直すと bias check を失い context を burn。再導出の衝動に抗い、読む。

1. 以前の trail を特定。アクティブ workspace の `agent-transcripts/` 下のローカルトランスクリプト（system prompt が path を名指し。`~/.cursor/projects/*/` を glob しない。workspace 境界を越え unrelated プロジェクトの private chat を読む）、cloud-agent URL、または push 済みブランチ。metadata overview と最後のメッセージを先に読み、decision point まで scan back。長い transcript は subagent で parse し、reduced timeline をメインスレッドに保持（**principle-guard-the-context-window** スキル）。
2. operational state を再構築。branch と worktree、すでに land したもの（`git log`、base 対 `git diff`）、open todos、下された決定。以前の trail が authoritative input。再導出 bias に抗う。
3. done vs pending を diff。ship 済みと plan を比較、resume point を名指し、以前の repro を再実行せず完了作業をやり直さない。
4. 残作業を matching playbook に route し verdict を選ぶ：execution 続行、完了 recommendation を ship、以前の結論を ratify または override、失敗 run の postmortem。pickup playbook はここで終わり。route 先 playbook が残りを所有。
5. 実アーティファクト上で inherited claims を original goal に対して verify（**`/verify-done`**）。pass した以前の self-report は proof ではない。

**Reply:** 以前のエージェントが止まった場所、inherit したもの vs やり直したもの（ ideally やり直しなし）、resume point、outcome。

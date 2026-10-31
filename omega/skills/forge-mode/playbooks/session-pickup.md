### Session pickup

**resume point を自分が持つ。prior trail を読み、redo しない。**

1. prior trail を locate。active workspace の `agent-transcripts/` 下の local transcript（system prompt が path を名指す。`~/.cursor/projects/*/` を glob しない。workspace 境界を越え unrelated project の private chat を読む）、cloud-agent URL、または pushed branch。metadata overview と last messages を先に読み、decision point へ scan back。長い transcript は subagent で parse し、reduced timeline を main thread に（**principle-guard-the-context-window** skill）。
2. operational state を再構成。branch と worktree、既に land したもの（`git log`、base への `git diff`）、open todos、下した decision。prior trail は authoritative input。再 derive するバイアスに抵抗。
3. done vs pending を diff。ship したものと plan を比較、resume point を名指す。完了 work の prior repro や redo はしない。「scratch から verify」pass は trail を untrustworthy と扱っている。trail は authoritative。
4. 残 work を matching playbook に route し verdict を選ぶ: execution continue、finished recommendation の ship、prior conclusion の ratify か override、failed run の postmortem。pickup playbook はここで終わる。routed playbook が残りを own。
5. inherited claim を original goal に対して real artifact で verify（**principle-prove-it-works** skill）。pass した prior self-report は proof ではない。

**Reply:** prior agent が止まった場所、inherit したもの vs redo（理想は redo なし）、resume point、outcome。

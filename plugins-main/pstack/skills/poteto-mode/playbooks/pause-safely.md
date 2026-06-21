### Pause safely

**きれいな stop を所有する。cold-start エージェントが resume できる checkpoint を残す。** 「pause safely」「I need to go offline」「restart Cursor」「board my flight」向け。context が compact または summarize されそうなとき。これは explicit のみ。「keep going」「going to bed, keep going」「don't stop」では pause しない。それらは continue。Autonomous run が iteration ごとに checkpoint 済み。

1. safe boundary で stop。現在の atomic step を finish または back out。known-broken state で mid-edit stop しない。新しいものは開始しない。nested subagent は cancel。
2. pause のために irreversible line を越えない。すでに out していた PR と push 以外はなし。
3. 作業を durable に。uncommitted edit を current branch 上で1つの明確な `wip:` commit として commit。失われないように。tree が broken なら commit body に1行で述べる。
4. off-context で resume note を書く。intent、何をしていたか、progress と verify 済み、current state、next steps、key files、gotchas を capture。compaction trigger では `/tmp/<slug>-resume.md` のようなファイルに書く。in-context plan は summarization を survive しない。show-me-your-work trail があるなら duplicate せず指す。

**Reply:** loop のどこにいるか、disk 上 vs まだ head 内（paths、diff dump なし）、作った commit と tree が clean か、resume 時の first action。これは pause で final report ではない。resume は Session pickup playbook がこの note を読む。

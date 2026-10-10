### Pause safely

**clean stop を自分が持つ。cold-start agent が resume できる checkpoint を残す。** 明示のみ。「keep going」「going to bed, keep going」「don't stop」では pause しない。

1. safe boundary で stop。現在の atomic step を finish か back out。新しいものは始めない。nested subagent は cancel。
2. pause のため不可逆 action は取らない。PR も push も、既に out していたもの以外はしない。
3. work を durable に。uncommitted edit を current branch 上の 1 つの明確な `wip:` commit に。失わない。tree が broken なら commit body に 1 行で言う。
4. resume note を off-context に書く。intent、何をしていた、progress と verified なもの、current state、next steps、key files、gotchas。compaction trigger 用は `/tmp/<slug>-resume.md` のような file に。decision-log trail があれば duplicate せず指す。

**Reply:** loop のどこにいる、disk 上 vs まだ頭の中（path、diff dump なし）、した commit と tree が clean か、resume の first action。pause で final report ではない。

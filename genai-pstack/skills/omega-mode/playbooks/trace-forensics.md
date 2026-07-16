### Trace forensics

**artifact から診断を所有する。load、shape、原因に narrow、source に attribute。** drop された `.cpuprofile`、`Trace-*.json.gz`、`Spindump.txt`、または `.heapsnapshot` と「why is this slow / unresponsive / leaking / crashing」のペア向け。

**Runtime forensics**（live process を instrument）とは別。ここ capture はすでに存在。artifact は fixed dataset。read する。re-run しない。tooling を generic に保ち playbook portable：cpuprofile と `.json.gz` 用 DevTools または trace parser、spindump 用 text editor、heapsnapshot 用 heap tooling。

1. format を特定し right tool で load。大 artifact は subagent で parse（[`../principles/guard-the-context-window.md`](../principles/guard-the-context-window.md)）。reduced finding をメインスレッドに保持。
2. raw artifact を query 可能な形に transform。trace または heap snapshot を sqlite に dump。sample、frame、node ごとに1 row。read 前に queryable shape に到達。
3. 原因に narrow。最多 time を hold する frame を query し call tree を hot path まで walk。leak なら leaked object から GC root へ retainer chain。spindump なら on-CPU stuck または blocked thread と wait reason。
4. source に attribute。hot frame を artifact 自身の symbol で file、symbol、line に map。source mapping なし frame はまだ diagnosis ではない。symbol resolve、または artifact が carry しないと plain に述べる。
5. paired capture があるとき confirm。before/after artifact を diff し attribution が real regression であること。background noise ではない。なければ finding を artifact が support する strongest hypothesis と mark。confirmed cause ではない。
6. cited diagnosis を hand back。求められない限り fix なし。原因が分かったら Bug fix または Perf issue に route。throughput checkpoint は1行：`throughput checkpoint: n/a, read-only forensics`。

**Reply:** artifact と format、reduced finding、source location、artifact paths、paired capture が confirm したか。


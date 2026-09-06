### Runtime forensics

**診断を所有する。live process を instrument。source から theorize しない。** 「why is X leaking / spinning / slow at runtime」、heap snapshot、idle-but-busy process、intermittent glitch 向け。成果物は cited diagnosis。fix ではない。

1. control スキル経由で matching surface 上で live signal を capture：spinning process なら CPU profile、leak なら heap snapshot、visual glitch なら CDP trace。guess ではなく real artifact。
2. artifact を smoking gun に reduce：hot path 上の function、leaked object から GC root への retainer chain、input なしで fire する loop。大 artifact は subagent で parse（**guard-the-context-window** 原則スキル）。reduced finding をメインスレッドに保持。
3. 信じる前に mechanism を prove。running process 上で CDP eval 経由 instrumentation inject、または reload なし live code hotfix で仮説を安く confirm。
4. finding を source に map：file、symbol、allocate または schedule する line。
5. throughput checkpoint は1行のまま：`throughput checkpoint: n/a, read-only forensics`。

**Reply:** capture した signal、reduced finding、mechanism の prove 方法、source location、artifact paths。求められない限り fix なし。原因が分かったら Bug fix または Perf に hand back。

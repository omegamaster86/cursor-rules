### Runtime forensics

**診断を自分が持つ。live process に instrument し、source から理論で語らない。** 成果物は cited diagnosis。fix ではない。

1. control skill で matching surface 上の live signal を取得：spin する process の CPU profile、leak の heap snapshot、visual glitch の CDP trace。推測ではなく実 artifact。
2. artifact を smoking gun に縮約：hot path の function、leaked object から GC root への retainer chain、入力なしで走る loop。大きい artifact は subagent で parse（**guard-the-context-window** principle skill）。縮約した finding は main thread に残す。
3. 信じる前に mechanism を証明。実行中 process への CDP eval で instrumentation を注入、または reload せず live code を hotfix して hypothesis を安く確認。
4. finding を source に写像：file、symbol、allocate または schedule する行。
5. throughput checkpoint は 1 行のまま：`throughput checkpoint: n/a, read-only forensics`。

**Reply:** 取得した signal、縮約 finding、mechanism の証明方法、source location、artifact paths。求められなければ fix なし。原因が分かったら Bug fix または Perf に戻す。

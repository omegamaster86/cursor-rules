### Trace forensics

**artifact から診断を自分が持つ。load、shape、原因に絞り、source に attribute。**

**Runtime forensics**（live process を instrument）とは別。ここでは capture は既にある。artifact は固定 dataset。読む。再実行しない。playbook の移植性のため tooling は汎用：cpuprofile と `.json.gz` 用 DevTools や trace parser、spindump 用テキストエディタ、heapsnapshot 用 heap tooling。

1. format を特定し、適切な tool で load。大きい artifact は subagent で parse（**principle-guard-the-context-window** skill）。縮約 finding は main thread に残す。
2. raw artifact を query 可能な形に変換。trace や heap snapshot を sqlite に dump。sample、frame、node ごとに 1 行。読む前に queryable shape に到達。
3. 原因に絞る。最も時間を占める frame を query し call tree を hot path まで walk。leak なら leaked object から GC root へ retainer chain。spindump なら on-CPU または blocked の thread と wait reason。
4. source に attribute。hot frame を artifact の symbol で file、symbol、line に写像。source mapping のない frame はまだ diagnosis ではない。symbol を解決するか、artifact に載っていないと明言。
5. paired capture があるときはそれで確認。before/after artifact を diff。無ければ finding は artifact が支える最強 hypothesis とし、confirmed cause ではないとマーク。
6. cited diagnosis を返す。求められなければ fix なし。原因が分かったら Bug fix または Perf issue にルート。throughput checkpoint は 1 行：`throughput checkpoint: n/a, read-only forensics`。

**Reply:** artifact と format、縮約 finding、source location、artifact paths、paired capture で確認したかどうか。

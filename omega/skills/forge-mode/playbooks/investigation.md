### Investigation

**answer を所有する。Plan、route、write。**

読み取り専用リクエスト：「how does X work?」「why was Y built this way?」「are we sure about Z?」「should we do X or Y?」。cited explanation または recommendation を produce。code change ではない。

1. 主に **why**（設計 rationale・「why was Y built」・トレードオフ・履歴）なら **why** スキルに委譲。主に **how**（構造・フロー・配置）なら **how** スキル（narrow question は Explain mode、「are we sure?」は Critique mode）。
2. throughput checkpoint は1行のまま：`throughput checkpoint: n/a, read-only investigation`。4 item version は code-shaped work 用。
3. `how`-shaped output（Overview / Key Concepts / How It Works / Where Things Live / Gotchas）、または alternative 間 decision なら tradeoffs table 付き recommendation を produce。

PR、babysit、code change に先行しない限り `architect` なし。code change に先行するなら user に hand back し Bug fix または Feature に re-route。

**Reply:** investigation output。「are we sure?」answer なら reasons 付き real judgment。premise が wrong なら push back（Autonomy 参照）。

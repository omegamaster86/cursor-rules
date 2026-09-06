### Investigation

**answer を所有する。Plan、route、write。**

読み取り専用リクエスト：「how does X work?」「why was Y built this way?」「are we sure about Z?」「should we do X or Y?」。cited explanation または recommendation を produce。code change ではない。

1. **how** スキル経由で route（narrow question は Explain mode、「are we sure?」は Critique mode）。設計根拠の質問は `git log` / `gh pr view` で PR・コミット履歴を確認する。
2. throughput checkpoint は1行のまま：`throughput checkpoint: n/a, read-only investigation`。4 item version は code-shaped work 用。
3. `how`-shaped output（Overview / Key Concepts / How It Works / Where Things Live / Gotchas）、または alternative 間 decision なら tradeoffs table 付き recommendation を produce。

PR、babysit、code change に先行しない限り `architect` なし。code change に先行するなら user に hand back し Bug fix または Feature に re-route。

**Reply:** investigation output。「are we sure?」answer なら reasons 付き real judgment。premise が wrong なら push back（Autonomy 参照）。

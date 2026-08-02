### Bug fix

**このタスクを所有する。Plan、review、verify。** 調査と fix を subagent に delegate、リードに留まる。

科学的に。ship された各行は runtime evidence に trace。belt-and-suspenders の「効くかも」は仮説であり fix ではない。ship しない。evidence が仮説を反証したら、それが動機づけたものを revert。evidence が正当化する最小変更だけ ship。それ以上はない。Perf も同じ discipline。evidence は trace。

1. control スキル経由で matching surface 上で自分で再現（Non-negotiables）。repro をユーザーに渡さない。ユーザーに聞くよう言う debug または instrumentation protocol はこれを上書きしない。計装 runtime を自分で drive。control surface が target に届けない具体的理由を述べたうえで、drive できる限りまで drive した後だけユーザーに聞く。直接 repro しないなら force：trigger を合成、条件を tighten、または instrument して発火させる。
2. 原因を binary-search。candidate 仮説を形成し、1つ残るまで排除。`how` で affected subsystem、`git log` / `gh pr view` で regression 履歴から seed。各 pass で残 problem space を最も切る split を取り、runtime evidence を得て eliminate。program state が unclear なら instrumentation または logging を追加し、コード実行中に読む。guess しない。長いまたは stubborn な hunt は Cursor の `/loop` で drive。step-3 architect / review-orchestrator fan-out 前に、surviving *mechanism* を runtime evidence で confirm。
3. fix を plan。function boundary を越えるなら先に `architect`。触るファイルが2以上またはデータ経路が変わるなら **File change map** + **Data flow** の Mermaid を提示（[`../references/plan-diagrams.md`](../references/plan-diagrams.md)）。CreatePlan 可なら Cursor Plan に書く。specific scope で設定 bug-fix model（デフォルト `gpt-5.5-high-fast`）の subagent に implementation を delegate。diff を review。
4. 同 surface で verify。元 repro が pass。Inconclusive または wrong-surface は pass ではない。flag。ユニットテストは branch 動作を示す。バグ不在は示さない。
5. git history で failing repro が fix より先に land するよう commit を stage。diff が story を語る。**tdd** スキル参照。安価なローカル test path があるバグでは failing-test-first cadence。テストが expensive、integration-heavy、unclear なら skip。
   これが canonical **sequence-verifiable-units** 原則スキル。failing test 先、fix が上。
6. **Opening a PR** を実行。

Investigation は `how` を parallel subagent に fan-out。regression 履歴が必要なら `git`/`gh` で並列確認。

**Reply:** 何が壊れていたか、root cause、fix、verify 方法。failing-then-passing repro 出力を verbatim で paste。


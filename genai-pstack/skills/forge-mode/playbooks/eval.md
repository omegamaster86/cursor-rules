### Eval

**experiment design を所有する。Plan、blind、run、synthesize。**

Eval は promote 前に change が agent behavior に与える影響を test：新 skill variant、structural change、prompt tweak。失敗モードは observer effect。eval されていると知る agent は differently behave。candidate は blind で run 必須。

**blinding の non-negotiables：**

- candidate が見る directory、file、prompt に `eval`、`test`、`judge`、`experiment`、`rubric`、`score`、`compare`、`benchmark`、`candidate`、`multi-agent-candidates` を入れない。
- candidate prompt は organic user request に見える。meta ではなく goal を述べる。「build me a small todo cli」であって「show me how you follow the principles chain」ではない。
- chain-eliciting cue なし。適用した skills、principles、files の list を candidate に求めない。meta-prompt が citation behavior を inflate。design notes を一般に求め、self-report ではなく code shape から chain-following を grade。
- directory と slug name を sanitize。`candidate-1` や `agent-a` ではなく user が pick しうる project-shaped name。
- 他 candidate が存在することを candidate に言わない。
- judge は judging していると知ってよいが sanitized label の output のみ。model name 禁止。
- 2 variant compare：1 judge が1 scale で both sets を single pass score。どちら set か blind。異なる prompt の2 judge run は compare 不可。calibration drift。

**Steps:**

1. **Frame.** test 中 variant と success behavior を述べる。judge のみ rubric（3-6 concrete criteria）を書く。candidate から hold back。
2. **Set up sanitized environments.** variant 配置済み per-candidate working dir。organic task が持つ context を plant：project skeleton、candidate が naturally read する skills。
3. **Author one organic prompt.** user が type する内容。measure 対象の leakage なし。
4. **multi-agent-candidates** スキル Phase B に従い N parallel candidate を different models で spawn。各 sanitized dir で work。各に same prompt。
5. **multi-agent-candidates** スキル Phase C に従い different model family で1 blinded judge spawn。judge は sanitized label と rubric の output を見る。model name 禁止。
6. **transcript から chain を verify。self-report ではない。** 各 candidate の local transcript を active workspace の `agent-transcripts/` 下で read（system prompt が path を名指し）。`~/.cursor/projects/*/` を glob しない。workspace 境界を越え unrelated プロジェクトの private chat を読む。各 candidate が actually open した file を見る。principle cite は leaf skill read ではない。read も apply ではない。actually read した files ＋ code shape から chain-following を grade。candidate 自身の claim から never。
7. **すべての candidate output を end to end で自分で read。** judge verdict と compare。disagreement は model bias または rubric ambiguous。synthesize。

**Reply:** test 中 variant、rubric、per-candidate notes、judge verdict、synthesis、variant promote 可否 recommendation。

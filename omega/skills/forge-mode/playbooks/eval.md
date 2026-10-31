### Eval

**実験設計を自分が持つ。計画、blind、実行、合成。**

**blinding の Non-negotiables:**

- candidate が見る directory、file、prompt に `eval`、`test`、`judge`、`experiment`、`rubric`、`score`、`compare`、`benchmark`、`candidate`、`multi-agent-candidates` を入れない。
- candidate prompt は organic user request に見える。goal を述べ、meta は述べない。
- chain-eliciting cue なし。どの skill、principle、file を適用したか列挙させない。design notes は一般に求め、chain-following は code shape から grade。self-report からではない。
- directory と slug 名を sanitize。ユーザーが選びそうな project 形の名前。
- candidate に他 candidate の存在を言わない。
- judge は judging だと知ってよいが、出力は sanitized label だけ。model 名は見ない。
- 2 variant 比較：1 judge が 1 scale で両 set を single pass で score。どちらの set か blind。

**Steps:**

1. **Frame.** テスト中の variant と success とする挙動を述べる。judge 用 rubric（3–6 の concrete criteria）を書く。candidate からは伏せる。
2. **Set up sanitized environments.** variant を入れた candidate ごとの working dir。organic task が持つ context を植える：project skeleton、candidate が自然に読む skill。
3. **1 つの organic prompt を書く。** ユーザーが打つ内容。何を測っているかの leakage なし。
4. **multi-agent-candidates** skill の Phase B に沿い、異なる model で N 並列 candidate を spawn。各々独自 sanitized dir。同一 prompt。
5. **multi-agent-candidates** skill の Phase C に沿い、別 model family で 1 blinded judge を spawn。judge は sanitized label と rubric だけ。model 名は見ない。
6. **transcript から chain を検証。self-report ではない。** 各 candidate の local transcript を active workspace の `agent-transcripts/` 下で読む（system prompt がこの path を名指す）。`~/.cursor/projects/*/` を glob しない。workspace 境界を越え unrelated project の private chat を読む。各 candidate が実際に開いた file を見る。chain-following は本当に読んだ file と code shape から grade。candidate 自身の主張からはしない。
7. **全 candidate 出力を end to end で自分で読む。** judge verdict と比較。不一致は model bias または rubric の曖昧さ。合成。

**Reply:** テスト中 variant、rubric、candidate ごとの notes、judge verdict、合成、variant を promote すべきかの recommendation。

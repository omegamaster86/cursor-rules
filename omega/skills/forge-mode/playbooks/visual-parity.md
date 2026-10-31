### Visual parity

**pixel-exact equivalence を自分が持つ。baseline が spec。触らない。** equivalence は目ではなく image diff で検証。

1. migration の前に先に baseline を確立：現 component の各 state を screenshot する visual regression harness、2 実装を合わせるときは target も。baseline なしに parity 主張なし。follow-up ではなく blocking prerequisite。
2. anti-shortcut 条項を述べて守る：harness 改変なし、baseline 改ざんなし、diff を通すための component 再構成なし。baseline が誤って見えるなら止めて聞く。編集しない。
3. 1 component ずつ migrate。worktree 間で並列化、component ごとに 1 owner（**separate-before-serializing-shared-state** principle skill）。shared primitive は blocking phase で先に migrate。
4. control skill で matching surface 上、各 component を baseline に対して image diff で検証。nonzero diff は fail。pixel delta を investigate。component ごとに `/loop` して diff が zero になるまで。
5. component ごと、または安全な batch ごとに **Opening a PR** を実行。

**Reply:** migrate した component、各 diff 結果、baseline harness の場所、残り。

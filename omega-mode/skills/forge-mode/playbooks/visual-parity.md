### Visual parity

**pixel-exact equivalence を所有する。baseline が spec。触らない。** 「make X match Y exactly」、styling-system migration、framework 間 UI port 向け。等価性は eye ではなく image diff で verify。

1. migration 前に baseline を establish：current component の states 横断 screenshot の visual regression harness、2 implementation match 時は target も。baseline なし parity claim なし。blocking prerequisite。follow-up ではない。
2. anti-shortcut clause を stated し hold：harness modification なし、baseline tampering なし、diff pass のため component restructure なし。baseline が wrong に見えたら stop して ask。edit しない。
3. 1 component ずつ migrate。各 independent artifact。worktree 横断 parallelize、component ごとに1 owner。shared primitive は blocking phase として先に migrate。
4. control スキル経由 matching surface 上 image diff で各 component を baseline に対 verify。nonzero diff は fail。pixel delta を investigate。wave through しない。diff zero まで component ごとに `/loop`。
5. component または safe batch ごとに **Opening a PR**。

**Reply:** migrate した components、各 diff result、baseline harness location、残り。

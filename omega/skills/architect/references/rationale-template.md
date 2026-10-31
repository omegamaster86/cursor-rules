# Rationale template

型スケッチと併送する prose。1 ページ。sentence-case 見出し、boilerplate なし。イタリック注記を実内容に置き換える。

## Problem

*1 段落。何をしようとしているか、既存システムや constraint の何が形状を non-obvious にするか。[Phase A](../SKILL.md#phase-a-ground-the-problem) で設計が守るべき constraint（interop する既存型、壊せない caller、境界を越えた invariant）が出たらここに名指しし、読者が同じ constraint を見るようにする。*

## Usage (caller's view)

*型スケッチより先に書く。consumer が読む README または quickstart と、自分のコード内の 2〜3 の realistic call site。何を import し、何を呼び、何が返るか。[Shape](#shape) の型スケッチはここから導く。両者は一致させる。ずれたら usage に合わせてスケッチを reconcile し、逆はしない。caller の体験が spec。型はそれに従う。*

## Shape

*推奨 architecture。まず data structure。次に signature を通る data flow。load-bearing 決定を名指し。型に encode された invariant、validation の所在、意図的にしないことを述べる。interface depth を明示的に判断。public surface が隠す複雑さ、caller に残る露出、interface が必要以上に大きくない理由を述べる。各決定の背後の principle を引用（例: `per boundary-discipline`）。restate しない。*

## Synthesis decision

*[arena](../multi-agent-candidates/SKILL.md) が埋める。どの candidate が base になりなぜ、他から何を adapt し、何を reject しなぜ、を記録。*

## Tradeoffs accepted

*選んだ形状が受け入れる tradeoff を 1 bullet ずつ。形式: 「X を受け入れ Y と引き換えに」。将来の読者が oversight と誤解しうるものを名指し、 premature optimization や premature simplification に見えるものも含む。*

## Alternatives considered

*必須。具体的な代替形状を最低 1 つ、なぜ負けたか 1 行で。各代替を implementation の単純さだけでなく interface depth で判断。caller に露出する複雑さと隠す複雑さを名指し。design space に real contender があったら 2〜3 代替がここに属する。constraint が答を強いたときは 1 つでよく、結論は「viable な形状はこれだけだった理由…」で。同じ形状の flavor 列挙は避ける。ここは選んだ形状が検討して reject した設計代替であり、他 runner candidate ではない。*

## Open questions and risks

*スケッチ中に気づき、人が実装前に weigh すべきことと flag すべき risk。assertion ではなく question で書き、人の答えが resolution になるように。*

## Next implementation step

*スケッチに対して最初に build するもの。1 文。synthesis の直後（checkpoint を opt in したなら Phase D sign-off の後）にすぐ書き始めるもの。*

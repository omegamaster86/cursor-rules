# Architect runner prompt

orchestrator は Phase B でこのファイルを各 parallel candidate runner に渡し、周辺の変数入力を埋める: タスク、Phase A grounding artifact、隔離 working directory、出力先 path。working directory は可能なら git worktree、なければ sketch dir 下の runner ごとの subdirectory。重要なのは candidate 間の独立性。

architect の parallel exploration で 1 candidate 設計を出す。**architect** スキルを最初に全文読む。それがあなたの中の workflow。candidate design package を出力: 型スケッチ、関数シグネチャ、module map、[`rationale-template.md`](rationale-template.md) の形の prose rationale。

次の discipline を適用する。orchestrator はこれらの軸で candidate を比較して base を選ぶ。

- caller の usage を先。型の前に README 風 usage と 2〜3 の real call site を書き、型スケッチをそこから導く。usage が spec。一致させ、ずれたら usage に合わせてスケッチを reconcile。
- data structure を先。core 型を正しくするとコードは自明になる。各 dominant access pattern を提案構造で trace。「後で map / index / cache を足す」が答えなら構造が誤り。
- interface depth。public surface のサイズに対して背後に隠れた capability を比較。実装が単純でなくても complexity を callee に引き込む単純 interface を選ぶ。public API に transport や wire 型を置かない。interface の背後で domain 型に parse。
- shared state: 2 actor が両方 write しうるなら「何が起きる？」と問う。答えが「nothing」でなければ、**separate-before-serializing-shared-state** principle スキルに従い、read 境界での merge 付き per-actor state をデフォルトに。
- 境界を見える化する。本体は `not implemented` error、難しい logic は `// TODO` pseudocode、intent と invariant を述べる doc comment。読者は型とシグネチャだけで input から output まで trace できること。
- invariant を型に encode: **encode-lessons-in-structure** principle スキルに従い hard-to-misuse 型 > runtime check > prose comment。
- 境界で validate、内側は型を信頼、**boundary-discipline** principle スキルに従う。business logic は pure function。shell は薄く。
- invariant ごとに single source of truth。sync では derive。
- 該当なら **make-operations-idempotent** principle スキルに従い idempotent state transition。操作が 2 回走る・途中 crash したらどうなるかを問う。
- 短い call chain。flow の trace に 3 ファイル超が要るなら hierarchy を flatten、**laziness-protocol** と **minimize-reader-load** principle スキルに従う。

あなたは異なるモデル上の parallel runner の 1 つ。自分のモデルが出せる最良の設計を出す。他に hedge しない。candidate 間の差が base 選択と graft の signal。safe に見える中間に収束すると exploration を潰す。

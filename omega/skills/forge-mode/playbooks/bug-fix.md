### Bug fix

**このタスクを自分が持つ。計画、レビュー、検証。** investigation と fix は subagent に委譲し、リードは自分が続ける。

科学的に。出荷する各行は runtime evidence に辿れる。効く「かも」という belt-and-suspenders は hypothesis であって fix ではない。出荷しない。evidence が hypothesis を否定したら、それを動かした変更は revert。evidence が正当化する最小変更だけ出荷。それ以上はしない。

1. control skill（Non-negotiables）で matching surface 上、自分で再現する。debug や instrumentation protocol がユーザー再現を求めても例外なし。control surface がターゲットに届かない具体的理由を述べたうえでだけユーザーに聞く。それも control を限界まで使った後。直接再現できなければ trigger を合成、条件を絞る、または instrument して発火させる。
2. 原因を binary-search。候補 hypothesis を立て、潰して 1 つ残す。影響 subsystem への `how` と regression 履歴の **why** skill で seed。各 pass で残り problem space を最も切る分割を取り、runtime evidence を得て排除。program state が不明なら instrumentation や logging を足し、実行中に読む。推測しない。長い・粘る hunt は Cursor の `/loop` で回す。step 3 の architect / review-orchestrator-triple-hybrid fan-out の前に、残った *mechanism* を runtime evidence で確認。
3. fix を計画。function boundary を跨ぐなら先に `architect`。設定済み bug-fix model（デフォルト `cursor-grok-4.6-medium`）の subagent に具体 scope で実装を委譲。
4. 同じ surface で検証。元の repro が通る。「Inconclusive」や wrong-surface は pass ではない。フラグする。unit test は branch 挙動を示す。bug の不在は示さない。
5. commit を stage し、git 履歴で failing repro が fix の前に land する。**tdd** skill の failing-test-first cadence（bug に安い local test path があるとき）。test が高コスト・integration 重・不明瞭なら skip。
   これが canonical **sequence-verifiable-units** principle skill。failing test 先、fix はその上。
6. **Opening a PR** を実行。

**Reply:** 何が壊れていた、root cause、fix、検証方法。failing→passing の repro 出力を逐語で貼る。

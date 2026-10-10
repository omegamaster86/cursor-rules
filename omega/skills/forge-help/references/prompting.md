# Word the prompt

prompt は intent と done の check を述べる。playbook が step を供するので、plain 数文が spec に勝る。

## Put in

- goal。何が誤っているか、ユーザーが何を望むかを言う。
- done check。pass または fail できる。「make it better」や duration は check ではない。
- 示す proof。real command 出力、flow の video、保存値、before/after 数値を求める。
- ユーザーが既に知っていること。symptom、repro step、log、link はエージェントの search を省く。
- 実 constraint。「repro first」「don't change any code yet」「zero behavior change」「let me review before proceeding」はそれぞれエージェントの行動を変える。

## Leave out

- how。達成することを言い、より良い道を見つける余地を残す。
- skill や step のリスト。手書き順は playbook が保つ step を落とす・並べ替える。1 選択を override するときだけ skill を名指す。
- ユーザーの原因 theory は、エージェントが問題を restate するまで。述べた guess は search を狭める。

## Load the context first

- noisy report なら、何かする前に underlying issue を自分の言葉・plain English で restate するようエージェントに求める。misreading は code 前に出る。
- fresh chat なら `/recall` で topic の過去作業。旧 chat は新エージェントに無い context を持つ。
- 馴染みのない code を変える前に `/how` で mechanics、`/why` で理由。traced model 無しのエージェントは最初の plausible 箇所で symptom を直す。
- `/teach` で選択の case を求める、例「cause ではなく symptom を直すと説得して」。summary より case の方が check しやすい。

## Design before the plan

- 最初の設計を採らない。UI なら screenshot または video 付きで数 option の prototype を求め、evidence から選ぶ。
- prototype に open question を答えさせる。abstract plan を adversarial に review しない; reviewer は起きない risk を invent する。
- shared package または API なら README または tutorial を先に、そこから code に戻る。doc がエージェントが自分に対して check する target になる。
- 設計が settle した後だけ plan を求める。plan の各 step は check で終わる。

## Follow up short

- 「do it」「continue」「keep going until done」は chat が task を持っていれば十分な prompt。
- subject が変わるときは「new task」で始める。そうでなければ mode は message を次の step として扱う。

## Before stepping away

- 「im going to bed」「im stepping away」と言いエージェントの質問を止める。
- done を各 iteration が走らせる check として書き、`/loop` にその predicate を渡す。
- 名指し base から fresh worktree を求める。
- commit 前に止まることを事前に答える、例「don't ask me before committing」。
- 後で監査する decision log を求める。
- exit を渡す:「数時間 truly stuck なら stop して why を書き上げる」。

## Steer in one line

- goal を restate:「goal は repro だと言った。fix はまだ求めていない。」
- principle を名指す:「prove it works を適用。build log ではなく real output を見せて。」
- principle 名はエージェントが既に rule を読んだから効く。返答は rule が変えた決定を名指す。

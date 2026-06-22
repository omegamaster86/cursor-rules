### Autonomous run

**exit condition を所有する。done を定義し、止まらず drive。** 「going to bed」/「run until done」/「/loop until X」向け。

1. 最初の iteration 前に exit condition を checkable predicate として述べる（tests green、repro fixed、all N PRs merged、pixel-diff zero）。
2. Cursor の `/loop` コマンド（pstack スキルではなく組み込み）で wake mechanism を選ぶ。watch する event（CI、merge、ref advance）には event で wake する watcher subagent、long time-based heartbeat を fallback。event なしは re-check する価値がある間隔の fixed-interval heartbeat。
3. 各 iteration は evidence が正当化する最小変更、predicate に対して verify、advanced なら commit、助けなかった change は discard。belt-and-suspenders の「効くかも」は revert。ride させない。
   **sequence-verifiable-units** 原則スキルで work を sequence。end で batch check せず各 unit を verify。
4. 各 iteration **show-me-your-work** スキルで checkpoint。what changed と predicate が動いたかの row。
5. predicate が met なら stop。plateau は stop ではない。continue し approach を pivot して push past。genuine dead end を surface。spin しない。victory 宣言のため predicate を relax しない。

**Reply:** exit condition、iterations run、land したもの、discard したもの、final predicate state。

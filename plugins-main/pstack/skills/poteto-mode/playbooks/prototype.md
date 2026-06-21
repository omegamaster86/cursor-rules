### Prototype

**設計決定を所有する。コードではない。prototype は throwaway instrument。real build は Feature が follow。** 「prototype」「mock it up」「sketch this」「try this layout」、commit 前に UI、interaction、layout を explore 向け。また empirical fork（どの動作、タイミング、アプローチか）を、人間に聞く代わりに observe して settle 向け。quick sketch が答えられる質問を otherwise 聞くとき。

Laziness Protocol の「smallest change」と verification bar が invert する唯一の playbook。speed over polish。code quality は matter しない。planning なし。rigor は right design を安く選ぶこと。bold に：ユーザーが求めていない variation を propose、approach を throw して別を try。

1. prototype が存在する decision を scope：layout、interaction、density、または empirical fork なら behavior、timing、approach。decision なし means no prototype。Feature に route。
2. design space が open なら reference を gather。prior art を search、moodboard（themes、palettes、layouts）を summarize、build 前にユーザーに direction を pick させる。direction が set なら skip。
3. isolated scratch dir に throwaway build。production source から separate。visual decision なら vanilla HTML/CSS/JS または idea を render する lightest stack、CDN deps、hot reload dev server。behavioral または timing decision なら question を exercise する smallest script。production framework、tests、abstractions なし。
4. alternative を compare するとき、1 switcher（buttons または keypress）の背後に build。各 variant に label で user が名指しできるように。これが安くなった **exhaust-the-design-space** 原則スキル。
5. matching surface で verify。visual decision なら control スキル経由で各 variant を screenshot、interaction を drive。eye が test。behavioral または timing decision なら decide しているものを logging timing、output print、render watch で observe。ここ observation が test。assertion ではない。
6. alternative、tradeoff、recommendation を present。output は decision ＋ throwaway artifact。shippable code ではない。chosen direction を **Feature**（または shape なら `architect`）に real build へ hand。

**Reply:** explore した variants、evidence（visual なら screenshots、behavioral なら observed output または timing）、tradeoffs、recommendation、scratch path。prototype は throwaway と plain に述べる。

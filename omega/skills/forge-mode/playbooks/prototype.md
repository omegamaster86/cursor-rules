### Prototype

**設計判断を自分が持つ。コードではない。prototype は捨てる instrument。本 build は Feature が続く。**

Laziness Protocol の「最小変更」と verification bar が逆転する唯一の playbook。speed 優先、code quality は問わない、planning なし。rigor は安く正しい design を選ぶこと。ユーザーが求めていない variation を提案し、approach を捨てて別を試す。

1. prototype が存在する判断を scope：どの layout、interaction、density、empirical fork ならどの behavior、timing、approach。判断が無ければ prototype なし。Feature にルート。
2. design space が開いているとき reference を集める。prior art を検索、theme・palette・layout の moodboard を要約、build 前にユーザーに方向を選ばせる。方向が決まっていれば skip。
3. production source から離れた isolated scratch dir で throwaway build。visual 判断なら vanilla HTML/CSS/JS または idea を描く最軽 stack、CDN deps、hot reload 付き dev server。behavior や timing 判断なら質問を試す最小 script。production framework なし、test なし、abstraction なし。
4. 代替を比較するときは 1 switcher（button や keypress）の背後に build。各 variant に label。**exhaust-the-design-space** principle skill を安く実践。
5. matching surface で検証。visual なら control skill で各 variant を screenshot し interaction を drive。behavior/timing なら timing を log、出力を print、render を見て決めるものを観察。ここでの test は assertion ではなく観察。
6. 代替、tradeoff、recommendation を提示。出力は decision と throwaway artifact。出荷可能 code ではない。選んだ方向を **Feature**（または shape なら `architect`）に渡して本 build。

**Reply:** 探索した variant、evidence（visual なら screenshot、behavior なら観察した出力や timing）、tradeoff、recommendation、scratch path。prototype は throwaway と明言。

---
name: unslop
description: AI っぽい文体・記号・ filler を削る。ドキュメント、PR 本文、チャット返信の推敲時に /unslop。
disable-model-invocation: true
---

# Unslop

意味とトーンを保ちつつ、下のパターンを探して書き直す。

## 検出して直すパターン

ルール番号は他スキルが参照する安定 ID。削除したルールの番号は空番にする。

### 内容

3. **表面的な -ing 句。** "highlighting...", "ensuring...", "reflecting...", "showcasing...", "fostering..." など。削除するか、根拠となる具体に展開する。
5. **曖昧な出所。** "Experts believe", "Industry reports suggest", "Some critics argue" など。出典を書くか削除する。

### 語彙・表現

7. **AI 語彙。** Additionally, crucial, delve, enduring, enhance, fostering, garner, interplay, intricate, landscape（抽象用法）, pivotal, showcase, tapestry（抽象用法）, testament, underscore, vibrant など。平易な語に置き換える。
8. **「is」の回りくどい言い方。** "serves as", "stands as", "boasts", "features" など。"is" か "has" にする。
9. **「Not just X, but Y.」** 比較枠を外し、要点だけ述べる。
10. **三つ揃え。** 無理に 3 つにまとめない。自然な数にする。
11. **同義語のローテーション。** 同じ段落で protagonist, main character, central figure, hero を行き来しない。一つ選んで繰り返す。
12. **偽のレンジ。** X と Y が意味のある尺度上にない "from X to Y"。トピックを直接列挙する。

### スタイル

13. **em dash の多用。** em dash は使わない。句点かコンマだけ（括弧・en dash・ハイフン代用のダッシュも不可）。区切りが要るなら文を終えるかコンマにする。
14. **コロンの多用。** リストや例の前のコロンは可。文中の接続としてのコロンは不可。「If you're coming from traditional automation: instead of registering event handlers, you describe conditions」のコロンは何も足していない。比較枠なしで要点だけ立たせる。「Describing when the scheduler should fire works best as plain English。」同じ意味で句読点の crutch がない。
15. **太字の多用。** 固有名詞や略語をすべて太字にしない。
16. **インラインヘッダー風リスト。** 太字ラベル＋コロンで行を言い換えているのが tell 例: "**Performance:** Performance improved..."。散文に直す。太字の導入がピリオドで終わり項目名になり、その後に本当に新しい情報が続く形（"**Schema in TypeScript.** Tables live in one file."）は tell ではない。
17. **見出しの Title Case。** sentence case を使う。
18. **装飾用 emoji。** 見出しや箇条書きから外す。
19. **曲がった引用符。** 直線の引用符を使う。

### コミュニケーションの型

20. **チャットボット定型。** "I hope this helps!", "Let me know if...", "Of course!", "Certainly!", "Found the smoking gun!" などは削除。
22. **へつらい口調。** "Great question! You're absolutely right!" など。要点に直接答える。

### Filler

23. **Filler 句。** "In order to" は "To"。"Due to the fact that" は "Because"。"It is important to note that" は削除。
24. **過剰なヘッジ。** "could potentially possibly be argued that it might" は "may" 程度にする。
25. **汎用の結び。** "The future looks bright." など。具体的な計画や事実を書く。

### 隠語

26. **抽象比喩名詞。** substrate（基盤）、wedge、wedge in（追加）、vector（方法）、locus、vantage、nexus、primitive（名詞用法）、harness（比喩）、surface（"API surface" など）、bedrock、scaffolding（比喩）、modality、paradigm、gold-plating（必要以上）、ratchet（比喩。実機構の名前か、締まるだけの上限）、evacuate（コード移動は move out）、endgame（最終段階）、north star、flywheel など。技術っぽく見えるが多くはもっと具体の語がある。具体語を選ぶ。

### 平易な言い方

27. **感じ方ではなく、何をするか。** "the database stays close at hand", "SQL you can read", "types that follow your schema" は感覚の名前。直し方は機構か数値: "`.toSQL()` returns the exact string sent to the database", "a column rename fails the build"。読者に何をすべきか・知るべきかを書き、それを具体の指示・事実・数値で書く。そう言い換えられなければ削る。もう一つのチェック: 文が他プロジェクトのドキュにそのまま載せられるなら、このプロジェクトについて何も言っていない。削る。
28. **詰まった文は短くまたは分割。** 読者が戻って解析するなら二文に分けるか節を落とす。一文一アイデア。
29. **能動態。** 優先する。"is/are/was/were + 過去分詞" は actor を出す: "queries are validated" → "the compiler validates queries"、"the file is parsed by the loader" → "the loader parses the file"。受動は actor が不明か本当に不要なときだけ。
30. **副詞を削るか、動詞を強くする。** "runs quickly" は "is fast" か数値、"significantly improves" は測定した差分。弱い動詞を副詞で支えているなら動詞が間違っている。
31. **平易な語を選ぶ。** "utilize" と "leverage" は "use"、"facilitate" は "help"、"numerous" は "many"、"in the event that" は "if"。上品な同義語のほうが明確になることは稀。
32. **作り物の文体。** 直訳できるのに比喩や装い: 警句（"wire it or delete it"）、効果のための修辞的断片、コードの人格化（"the plan holds it"）、比喩動詞（"rides along", "stands on"）、定型の枠組み。「A dial worth turning」は "a parameter worth varying"。言いたいことをそのまま書く。比喩名詞はルール 26。
33. **過剰な圧縮。** 冠詞や動詞の脱落、無動詞断片、記号語、読者にデコードさせる略語。「Parser rejects bad date → exit 2, no write」は "The parser rejects a bad date, exits with code 2, and writes nothing." 冠詞と動詞のある完全な文にし、矢印と略語は書き出す。

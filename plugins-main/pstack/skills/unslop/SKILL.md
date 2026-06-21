---
name: unslop
description: あらゆる文章から AI 臭を削る。常に適用すること。
---

# Unslop

AI パターンを除去し、人間の声を加えるよう文章を編集する。

## プロセス

1. 下記パターンをスキャン。
2. 書き直す。意味を保ち、意図したトーンに合わせる。
3. 魂を加える（次節）。
4. 自己監査:「何がこれを明らかに AI 生成にしているか？」残りの tell を直す。

## 魂を加える

パターン除去は半分の仕事。無味乾燥で声のない文章も同様に明らか。

- **意見を持つ。** 事実を中立に列挙するより反応する。
- **リズムを変える。** 短い文。次に時間をかける長い文。混ぜる。
- **複雑さを認める。** 「印象的だが少し不安でもある」は「印象的」より良い。
- **合うときは「私」を使う。** 一人称は非プロフェッショナルではない。
- **少し乱れを入れる。** 完璧な構造は算法的に感じる。
- **具体に。** 「これは心配」ではなく「エージェントが午前3時に回り続けるのは何か不安がある」。

## 検出して直すパターン

### 内容

1. **重要性のインフレ。** "pivotal moment"、"testament to"、"evolving landscape"、"setting the stage for"、"indelible mark"、"deeply rooted"。大げささを削り、起きたことを述べる。
2. **知名度の名前ドロップ。** 文脈なくメディアを列挙。1 つ選び、何と言ったか述べる。
3. **表面的な -ing 句。** "highlighting..."、"ensuring..."、"reflecting..."、"showcasing..."、"fostering..."。削除するか実ソースで展開。
4. **宣伝文句。** "nestled"、"vibrant"、"breathtaking"、"groundbreaking"、"renowned"、"stunning"、"must-visit"。中立な記述を使う。
5. **曖昧な帰属。** "Experts believe"、"Industry reports suggest"、"Some critics argue"。出典を名指すか削除。
6. **型にはまった課題。** "Despite challenges... continues to thrive." 具体的事実に置き換える。

### 言語

7. **AI 語彙。** Additionally、crucial、delve、enduring、enhance、fostering、garner、interplay、intricate、landscape（抽象）、pivotal、showcase、tapestry（抽象）、testament、underscore、vibrant。平易な語に置き換える。
8. **コピュラ回避。** "serves as"、"stands as"、"boasts"、"features"。"is" か "has" と言う。
9. **否定的並列。** "It's not just X, it's Y." 直接要点を述べる。
10. **三の法則。** 無理に三つ組にする。自然な数を使う。
11. **同義語サイクル。** 1 段落で protagonist、main character、central figure、hero。1 つ選び繰り返す。
12. **偽の範囲。** X と Y が意味ある尺度上にない "from X to Y"。直接列挙。

### スタイル

13. **ダッシュの乱用。** ダッシュは避ける。ピリオドかカンマのみ（括弧、エンダッシュ、ハイフンダッシュ代替なし）。ダッシュは AI tell。括弧に替えても tell の入れ替えに過ぎない。分離が要るなら文を終えるかカンマ。
14. **コロンの乱用。** リストや例の前のコロンは可。文中コネクタとしては不可。"If you're coming from traditional automation: instead of registering event handlers, you describe conditions" はコロンで何も足さない。比較枠なしで要点が立つよう書き換える。"Describing when the scheduler should fire works best as plain English." 同じ意味、拐杖の句読点なし。
15. **太字の乱用。** すべての固有名詞や頭字語を太字にしない。
16. **インラインヘッダリスト。** tell は太字ラベルとコロンが行を言い換えること:"**Performance:** Performance improved..."。散文に変換。太字のリードインがピリオドで終わり項目を名指し、その後に本当に新しい詳細が続く（"**Schema in TypeScript.** Tables live in one file."）は可、tell ではない。
17. **タイトルケース見出し。** sentence case を使う。
18. **装飾絵文字。** 見出しと箇条から除去。
19. **曲線引用符。** 直線引用符に置き換える。

### コミュニケーションの痕跡

20. **チャットボット句。** "I hope this helps!"、"Let me know if..."、"Of course!"、"Certainly!"、"Found the smoking gun!" 除去。
21. **打ち切り免責。** "While specific details are limited..." ソースを探すか削除。
22. **おべっかトーン。** "Great question! You're absolutely right!" 直接応答。

### フィラー

23. **フィラー句。** "In order to" → "To"。"Due to the fact that" → "Because"。"It is important to note that" は削除。
24. **過剰ヘッジ。** "could potentially possibly be argued that it might" → "may"。
25. **汎用結論。** "The future looks bright." 具体的計画か事実を述べる。

### ジャーゴン

26. **抽象比喩名詞。** Substrate、wedge、vector、locus、vantage、nexus、primitive（名詞）、harness（比喩）、surface（"API surface"）、bedrock、scaffolding（比喩）、modality、paradigm、gold-plating。技術的に読めても大抵もっと平易な具体語がある。"Substrate" → "base"。"Wedge in" → "add"。"Vector" → "way" か "method"。"Gold-plating" → "more than the job needs"。具体語を選ぶ。

### 平易な言葉

27. **具体を言う。** 単純な要点を抽象枠で包まない。何をするかではなくどう感じるかを述べない。"the database stays close at hand"、"SQL you can read"、"types that follow your schema" は感覚の名前。修正は仕組みか数値:"`.toSQL()` returns the exact string sent to the database"、"a column rename fails the build"。読者に何をする・知るべきかを問い、それを書く。具体指示・事実・数値に言い換えられなければ削る。
28. **密な文を短くまたは分割。** 読者が解析のために戻るなら二つに割るか節を落とす。1 文 1 考え。
29. **能動態。** 優先。"is/are/was/were + 過去分詞" を捕まえ actor を名指す:"queries are validated" → "the compiler validates queries"、"the file is parsed by the loader" → "the loader parses the file"。actor が不明か本当に重要でないときだけ受動態。
30. **副詞を削るか、より強い動詞。** "runs quickly" → "is fast" か数値。"significantly improves" → 測定された差分。弱い動詞を支える副詞は動詞が間違いのサイン。
31. **平易な語を優先。** "utilize" → "use"、"leverage" → "use"、"facilitate" → "help"、"numerous" → "many"、"in the event that" → "if"。派手な同義語はめったに明瞭ではない。

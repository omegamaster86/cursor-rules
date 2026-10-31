### Authoring or modifying a skill

**skill の voice を自分が持つ。**

1. **create-skill** skill を使う（SKILL.md 執筆用の Cursor 組み込み）。
2. skill を validate：frontmatter に `name` と `description`、参照 file が存在、cross-skill link が resolve。
3. structural なら test case。subjective なら skip。
4. **Opening a PR** を実行。

迷ったら delete。判断を変える prose だけ残す。やることを言い、理由は skip。rule がそれなしで混乱するときだけ説明。tone は scope に合わせる。**encode-lessons-in-structure** principle skill に沿い structural source（types、README、config）を指す。他 skill は path で delegate。restate しない。繰り返し当たる workflow が未 capture → 新 skill を提案。

**Reply:** skill の要約、主要 design decision、validation notes。

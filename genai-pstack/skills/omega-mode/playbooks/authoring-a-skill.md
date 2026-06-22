### Authoring or modifying a skill

**スキルの voice を所有する。** エージェント向け散文は human 散文より bar が高い。役に立たない文は instruction になる。

1. **create-skill** スキル（SKILL.md 作成用 Cursor 組み込み）を使用。
2. スキルを validate：frontmatter に `name` と `description`、参照ファイル存在、cross-skill リンク resolve。
3. structural なら test case。subjective なら skip。
4. **Opening a PR** を実行。

迷ったら delete。散文は決定を変えることで keep を earn。tone を scope に match。structural source（types、READMEs、config）を指す。hardcode 詳細は stale。**encode-lessons-in-structure** 原則スキル。path で他スキルに delegate。restate しない。繰り返し当たる workflow で capture されていない → 新スキルを propose。

**Reply:** スキル要約、key design decisions、validation notes。

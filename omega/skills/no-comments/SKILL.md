---
name: no-comments
description: コメントの read-only 査読（削除しない）。冗長・抑制コメントの指摘レポート。/no-comments。コメント削除はユーザーが明示したときだけ。
disable-model-invocation: true
---

# No comments（査読のみ）

**omega 方針: コメントはエージェントが勝手に消さない。** 本スキルは Sicko による **レポート** のみ。コメント本文の削除・短文化・encode 後の削除は、ユーザーがファイルや行を明示した場合だけ行う。

## Scope

呼び出し元のファイルまたは diff。なければベースブランチ（既定 `main`）との diff と作業ツリーを使う。

## Steps

1. `Task` を `subagent_type: "comment-sicko"` で起動。scope を渡す。サブエージェントの reasoning / speed は **forge-mode** スキルの Subagents 節に従う。ルールの再掲はしない。
2. レポートを要約してユーザーに渡す。**レポートを理由にコメントを削除しない。** `MUST KILL` や削除候補は「要検討」として扱い、ユーザーが GO と言うまでファイルを変えない。
3. ユーザーが **特定コメントの削除または encode** を明示したときだけ、その指示どおり最小の編集を行う（型・test・lint へのエンコードは **`principle-encode-lessons-in-structure`** に沿う）。
4. 報告: 査読した範囲、Keep / 要検討の件数、ユーザー指示で実施した変更（無ければ「コメント変更なし」）。
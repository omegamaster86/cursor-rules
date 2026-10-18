---
name: no-comments
description: Comment Sicko を起動し、受理した指摘を直す。制約コメントはエンコード提案。/no-comments。
disable-model-invocation: true
---

# No comments

Comment Sicko を起動する。受理した指摘にだけ手を入れる。

Comment Sicko の判断をそのまま信頼する。

## Scope

呼び出し元のファイルまたは diff。なければベースブランチ（既定 `main`）との diff と作業ツリーを使う。

## Steps

1. `Task` を `subagent_type: "comment-sicko"` で起動。scope を渡す。サブエージェントの reasoning / speed は **forge-mode** スキルの Subagents 節に従う。ルールの再掲はしない。
2. レポートと diff を見る。アプリケーションコードの編集、スコープ逸脱、例外で守られた削除、誤った `MUST KILL` 理由、意図的に残したコードを有罪にするフラグは拒否する。当社コードの驚きに対する reshape フラグは actionable のまま。そういうコメントは復元しない。keep は変更不能なものについて証明があるときだけ残す。スコープ内の lint / TypeScript 抑制の見落としを監査する。正しさ・安全の抑制は actionable `MUST KILL` のまま。復元は exact な例外とスコープ内証明があるときだけ。薄い `IMPORTANT` / `do not remove` の kill/keep の前に `/how` または `/why` でシンボルを走らせる。kill が曖昧なら復元しない。keep が反証されたかまだ曖昧なら削除。拒否したレポートは 1 回だけ失敗理由を付けてやり直す。2 回目も拒否なら open として報告し `/no-comments` は fail。
3. 受理した trivial フラグは dead path 削除、パラメータ削除、正しい API 使用で直す。形の変更が要るものは受理セットと周辺コード向けに `/architect` を 1 回。スケッチで止める。Architect は形、Step 4 が実装。
4. スコープ内で最小の根本原因修正を実装。名前の付いた workaround はすべて除去。根本原因がスコープ外ならスコープ内の最小修正を land し残りは open。意図の指針は `forge-mode/principles/fix-root-causes.md` と `forge-mode/principles/redesign-from-first-principles.md`。どちらもフェンス拡大やスコープ外の個別対症療法を許可しない。症状ガードの bolt-on はしない。
5. `do not remove` / `do not change wording` / `talk to X before changing` 系の制約コメント。変更不能なものの keep は残す。スコープ内で最安の型・runtime・test・CI lint を提案。インタラクティブ承認を待つ。無人・eval は呼び出し側の事前承認が必要。承認されたら encode してから削除。そうでなければ削除し制約を open として報告し、スコープ外のスケッチを書く。
6. 削除数、復元コメント、再実行、architect スケッチ、修正、エンコード提案・実施、未強制の制約、その他 open 作業を報告する。

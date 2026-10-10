---
name: create-verification-skill
description: "ユーザーと同じように app を動かす project-local verification スキルを生成 — 言語・framework・platform 不問。/create-verification-skill、「make a control skill for this repo」、UI/CLI/service 振る舞いを証明する scripted 手段が無い project 向け。"
disable-model-invocation: true
---

# Create a verification skill

本気の project には、real app を動かして振る舞いを証明する scripted 手段が要る: 起動、ユーザーと同じように feature を exercise、evidence を capture。このスキルは repo 向けに `.cursor/skills/verify-<app>/` として project-local スキルを生成する。generator の出力は人ではなく次のエージェント向け: app を一度も見たことがないエージェントが cold、mid-task で読む。

## 1. Interview the repo, not the user

codebase から答え、観察できないことだけユーザーに聞く:

- **Surface:** ユーザーが実際に触るものは？ web UI、CLI/TUI、desktop app、API、mobile app、library？ 複数あり得る; primary を選び残りを注記。
- **Run:** ローカルで app はどう起動？ repo 自身の documented dev command を優先（package script、Makefile、README quickstart）。port、env var、seed data、auth を注記。
- **Drive:** エージェントはどう programmatic に触れる？ 既存 harness を先 — Playwright/Cypress spec、expect script、PTY helper、curl 可能 endpoint、debug port。その後 generic recipe: web/Electron は browser/CDP、CLI/TUI は tmux/PTY harness、service は plain HTTP。
- **Observe:** 何を evidence として capture できる？ screenshot、terminal transcript、response body、log、exit code、DB state。
- **Isolate:** 2 instance を並行できるか（port、data dir、profile）？ できなければ生成スキルに明記: shared instance の二重 drive を拒否する方がユーザーセッション破損よりまし。

checkout がそのまま build/start できないなら、生成前に直す（または precise に report）；壊れた base 向けスキルは誤った step を教える。無関係な欠損 asset が起動を止めるとき（API が serve しない static dir、sample config）、生成スキルは verification scaffolding として明記して作り、cleanup で除去してよい。

## 2. Generate the skill

YAML frontmatter（`name: verify-<app>` と app・surface・いつ使うかを述べる `description` — frontmatter 無しではスキルは登録されない）付き `.cursor/skills/verify-<app>/SKILL.md` を書き、interview で実際に見つかったことに根ざした次の節（placeholder を残さない）:

- **Launch:** verification 用に app を起動する exact command と ready の判定（log 行、応答する port、prompt）。teardown 含む。短命 CLI/TUI には生かす server なし: launch は binary build（または deps install）1 回、その後各 drive は隔離 PTY または tmux session で開始。
- **Doctor:** read-only 1 check で「この instance は drive に値するか？」 — process up、正しい version/build、port が自分、auth valid。何かおかしいときエージェントは常にこれを先に走らせる。
- **Drive:** この repo の real selector/command 付き harness recipe。例ではない。coordinate と tab 順より stable handle（ARIA label、data attribute、prompt 文字列、route path）を優先。
- **Evidence:** proof に何を capture しどこへ。proof 標準を述べる: real user path を exercise、internal setter や test-only endpoint ではない; action と結果 state を capture、最終画面だけではない; 見えるものと並行して side effect（書き込みファイル、insert 行、送信 message）を verify; mock は production 境界が既に外部 system を isolate する所だけ。安全 path が dry-run または test mode なら、名前を信じず observe で実際に skip するものを verify（file、network、git ref）: 一部 dry-run はまだ network や browser に触る。
- **Cleanup:** run が作った instance の teardown。process 名で kill しない; 自分が起動したものを kill。cleanup は instance と scratch state を除去し、evidence は除去しない: proof artifact は teardown 後も残り、スキルが名指す場所に。
- **Helpers:** スキルが ship する script は executable で invocation はスキル本文に示す。読者が reverse-engineer する helper は helper ではない。

## 3. Seed the feature map

`.cursor/skills/verify-<app>/features/README.md` と、identify できる user-facing feature ごとに 1 file（route、command、menu、docs から top 3–5 から）を作る。[`references/feature-map-example/`](references/feature-map-example/) の形に従い、README index と feature ごと 1 file。各 file はユーザー視点で: feature とは何、どう辿る、harness でどう drive、動作を証明する observable end state。4 つの H2 は `Sub-features`、`How to get to it (user POV)`、`Driving it with <harness>`、`Gotchas`。map は repo の maintained verification source; map が他 entry を列挙しているとき、都合の良い 1 entry だけ drive した proof は不完全。

## 4. Prove the generated skill before handing it over

指示を end-to-end 1 回: launch、doctor、mapped feature を 1 つ drive（1 つで十分; map は後の run が残りを cover するため）、evidence capture、cleanup。cleanup 後、名指し場所に evidence がまだあることを確認 — proof を食う cleanup はこの step fail。fail したものを直し、fail iteration ごとにも生成 cleanup を走らせ、壊れた attempt が process と port を残さない。一度も実行されなかった生成スキルは draft であり deliverable ではない。

## 5. Offer the maintenance loop

app 変更に map を honest に保つには `/maintain-verification-skill` を指す。cadence は聞かれたときだけ提案。

### Autopilot-full

**verdict を自分が持ち、PR は never。PR ごとに 1 owner が build から merge まで走り、code を書かなかった swarm が land する code を証明するまで merge しない。**

verdict は 1 patch を覆い、green CI は 1 head を覆う。step 4 は code-ready head で full swarm を 1 回。大きな変更のときだけもう 1 回。`playbooks/shipping.md` の patch-id rule が lane 結果を引き継げる。新 head ごとに green CI が要る。

1. **operator の gate が先。** grant は queue の item だけ。operator が自分用と名指した item と queue 外 PR は merge-ready で stop。plan の述べを求めるだけは go ではない。
2. **PR ごとに 1 owner を spawn。置き換え可能な場所に work を置く。** program 用に forge を 1 回 resolve。GitHub CLI（`gh`）が default。Origin が使えるなら PR 操作はすべて `origin pr ...`。なければ `gh` と fallback を記録。`gt` は要求しない。各 owner は Cursor cloud agent。`playbooks/opening-a-pr.md` で PR を開き、real artifact で証明し、`playbooks/babysit.md` で green まで、step 4–5 が clear したら merge。

   PR は早く開き CI と bot を並行させる。code-ready は slop-strip（`cursor-team-kit` の `/deslop`）と `/no-comments` の後。full swarm は finished code に走る。そのあと current trunk に rebase し code-ready head を report。self-proof は patch が land する base で走る。later head と merge-ready（self-proof、CI、babysit 完了）を report。fix round は trunk conflict か CI break までその base に留まる。rebase は CI を再起動する。code-ready push と verifier が要る later push の前に、触った path で repo の check を committed head で走らせる。

   VM は死ぬと仮定。すぐ push し root agent の store（system prompt の path）で **decision-log** スキルに従い trail を開始。保持する unit ごとに push。subagent を spawn した者は id、state、過去 run の stuck-after runtime を store に記録し parent が死んでも root が probe できる。force-push は自分の branch だけ `--force-with-lease` を最後に push した SHA に pin。自分が作っていない push では stop し root に report。
3. **owner を trunk から parallel、stack しない。** 各 PR は単独 land。
4. **swarm-verify は 1 回。** code-ready head で full swarm 1 回。新 behavior、再設計、大きな diff のときだけもう 1 回。rebase、conflict 解消、小 fix は新 head で single verifier。**swarm** スキルで code-ready SHA に independent verifier を fan out。gate を再実行し、control skill（`control-ui` / `control-cli` 等）か named driver で real surface の load-bearing behavior を live prove し diff を audit。live lane が無い、merge-ready report の receipt を audit していない verdict は clean ではない。

   lane が何と label したかに関わらず proven finding を owner に 1 fix-forward で送る。同じ defect の全 site を cover する red test を付ける。trunk だけに出る defect は trunk に記録し PR を gate しない。PR がコピーまたは新たに届ける defect は PR 自身のもの。fix は自分で push しない。branch の writer は 1 人。stuck owner は replace。
5. **owner は verify したものだけ merge。land する trunk で test 済み。** green CI だけでは merge 不可。swarm lane 開始後、merge prep は current trunk に rebase、新 head を report、green CI を待つ。

   merge 直前に trunk を fetch し、その変更が patch に効くか聞く。trunk の毎回 rebase は終わらない。land する code が未 test なら rebase して CI 待つ（conflict、両側変更 file、PR に走る check の変更）。lockfile 両側変更は、merge 結果で frozen install が pass し PR が変える package が head と同じに resolve するなら rebase 不要。fail なら rebase で直す。trunk が patch の caller か依存（呼ぶ code、依存 version）を変えたら merge 結果で patch の check を走らせ pass で merge。それ以外は merge。merge prep 後 3 回目の rebase を trunk が強制するなら hold し root に report。root が衝突 work を sequence する。
6. **root layer を走らせる。** gate を緩めるもの（budget 引き上げ、allowlist）は verifier proof のあと fresh countersign が要る。owner が green を欲しい側。grant が approval をカバーするなら countersign が approval。owner の記録は lane が check する countersign を指す。disabled / soft-failed check は必ず出す。forge が enforce する approval は give も bypass もしない。

   operator の go で `/loop 1h` を arm し delegated work が無くなるまで audit。長 run は drift し agent は黙って stall する。各 tick は trunk から本 playbook を再読み、unreported head や unrecorded agent など drift を owner に記録させて直す。drift は record の gap であって stall ではない。leaf lane まで全 agent を probe し side effect で judge する。status 文と summary は stuck child を隠す。error、turn 開始不可、stuck-after を過ぎて新しいものが無い agent は stuck。最初の tick まで push も trail 行も無い owner も stuck。operator かあなた待ちは stuck ではない。答える。stuck agent は stop の land を待たず即 replace。operator に変化があった tick は **ketchup** でキャッチアップ。変化なしは黙る。
7. **operator の stop で即 stand down。** hold は全 owner に zero-writes order。各々 stand を report し operator が release するまで brief を hold。

**Reply:** **ketchup** スキルで、各 PR の state と verdict、merge したもの、countersign と理由、open operator gate、各 PR と trail への link を含めて operator をキャッチアップ。

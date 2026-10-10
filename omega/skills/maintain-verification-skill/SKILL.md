---
name: maintain-verification-skill
description: "project の verification スキルと feature map を honest に保つ定期 pass: feature ごと並列 source reader、全 feature を drive する 1 live session、証明済み修正は最大 1 PR。/maintain-verification-skill または「audit the verify skill」。"
disable-model-invocation: true
---

# Maintain a verification skill

feature map は app が変わった瞬間に rot する。このスキルは `/create-verification-skill` で生成した（または feature map 付き project-local verification）スキルの upkeep loop。rigor の単位は feature であり全文ではない: 各 feature file を source から cover し、各 feature を live で exercise するが、すべての bullet を terminal 化しない。

## Outcomes

1 つ選び、どれか言う:

- **clean** — 各 feature が source と live coverage を得た; ship するに値するものなし。branch なし、PR なし。
- **changed** — 証明済み doc、harness、map 修正を 1 PR で ship。
- **blocked** — coverage が完了できない、または証明済み fix を安全に ship できない。何が block したか exact に言う。

## Edit scope

verification スキル自身の directory だけ編集（SKILL.md、features/、所有 harness script）。run 中は product code を編集しない: map が述べる振る舞いを app がもうしないなら doc drift（map を直す）または product regression（report し、doc で糊塗しない）。

## Pass

0. **Locate the target.** メンテ対象 verification スキルを見つける: 本文に launch/drive 節と feature map がある project-local スキル（通常 `.cursor/skills/verify-*/`）。複数 candidate → どれか聞く; なし → 対象を捏造せず `/create-verification-skill` を指して stop。

1. **Index hygiene.** feature map README を読み sibling を glob。欠落・余分・重複・dead entry を直す。軽量; 生成 inventory なし。

2. **Source wave.** feature file ごとに read-only subagent 1 つ、並行起動。各々が source から「この user-facing feature はどう動く？」を説明、引用付きで likely doc drift を flag、concise live-verification recipe を 1 つ返す。子は app を drive せずファイルを編集しない。返却形: feature summary / source entry points / likely drift or none / one recipe。

3. **Reconcile.** 各 feature file に返却 summary がある。重なる recipe を practical に少ない app state に merge。引用 drift を spot-check; clean claim を再証明しない。最近の churn を sweep し map に無い user-facing surface — missing と言う前に concrete source path を要求。

4. **Live pass.** source が clean に見えても必須。coordinator がすべての driving を所有; verification スキル自身の launch model に従う — server/UI は 1 長寿命 instance を serial drive、短命 CLI は drive ごと fresh 隔離 session（Launch 節が決め、ここではない）。各 feature を最低 1 回 exercise し、pass 全体で 3 invariant を守る（fail 内容は問わない）: (1) health-check 後に surprising なことをしていない instance を drive しない — 最初の drive 前に doctor、session が単位なら各 fresh session で doctor、fail drive 後に再 doctor、doctor が見えない fail（healthy process の wedged UI state）なら known state に reset または relaunch して hope しない; (2) これまで capture した evidence はすべての cleanup を生き延び、名指し場所で確認、assume しない; (3) drive が始めたものはその drive の有用性を超えて生き残らない — fail iteration residue は session が stuck、exit、shared かに関わらず clean（shared instance なら residue を clean、instance ではない）。skill drift による doctor fail は drift: edit scope で直し 1 回 retry — fix が invalid したものだけ restart、それ以上はしない — pass を `blocked` と言う前に。到達不能 feature は concrete prerequisite（auth、entitlement、OS、external state）と試した route があればだけ `verified-unreachable`; map がその prerequisite を omit なら drift。triage からの harness fix は ship 前に live で再 drive。最終 teardown は run の最後の drive の後 — 再証明含む — 何も run を超えて生き残らない（evidence は残る、スキル per）。

5. **Triage.** user-POV 説明が誤りまたは欠落 → doc drift、直す。動く振る舞いを harness が drive できない → harness gap、直す; harness fix は generation と同じ helpers ルール（script executable、invocation はスキル本文に document）。実際に壊れた app 振る舞い → product gap; ユーザー向けに記録しこの PR から外す。

6. **Ship or stop.** changed なら: 証明済み修正 1 PR、変更 file をすべて先に再読。clean または blocked なら: PR なし、outcome と coverage を正直に report。

concise run notes（cover した feature、unreachable prerequisite、確認 drift、outcome）を scratch 場所に; commit しない。

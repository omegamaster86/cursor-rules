# Session log — premature-completion-reporting

更新: 2026-10-28
ブランチ: feat/nonmain-review-v3（本チャットはコード未編集。下記 WIP は別作業のローカル状態）
前チャット: 39e76e3c-246c-4e3c-b99b-5f1dda88824f

## カプセル
- エージェントが修正後も IDE/tsc/ランタイム赤のまま「完了」報告する原因を forge-mode / verify-done / transcript から整理した。
- recall で決定的な一次ソースは oki-v2 チャット `6ff70ff4-5bbf-486e-9568-c2dca9286b37`（15:43 形状変更の中途半端完了 → 15:44「エラー状態で完了するのやめろ」）。
- 対策案は omega（cursor-rules）側が中心。最小 PR は forge-mode 完了節 + verify-done で TS 変更時 tsc 必須。
- 本チャットではルール変更・実装は未着手。調査と修正方針の合意まで。

## 確定 / 未確定
- 確定: 直接原因は (1) verify-done 未実行または Lints のみ (2) 返り値型変更と caller 非同期更新 (3) forge-mode 中の `# 実行結果報告` 締め。
- 確定: oki-v2 事例では指摘後に `npx tsc --noEmit` で収束。エージェント自身が「中途半端」「型と参照が壊れている」と認めている。
- 未確定: cursor-rules への PR 優先順（PR1 forge-mode+global vs PR2 verify-done tsc 固定）のユーザー決定。
- 未確定: `/correct` スキルエントリ追加の要否。

## 変更ファイル
| ファイル | 状態 |
| --- | --- |
| （本チャット） | 調査のみ。リポジトリ未変更 |
| nonmain-review 配下多数 | 未コミット WIP（#366 系。本スレッドとは無関係） |

## 試してダメだったこと
- transcript 全文 grep で「エラー状態で完了にするな」完全一致は oki-v2 の1件のみ。frontend slug だけではユーザー文言を拾いにくい（worktree 別 slug）。

## 次の一手
1. ~~omega へ PR1+PR2 反映~~ → 完了。各 PJ へ `omega-sync` / PR マージ後、frontend 等で `/verify-done` が typecheck を走らせることを spot-check。

## 参照（新チャットで Read）
- frontend/.cursor/commands/verify-done.md（完了ゲート正本）
- frontend/.cursor/commands/forge-mode.md
- frontend/.cursor/skills/forge-mode/playbooks/refactoring.md（caller 同時更新ステップ追加候補）
- agent-transcripts/6ff70ff4-5bbf-486e-9568-c2dca9286b37（oki-v2 slug 配下）
- mapUraHistory 事例: frontend-oki-v2 `mapUraHistoryToMatchupTable.ts` / `UraProgramMatchupModal.tsx`


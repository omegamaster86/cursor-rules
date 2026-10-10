# コピー向けプロンプト例

実パス・スキル・完了条件に差し替える。くだけた言い回しでよい。

## 理解する

- `/forge-mode <thread> を読んで。根本の問題を自分の言葉で、専門用語なしで言い直して。`
- `/forge-mode <symptom> の原因を調べて。分かっていること、使ったデータ、有力な仮説を出して。まだコードは変えない。`
- `/how で <subsystem> の動きを把握して。続けて /why で最近壊れた理由を調べて。`
- `/recall 先週の <topic> の作業をまとめて。そのあと <issue> を読んで。`
- `/teach <other way> ではなくこう実装した理由とトレードオフを教えて。`
- `/forge-mode このブランチを引き継いで。decision log を読み、済みを把握して続けて。済みの作業はやり直さない。`

## 作る

- バグ: `/forge-mode <symptom>。先に repro、そのあと fix と verify。`
- アプリのバグ: `/forge-mode /verify-<app> で repro。main で repro するなら直して、証明用の video を見せて。`
- 安いテストがあるバグ: `/forge-mode 先に <bug> を repro。安いテスト経路があれば /tdd してから fix、再実行。`
- 機能: `/forge-mode <behavior> を追加。<current output> はバイト単位で同一のまま。両方 verify。`
- リファクタ: `/forge-mode <code> を 1 モジュールに移す。挙動ゼロ変更。移す前の出力を記録し、後で変わっていないことを証明。`
- 性能: `/forge-mode <fixture> で <operation> が <time>。trace して、測った原因を直し、before/after を見せて。`

## 設計と計画

- `/forge-mode <feature> の案を数パターン prototype。比較用 screenshot か video を撮って。`
- `/forge-mode <feature> が必要。先に /architect。未決は prototype で答えて。進む前にレビューさせて。`
- `/forge-mode 先に <new package> の使い方チュートリアルを書いて。そのあと /teach で現状より良い理由を教えて。`
- `/multi-agent-candidates`（または `/architect`）でこのスレッドとアプローチの第二意見を聞いて。`
- `/forge-mode この設計をプランに落とす。小さく検証可能な PR、各 PR に独自の verification。`
- `/forge-mode <library> を <target> に移行するプラン。小さく検証可能な PR。結果は元と完全一致、バグ込みで。`

## レビューと ship

- ブランチで `/review-orchestrator-triple-hybrid`。疑って。まだ変更しない。dismiss も読む。`
- `/swarm <dir> 下の各 package を check script で確認。package あたり 1 worker。1 本の report。`
- `/forge-mode PR を開く。小さく順序付き commit、説明に evidence。`
- `/forge-mode この PR を babysit。green にして。` 状態だけ: `/forge-mode PR <number> の状況は？未処理は？`
- `/forge-mode スタックを land。`

## 離席と再開

- `/forge-mode 寝る。<base> から新しい worktree で <goal>。完了は <checks>。decision log を残す。commit 前に聞かない。/loop で完了まで。数時間本当に詰まったら止めて理由を書く。`
- `/decision-log 昨夜やったことを要約して。` 先に **decision-log** スキルの Attention を読む（Notion 正本。ローカル `decisions.tsv` がある run も同スキルで要約）。
- `/forge-mode このキューを full autopilot。各項目は独立。`
- `/forge-mode 変更を autopilot するがスタックに積む。ship はしない。スタックは自分で land する。`
- `/reflect 学びを捕まえて次 run で繰り返さない。` 将来の判断を変える edit だけ承認。
- `/bro` で直前の返信を平易な言葉で言い直す。

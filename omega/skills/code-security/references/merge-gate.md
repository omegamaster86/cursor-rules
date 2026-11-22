# マージ前ゲートと肯定所見

RESULTS に書く。チャットの security-review 表と同じ役割で、**検証したコントロール**と**人手の確認項目**を残す。

## 肯定所見

ソースで確認できたものだけ。各 1 行。

- 管理 Edge が `requireAdminWithServiceRole`（または同等）で止まっている関数名
- RPC が `service_role` 限定で、`REVOKE` または関数内ガードと一致しているもの
- 所有者チェックが関数内にある RPC

確認していないものを「妥当」と書かない。

## マージ前ゲート

finding の `merge_gate` 文字列、またはレンズから導出した確認を表にする。最大 8 行。実行は監査ジョブの範囲外（人手または別テスト）。

| 列 | 内容 |
|----|------|
| 前提 | ロール（anon / user A / user B / 管理者） |
| 操作 | 叩く RPC・URL・画面 |
| 期待 | 拒否または所有者のデータのみ |

例（該当 finding があるときだけ書く）:

- anon で audience 系 RPC を実行したときの応答
- user A が user B の `target_user_id` で一覧 RPC を呼べないこと
- 他人の Storage URL を検証 Edge に渡して拒否されること
- 一般ユーザーが `*_for_admin` とレガシー承認 RPC を実行できないこと

ゲートが 0 件なら「手動ゲートなし」と 1 行書く。

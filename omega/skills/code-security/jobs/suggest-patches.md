# Job: suggest patches

`CODE-SECURITY-*/findings.jsonl` の verified finding から、**適用はユーザー任せ**の `.patch` を生成。

## 前提

- git リポジトリ必須
- stamp の `revision.dirty` が true なら停止（コミット後に再スキャンを案内）
- full scan: stamp commit == `HEAD`。commit scan: 対象コミットが HEAD の祖先で、snippet がまだ存在

**PATCH BASE** = 現在の `HEAD`（40 hex）

## 引数

- `all` | `high` | `F1,F3`

## 手順

1. 最新の `CODE-SECURITY-*` を選ぶ（ユーザー指定がなければ newest）
2. selection を解決。finding id は `^F[0-9]{1,9}$` のみ信頼
3. `CODE-SECURITY-<ts>/patches/` を用意（同じ report ディレクトリ内）
4. **4 finding ずつ wave**:
   - `git clone --shared --no-checkout` + `checkout --detach <PATCH BASE>` で scratch（パスは `.code-security-run/patch-<ts>/scratch-F<n>`）
   - **patch-generator** Task: FINDING JSON、WORKSPACE、修正を stage
   - **patch-verifier** + **adversarial researcher** Task 並列（[../references/verifier-panel.md](../references/verifier-panel.md)）
   - objection 時は 1 revision ラウンドのみ
   - 合格時 `git diff --cached` を `F<n>.patch` に。`F<n>.md` に根拠・テスト・却下理由
5. `PATCHES.md` 索引を書く
6. ユーザーの checkout は触らない。commit / push / PR はしない

## 締め

パッチ一覧、apply はユーザー判断。「適用してほしければ指示して」と 1 行。

---
name: verify-done
model: inherit
description: タスク完了宣言の前に、変更に応じた proof を選び実行する。テストは手段の一つ。毎回フルテストは不要。omega-mode 完了ゲートおよびユーザー任意呼び出し用。
---

# 完了前検証（verify-done）

**タスク完了を宣言する前**、または **omega-mode プレイブックの最終ゲート**として実行する。

代理指標・自己報告・「コンパイルできた」だけでは完了と言わない。**実アーティファクト**（実行結果、実値、diff、再実行可能スクリプト）で証明する。

**テストは手段の一つ。** 毎回 `npm test` 全件は不要。変更種別に応じて **1〜3 個の proof** を選び実行する。

哲学・背景は `omega-mode/principles/prove-it-works.md`。本コマンドが **実行手順の正本**。

## いつ使う

| 入口 | タイミング |
|------|------------|
| `/verify-done` | ユーザーが任意で「本当に動いてる？」を確認したいとき |
| `omega-mode` | 実装・修正タスクの**完了宣言前**（Opening a PR の直前） |
| プレイブック | Refactoring step 5、Session pickup step 5 など、proof が必要なステップ |

**読み取り専用 Investigation**（コード変更なし）では Step 2 の Tier A のみで足りる場合がある。

## 実行環境（重要）

- 本コマンドは **コマンドを配置した対象リポジトリ（PJ）** 内で完結させる。
- **proof は実際に実行する**（`Read` / diff 確認だけで終わらせない — Tier に応じてコマンド実行・値の読み取り・smoke を行う）。
- サブエージェントや delegate の要約は **proof にしない**。`git diff`、実行出力、DB/API の実値を自分で確認する。
- UI / CLI 検証はブラウザ MCP または手動 smoke（PJ に Playwright 等があればそれを使う）。

## Step 0: スコープ確定

- 検証対象: 会話のタスク、または `git diff`（未指定なら `origin/<base>...HEAD`）。
- **成功条件**を1文で書く（例: 「Todo 作成フォーム送信後、一覧に行が増える」）。
- レポート冒頭に **スコープ・成功条件・選んだ Tier** を記載する。

## Step 1: proof の選び方（Tier）

変更種別に応じて **最小十分な proof** を選ぶ。複数 Tier にまたがる場合は **厳しい方** を足す。

| Tier | 変更例 | proof の例（1〜3 個から選ぶ） |
|------|--------|--------------------------------|
| **A** | ドキュメント・コメント・設定のみ | 対象 diff の内容確認。意図どおりかを明示 |
| **B** | 型・リネーム・import 整理（behavior 不変） | 型check / lint（**これだけでは不十分** — 既存 harness・該当 smoke・characterization test があれば実行） |
| **C** | ロジック・API・DB・フォーム・認証 | 影響パスの **実行**（unit / 対象テストファイル / curl / RPC / SQL Editor） |
| **D** | 統合・複数層・UI フロー | 入力→出力チェーン（E2E / Playwright / 手動 smoke / equivalence script） |

**選定ルール:**

- 「ビルドが通った」「lint が通った」は **Tier B 以下では proof にならない**。
- 「テスト suite 全件 green」は **デフォルトにしない**。変更に関係するテスト・パスだけ実行する。
- リファクタで behavior 不変を claim する場合: equivalence harness / old-vs-new diff script / recorded baseline replay（**compiles だけは pin にならない**）。
- 可能なら **再実行可能なスクリプト**（決定論的 compare）を残す。

## Step 2: 実行しないもの（proxy 禁止）

以下を **完了の根拠にしない**:

- エージェント自身の「動きました」報告
- サブエージェントの summary のみ
- ファイル mtime、キャッシュされたスクリーンショット
- lint / typecheck のみ（Tier C 以上の変更で）
- コードを読んだだけ（実行していない）

検証が失敗したら、**観察方法**（コマンド・環境・データ）を先に疑う。

## Step 3: 実行と記録

選んだ proof を **順に実行**し、各項目について記録する:

1. **何を実行したか**（コマンド・URL・操作）
2. **期待と実際**（pass / fail / inconclusive）
3. **実値または出力の要約**（ログ1行、HTTP status、DB 行数など）

PJ にテストがある場合の参照（任意）:

- `nextjs-library-guide` / `web-library-guide` の `test-unit.md`, `test-component.md`, `test-e2e.md`
- Flutter: `flutter-library-guide` の `test-unit.md`

## Step 4: 結果レポート

以下の形式で出力する。**pass するまで「完了」「done」と宣言しない**（ユーザーが read-only 確認のみを求めた場合は除く）。

```markdown
## verify-done 結果

### スコープ
[ファイル / subsystem / diff 範囲]

### 成功条件
[1文]

### 選んだ Tier と proof
| # | proof | 結果 | 根拠（出力要約） |
|---|-------|------|------------------|
| 1 | ... | pass/fail | ... |

### 総合
- [ ] **PASS** — 上記 proof で成功条件を満たした
- [ ] **FAIL** — 未解決。完了宣言不可
- [ ] **PARTIAL** — 実行できなかった proof と理由（環境不足等）

### 未検証・リスク（あれば）
[実行できなかった項目、follow-up で必要な確認]
```

## Step 5: omega-mode との接続

- **Opening a PR** の前に本コマンドを通し、**PASS** であること。
- FAIL / PARTIAL のまま PR を開かない（ユーザーが明示的に proceed を指示した場合を除く）。
- Refactoring プレイブック step 5（behavior unchanged の prove）も本コマンドの Tier B/C/D で満たす。

## 関連

- 哲学: `omega-mode/principles/prove-it-works.md`
- 単位ごとの積み方: `omega-mode/principles/sequence-verifiable-units.md`
- omega-mode 入口: `commands/omega-mode.md`


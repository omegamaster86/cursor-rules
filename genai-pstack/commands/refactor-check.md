---
name: refactor-check
model: inherit
description: ユーザーがリファクタを指示したとき、削減・簡素化・読者負荷の観点で読み取り調査し、修正案とコミット順を提示する。自動適用はしない。
---

# リファクタ・削減チェック

**ユーザーがリファクタを指示したとき**、または `omega-mode` の Refactoring プレイブックの subtract / 簡素化調査フェーズで実行する。

対象スコープについて **読み取り調査と修正案提示まで** 行う。**修正の自動適用・コミットはしない**（ユーザーが GO と言うまで）。

旧 `principle-laziness-protocol` / `principle-subtract-before-you-add` / `principle-minimize-reader-load` および `change-discipline.md` を本コマンドに統合。

## 実行環境（重要）

- 本コマンドは **コマンドを配置した対象リポジトリ（PJ）** 内だけで完結させる。
- 静的解析は **`git diff` / `grep` / `codebase_search` / `Read`** のみ。
- **behavior は変えない。** 振る舞い変更は bug fix / feature へ分離する。

## 前提

- ベースブランチは未指定ならデフォルトブランチ（多くは `main` または `master`）。会話で別ブランチ・ファイルパスが指定されていればそれを使う。
- 対象が未指定なら `git diff origin/<base>...HEAD` の変更範囲、または会話で名指しされた subsystem。
- 流用・二重定義の調査は **`/reuse-check`** を別途（本コマンドの範囲外）。
- 推測的 cleanup は提案に留め、確信が弱いものは **任意** に落とす。

## Step 0: スコープと contract

- 対象 subsystem / ファイルパスを確定し、レポート冒頭に記載する。
- 既存の characterization test・snapshot・equivalence harness があるか確認する。
- pin がなく coverage も薄い領域を structure touch する場合は、**touch 前に pin 推奨** をレポートに含める。

## Step 1: Subtract（削る候補の列挙）

**new shape を導入する前に**、次を差分または指定範囲で `grep` / `Read` する。

| 観点 | 手順 |
|------|------|
| dead weight | 未参照 `export`、到達不能コード、使われていない import |
| one-caller ラッパー | 呼び出し元が 1 つの thin wrapper / pass-through helper |
| 冗長バリデータ | 上流で済んでいる形式チェック・重複ガード |
| orphan / スタブ | 中身のない placeholder、参照だけ残ったファイル |
| 推測的ガード | 仕様外の null チェック、未使用フィールド用スキーマ |

**方針:**

- 磨く前に切る（品質投資の前に表面積を最小化）
- 観測された使用向けに設計し、推測的エッジケース向けに作らない
- 「将来使うかも」だけで共通化・抽象化しない（`nextjs-directory-structure` の `colocation-shared` 参照）

**リファクタの推奨順序:**

1. 上記の削除・インライン
2. 必要なら新しい形を導入
3. 各ステップで behavior pin を green に保つ

## Step 2: Laziness（簡素化の問い）

| 問い | 意図 |
|------|------|
| 追跡に 3 ファイル超が要るか？ | 要るならフラット化・統合を検討 |
| 同じ決定が複数箇所にあるか？ | SSOT に寄せる |
| 新レイヤー・配線で済ませようとしていないか？ | より直接経路を探す |
| diff をさらに小さくできるか？ | 問題を解く最小変更 |

**層アーキテクチャとの関係:** Page → Server Action → Edge → DB などの層分離は社内規約として維持する。
ただし **層の中**や **追跡ホップ全体**で 3 ファイル超が要るなら、層を増やす前にフラット化・統合を検討する。
`component-split` の分割は、読者負荷が下がるときだけ行う。

## Step 3: Reader load（読者負荷）

各変更について 2 軸を評価する:

1. **追跡するレイヤー** — 質問と答えの間の間接化の数
2. **保持する状態** — 隠れた・可変コンテキスト（不要な useEffect コピー等）

**30 秒テスト:** 新しい読者が「X はどこから来るか？」「X を何が変更できるか？」に答えられるか。
できなければレイヤーまたは状態を切る提案を出す。

**成功の目安（いずれか）:**

- 質問と答えの間のレイヤーが減った
- 隠れた状態が減った
- 第 2 コンシューマーのない間接化が減った
- diff が問題解決に必要な最小だった

どこも読者負荷を下げていない変更は **revert 推奨** と明記する。

## Step 4: 判断チェックリスト

1. まず削れるか？（未使用・ラッパー・重複検証・スタブ）
2. この追加は観測された需要か？（推測だけなら見送り）
3. 追跡に 3 ファイル超か？
4. 同じ決定を別の場所でもしているか？
5. 配線を迂回できないか？
6. 読者負荷は下がったか？

## Step 5: 出力フォーマット（必ずこの形式）

```markdown
## リファクタ・削減チェック

### スコープ
- ベース: `<branch>` または `<paths>`
- 対象ファイル数: N
- behavior contract / pin: [あり | なし — 推奨]

### 削減候補（Must / Should / 任意）

#### 1. [短いタイトル]
- **箇所**: `path` Lxx–Lyy
- **種別**: dead weight | one-caller wrapper | 冗長ガード | orphan | 推測的ガード
- **根拠**: grep | Read | 呼び出しグラフ
- **修正案**: 削除 | インライン | 統合先
- **reader-load 効果**: [layer 減 | state 減 | なし]

### 簡素化案（Laziness）
- [3 ファイル超の経路、SSOT 候補、配線短縮案]

### 触らないもの
- [behavior 変更になりうるもの、推測的 cleanup]

### 推奨コミット順
1. subtraction（削除・インライン）
2. reshape（構造変更）
3. follow-on cleanup

### 関連コマンド
- 流用・二重定義: `/reuse-check` の結果（あれば要約）
- PR 監査: `deep-review-code-quality`

### 探索ログ（簡潔）
- git / grep パターン / codebase_search クエリ
```

## アンチパターン（指摘対象）

- リファクタ開始直後に新ファイル・新抽象を量産する
- Server Action・Edge・DB で同種の形式チェックを繰り返す
- 検証済みデータの深部で `if (!field)` を繰り返す
- 1 箇所専用ロジックを根拠なく shared へ上げる
- 「効くかも」 speculative cleanup を Must にしない

## 注意

- 本コマンドは **調査と提案** のみ。実装はユーザーの明示指示後に行う。
- セキュリティ・コーディング規約の総合レビューは範囲外。必要なら `review-orchestrator-triple-hybrid` 等を使う。

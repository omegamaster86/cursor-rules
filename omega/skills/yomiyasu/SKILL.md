---
name: yomiyasu
description: >-
  AIが生成した不自然な日本語を、人間が読みやすい自然な文章へ書き直す（Cursor / omega 向け抜粋版、上流 v3.1 系）。
  「読みやすくして」「AI臭を消して」、技術記事・PR説明・仕様・study-log 下書きの推敲で使用。
  forge-mode Ship 中の自動適用はしない。
metadata:
  upstream_version: "3.1.0"
---

# yomiyasu（omega / Cursor）

AI特有の比喩・壊れた主述・装飾過多を直し、**意味を変えず**に読みやすい日本語へ再構成する。ルールの正本は `references/writing-rules.md`（上流 SKILL §1）。

### 用途と表記の扱い

- 原文があれば推敲、資料だけなら新規作成。新規作成では主張・条件・担当・数値・未確認が資料どおりか読み比べる。
- 補助動詞と形式名詞の「事」「為」はひらがなにする。そのほかの表記揺れは原文のまま。

## omega での位置づけ

| 項目 | 方針 |
|------|------|
| 起動 | **ユーザー明示依頼時のみ**（チャットへの貼り付け推敲、Markdown ファイル指定） |
| forge-mode | Ship 中は自己起動しない。PR 本文を日本語で書く依頼があったときだけ |
| study-log | 記事の**下書き完成後**の任意ステップ。study-log 執筆と同一ターンで両方オンにしない |
| decision-log | Notion 本文を日本語で整える依頼時。事実・数値は `writing-rules.md` の不増補を厳守 |
| 干渉 | 他の日本語校正スキルと同時有効化しない（上流 README 同様） |

Claude Code プラグイン・`npx skills`・`yomiyasu_check.py`（run/verify）は omega では**同梱しない**。Cursor では **lint + diff** と目視点検で足りる（上流 Step 3–5 の check/verify に相当する観点は `review-points.md` で手順化）。

## 読む順（on-demand）

1. `references/writing-rules.md` — 必須
2. 文書の種類 — 決めたら `references/doc-types/<種類>.md`（13種。Step 1）
3. ドメイン — `references/domains/tech.md` / `business.md` / `essay.md`
4. 変換・lint 解釈 — `gemini-syntax.md`, `slop-catalog.md`, `calques.md`, `rephrase-test.md`, `review-points.md`
5. 読者・敬語 — 指定があれば `audience.md`, `persona.md`
6. 自分で書いた原稿の事実 — `fact-recovery.md`（必要時）

## 実行手順

### Step 1: 種類と読み手

- 種類は pr / article / incident / proposal / minutes / manual / slides / essay / formal / promo / mail / paper / script の13種。当たらなければ決めない。決めたら書き直す前に `references/doc-types/<種類>.md` を読み、当てない規則を当てない。
- 読み手は expert / informed / general。informed か general なら `references/audience.md` を読む。説明の要る用語に原文・資料に説明がなければ「ここに説明が必要です: 語（場所）」と書く。
- 書き手と読み手の関係は依頼で言われたときだけ `references/persona.md` を読んで敬語を調整する。
- 作業フォルダの git 最上位に `.yomiyasu-words/` があれば `allow.txt` / `flag.txt` / `flag-patterns.txt` を読む（allow は外す、flag は直訳語と同様に文として書き直す）。

### Step 2: 上から読み、1か所ずつ直す

1. 原文に lint（種類が決まっていれば `--doc-type`）。候補は合図ではない。0件でも §1 の型を探す。直訳語は `calques.md` の2問で読み直す。`review-points.md` / `slop-catalog.md` 10章を参照。
2. 型を探す前に、読み手として上から1回読み、止まる所を内部メモする（出力しない）。
3. 直す前に案を1つ書き、`rephrase-test.md` の6点で確かめる。1点でも変わる案は捨て原文を残す。fact の穴は `fact-recovery.md`。
4. 本文は1か所ずつ直す。sed/perl/python の一括置換は使わない。

書き直す前の lint:

```bash
python3 .cursor/skills/yomiyasu/scripts/yomiyasu_lint.py path/to/file.md --doc-type=article
# 未 sync なら omega/skills/yomiyasu/scripts/...
```

### Step 3: 検査（omega: lint + diff）

最終稿を保存したあと、上流の `yomiyasu_check.py run` の代わりに lint と diff を別々に実行する。

```bash
python3 .cursor/skills/yomiyasu/scripts/yomiyasu_lint.py 最終稿.md --doc-type=<種類>
python3 .cursor/skills/yomiyasu/scripts/yomiyasu_diff.py 元の文.md 最終稿.md --stance=<勧め|決まり|説明> --doc-type=<種類> --reader=<expert|informed|general>
```

`--stance` は §1 の立場。決めきれなければ diff から省いてよい。新規作成は diff の原文側に資料を渡すか、資料照合は `review-points.md` の目視手順に従う。出力の1行目（状態）と候補に従う。

Python が使えないときは同観点を目視。確認の記録は `yomiyasu-check: not_run reason=no_python`。

### Step 4: 読み手として読み、候補を確かめる

- 最終稿を読み手として通読する。
- diff の候補を `review-points.md` に従い1つずつ確かめる。意味が変わっていれば元に戻す。修正は1回まで。その後 lint + diff を再実行。

### Step 5: 提出前の点検（omega: verify なし）

上流の `verify --final` は同梱しない。代わりに:

- 最終稿の lint の info（残した語）を Step 2 の問いで読み直す。
- 原文と最終稿で地の文の読点を比べ、増えた読点が `writing-rules.md`「文長と読点の調整」の残す読点に当たらなければ外す（`review-points.md`「読点の増加」）。
- 直したら Step 3 をやり直す。

## 出力フォーマット

本文だけを返す指定なら、メタ欄は出さない（検査は同じ）。

```markdown
### 書き直した本文

（推敲済み本文。見出しや箇条書きを保つ）

---

### 変えたところ
- 元の表現 → 書き直し後（理由）。最大5点。なければ「なし」

### 残したAIっぽいところ
- （意味のために残した表現と理由。なければ見出しごと省略）

### 書き手に確かめたい点
- （最大3点。なければ見出しごと省略）

### 事実の確かめ
（補った・直した事実の出典。なければ省略）

### 確認の記録
- 書き手・読み手・場面: 書き手: …／読み手: …／場面: …（指定か推定）
- 実行した検査: lint / diff / 目視（実行したものだけ）
- 実行しなかった検査: 最終稿の照合（check・verify 未同梱のため）ほか
- 硬化の検査・勢いの検査: diff 出力があれば写す
- 見直し候補: diff 出力の件数行があれば写す
- 状態: lint/diff の先頭行、または `yomiyasu-check: not_run reason=no_python`
```

エッセイ・promo と判断して個性を残したときは、確認の記録の下に1行（例: 「エッセイと判断したので、文の個性を残しました」）。

ファイル編集依頼時は指定パスへ保存し、上記メタは返信に含める。

## 上流との関係

submodule `yomiyasu/`（[nanaism/yomiyasu](https://github.com/nanaism/yomiyasu) **v3.1.0**）。omega は Cursor 用抜粋（`references/` + lint/diff）。同期: `scripts/sync-from-upstream.sh`、手順: `references/UPSTREAM.md`。
---
name: yomiyasu
description: >-
  AIが生成した不自然な日本語を、人間が読みやすい自然な文章へ書き直す（Cursor / omega 向け抜粋版、上流 v2.5 系）。
  「読みやすくして」「AI臭を消して」、技術記事・PR説明・仕様・study-log 下書きの推敲で使用。
  forge-mode Ship 中の自動適用はしない。
metadata:
  upstream_version: "2.5.0"
---

# yomiyasu（omega / Cursor）

AI特有の比喩・壊れた主述・装飾過多を直し、**意味を変えず**に読みやすい日本語へ再構成する。ルールの正本は `references/writing-rules.md`（上流 SKILL §1）。

## omega での位置づけ

| 項目 | 方針 |
|------|------|
| 起動 | **ユーザー明示依頼時のみ**（チャットへの貼り付け推敲、Markdown ファイル指定） |
| forge-mode | Ship 中は自己起動しない。PR 本文を日本語で書く依頼があったときだけ |
| study-log | 記事の**下書き完成後**の任意ステップ。study-log 執筆と同一ターンで両方オンにしない |
| decision-log | Notion 本文を日本語で整える依頼時。事実・数値は `writing-rules.md` の不増補を厳守 |
| 干渉 | 他の日本語校正スキルと同時有効化しない（上流 README 同様） |

Claude Code プラグイン・`npx skills`・`yomiyasu_check.py`（run/verify）は omega では**同梱しない**。Cursor では **lint + diff** と目視点検で足りる。

## 読む順（on-demand）

1. `references/writing-rules.md` — 必須
2. 文書の種類 — 決めたら `references/doc-types/<種類>.md`（13種。表は Step 1）
3. ドメイン — `references/domains/tech.md` / `business.md` / `essay.md`
4. 変換・lint 解釈 — `gemini-syntax.md`, `slop-catalog.md`, `calques.md`, `rephrase-test.md`, `review-points.md`
5. 読者・敬語 — 指定があれば `audience.md`, `persona.md`
6. 自分で書いた原稿の事実 — `fact-recovery.md`（必要時）

## 実行手順

### Step 1: 把握

1. **種類・読者・ドメイン** — 種類は pr / article / incident / proposal / minutes / manual / slides / essay / formal / promo / mail / paper / script のいずれか（指定なければ依頼と本文から推定。決めきれなければ決めない）。読者は expert / informed / general（同様）。ドメインは tech / business / essay。
2. **段落と文の関係** — 話題、接続、意味の4点（主張・比重・言い切り・働き）、文の種類（事実・意見・比喩等）を内部で確認（出力に含めない）。
3. **立場** — 勧め / 決まり / 説明。文末を選ぶ前に文書の用件と段落の目的を確認（`writing-rules.md`「文書の立場と文末」）。

種類ごとに**当てない規則**がある（例: slides は箇条書きを地の文に戻す直しを当てない、pr は変更点の箇条書きを当てない）。詳細は上流 SKILL の表と各 `doc-types/*.md`。

### Step 2: 書き直し

書き直し**前**に lint をかける（種類が決まっていれば `--doc-type`）。

```bash
python3 omega/skills/yomiyasu/scripts/yomiyasu_lint.py path/to/file.md
# omega-sync 後: python3 .cursor/skills/yomiyasu/scripts/yomiyasu_lint.py ...
```

lint は合図ではなく手がかり。指摘語を別語に**差し替えるだけ**で済ませず、`calques.md` / `review-points.md` の問いで関係を読み直す。型に当たった箇所は `rephrase-test.md` の6点で案を確かめる。`writing-rules.md`・ドメイン・`gemini-syntax.md`・`slop-catalog.md` に従い直す。直す箇所がほとんどなければ無理に書き換えない。

表記: 補助動詞と形式名詞の「事」「為」はひらがなに直す。それ以外の表記揺れ（長音・送り仮名・全半角）は原文のまま。

### Step 3: lint（保存する推敲）

```bash
python3 .cursor/skills/yomiyasu/scripts/yomiyasu_lint.py path/to/file.md
```

`--strict`（CI）、`--doc-type`（13種）。指摘は機械候補。修正ループは最大2回。

### Step 4: diff 点検

```bash
python3 .cursor/skills/yomiyasu/scripts/yomiyasu_diff.py before.txt after.txt --stance=説明
```

`--stance` は Step 1 の立場（`勧め` | `決まり` | `説明`）。候補と全文差分で、言い回しの増減、文の種類の変化、許可・能力・保証、元にない語、段落・箇条書き・読点・見出しの変化を点検（観点は `review-points.md`）。修正は1回まで。

Python が使えない場合は同観点を目視。上流の `yomiyasu_check.py` は使わない。

## 出力フォーマット

依頼に**本文のみ**とあれば、メタ欄は出さず本文だけ返す。

通常の対話リライト:

```markdown
### 書き直した本文

（推敲済み本文。未定・調査中の状態は残す。注記・質問は本文に入れない）

---

### 変えたところ
- （最大5点。理由を短く。なければ「なし」）

### 残したAIっぽいところ
- （意味を担うため残した箇所のみ。なければ見出しごと省略）

### 書き手に確かめたい点
- （最大3点。なければ見出しごと省略）

### 事実の確かめ
（補った・直した事実の出典。なければ省略）

### 確認の記録
- 実行した検査: lint / diff / 目視（実行したものだけ）
- 実行しなかった検査: （あれば理由。なければ「なし」）
```

ファイル編集依頼時は指定パスへ保存し、上記メタは返信に含める。絵文字・不要カッコなし。

## 上流との関係

submodule `yomiyasu/`（[nanaism/yomiyasu](https://github.com/nanaism/yomiyasu) **v2.5.0**）。omega は Cursor 用抜粋（`references/` + lint/diff）。同期: `scripts/sync-from-upstream.sh`、手順: `references/UPSTREAM.md`。

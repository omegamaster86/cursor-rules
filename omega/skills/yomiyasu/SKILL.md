---
name: yomiyasu
description: >-
  AIが生成した不自然な日本語を、人間が読みやすい自然な文章へ書き直す（Cursor / omega 向け抜粋版）。
  「読みやすくして」「AI臭を消して」、技術記事・PR説明・仕様・study-log 下書きの推敲で使用。
  forge-mode Ship 中の自動適用はしない。
---

# yomiyasu（omega / Cursor）

AI特有の比喩・壊れた主述・装飾過多を直し、**意味を変えず**に読みやすい日本語へ再構成する。

## omega での位置づけ

| 項目 | 方針 |
|------|------|
| 起動 | **ユーザー明示依頼時のみ**（チャットへの貼り付け推敲、Markdown ファイル指定） |
| forge-mode | Ship 中は自己起動しない。Opening a PR の boilerplate 最小方針と競合しないよう、PR 本文を日本語で書く依頼があったときだけ |
| study-log | 記事の**下書き完成後**の任意ステップ。study-log 執筆と同一ターンで両方オンにしない |
| decision-log | Notion 本文を日本語で整える依頼時。事実・数値は `writing-rules.md` の不増補を厳守 |
| 干渉 | 他の日本語校正スキルと同時有効化しない（上流 README 同様） |

## 読む順（on-demand）

1. `references/writing-rules.md` — 意味保持・立場と文末・段落（必須）
2. ドメイン — `references/domains/tech.md` / `business.md` / `essay.md` のいずれか（省略時は文面から推定）
3. 変換時 — `references/gemini-syntax.md`、`references/slop-catalog.md` を必要箇所だけ参照

Claude Code プラグイン・`npx skills`・`openskills`・`.claude-plugin/` は omega では**同梱しない**（Cursor の `.cursor/skills/yomiyasu` のみ）。

## 実行手順

### 1. 把握

- ドメイン: `tech` | `business` | `essay`（ユーザー指定または文面から）
- 段落の話題、文同士の関係、意味の4点（主張・比重・言い切り・働き）、文書の立場（勧め / 決まり / 説明）を確認（メモは出力に含めない）

### 2. 書き直し

`writing-rules.md` とドメイン仕様に従い、`gemini-syntax.md` / `slop-catalog.md` で語表・構文を直す。上流 `SKILL.md` Step 2 のチェックリスト（指示代名詞、比喩、接続、予告文、箇条書きと文末など）に沿う。直す箇所がほとんどなければ無理に書き換えない。

### 3. 静的検査（任意）

Markdown を保存する推敲では、スキル同梱リンターを実行できる。

```bash
# omega-link 後（PJ ルートから）
python3 .cursor/skills/yomiyasu/scripts/yomiyasu_lint.py path/to/file.md

# cursor-rules 正本で直接
python3 omega/skills/yomiyasu/scripts/yomiyasu_lint.py path/to/file.md
```

CI 用: `--strict`。指摘は機械候補。評価語・必要な否定は無理に消さない。修正ループは最大2回。

### 4. Diff 点検（任意・長文）

```bash
python3 .cursor/skills/yomiyasu/scripts/yomiyasu_diff.py before.txt after.txt --stance=説明
```

`--stance` は Step 1 で決めた立場（`勧め` | `決まり` | `説明`）。Python が使えない場合は、文末の立場・増減語・段落変化を目視で同観点チェック。修正は1回まで。

## 出力フォーマット

対話リライト時は次の形。絵文字・不要カッコなし。

```markdown
### 書き直した本文

（本文）

---

### 変えたところ
- （最大5点。なければ「なし」）

### 残したAIっぽいところ
- （意味を担うため残した箇所のみ。なければ見出しごと省略）

### 書き手に確かめたい点
- （最大2点。なければ見出しごと省略）
```

ファイル編集依頼のときは、ユーザーが指定したパスへ書き直し本文を保存し、上記メタは返信に含める。

## 上流との関係

正本リポジトリは cursor-rules 直下の git submodule `yomiyasu/`。omega に載せているのは **Cursor 用の抜粋**（`references/` 一部 + `scripts/yomiyasu_lint.py` + `yomiyasu_diff.py`）。取り込み手順は `references/UPSTREAM.md`。

出典: [nanaism/yomiyasu](https://github.com/nanaism/yomiyasu)（MIT）

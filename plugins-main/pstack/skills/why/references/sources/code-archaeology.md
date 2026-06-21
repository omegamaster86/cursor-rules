# コード考古学（git + リポジトリ内）

## このソースが含むもの

- コミット履歴（メッセージ、日付、著者、diff）
- PR 説明、レビューコメント、議論スレッド（`gh` 経由）
- インラインコードコメント、TODO、FIXME、非推奨注記
- ADR（リポジトリが保持する場合）
- テスト。名前とアサーションは変更を動機づけたエッジケースをしばしばエンコード
- 同じコミットで変更された関連ファイル（共変シグナル）
- CHANGELOG エントリ、リポジトリ内リリースノート
- コミットメッセージと PR 本文の issue/チケット ID

最も信頼できるソース。コードに直接結びつき、最も完全。リポジトリを通ったものはここにあるべき。

## 検索方法

シードコミットリストを拡張:

```bash
# Full history of the file through renames
git log --follow --oneline -- <file>

# Pickaxe: commits that added or removed this exact text
git log -S '<exact_string_from_code>' -- <file>

# Or for patterns:
git log -G '<regex>' -- <file>

# Who wrote each line and when
git blame -L <start>,<end> <file>

# The full diff of a specific commit
git show <hash>

# Commits between two points affecting this file
git log <old>..<new> -p -- <file>
```

各実質的コミットについて PR コンテキストを引く:

```bash
# Find the PR number from the merge commit or branch
git log -1 --format=%B <hash>

# Full PR context: body, review comments, linked issues
gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews,files

# The --json reviews and comments fields are where the real signal is
```

帯外 doc を探す:

```bash
# ADRs often live in docs/adr/ or similar
rg -l -i 'architecture.decision' --glob '*.md'

# TODOs and FIXMEs near the target
rg -n -C2 '(TODO|FIXME|HACK|XXX|NOTE)' <target_file>

# Related tests. Names often encode the "why"
rg -l '<symbol>' --glob '*test*'
```

## ここでの良い証拠

- 変更だけでなく解決する問題を説明する PR 説明（「X を引き起こすページネーションバグを修正」）
- 代替が議論された長いレビュースレッド
- 対象行近くの非自明制約を説明するインラインコメント
- コードを動機づけたエッジケースを示す `test_handles_edge_case_when_X` 名テスト
- チケットやインシデント ID を参照するコミットメッセージ
- ユーザー可視根拠を要約する CHANGELOG エントリ

## 一般的落とし穴

- **Squash-merge 平坦化。** squash リポジトリではブランチ履歴の個別コミットが失われる。PR 本文とコメントにフォールバック。
- **誤解を招くコミットメッセージ。** 「Small refactor」が意図的振る舞い変更を隠すことがある。メッセージではなく diff を見る。
- **cargo-cult パターン。** 著者が理由を理解せずパターンをコピーした可能性。パターンがコードベースでより早く始まったコミットを調べ*その*コミットを調査。
- **Bot コミットと自動マージ。** Dependabot、Renovate、自動 backport は通常動機を運ばない。意図探しではスキップ。
- **コードを意図の証拠として扱う。** コード自体は存在理由の証拠ではない。証拠は commit message、PR、コメント、テスト、doc。「関数が X と名付けられている」を意図の証拠として引用しない。

## 返すもの

質問に関係する各 commit/PR/comment について:
- 正確なテキスト（引用）
- hash / PR 番号 / file:line
- 著者と日付
- direct（質問に明示的）か circumstantial か

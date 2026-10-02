# コード考古学（git + リポジトリ内）

## このソースに含まれるもの

- コミット履歴（メッセージ、日付、作者、diff）
- PR 説明、レビューコメント、議論（`gh` 経由）
- インラインコメント、TODO、FIXME、非推奨注記
- ADR（アーキテクチャ決定記録）（リポジトリが保持している場合）
- テスト。名前とアサーションは変更の動機となったエッジケースをしばしばエンコードする
- 同じコミットで変更された関連ファイル（共変シグナル）
- CHANGELOG、リポジトリ内リリースノート
- コミットメッセージと PR 本文に出る issue / チケット ID

最も信頼でき、コードに直結し、最も完全。リポジトリを通ったものはここにあるはず。

## 検索方法

シードコミットリストを広げる:

```bash
# リネームを通したファイルの全履歴
git log --follow --oneline -- <file>

# Pickaxe: この文字列を追加/削除したコミット
git log -S '<exact_string_from_code>' -- <file>

# パターン用:
git log -G '<regex>' -- <file>

# 各行の作者と日時
git blame -L <start>,<end> <file>

# 特定コミットの完全 diff
git show <hash>

# 2点間でこのファイルに触れたコミット
git log <old>..<new> -p -- <file>
```

実質的なコミットごとに PR 文脈を取る:

```bash
# マージコミットまたはブランチから PR 番号
git log -1 --format=%B <hash>

# PR 全文: 本文、レビューコメント、リンク issue
gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews,files

# 本当のシグナルは --json の reviews と comments
```

リポジトリ外ドキュメント:

```bash
# ADR は docs/adr/ など
rg -l -i 'architecture.decision' --glob '*.md'

# 対象付近の TODO / FIXME
rg -n -C2 '(TODO|FIXME|HACK|XXX|NOTE)' <target_file>

# 関連テスト。名前はしばしば「なぜ」をエンコード
rg -l '<symbol>' --glob '*test*'
```

## ここでの良い証拠

- 解く問題を説明する PR 説明（変更だけではない）（「X を起こすページネーションバグを直す」）
- 代替が議論された長いレビュー
- 対象行付近の非自明な制約を説明するインラインコメント
- 動機のエッジケースを示す `test_handles_edge_case_when_X` のようなテスト名
- チケットやインシデント ID を参照するコミットメッセージ
- ユーザー可視 rationale を要約する CHANGELOG 項目

## よくある落とし穴

- **Squash-merge の平坦化。** squash するとブランチ内の個別コミットが失われる。PR 本文とコメントにフォールバック。
- **誤解を招くコミットメッセージ。** 「小さなリファクタ」が意図した挙動変更を隠すことがある。メッセージより diff を見る。
- **模倣パターン。** 作者は理由を理解せずコピーしたかもしれない。パターンがコードベース内でより早く始まったコミットを追い、**その**コミットを調べる。
- **Bot コミットと自動マージ。** Dependabot、Renovate、自動バックポートは動機をほぼ持たない。意図を探すときはスキップ。
- **コードを意図の証拠にしない。** コード自体は存在理由の証拠にならない。証拠はコミットメッセージ、PR、コメント、テスト、ドキュメント。「関数が X と名付けられている」は意図の証拠として引用しない。

## 返すもの

質問に関係するコミット/PR/コメントごとに:

- 正確なテキスト（引用）
- ハッシュ / PR 番号 / file:line
- 作者と日付
- direct（質問に明示的）か circumstantial か

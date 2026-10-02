# Linear チケット

## このソースに含まれるもの

- 機能・バグとその動機を説明する issue
- issue に添付されたプロジェクトドキュメント（しばしば PRD や仕様）
- 親子 issue 関係（より大きな initiative → 具体チケット）
- issue コメント（明確化、スコープ変更、「なぜやるか」の rationale）
- ラベル（`compliance`、`customer-request`、`perf` など動機の種類のシグナル）
- スコープ変更を説明するステータス更新
- 添付とリンクされた GitHub PR

Linear にはプロダクト／ビジネス文脈がよくある。「顧客 X が依頼したから」「Q3 コンプライアンス initiative のため」という層。

## 検索方法

Linear MCP を使う。

1. **リンクチケットから。** シードコミットや PR がチケット ID（`ENG-1234`、`[BUG-567]`）を参照していれば、まず `get_issue` で取得。コメントまで全文読む。
2. **キーワードで関連 issue を列挙。** `list_issues` で機能名、主要シンボル、ビジネス用語をテキスト検索。言い回しを変えて試す。
3. **issue ツリーを歩く。** サブ issue に着地したら親を取得。サブは戦術的、親が「なぜ」を持つことが多い。
4. **プロジェクトドキュメントを読む。** issue がプロジェクトに属すなら `get_project` で添付 doc を確認。プロジェクトレベルに仕様と rationale が最もよく残る。
5. **ラベルとマイルストーン。** ラベルは動機のカテゴリ（customer-request、incident-followup、compliance）。マイルストーンは期限と結びつき、動機が見えやすい。

## 良い証拠

- ビジネス問題を述べる issue 説明（「顧客 Acme は SOC2 監査のため X が必要」）
- 決定を記録するコメント（「A は billing サービスに触れるため B にした」）
- initiative 的な親 issue タイトル（「Q3 Enterprise Readiness」「Reduce Payment Failures」）
- 添付 PRD や仕様
- `customer:acme`、`incident-followup`、`compliance`、`perf-regression` などのラベル

## よくある落とし穴

- **スコープドリフト。** PR が参照するチケットは閉じて別スコープで再開されていることがある。履歴全体を読む。
- **機械的テンプレート。** 「Why」必須でも boilerplate だけ。「UX 改善」など汎用文は本当の答えではない可能性。
- **古いチケット。** 計画が変わった古い内容。日付とコードの出荷日を照合。
- **duplicate チェーン。** duplicate-of を辿って正本チケットへ。
- **非公開ワークスペース。** issue にアクセスできないなら推測せずギャップとして記録。

## 返すもの

関連チケットごとに:

- チケット ID とタイトル
- 説明またはコメントからの問題／動機の引用（言い換え不可。synthesizer が exact テキストで引用する）
- ラベル、親 issue、プロジェクト
- 作者、作成日、クローズ日
- リンク（あれば）

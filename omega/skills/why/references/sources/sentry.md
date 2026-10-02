# Sentry エラー履歴

## このソースに含まれるもの

Sentry はうまくいかなかったことの記録。防御・修正・エラーハンドリングコードでは、チェック・catch・リトライ・フォールバックを追加させた具体的な例外、スタックトレース、頻度という**直接の動機**がよくある。

- **Issues.** カウント、first/last seen、影響リリース、コメント付きのグループ化エラー
- **Events.** issue 内の個別インスタンス（スタックトレース、タグ、ユーザーコンテキスト）
- **Releases.** 関連 issue 付きデプロイ記録（「どのバージョンで直った？」に有用）
- **Replays.** ユーザー向けエラーのセッション録画（有効な場合）
- **Profiles.** パフォーマンスプロファイル（「なぜ」より「どれくらい遅い」向き）
- **Issue コメントとアサイン.** 根本原因のエンジニアメモがあることも

Sentry の最有価値は**時間相関**:「issue X は 2024-01-02 作成、1日 500 events でピーク、2024-01-15 の v2.14.0（防御チェックを出荷したリリース）以降は出なくなった」

## 検索方法

Sentry MCP を使う。

1. **オリエント。** プロジェクト slug と org が不明なら:

   ```
   find_organizations
   find_projects
   ```

2. **対象関連 issue を検索.**

   ```
   search_issues（自然言語。例: "PaymentService timeout のエラー", "uploadFile の未処理例外"）
   ```

   良いクエリ要素: 対象が扱う例外クラス、対象の関数／クラス名、対象がチェックするエラーメッセージ、対象のファイルパス。

3. **リリースと時間窓で絞る.**

   ```
   search_issue_events（release、時間、環境、trace ID、タグでフィルタ）
   get_issue_tag_values（issue のバージョン・ユーザー・環境分布）
   ```

   疑わしい issue では確認:
   - **First seen** — エラーはいつから？
   - **Last seen** — いつ止まった？対象の出荷日と一致？
   - **Affected releases** — どのバージョンで？修正は？
   - **頻度の推移** — スパイクして解消？

4. **全文脈の event を取得.**

   ```
   get_sentry_resource（Sentry URL または type+ID）
   ```

   スタックトレースは対象を通る？タグと breadcrumb は対象が防ぐ条件と一致？

5. **対象付近のリリース.**

   ```
   find_releases（対象のコミット日付前後）
   ```

   リリースバージョンと PR マージ日を照合。

6. **Seer は控えめに.**

   ```
   analyze_issue_with_seer
   ```

   Seer は AI 根本原因分析。仮説生成には有用だが inference として扱い、 authoritative ではない。一次証拠は event とスタックトレースとタイムスタンプ。Seer の narrative は二次。

## 良い証拠

- **First seen** が対象 PR の直前、**Last seen** が直後 — 対象がこのエラーに対処した示唆
- 対象関数を通過または着地するスタックトレース — 防いでいる失敗モードの具体
- PR 作者による issue コメントで修正を説明
- 対象の PR 説明やコミットが Sentry issue URL/ID を参照
- 高 event 数の issue が対象を含むリリース後に停止

## よくある落とし穴

- **グルーピングドリフト。** fingerprint でグループ。リファクタで「同じ」エラーが新 issue ID になる。急終了なら再グループの可能性。直後の新 issue を確認。
- **リリース相関はノイジー。** 1リリースに多数コミット。v2.14.0 で止まっても対象の証明ではない。同リリースの別変更と照合。
- **サイレント修正。** 上流変更で止まり、防御コードとは無関係のことがある。相関は示唆、著者証明ではない。
- **resolved ≠ fixed.** 手動 resolved でコード変更なし。`resolved` は人間マーカー。
- **Seer の hallucination.** 自信ある説明が誤り。claim 時は event・スタック・タイムスタンプに戻る。
- **サンプリング.**  aggressive サンプリングで event 数が低く見える。疑わしければギャップを記録。

## 返すもの

関連 issue ごとに:

- Issue ID とタイトル
- プロジェクトと organization
- First seen / last seen
- Event 数（サンプリング率が分かれば）
- 影響リリース
- 対象との関連を示す代表スタックトレース抜粋（verbatim、要約不可）
- 対象出荷日との first/last 相関
- Issue リンク
- 作者コメントや resolution メモ

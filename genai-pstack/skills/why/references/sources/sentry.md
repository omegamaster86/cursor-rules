# Sentry エラー履歴

## このソースが含むもの

Sentry はうまくいかなかったことのアーカイブ。防御的、修正的、エラーハンドリングコードには often 直接動機: チェック、catch、リトライ、フォールバック追加を押した特定例外、スタックトレース、頻度。

- **Issues.** カウント、first/last seen タイムスタンプ、影響リリース、コメント付きグループ化エラー
- **Events.** issue 内個別エラーインスタンス（スタックトレース、タグ、ユーザーコンテキスト）
- **Releases.** 関連 issue 付きデプロイ記録（「どのバージョンが直した？」に有用）
- **Replays.** ユーザー向けエラーのセッション録画（有効時）
- **Profiles.** 性能プロファイル（「why」より「how slow」向け）
- **Issue comments & assignments.** しばしば根本原因のエンジニアメモ

Sentry の最も価値あるものは**時間相関**:「issue X は 2024-01-02 作成、500 events/day ピーク、2024-01-15 v2.14.0 リリース後出現停止。防御チェックを出荷したリリース」。

## 検索方法

Sentry MCP を使用。

1. **向き合い。** プロジェクト slug と organization が不明なら:

   ```
   find_organizations
   find_projects
   ```

2. **対象関連 issue を検索。**

   ```
   search_issues (natural language, e.g., "errors in PaymentService timeout", "unhandled exceptions in uploadFile")
   ```

   良いクエリ要素: 対象が扱う例外クラス、対象の関数/クラス名、対象がチェックするエラーメッセージ、対象ファイルパス。

3. **リリースと時間ウィンドウで絞る。**

   ```
   search_issue_events (filter by release, time, environment, trace ID, tags)
   get_issue_tag_values (for an issue, see distribution across versions, users, environments)
   ```

   疑わしい issue について確認:
   - **First seen.** エラーはいつ始まった？
   - **Last seen.** いつ止まった？対象出荷日と一致？
   - **Affected releases.** どのバージョンで見え、どれが fix？
   - **Frequency trajectory.** スパイクして解決？

4. **コンテキストのためフルイベント取得。**

   ```
   get_sentry_resource (pass a Sentry URL or type+ID)
   ```

   スタックトレースは対象コードを通るか。タグと breadcrumb は対象が防御する条件と一致？

5. **対象近傍のリリースを確認。**

   ```
   find_releases (around the commit date of the target)
   ```

   リリースバージョンと PR マージ日を突合。

6. **Seer は控えめに。**

   ```
   analyze_issue_with_seer
   ```

   Seer は AI 根本原因分析を産出。仮説生成器として有用だが inference として扱い authoritative ではない。実イベントとスタックトレースが主要証拠。Seer 叙述は二次。

## 良い証拠

- **first seen** が対象 PR 直前、**last seen** が直後で、対象がこのエラーに対処した示唆
- 対象関数を通る/着地するスタックトレースで、防御対象の正確な失敗モードを示す
- 修正を述べる PR 著者の issue コメント
- 対象 PR 説明/commit message が Sentry issue URL または ID を参照
- 対象を含むリリース後に止まった高イベント数 issue

## 一般的落とし穴

- **Grouping drift.** Sentry は fingerprint でグループ。リファクタ/改名で「同じ」エラーが新 issue ID で追跡。issue が abrupt 終了ならエラーが regroup されただけかも。直後の新 issue を確認。
- **Release 相関はノイズ多い。** 1 リリースに多コミット。v2.14.0 で issue 停止は対象 fix の証明ではない。同リリースの別変更かも。対象の正確 commit と突合。
- **Silent fixes.** エラー停止は上流変更のためで防御コードではないことがある。相関は fix を示唆。著者証明ではない。
- **Resolved != fixed.** issue は手動 resolved でコード変更なし。`resolved` は人間マーカーであり fix 証拠ではない。
- **Seer hallucinations.** Seer は confident で誤った説明を生成しうる。主張するときは実イベント、スタック、タイムスタンプにフォールバック。
- **Sampling.** 一部プロジェクトは aggressive サンプリング。低イベント数は稀エラーではなく高サンプリングかも。疑わしければギャップを記す。

## 返すもの

各関連 issue について:
- Issue ID とタイトル
- Project と organization
- First seen / last seen タイムスタンプ
- Event count（既知なら sampling rate）
- Affected releases
- 対象関連を示す代表スタックトレース snippet（逐語抜粋、要約不可）
- 対象出荷日との first/last-seen 相関
- Issue リンク
- 著者コメントまたは resolution メモ

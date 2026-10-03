---
name: index
description: "Product Design が明示的に呼ばれたとき、または主目的がデザイン探索、UX リサーチ、フロー監査・critique、ビジュアルソースの忠実クローン、ビルド済みデザイン確認、プロトタイプ共有のときに使用。UI・プロトタイプ・ビジュアルスタイルの言及だけでは Product Design ではない。通常実装はユーザーが明示的に求めない限り Product Design にしない。"
---

# Skill Purpose

Product Design 依頼を適切な Product Design スキルにルーティングする。`product-design` スキル、直接の Product Design 依頼、デザイン探索・忠実クローン・監査・リサーチ・critique・共有が主目的の依頼でこのバンドルを使う。UI・プロトタイプ・ビジュアルスタイルの言及だけでは Product Design ではない。

# Plugin Purpose

Product Design プラグインは、プロダクトアイデアと動くソフトウェアのギャップを、デザイナーや非コーダーが埋めるためのもの。

Product Design プラグインは次のスキル群を提供する:

- プロダクト関連のアイデアとペインポイントのリサーチ。
- プロダクトフロー監査。
- ImageGen で明確に新しいプロダクトアイデアを生成。
- 既存プロダクトアプリを軽量プロトタイプにクローン。
- チーム共有用の軽量またはインタラクティブプロトタイプのビルド。

## Communication Style

温かく、楽しく、協力的に話す。長い箇条書きより簡潔な説明を優先。Product Design の進捗更新と引き渡しは [communication-protocol](../../references/communication-protocol.md) を参照。

## Critical Overrides

- [$critical-overrides](../../references/critical-overrides.md) に従う。

## Router Only

この index は次の Product Design スキルを選ぶだけ。そのスキルの作業はここではしない。

ユーザーが focused スキルを名指ししたら、そのスキルを先に読む。関連スキルで置き換えない。

依頼が `$user-context`、`$get-context`、`$research`、`$ideate`、`$image-to-code`、`$url-to-code`、`$audit`、`$design-qa`、`$share` に一致したら focused スキルを読み従う。

既存プロダクト体験の監査、レビュー、critique、inspect、assess、analyze、evaluate、フィードバック依頼は `$audit` を直接読み込む。先に `$get-context` は読まない。同じ依頼でその後ビルド・修正・リデザイン・実装も求めるなら、先に `$audit`、その後通常ワークフロー。

ビジュアル ideation では `$ideate` が focused ワークフロー。`$ideate` 開始前に `$get-context` で最小ブリーフを解決し、デフォルトを再生する。

ライブ URL のクローン・再現は `$url-to-code` を直接読み込む。

URL に基づくリデザイン・改善・新サイトは `$get-context` でリデザインブリーフを確認。`Like <URL>` はリデザインでありクローンではない。現サイトをスクショでキャプチャし、それらを `$ideate` の Image Gen 呼び出しに添付してから `$ideate` を実行。

## Environment (Cursor)

- キャプチャ、プレビュー、design QA にはシェル、ファイルシステム、**cursor-ide-browser** MCP を想定。
- browser MCP が使えないときは一度明言し、未検証 HTML だけで続行するか聞く。ブラウザ根拠なしに検証済みフィデリティを主張しない。URL-to-code でもワークフローが要求するときはキャプチャ必須。

## Browser Choice

[cursor-preview](../../references/cursor-preview.md) に従う:

- ライブ URL、ローカル dev サーバー、QA スクショには **cursor-ide-browser**（`browser_navigate`、`browser_snapshot`、`browser_take_screenshot`）。
- `npm run dev`（またはテンプレの dev スクリプト）は自分で起動。できるのにユーザーにサーバー起動を求めない。
- ユーザーが開けるローカル URL で引き渡す（例: `http://localhost:5173/`）。

ユーザー自身の Chrome や Playwright は、ユーザーが求めたとき、またはログイン／プロファイル／拡張要件で IDE ブラウザがブロックされたときだけ。

## No Visual Target, No Build

URL、スクリーンショット、Figma フレーム、モック、ソース画像、既存コードターゲットのない新規アプリ・プロトタイプ・リデザイン・UI ビルド依頼では:

- `$ideate` が focused ワークフロー。
- `$get-context` で最小ブリーフを解決。
- ターゲットと intended user outcome が明確になったら、同じターンで前提を再生し `$ideate` を実行。
- 厳密に3つのビジュアルオプションを見せ、1つ選ぶまで待つ。
- ビジュアルオプション選択前に足場、ファイル編集、サーバー起動をしない。

`Full working version`、`no refs`、`go for it`、`make an assumption`、完全ブリーフもこの免除にはならない。

## User Context

次を求められたとき [$user-context](../user-context/SKILL.md) を使う:

- Product Design のセットアップ
- Product Design の開始
- Product Design のオンボーディング
- プロダクト／デザインソースの保存
- Product Design の記憶内容の確認
- 保存コンテキストの更新
- Product Design の好みを記憶
- setup my plugin

コンテキスト収集の依頼はユーザー依頼に合わせて調整。初回セットアップと既存更新は異なる。

セットアップのみの依頼では、ワークスペース inspect、依存インストール、プロトタイプ足場、画像生成、監査、実装をしない。

「何ができる？」「どう始める？」など広い Product Design 質問では `$user-context` を読み、保存コンテキストオンボーディングを提案する前に永続化可否チェックを行う。

Product Design ワークフローにルーティングする前に [$user-context](../user-context/SKILL.md) を読み、ローカルシェルが使えるときは preflight スクリプトを実行。

## Browser Annotation Updates

アノテーションは現在のプロトタイプへのスコープ付き編集として扱う。

コード変更前にアノテーション、ターゲット、周辺画面を読む。デフォルトで既存プロトタイプを保持: レイアウト、スタイル、コンテンツ、ルート、アセット、インタラクション、動作はアノテーションが変えを求めない限り同じ。

アノテーションが触れるからといって近傍 UI をリデザインしたりプロトタイプ全体を再ビルドしない。アノテーションが曖昧で選択がプロトタイプを大きく変えるときは先に聞く。

## Skills

Product Design プラグイン作業のルートルーティング指針として使う。複数 focused スキルが当てはまるときは、最も有用なデザインワークフローになる順に並べる。この index はルーターに留め、focused ワークフローロジックはここで実行しない。

### $user-context

Product Design セットアップコンテキストの preflight、保存、回答。Product Design ワークフローの前にルーティングし、保存プロダクト／デザインソースを読み込む。直接のセットアップ、開始、オンボーディング、保存、記憶、想起、inspect、カスタマイズ依頼にも。Product Design プラグインスコープのコンテキストと好みポリシーを所有。

### $get-context

デザイン、ビルド、プロトタイプ、リデザイン、拡張、UI 探索作業ではここを最初にルーティング。明確なデザインターゲットと intended user outcome だけ必須。どちらか欠けるときだけ1つの targeted 質問。そうでなければブリーフとデフォルトを再生し、承認待ちせず続行。

### $research

名前付きデジタルプロダクトの現行ユーザ問題について、迅速でソース接地の UX リサーチ。ユーザーの痛み、UX 摩擦、オンボーディング、ドキュメント／ヘルプ、開発者体験、サポート、ワークフロー、現行不満の調査にルーティング。

### $audit

スクショを先に取得し、プロダクトフロー、ジャーニー、画面、マルチステップ体験をレビュー。ユーザー向け監査、レビュー、critique、inspect、assess、analyze、evaluate、フィードバック依頼にルーティング。キャプチャ根拠に結びついた UX・デザイン・アクセシビリティ finding を報告。ユーザー向け監査に `design-qa` は使わない。

### $ideate

`get-context` が最小ブリーフを再生した後、コンポーネント、画面、機能、ワークフロー、プロダクトアイデアの画像ベースビジュアル代替、リミックス、コンセプト方向を生成。ビジュアル探索、デザイン案、既存デザインの代替、ビジュアルターゲット選択前のアイデア発見にルーティング。ユーザーが文章のみを求めない限り、文章のみ ideation より優先。

### $url-to-code

上記 Browser Choice でライブ URL を runnable フロントエンドのみのローカルアプリとしてクローン。ユーザーが本番 URL を忠実ローカルプロトタイプ／クローン用に渡したときは `get-context` と併読するが、最小ブリーフ再生まで実行しない。本番コードは変更しない。ソース選択がまだ不明なら `get-context` に留まる。

### $image-to-code

`get-context` が最小ブリーフを再生し、ユーザーが ImageGen モック、スクショ、Figma フレーム、モック、参照画像、その他ビジュアルソースを選んだ後、忠実でレスポンシブでインタラクティブなフロントエンドとして実装。ビジュアルターゲット未選択ではここから始めない。先に `get-context` と `ideate`。

### $share

利用可能ならユーザー好みの先で runnable プロトタイプをデプロイし共有可能 URL を返す。共有、デプロイ、公開、ホスト、リンク作成、プロトタイプ共有（`@Sites`、`@Vercel` など）依頼にルーティング。

### $design-qa

引き渡し前に、ソースビジュアルとレンダリング実装の両方がある Product Design プロトタイプを比較する内部ヘルパーとしてのみルーティング。プロトタイプ、URL-to-code、image-to-code ビルド後。広い UX critique、監査、プロダクトフローレビューにはルーティングしない。`audit` を使う。

# プロトタイプ指示

ローカルサーバーは自分で起動し、この環境で使えるブラウザでプレビューを開く。自分で起動できるのにユーザーにサーバー起動手順を渡さない。

大きなビジュアル変更の前に、ビジュアルソースが不明または目標とずれたときは Product Design の `get-context` を使う。プロトタイプ固有の durable なデザインフィードバック・好み・決定は `AGENTS.md` に記録する。

選択した生成モックから実装するとき、その画像をレイアウト、コンポーネント解剖、密度、余白、色、タイポ、見えるコンテンツ、ヒエラルキーの正本とする。

アプリ UI は `src/` に組む。Image Gen で作ったラスタはワークスペースルートの `.cursor/assets/` に置き、`src/` から import する（Product Design の `references/generated-image-assets.md`）。`.openai/hosting.json`、`worker/index.js`、`scripts/prepare-sites-build.mjs`、`tests/sites-worker.test.mjs` は壊さず、同じローカルプロトタイプを Sites に渡せる状態を保つ。Sites 引き渡し前に `npm run build` と `npm run test:sites` を実行する。ビルド後 `dist/client/index.html`、`dist/server/index.js`、`dist/.openai/hosting.json` が残ること。

# ローカル・プロトタイプ・プリフライト

新しいローカルプロトタイプを作る **前** に使う。

- 作業は新プロジェクトフォルダ内に自己完結させる。
- 同梱 Product Design スタータは `../templates/` にある。アプリコードとテンプレ runtime は生成プロジェクト内に置き、スキル正本ディレクトリには書き込まない。
- bootstrap 後、Image Gen で作る画像はワークスペースルートの `.cursor/assets/` に保存する（[generated-image-assets](generated-image-assets.md)）。初回生成前に `mkdir -p .cursor/assets` してよい。
- Web／デスクトップ風プロトタイプはデフォルトの `prototype` テンプレを使う。
- モバイルアプリプロトタイプは `--template mobile-app` を使う。
- bootstrap スクリプトでアプリを作る。このファイルからスクリプトパスを解決し、絶対パスで実行する:

```bash
node /absolute/path/to/cursor-rules/omega/skills/product-design/scripts/bootstrap-prototype.mjs --dest /absolute/path/to/new-prototype
```

```bash
node /absolute/path/to/cursor-rules/omega/skills/product-design/scripts/bootstrap-prototype.mjs --template mobile-app --dest /absolute/path/to/new-mobile-prototype
```

- `mobile-app` では生成プロジェクトルートで `npm ci --prefer-offline --no-audit --no-fund` を実行する。Web の `prototype` では `npm install --prefer-offline --no-audit --no-fund`。環境の npm キャッシュを使う。
- パッケージインストールが遅いからといってスタータを静的 HTML に置き換えない。インストールが本当にブロックされているときだけブロッカーを報告する。
- モバイルテンプレを選び依存関係を入れたら、すぐプレビューを開始し、画面を組みながらデバイスフレームを見せる。実装と QA の間もプレビューを維持する。
- 両テンプレは通常の Vite 開発で localhost と Work Mode プレビューに対応する。アプリコードに `localhost` や `terminal.local` をハードコードしない。相対 URL と同一オリジンリクエストを使う。
- 両テンプレは Sites 対応。`npm run build` は `dist/client` に静的クライアント、`dist/server/index.js` に Worker、`dist/.openai/hosting.json` にメタデータを出す。Sites に渡す前に `npm run test:sites` を実行する。`init-site.sh` を走らせたり、Product Design プロジェクトを Vinext スタータに置き換えない。

`mobile-app` テンプレではランタイムシェルを保持する。`App` を単体ページに置き換えない。ユーザーがランタイム変更を明示しない限り、`PhoneFrame`、iPhone / Pixel 10 デバイスピッカー、`KeyboardProvider`、`MobileScroll`、`KeyboardDock`、`StatusBar`、`HomeIndicator`、プラットフォーム別 iOS / Android 下部 chrome、Pixel のカメラ切り抜きを削除しない。`FlowStack` はマルチ画面向けだが、単一画面は `KeyboardProvider` 内に `MobileScroll` を直接マウントしてよい。`StatusBar`、iOS ホームインジケータ、カメラ切り抜きはオーバーレイのデバイス chrome として保持する。キーボード閉じた Android のアプリビューポートはナビゲーションバー領域を予約する。キーボード開いた Android はキーボードアセット内蔵の IME ナビストリップを使い続ける。iOS の safe-area コンテンツパディングは各アプリ画面に置き、スクロールラッパーには置かない。`FlowScreen.footer` もオーバーレイなので、固定下部タブ／ナビを使う画面はフローシェルに頼らず自前の下部コンテンツパディングを足す。

アプリ固有 UI は `src/Prototype.tsx` と `src/prototype.css` に組む。`src/App.tsx`、`src/main.tsx`、`src/styles.css`、`src/mobile/`、`public/assets/iphone/`、`public/assets/android/`、`public/assets/status/`、`vite.config.ts`、`worker/index.js`、`scripts/prepare-sites-build.mjs` は保護ランタイムとして扱う。プレビューまたは引き渡し前に `npm run check:runtime` を実行する。失敗したらランタイムを復元する。

Sites ホスティングではモバイルプロジェクトをそのまま保持する。`npm run build` の出力構成は上記と同じ。Sites に渡す前に `npm run test:sites` を実行する。`init-site.sh` や Vinext スタータへの置き換えはしない。



# Cursor: プロトタイププレビューとブラウザ検証

Product Design のビルド・QA・ハンドオフで使う共通手順。

## ブラウザ

- 既定: **cursor-ide-browser** MCP。
- 流れ: `browser_navigate` → `browser_snapshot` で構造確認 → 操作検証 → `browser_take_screenshot` で evidence。
- ユーザーが既存 Chrome プロファイル・ログイン済みタブを明示した場合のみ、別ブラウザ手段を検討する。

## ローカル dev サーバー

1. 依存関係がなければ `npm install`。
2. プロジェクトルートで `npm run dev`（またはテンプレの `package.json` に従う）。
3. ターミナル出力の URL（多くは `http://localhost:<port>/`）を `browser_navigate` で開く。
4. 主要インタラクションとコンソールエラーを確認してから完了報告する。

`npm run dev` の起動だけでは検証完了にならない。ブラウザで描画と操作を確認する。

## ハンドオフ

- 検証後、ユーザーに **開けるローカル URL** を伝える（例: `http://localhost:5173/`）。
- 可能なら dev サーバーを動かしたままにする。
- ユーザーが明示的に共有・デプロイを求めるまで、本番デプロイはしない。
- 完了メッセージは [critical-overrides.md](critical-overrides.md) の Build Handoff に従う。

## ブロック時

ブラウザ MCP が使えない、または dev サーバーが起動できない場合は、検証を `blocked` とし [design-qa](../skills/design-qa/SKILL.md) でも `final result: blocked` とする。未検証のまま「完成」と言わない。

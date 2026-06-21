---
name: control-ui
description: Web/IDE/Electron UI を駆動・検証するためのローカルブラウザ/CDP ハーネスを構築または適応。ローカル UI 確認、スクリーンショット、アクセシビリティ、パフォーマンスプロファイル、ビジュアル差分、UI 不具合再現に使用。
---

# Control UI

ローカルのブラウザ自動化を使って UI 挙動を証拠付きで検証します。まずリポジトリの Playwright・ブラウザ・Electron ハーネスを再利用し、なければ dev server や Chromium デバッグポート周辺で一時ハーネスを構成します。

## 利用用途

- 実ブラウザのフォーカス、キーボード入力、スクロール、リサイズ、描画に依存する UI 不具合の再現。
- スクリーンショットとスナップショットでビジュアル/アクセシビリティ変更を確認。
- 配布前のローカル Web / IDE / Electron 挙動をチェック。
- コンソールログ、ネットワークログ、CPU プロファイル、トレース、ヒープスナップショットを収集。
- `verify-this` のための before/after 証拠を作成。

## セットアップパターン

1. リポジトリのドキュメントに従ってローカルでアプリ起動。
2. 既存ハーネスを検出: Playwright テスト、Cypress 仕様、Storybook、ブラウザスクリプト、Electron 起動スクリプト、スナップショットツール。
3. Web アプリでは既存ブラウザツールでローカル URL に接続。
4. Electron/Chromium では対応時にリモートデバッグポートを有効化。
5. タブ順のみでなく安定した識別子で正しいページを選択。
6. 座標依存より、アクセシビリティロール、ラベル、安定した `data-*` セレクタを優先。

## 汎用 Web ハーネス

可能ならリポジトリの導入済みブラウザツールを使います。Playwright がある場合の最小例:

```javascript
import { chromium } from "playwright";

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
await page.goto("http://127.0.0.1:<port>");
await page.getByRole("button", { name: /submit/i }).click();
await page.screenshot({ path: "/tmp/ui-harness-after.png", fullPage: true });
await browser.close();
```

この検証のためだけに Playwright を新規依存として追加しない。既存の devDependencies または環境に既にあるブラウザツールを優先。

## 汎用 CDP ハーネス

`--remote-debugging-port=<port>` 付きで起動された Electron/Chromium アプリは CDP 接続します。

```javascript
import { chromium } from "playwright";

const browser = await chromium.connectOverCDP("http://127.0.0.1:<debug-port>");
const pages = browser.contexts().flatMap((context) => context.pages());
let page;
for (const candidate of pages) {
  if (await candidate.locator("<app-root-selector>").count()) {
    page = candidate;
    break;
  }
}

if (!page) {
  console.log(await Promise.all(pages.map(async (p) => ({
    title: await p.title(),
    url: p.url(),
  }))));
  throw new Error("対象ページが見つかりません");
}

await page.screenshot({ path: "/tmp/ui-harness-cdp.png", fullPage: true });
await browser.close();
```

`<app-root-selector>` は現在のリポジトリ固有の root ノード、ランドマーク、または `data-*` 属性など安定したマーカーに置き換える。

## 操作ループ

1. 操作前にページのスナップショット/スクリーンショットを保存。
2. 最新のページ構造から対象を選ぶ。
3. 一度に1つの操作だけ実施: click / type / keypress / drag / scroll / navigate / resize。
4. 新しいスナップショット/スクリーンショットを保存。
5. 想定の状態遷移を検証。
6. ユーザーが証拠提出を依頼した場合、before/after 比較の成果物を保存。

## CDP 機能

上位レベル API で不足する場合のみ低レベル CDP を使う。

- パフォーマンス: CPU プロファイル、トレース、paint フラッシュ、FPS、レイアウトシフト確認。
- メモリ: リーク調査のためのヒープスナップショットおよび強制 GC。
- ネットワーク: リクエストブロック、スロットリング、キャッシュ無効、リクエスト/レスポンスログ。
- レンダリング: ビューポート変更、配色スキームエミュレーション、reduce motion、アクセシビリティチェック。
- デバッグ: コンソールストリーム、例外捕捉、DOM スナップショット。

## ページ選択

1 つのデバッグポートで複数ウィンドウ/タブがある場合:

- テスト対象を示す明示的なマーカー（app root selector）を優先。
- 必要なら除外マーカーで誤選択を回避。
- 該当ページがない場合は、推測せず利用可能タイトル/URL を列挙。

## ガードレール

- ナビゲーションや構造変更後は古い要素参照に依存しない。
- クリック座標は、直前に新規スクリーンショットを取得した場合のみ使用。
- テストデータはローカルのみかつ破棄可能に保つ。
- プライバシー配慮が必要なワークスペースのスクリーンショット/ヒープスナップショットは、明示同意がない限り保存しない。
- 他リポジトリのセレクタ、ポート、スクリプトパスをハードコードしない。現在リポジトリのローカルマーカーを発見して利用。
- 作業後は開発サーバ、デバッグセッション、テンポラリプロファイルをクリーンアップ。

# モバイルプロトタイプ・エージェントガイド

## プロトタイプ指示

Cursor では自分で `npm run dev` を実行し、cursor-ide-browser MCP でアプリを検証し、ローカル URL（例: `http://localhost:5173/`）をユーザーに渡す。ユーザーが明示的に共有・公開・デプロイを求めない限りデプロイしない。自分で起動できるのにサーバー起動手順を渡さない。

モバイルアプリ変更の計画・実装前に、この `AGENTS.md` を全文読む。テンプレランタイムとコンポーネント指針の正本。

大きなビジュアル変更の前に、ビジュアルソースが不明または目標とずれたときは Product Design の `get-context` を使う。プロトタイプ固有の durable なデザインフィードバック・好み・決定は `AGENTS.md` に記録する。

選択した生成モックから実装するとき、その画像をレイアウト、コンポーネント解剖、密度、余白、色、タイポ、見えるコンテンツ、ヒエラルキーの正本とする。

## 編集境界

- アプリ固有 UI は `src/Prototype.tsx` と `src/prototype.css` に組む。
- `src/App.tsx`、`src/main.tsx`、`src/styles.css`、`src/mobile/`、`public/assets/iphone/`、`public/assets/android/`、`public/assets/status/`、`vite.config.ts`、`worker/index.js`、`scripts/prepare-sites-build.mjs` は保護ランタイム。ユーザーがモバイルランタイム自体の変更を明示しない限り編集・置換・削除・再作成しない。明示的ランタイム変更では、新挙動を検証したあとだけ該当 lock ハッシュを更新する。
- プレビューまたは引き渡し前に `npm run check:runtime` を実行する。失敗したらチェックを弱めず保護ランタイムを復元する。
- `npm run build` はモバイルランタイムを保持し、Sites 必須の静的 Cloudflare Worker 出力を準備する。Sites 引き渡し前に `dist/client/index.html`、`dist/server/index.js`、`dist/.openai/hosting.json`、ソース `.openai/hosting.json` を確認し `npm run test:sites` を実行する。このプロジェクトを Vinext スタータに置き換えない。

## ランタイム契約

- ユーザータスクが明示的に求めない限りモバイルデバイスランタイムを保持する。単体ページに置き換えない。ビジュアルフィデリティはデバイス画面内のアプリ所有コンテンツに適用し、テンプレ所有のデバイス chrome には適用しない。
- `App` は `PhoneFrame` -> `KeyboardProvider` で構成し、`StatusBar`、アプリコンテンツ、`HomeIndicator`、`KeyboardDock` をフレーム内にマウントする。`StatusBar` と iOS ホームインジケータはオーバーレイ chrome。Android キーボード閉じ時はアプリビューポートがナビ領域を予約する。Android キーボード開き時は現行のフルスクリーンキーボードレイアウトを保持（アセット内 IME ナビストリップ、別黒ナビバーは非表示）。iOS 画面はホームインジケータ領域の背後に描画し、safe-area コンテンツパディングは画面側が持つ。
- `iPhone` / `Pixel 10` デバイスピッカーと両 calibrated プリセットを保持。Pixel 画面は `427 x 952`；`32 x 32` カメラ円と `public/assets/android/navigation-bar.svg` 下部ナビは保護 chrome でアプリコンテンツではない。
- デバイスピッカーは右上の軽量スタイル（トリガー枠なし透明、コンテンツサイズ、右寄せメニュー 3px inset と指定のヘアライン・影）を保持。プロトタイプルートとデフォルトアプリ画面は白。
- `StatusBar` はライブ chrome（プラットフォーム別タイポ、ステータスアイコンアセット、余白）。Pixel 10 は Roboto、Android インジケータ、上左右 32px。iPhone は iOS インジケータ、システムタイポ、調整済み余白。`9:41` など固定時刻をハードコードしない。実時計を置き換えない。ユーザーが固定／モック時刻を明示しない限りステータス内容をアプリマークアップに移さない。
- `PhoneFrame` は calibrated フレーム、スクリーンポータル、デバイスピッカー、カメラ切り抜き、カスタムカーソルを所有。デバイスアセットは `public/assets/iphone/` と `public/assets/android/`。読み込み失敗時はパス修復またはアセット復元し、フレーム・キーボード・画像描画を削除しない。
- 単一画面は `MobileScroll` を直接使う。ルートが固定ヘッダー／フッターを持つマルチ画面は `FlowStack`。各ルートは `FlowScreen`: `{ id, header?, headerHeight?, footer?, footerHeight?, render }`。`flow.push(screen)`、`flow.pop()`、`flow.replace(screen)` を `FlowStack` コールバックまたは `useFlow()` から使い、別ルータを導入しない。
- カルーセル、水平レール、スワイプカード、メディアストリップ、水平スクロールカード、チップレールなどは `Carousel`。
- 永続コンポーザー、独立シート、プッシュ／ピークサイドバー、アプリ全体トランジションなどレイヤードシェルは `Prototype.tsx` で直接合成。`FlowStack` に無理に押し込まない。固定 chrome は `MobileScroll` 外の兄弟レイヤー。
- `FlowScreen` では固定ヘッダー／フッターは `FlowScreen.header` / `footer` に置く。`headerHeight` は見えるアプリツールバー高さ；`FlowStack` がデバイス上部 safe-area／ステータス inset を自動加算。ヘッダーに `StatusBar` やその高さを含めない。`footerHeight` はアプリフッター全体高さ。`FlowScreen.footer` はオーバーレイでレイアウト予約ではない。使う画面は `padding-bottom: calc(var(--flow-footer-height) + var(--mobile-safe-area-height) + 24px)` など自前の下部パディングで最終コンテンツをフッター上にスクロール可能にしつつ背後に描画。
- `MobileScroll` 内はスクロールコンテンツのみ。固定ヘッダー、ナビ、タブ、コンポーザー、オーバーレイは外に。スクロール物理、safe area、キーボード inset、スクロールバー、ドラッグクリック抑制を維持し、固定 chrome 下にコンテンツを描画しない。
- `MobileScroll` 内のボタン・リンク・カード・画像はタップ slop を超えるドラッグでもスクロール可能。ドラッグジェスチャを自分で持つ稀なコントロールだけ `data-scroll-drag="ignore"`。
- 通常画面パディングに `var(--keyboard-height)` を足さない。スクロールビューポートは既にキーボード上に縮む。固定コンポーザー・検索バー・トースト chrome は `useKeyboardInsets().bottomInset`（Android 閉じは 0、開きはキーボード高さ；iOS は閉じでホームインジケータ、開きでキーボード直上）。`bottom: 0` や `keyboardHeight` だけに pin しない。
- すべてのテキスト入力は `KeyboardInput`、`KeyboardTextarea`、`MobileTextField`。生 `input`/`textarea` はフォーカス、キーボードアニメ、safe-area、付属面を切る。
- 電話スコープのシートは `BottomSheet`。props は `open`、`onOpenChange`、`title`、任意 `description`、任意 `snap`、`children`。電話スクリーンポータル経由で描画し、開く前にキーボードを閉じる。

## 水平カルーセル

- 水平ドラッグ可能カード、画像、メディア、チップなどは `Carousel`。`overflow-x`、カスタムポインタ、汎用 div で再実装しない。
- `Carousel` は `MobileScroll` 内にネスト可能。水平ジェスチャを所有し、垂直は親に渡す。
- `Carousel` 上や周りに `data-scroll-drag="ignore"` を付けない（親垂直スクロールを妨げる）。
- `Carousel` に CSS scroll snap を足さない。ランタイムが慣性とリリースモーションを所有する。
- 全方向で親スクロールを止める必要があるコントロールだけ `data-scroll-drag="ignore"`。

詳細は `src/mobile/COMPONENTS.md`。

## キーボードルール

シミュレートキーボードは別トップレイヤーコンポーネント。iOS ナビ／モーダル風 UI を出す前に先に閉じる。

次の前に `keyboard.hide()`:

- FlowStack の push/pop/replace
- ボトムシート、アクションシート、ダイアログ、メニュー、ナビシートを開く
- 先の画面がテキスト入力フォーカスを引き継ぐべきでないトランジション

`FlowStack` は push/pop/replace で既に閉じる。`BottomSheet` は開く前に閉じる。新しいモーダル／シート／ナビ primitives を足すときも同ルール。

コンポーザーなどキーボード付属面を閉じるときは open 状態を変える同じイベントで `keyboard.hide()`。付属面はタイマーや visibility フラグではなく `useKeyboardInsets()` で位置し、同時に閉じる。

テキスト入力がフォーカスを失ったらシミュレートキーボードを閉じる。カスタムでランタイムのキーボード対応フィールドを使わないときは blur で `keyboard.hide()`。フォーカスが別のテキスト入力に直接移り同じキーボードセッションを共有すべきときだけ開いたまま。

## インタラクションルール

- ポインタがドラッグになったあとボタンや入力を発火しない。`MobileScroll` のドラッグ抑制を保持。
- フレーム内のネイティブ画像／ファイルドラッグを許可しない。フレームレベルの `dragstart` 抑制と非ドラッグ画像スタイルを保持し、画像上から始まったドラッグでもスクロールする。
- テキスト入力はキーボード対応フィールドを使う。
- 固定 phone chrome はプッシュ画面と一緒にアニメしない。画面コンテンツはアニメ可。ステータスバー、カメラ切り抜き、プレビュー chrome は固定。
- キーボードはホームインジケータ／safe area より下の z-index、表示中は通常 UI より上。
- ホームインジケータはプロトタイプ内最上位 safe-area レイヤー。

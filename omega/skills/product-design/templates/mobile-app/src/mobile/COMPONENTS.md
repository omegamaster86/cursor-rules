# モバイルランタイムコンポーネント

## Carousel

`Carousel` は水平コレクション（カード、画像、メディア、スワイプ項目、チップ／フィルタレール）の標準コンポーネント。`MobileScroll` 内に直接置く。利用側はジェスチャラッパやポインタハンドラを足さない。

```tsx
<MobileScroll>
  <section>
    <Carousel
      ariaLabel="Event details"
      className="event-carousel"
      contentClassName="event-carousel-track"
    >
      {cards}
    </Carousel>
  </section>
</MobileScroll>
```

ランタイムは軸でネストジェスチャを解決する。水平は `Carousel`、垂直は親 `MobileScroll` に渡す。水平を取ったあとのわずかな垂直ドリフトは親の移動・ラバーバンド・慣性を起こさない。タップはクリック可能、完了したドラッグは項目クリックを抑制する。

カルーセルや通常レールに `data-scroll-drag="ignore"` は使わない。全方向で親スクロールを止める強い opt-out になる。ランタイムの JS 慣性の上に CSS scroll snap を重ねない。将来 snap を足すならコンポーネントオプションにし、リリースモーションは一系統に任せる。

## Keyboard-linked surfaces

テキスト入力はすべて `KeyboardInput`、`KeyboardTextarea`、`MobileTextField` を使う。コンポーザー、検索面、その他キーボード連動 UI は `useKeyboardInsets().bottomInset` で位置する。inset はアプリビューポート基準: Android はキーボード閉じたビューポートが既にナビ上で終わり、開いたときはキーボード高さを返す。iOS はオーバーレイホームインジケータ inset が必要で、開いたときはキーボード高さ。`keyboardHeight` だけに pin しない。面を閉じるときは open 状態を更新する同じイベントで `keyboard.hide()` を呼ぶ。

## BottomSheet

`BottomSheet` は開く前にキーボードを閉じ、デフォルトで出入り両方アニメする。`open` は `onOpenChange` で制御。利用側の exit アニメラッパは不要。

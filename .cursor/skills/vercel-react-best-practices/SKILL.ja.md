---
name: vercel-react-best-practices
description: Vercel エンジニアリングによる React/Next.js のパフォーマンス最適化ガイド。このスキルは、React/Next.js のコード作成・レビュー・リファクタ時に最適なパターンを適用するために使用します。React コンポーネント、Next.js ページ、データ取得、バンドル最適化、パフォーマンス改善のタスクで有効です。
license: MIT
metadata:
  author: vercel
  version: "1.0.0"
---

# Vercel React ベストプラクティス

Vercel が保守する React/Next.js アプリケーション向けの包括的なパフォーマンス最適化ガイドです。8カテゴリ・計45ルールで構成され、影響度の高い順に整理されています。自動リファクタリングやコード生成の指針として利用できます。

## 適用タイミング

以下の場面で参照してください:
- 新しい React コンポーネントや Next.js ページを作成する時
- データ取得（クライアント/サーバー）を実装する時
- パフォーマンス観点でコードレビューする時
- 既存の React/Next.js コードをリファクタする時
- バンドルサイズや読み込み速度を最適化する時

## 優先度別ルールカテゴリ

| 優先度 | カテゴリ | 影響度 | 接頭辞 |
|----------|----------|--------|--------|
| 1 | ウォーターフォール解消 | CRITICAL | `async-` |
| 2 | バンドルサイズ最適化 | CRITICAL | `bundle-` |
| 3 | サーバーサイド性能 | HIGH | `server-` |
| 4 | クライアント側データ取得 | MEDIUM-HIGH | `client-` |
| 5 | 再レンダー最適化 | MEDIUM | `rerender-` |
| 6 | レンダリング性能 | MEDIUM | `rendering-` |
| 7 | JavaScript 性能 | LOW-MEDIUM | `js-` |
| 8 | 高度なパターン | LOW | `advanced-` |

## クイックリファレンス

### 1. ウォーターフォール解消 (CRITICAL)

- `async-defer-await` - 実際に使う分岐に await を移す
- `async-parallel` - 独立した処理は Promise.all() を使う
- `async-dependencies` - 部分依存は better-all を使う
- `async-api-routes` - API ルートでは早く開始し遅く await
- `async-suspense-boundaries` - Suspense でストリーミング

### 2. バンドルサイズ最適化 (CRITICAL)

- `bundle-barrel-imports` - 直接インポートし、バレルを避ける
- `bundle-dynamic-imports` - 重いコンポーネントは next/dynamic
- `bundle-defer-third-party` - 解析/ログは hydration 後に読み込む
- `bundle-conditional` - 機能が有効化された時のみ読み込む
- `bundle-preload` - ホバー/フォーカス時にプリロード

### 3. サーバーサイド性能 (HIGH)

- `server-cache-react` - React.cache() でリクエスト内重複を除去
- `server-cache-lru` - リクエスト間は LRU キャッシュを使う
- `server-serialization` - クライアントに渡すデータを最小化
- `server-parallel-fetching` - コンポーネント構成で並列取得
- `server-after-nonblocking` - 非同期後処理は after() を使う

### 4. クライアント側データ取得 (MEDIUM-HIGH)

- `client-swr-dedup` - SWR でリクエスト重複を自動排除
- `client-event-listeners` - グローバルイベントリスナーを重複させない

### 5. 再レンダー最適化 (MEDIUM)

- `rerender-defer-reads` - コールバックだけで使う状態を購読しない
- `rerender-memo` - 重い処理はメモ化コンポーネントへ抽出
- `rerender-dependencies` - effect にはプリミティブ依存を使う
- `rerender-derived-state` - 生値ではなく派生ブール値を購読
- `rerender-functional-setstate` - 安定コールバックには関数型 setState
- `rerender-lazy-state-init` - 高コスト初期値は関数で渡す
- `rerender-transitions` - 非緊急更新は startTransition を使う

### 6. レンダリング性能 (MEDIUM)

- `rendering-animate-svg-wrapper` - SVG ではなく div ラッパーをアニメーション
- `rendering-content-visibility` - 長いリストに content-visibility
- `rendering-hoist-jsx` - 静的 JSX をコンポーネント外へ
- `rendering-svg-precision` - SVG 座標の精度を下げる
- `rendering-hydration-no-flicker` - クライアント専用データは inline script
- `rendering-activity` - show/hide に Activity コンポーネント
- `rendering-conditional-render` - 条件分岐は && ではなく三項演算子

### 7. JavaScript 性能 (LOW-MEDIUM)

- `js-batch-dom-css` - CSS 変更は class/cssText でまとめる
- `js-index-maps` - 繰り返し参照は Map を構築
- `js-cache-property-access` - ループ内のプロパティ参照をキャッシュ
- `js-cache-function-results` - 関数結果をモジュールレベルの Map にキャッシュ
- `js-cache-storage` - localStorage/sessionStorage をキャッシュ
- `js-combine-iterations` - filter/map の複数ループを1回にまとめる
- `js-length-check-first` - 高コスト比較前に length を確認
- `js-early-exit` - 関数は早期 return を使う
- `js-hoist-regexp` - 正規表現生成はループ外へ
- `js-min-max-loop` - sort ではなく loop で min/max
- `js-set-map-lookups` - Set/Map の O(1) 参照を使う
- `js-tosorted-immutable` - イミュータブルには toSorted()

### 8. 高度なパターン (LOW)

- `advanced-event-handler-refs` - イベントハンドラを ref に保持
- `advanced-use-latest` - 安定した callback 参照に useLatest

## 使い方

詳細説明とコード例は個別のルールファイルを参照してください:

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
rules/_sections.md
```

各ルールファイルには以下が含まれます:
- 重要性の簡潔な説明
- 誤ったコード例とその理由
- 正しいコード例とその理由
- 追加の背景情報と参考リンク

## 完全版ドキュメント

全ルールを展開した完全版: `AGENTS.md`

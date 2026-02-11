---
name: vercel-react-best-practices
description: Vercel Engineering による React / Next.js パフォーマンス最適化ガイドライン。React/Next.js コードの新規実装・レビュー・リファクタリング時に、最適なパフォーマンスパターンを適用するために使用する。React コンポーネント、Next.js ページ、データ取得、バンドル最適化、性能改善に関わるタスクで発火する。
license: MIT
metadata:
  author: vercel
  version: "1.0.0"
---

# Vercel React Best Practices

Vercel が保守する React / Next.js 向け包括パフォーマンスガイド。8カテゴリ・57ルールを収録し、影響度順で自動リファクタリングとコード生成を支援します。

## 適用タイミング

以下の場面で参照してください。
- 新しい React コンポーネントや Next.js ページを作成するとき
- クライアント/サーバーのデータ取得を実装するとき
- 性能問題の観点でコードレビューするとき
- 既存コードをリファクタリングするとき
- バンドルサイズや読み込み時間を最適化するとき

## 優先度別カテゴリ

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | ウォーターフォール排除 | CRITICAL | `async-` |
| 2 | バンドルサイズ最適化 | CRITICAL | `bundle-` |
| 3 | サーバーサイド性能 | HIGH | `server-` |
| 4 | クライアント側データ取得 | MEDIUM-HIGH | `client-` |
| 5 | 再レンダー最適化 | MEDIUM | `rerender-` |
| 6 | 描画性能 | MEDIUM | `rendering-` |
| 7 | JavaScript 性能 | LOW-MEDIUM | `js-` |
| 8 | 高度なパターン | LOW | `advanced-` |

## クイックリファレンス

### 1. ウォーターフォール排除 (CRITICAL)
- `async-defer-await` - 必要な分岐まで await を遅延
- `async-parallel` - 独立処理は Promise.all() で並列化
- `async-dependencies` - 部分依存は better-all で最適並列化
- `async-api-routes` - API ルートで Promise を先行開始し後で await
- `async-suspense-boundaries` - Suspense で段階表示（ストリーミング）

### 2. バンドルサイズ最適化 (CRITICAL)
- `bundle-barrel-imports` - バレル経由ではなく直接 import
- `bundle-dynamic-imports` - 重いコンポーネントは next/dynamic
- `bundle-defer-third-party` - 解析/ログ系は hydration 後に読み込み
- `bundle-conditional` - 機能有効時のみモジュール読み込み
- `bundle-preload` - hover/focus で事前ロード

### 3. サーバーサイド性能 (HIGH)
- `server-auth-actions` - Server Actions でも認可/認証を必須化
- `server-cache-react` - React.cache() で同一リクエスト内重複排除
- `server-cache-lru` - リクエスト間は LRU キャッシュ
- `server-dedup-props` - RSC props の重複シリアライズ回避
- `server-serialization` - Client Component へ渡すデータ最小化
- `server-parallel-fetching` - コンポーネント構成で fetch を並列化
- `server-after-nonblocking` - after() で非ブロッキング処理

### 4. クライアント側データ取得 (MEDIUM-HIGH)
- `client-swr-dedup` - SWR による自動重複排除
- `client-event-listeners` - グローバルイベントリスナー重複排除
- `client-passive-event-listeners` - スクロール系は passive リスナー
- `client-localstorage-schema` - localStorage のバージョン管理と最小化

### 5. 再レンダー最適化 (MEDIUM)
- `rerender-defer-reads` - コールバック専用 state の購読回避
- `rerender-memo` - 高コスト処理を memo 化コンポーネントへ分離
- `rerender-memo-with-default-value` - 非プリミティブ既定値を定数化
- `rerender-dependencies` - effect 依存はプリミティブ化
- `rerender-derived-state` - 生値でなく導出ブール値を購読
- `rerender-derived-state-no-effect` - 導出 state は render 中に計算
- `rerender-functional-setstate` - 安定コールバックに関数型 setState
- `rerender-lazy-state-init` - 高コスト初期値は関数で遅延初期化
- `rerender-simple-expression-in-memo` - 単純式に useMemo を使わない
- `rerender-move-effect-to-event` - 作用は event handler 側へ移動
- `rerender-transitions` - 非緊急更新は startTransition
- `rerender-use-ref-transient-values` - 一時値は useRef を利用

### 6. 描画性能 (MEDIUM)
- `rendering-animate-svg-wrapper` - SVG 本体ではなく wrapper をアニメーション
- `rendering-content-visibility` - 長いリストは content-visibility を活用
- `rendering-hoist-jsx` - 静的 JSX をコンポーネント外へ抽出
- `rendering-svg-precision` - SVG 座標精度を落として軽量化
- `rendering-hydration-no-flicker` - クライアント専用データを inline script で処理
- `rendering-hydration-suppress-warning` - 予期される不一致は警告抑制
- `rendering-activity` - show/hide は Activity コンポーネント利用
- `rendering-conditional-render` - 条件分岐は && ではなく三項演算子
- `rendering-usetransition-loading` - ローディング state は useTransition 優先

### 7. JavaScript 性能 (LOW-MEDIUM)
- `js-batch-dom-css` - CSS 変更は class/cssText でまとめる
- `js-index-maps` - 繰り返し検索は Map 化
- `js-cache-property-access` - ループ内プロパティ参照をキャッシュ
- `js-cache-function-results` - 関数結果をモジュールスコープ Map にキャッシュ
- `js-cache-storage` - localStorage/sessionStorage 読み取りをキャッシュ
- `js-combine-iterations` - 複数 filter/map を単一ループに統合
- `js-length-check-first` - 高コスト比較前に length チェック
- `js-early-exit` - 早期 return を活用
- `js-hoist-regexp` - RegExp 生成はループ外へ
- `js-min-max-loop` - min/max は sort でなくループで算出
- `js-set-map-lookups` - 検索は Set/Map で O(1) 化
- `js-tosorted-immutable` - 不変ソートは toSorted() を利用

### 8. 高度なパターン (LOW)
- `advanced-event-handler-refs` - イベントハンドラを ref に保持
- `advanced-init-once` - アプリ初期化をマウントごとに行わない
- `advanced-use-latest` - stable callback ref 用の useLatest 相当パターン

## 使い方

詳細は各ルールファイルを参照してください。

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
```

各ルールファイルには次を含みます。
- なぜ重要かの短い説明
- Incorrect コード例と解説
- Correct コード例と解説
- 補足コンテキストと参考情報

## 統合版

全ルール展開版: `AGENTS.md`

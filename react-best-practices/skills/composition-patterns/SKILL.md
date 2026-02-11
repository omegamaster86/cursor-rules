---
name: vercel-composition-patterns
description:
  スケールする React コンポジションパターン。boolean props の増殖がある
  コンポーネントのリファクタリング、柔軟なコンポーネントライブラリの構築、
  再利用可能な API 設計で利用する。複合コンポーネント、render props、
  context provider、コンポーネント設計に関するタスクで発火する。
  React 19 の API 変更も含む。
license: MIT
metadata:
  author: vercel
  version: '1.0.0'
---

# React コンポジションパターン

柔軟で保守しやすい React コンポーネントを構築するためのコンポジションパターンです。
複合コンポーネントの活用、state のリフトアップ、内部要素の合成によって boolean props の増殖を避けます。
このパターン群は、コードベースの規模が拡大しても人間と AI エージェントの双方が扱いやすい設計を維持します。

## 適用するタイミング

次の場面で本ガイドラインを参照してください。

- boolean props が多いコンポーネントをリファクタリングするとき
- 再利用可能なコンポーネントライブラリを作るとき
- 柔軟なコンポーネント API を設計するとき
- コンポーネント設計をレビューするとき
- 複合コンポーネントや context provider を扱うとき

## 優先度ごとのルールカテゴリ

| Priority | Category         | Impact | Prefix          |
| -------- | ---------------- | ------ | --------------- |
| 1        | コンポーネント設計 | HIGH   | `architecture-` |
| 2        | 状態管理         | MEDIUM | `state-`        |
| 3        | 実装パターン     | MEDIUM | `patterns-`     |
| 4        | React 19 API     | MEDIUM | `react19-`      |

## クイックリファレンス

### 1. コンポーネント設計 (HIGH)

- `architecture-avoid-boolean-props` - 挙動の切り替えに boolean props を増やさず、コンポジションで表現する
- `architecture-compound-components` - 共有 context を持つ複合コンポーネントで複雑性を分解する

### 2. 状態管理 (MEDIUM)

- `state-decouple-implementation` - state の管理方法を知るのは Provider のみ
- `state-context-interface` - 依存性注入できるよう `state/actions/meta` の汎用インターフェースを定義する
- `state-lift-state` - 兄弟コンポーネントから利用できるよう state を Provider に移す

### 3. 実装パターン (MEDIUM)

- `patterns-explicit-variants` - boolean モードではなく明示的なバリアントコンポーネントを作る
- `patterns-children-over-render-props` - `renderX` props より `children` 合成を優先する

### 4. React 19 API (MEDIUM)

> **⚠️ React 19+ 専用。** React 18 以下ではこのセクションをスキップしてください。

- `react19-no-forwardref` - `forwardRef` を使わず、`useContext()` の代わりに `use()` を使う

## 使い方

詳細な説明とコード例は各ルールファイルを参照してください。

```
rules/architecture-avoid-boolean-props.md
rules/state-context-interface.md
```

各ルールファイルには以下を含みます。

- なぜ重要かの簡潔な説明
- 不適切なコード例と解説
- 推奨コード例と解説
- 追加の文脈と参照

## 統合版ドキュメント

すべてのルールを展開した完全版ガイド: `AGENTS.md`

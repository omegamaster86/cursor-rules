# React コンポジションパターン

スケール可能な React コンポジションパターンを整理したリポジトリです。
これらのパターンは、複合コンポーネントの活用、state のリフトアップ、内部要素の合成によって boolean props の増殖を防ぎます。

## 構成

- `rules/` - ルールごとの個別ファイル
  - `_sections.md` - セクション情報（タイトル、影響度、説明）
  - `_template.md` - 新しいルール作成用テンプレート
  - `area-description.md` - 個別ルールファイル
- `metadata.json` - ドキュメントのメタデータ（バージョン、組織、要約）
- **`AGENTS.md`** - 統合版出力（生成物）

## ルール

### コンポーネント設計（CRITICAL）

- `architecture-avoid-boolean-props.md` - 挙動の切り替えに boolean props を増やさない
- `architecture-compound-components.md` - 共有コンテキストを使う複合コンポーネント構造にする

### 状態管理（HIGH）

- `state-lift-state.md` - state を Provider コンポーネントへリフトアップする
- `state-context-interface.md` - 明確な context インターフェース（state/actions/meta）を定義する
- `state-decouple-implementation.md` - 状態管理実装を UI から分離する

### 実装パターン（MEDIUM）

- `patterns-children-over-render-props.md` - `renderX` props より `children` を優先する
- `patterns-explicit-variants.md` - 明示的なコンポーネントバリアントを作る

## コア原則

1. **設定よりコンポジション** - props を増やす代わりに、利用側に合成させる
2. **state はリフトアップ** - state をコンポーネント内に閉じ込めず Provider に置く
3. **内部も合成する** - サブコンポーネントは props ではなく context にアクセスする
4. **バリアントは明示する** - `isThread` 付き `Composer` ではなく `ThreadComposer` / `EditComposer` を作る

## 新しいルールの追加

1. `rules/_template.md` を `rules/area-description.md` にコピーする
2. 適切な領域プレフィックスを選ぶ
   - コンポーネント設計は `architecture-`
   - 状態管理は `state-`
   - 実装パターンは `patterns-`
3. frontmatter と本文を記入する
4. 説明付きの明確なコード例を用意する

## 影響度レベル

- `CRITICAL` - 土台となるパターン。保守不能コードを防ぐ
- `HIGH` - 保守性を大きく改善する
- `MEDIUM` - コードをよりクリーンにする実践

---
name: user-context
description: "Product Design の保存ユーザーコンテキストの読み込み・管理。セットアップ、開始、オンボーディング、プロダクト／デザインソースの保存、記憶内容の確認、コンテキスト更新、好みの記憶に使用。例: プロダクト URL、Figma、スクリーンショット、参照画像、コードベースパス、Storybook、トークン、デザインシステム、ブランドアセット、一般的なプロダクト／デザインメモ。"
---

# User Context

User Context はデザイナーがよく使うプロダクトとデザイン参照を保存し、将来の Product Design が正しいソースから始められるようにする。

次を求められたときに使う:

- Product Design のセットアップ
- Product Design の開始
- Product Design のオンボーディング
- プロダクト／デザインソースの保存
- Product Design が何を記憶しているか確認
- 保存コンテキストの更新
- Product Design の好みを記憶
- setup my plugin

## Critical Overrides

- 進行前にプラグインルーター [$index](../index/SKILL.md) を参照する。
- [$critical-overrides](../../references/critical-overrides.md) に従う。
- オンボーディングや将来会話向け保存を提案する前に、ローカルシェルが使え、Cursor 状態ディレクトリが存在し書き込み可能（または作成可能）ことを確認する。デフォルト: `~/.cursor/product-design/`、またはプロジェクト保存時 `./.cursor/product-design/`。`PRODUCT_DESIGN_STATE_DIR` で上書き可。`user-context.md` が既にあるときは書き込み可能か確認する。
- チェックが完了できない／失敗したら永続コンテキストは利用不可。保存オンボーディングを提案しない。将来会話向けに保存したと言わない。保存を求められたら、今の会話では使えるが将来には保存できないと説明する。

## Saved User Context

`user-context.md` があればデフォルトで使う。

保存済み参照で Product Design を接地する。ユーザーが別のことを求めない限り、ideation・プロトタイプ・監査・クローン・critique は保存コンテキストに合わせる。

ビジュアル接地が必要なときは、保存スクリーンショット・参照画像・トークン・デザイン言語・コンポーネント参照を ImageGen、ideation、プロトタイプ、監査、critique に含める。

## State File

保存コンテキストの場所:

```text
~/.cursor/product-design/user-context.md
```

プロジェクトスコープ（任意）:

```text
.cursor/product-design/user-context.md
```

スクリーンショットと参照画像は `user-context.md` の横:

```text
.../product-design/assets/
```

ファイルが無く、ユーザーがセットアップ・保存を求めない、タスクがプロダクト／デザインコンテキスト不足でブロックされていない限り、通常どおり続行する。

## Preflight

保存コンテキストが必要な Product Design ワークフローでは実行:

```bash
python3 scripts/user_context_preflight.py
```

返された保存エントリをタスクの起点コンテキストとして使う。

スクリプトが保存なしと報告したら、セットアップが必須でない限り現在のプロンプトから続行する。

preflight で保存参照をすべて開かない。現在のタスクに必要なものだけ inspect する。

## Setup

ユーザーがセットアップ、記憶内容、プロダクトについて知っていること、参照保存を求めたときは [references/onboarding.md](references/onboarding.md) を使う。

セットアップのみの依頼では、記憶できることを説明し有用なソースを求める。

初回セットアップと既存コンテキスト更新では聞き方を変える。

セットアップ中はワークスペース inspect、依存インストール、プロトタイプ足場、画像生成、監査、実装をしない。

保存する参照を受け取ったあと:

```bash
python3 scripts/init_user_context.py
```

作成した `user-context.md` に参照を追加する。

## Save

保存する有用で durable な Product Design コンテキスト:

- プロダクト URL
- Figma ファイル
- スクリーンショットと参照画像
- コードベースパス
- Storybook とコンポーネントドキュメント
- デザイントークンとテーマソース
- ブランド、ロゴ、アイコン、イラスト、画像、アセットソース
- 好みのブラウザ、キャプチャツール、共有先
- 将来の精度を上げるチーム規約

保存するスクリーンショット・参照画像は `user-context.md` 横の `assets/` にコピーし、エントリからリンクする。

画像には将来開かなくても分かる説明的ファイル名を付ける。

良い例:

```text
assets/chatgpt-settings-modal-dark-mode.png
assets/payment-sheet-mobile-error-state.png
assets/product-dashboard-sidebar-navigation.png
assets/storybook-primary-button-states.png
assets/brand-logo-lockup-purple-gradient.png
assets/onboarding-flow-welcome-step.png
assets/checkout-confirmation-screen.png
assets/account-menu-open-state.png
```

秘密、認証情報、API キー、私有トークン、コピーした顧客データ、永続すべきでないものは保存しない。

構造:

```md
# {Category}

- Description: {what this category is and when future Product Design runs should use it}

## Saved Links And Context

{Saved reference or fact}
- Date Added: YYYY-MM-DD.
- File: assets/{clear-descriptive-name}.png
- Useful Context: {what this reference represents}
- Future Use: {how future Product Design work should use it}
```

ローカル画像があるときだけ `File:` を含める。

カテゴリに保存がまだ無いときは厳密に:

```md
status: not provided
```

保存コンテキストは curated に。可能な URL やファイルのダンプより少数の高価値参照を優先する。

## Read

- `status: not provided` を事実として扱わない。
- ローカルシェルが使えるときは `scripts/user_context_preflight.py` を読む。
- 保存コンテキストをデフォルト接地として使い、現在のタスクに必要なものだけ inspect する。

---
name: image-to-code
description: "選択した画像、スクリーンショット、モック、Image Gen 参照を忠実でレスポンシブなフロントエンドとして実装する。"
---

# Image to Code

ビジュアルターゲット画像を高品質でインタラクティブな Web サイト／アプリに翻訳する。

## Critical Overrides

- 進行前にプラグインルーター [$index](../index/SKILL.md) を参照する。
- [$critical-overrides](../../references/critical-overrides.md) に従う。
- 生成ラスタの保存先: [$generated-image-assets](../../references/generated-image-assets.md)（作業ワークスペースルートの `.cursor/assets/`）。

## User Context

開始前に [$user-context](../user-context/SKILL.md) を読み、ローカルシェルが使えるときは preflight を実行する。

保存参照を接地材料として使う（必要なものだけ inspect）。

### [重要] Cursor でのプロトタイププレビュー

[cursor-preview](../../references/cursor-preview.md) に従う。dev サーバー開始は検証ではない。cursor-ide-browser でローカル URL を開き、レンダリングを inspect、主要インタラクション、コンソールエラー、design QA 合格が必要。

HTTP ヘルス、ビルド成功、デプロイ成功をブラウザ検証の代用にしない。browser MCP 使えないときは検証 blocked と報告。

## Workflow

**重要: これはガイダンスではなく完了すべきチェックリスト。**

1. 再現する選択画像、スクリーンショット、モック、Image Gen 結果が無いときは開始しない。文章ブリーフだけでは不十分。

2. ビルド前に選択ビジュアルを一意に解決。

    - 番号付き `$ideate` 選択なら、直近 ideation の **表示順** N 番目の generated-image 結果。概念計画順や Image Gen 送信順は使わない。
    - `$ideate` の概念名リストは、明示的に表示画像順で書かれたときだけ使う。
    - generated-image ID、選択添付、スクリーンショット、モック、Figma フレームは裸の序数より強い。利用可能ならその参照を優先。
    - 選択を一意に解決できないときは実装前に停止し、概念名または画像の再添付／選択を求める。近いオプションを推測してビルドしない。

    モバイルランタイム例外: 1:1 フィデリティはデバイス画面内のアプリ所有コンテンツのみ。`PhoneFrame`、`StatusBar`、`HomeIndicator`、`KeyboardDock`、デバイスアセットはテンプレインフラ。参照に無くても、別 chrome を描いても保持する。デバイス chrome を画像アセットとして再現しない。

3. 解決した画像を再現するデザインとして扱う。

4. モバイルビューポートならモバイルアプリをビルド。新規ローカルアプリは [local-prototype-preflight](../../references/local-prototype-preflight.md) で `--template mobile-app`。不明ならデスクトップ。

   `mobile-app` テンプレでは計画・実装前に `AGENTS.md` を読みランタイムとコンポーネント指針に従う。

5. 参照デザインをレビューし、デザイン内の画像アセットをすべて catalog し、Image Gen で個別生成。拡大して必要アセットを漏らさない。

    例: ヒーロー（フルブリード背景含む）、記事画像、サムネ、装飾イラスト、テクスチャ、ロゴ、プロダクト画像、アバター。

    ルール:

    - **必須:** div アート、CSS アート、インライン SVG、手作り SVG、HTML 図形、絵文字、文字グリフでアイコン・画像を代替しない。Image Gen と最適アイコンライブラリを使う。
    - テキストが画像の一部なら画像に残す（ヒーロー、看板、パッケージ、記事アートなど）。ソースが画像上の編集可能 UI テキストと明確に示す場合を除き、透明テキストボックスや HTML/CSS オーバーレイで再現しない。
    - 参照がカスタムビジュアルを示すところに汎用プレースホルダーを使わない。
    - 生成アセットは参照モックのアートディレクション、パレット、レンダリング、デザイン言語に合わせる。
    - Image Gen は透過非対応；透過必要なら後処理。
    - モバイルプロトタイプではベゼル、ノッチ、ステータスバー、時計、電波／バッテリー、ホームインジケータを catalog／生成しない。モバイルランタイムが所有。

### 並列アセット制作

参照アセットを catalog・計測したあと、メインがアプリ構造を組みながら最大3アセットサブエージェントを起動。

各サブエージェントにラスタ1タスク（参照クロップ、寸法、焦点、スタイル、**出力パス = ワークスペースルート `.cursor/assets/<slug>.png`**、消費コンポーネント）。サブエージェントは生成・inspect・`.cursor/assets/` へ保存・パス報告のみ。ソース編集、ブラウザ、デプロイはしない。

ファーストビュー重要アセットを優先し、サポートは再利用。標準 UI アイコンや提供ブランドロゴは委譲しない。

6. ページ全セクションを定義。各セクションでレイアウト、要素間余白、要素サイズを meticulous に計測。

7. ターゲットに合う自由利用フォントを探す。

8. ターゲットに合う自由利用アイコンライブラリを探す。Lucide デフォルトにしない。最適一致を探す。

    - **必須:** インライン SVG、手作り SVG、HTML/div 図形、CSS 図形、グラデーション、絵文字、文字グリフで代替しない。

9. [local-prototype-preflight](../../references/local-prototype-preflight.md) からアプリをビルド。ユーザーが静的モック、本番同等、別スコープを求めない限り、次を生きた状態に:

    - 動作ナビ、リンク、タブ、メニュー、主要 CTA。
    - メイン体験の入力、フィルタ、トグル、選択、フォーム。
    - hover、focus、selected、open/closed、loading、empty、success など見える状態。
    - プロダクトにあればメインタスク・コンバージョン・ジャーニーを端から端まで。

    コア外コントロールはビジュアルのみ可。認証、永続化、バックエンド/API、統合、網羅的エッジは依頼時まで。

    - 生成した画像をすべて配置してから進む。プレースホルダー（CSS/SVG 含む）を残さない。
    - コア体験のコントロールを静的 chrome にしない。依頼なしに新ページ・ルートを作らない。

10. ローカルアプリを実行。

11. [$index](../index/SKILL.md#browser-choice) でローカルをキャプチャ。

12. ブロッキングゲートとして [design-qa](../design-qa/SKILL.md)。

    - 参照画像と最新プロトタイプスクリーンショットを QA レポート前に開く。
    - 同じビューポート・同じインタラクション状態で比較。合わなければ先にキャプチャ。
    - `design-qa.md` をプロジェクトルートに保存。
    - P0/P1/P2 修正、`final result: passed` まで反復。
    - P3 でループし続けない。
    - ブロック時は `final result: blocked`。
    - `passed` でない限り引き渡ししない。

13. アプリ／サイトを引き渡し。

    - design-qa 合格後のみ。
    - ローカルで動かし続け、dev サーバーとローカル URL。
    - 明示デプロイ依頼までデプロイしない。
    - プレビュー後は `critical-overrides.md` の共有引き渡し。
    - [critical-overrides](../../references/critical-overrides.md#build-handoff) の nudge を含める。

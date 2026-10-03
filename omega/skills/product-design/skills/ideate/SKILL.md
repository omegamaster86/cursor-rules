---
name: ideate
description: "Product Design ブリーフから画像ベースの代替案、リミックス、新しいデザイン方向を生成する。デザイン案、ビジュアル探索、リミックス、コンテキストからの画像生成アプローチの依頼に使用。"
---

# Ideate

ユーザーのアイデア向けにデザインコンセプトを生成する。

[$index](../index/SKILL.md) の共有 Product Design ルーティング指針に従う。

## Critical Overrides

- 進行前にプラグインルーター [$index](../index/SKILL.md) を参照する。
- [$critical-overrides](../../references/critical-overrides.md) に従う。
- 生成ラスタの保存先: [$generated-image-assets](../../references/generated-image-assets.md)（作業ワークスペースルートの `.cursor/assets/`）。

## User Context

開始前に [$user-context](../user-context/SKILL.md) を読み、ローカルシェルが使えるときは preflight を実行する。

提供 URL、Figma、スクリーンショット、参照画像、コードベース、Storybook、トークン、デザインシステム、ブランドアセット、コンポーネント参照、ブラウザ設定、共有先を Image Gen 生成に添付しブリーフに合わせる。

保存参照をすべて inspect しない。必要なものだけ。

## Workflow

`$get-context` が最小デザインブリーフを満たすまで画像を生成しない。

画像生成前に:

1. ブリーフを理解。

- ターゲット: コンポーネント、画面、機能／ワークフロー、広いプロダクトアイデア。
- intended user、プロダクト表面、ゴール。
- ユーザーの硬い制約を保持。
- 最小ブリーフ未満なら `get-context` を実行。

2. コンテキストを解決。

- 提供ファイル、スクショ、リンク、見える参照を使う。
- ローカルワークスペースでは近くのデザインドキュメントとビジュアルコンテキストを探す。
- `user-context`、`storybook/`、`.storybook/`、`design-system/`、`tokens/`、`components/`、`app/`、生成プロトタイプルートなど。
- 既存プロジェクトでは類似画面、Storybook キャプチャ、トークン、コンポーネント参照を先に。アプリにアクセスできないときは類似画面の提供を求める。Image Gen プロンプトにデザイン言語とトークンを足す。

3. 参照を直接 inspect。

- 生成前にスクショ、画像、Figma フレーム、アプリ表面を見る。ファイル名だけから推測しない。
- ローカルパスや参照が見えないときは停止し、パス確認、ファイルアップロード、アプリ起動、ワークスペース指定を求める。

4. バリエーションモードを決める。

- 有用なローカルデザインコンテキストがありユーザーが新スタイルを求めていないときは既存方向内。
- コンテキストが無い、または広い探索を求められたときはコンセプトとビジュアルシステムの両方を変える。
- 特定コンポーネント／既存表面では、ブランドスタイルより先に構造、インタラクション、ヒエラルキー、強調を変える。
- 広いプロダクトアイデアでは意味のある3方向を探索。

5. Image Gen 前にターゲット寸法を選ぶ。

- 依頼と参照に最も合う寸法。
- モバイルアプリ: `390 x 844`。
- タブレット: `834 x 1194`。
- デスクトップアプリ、ダッシュボード、管理、SaaS: `1440 x 1024`。
- LP・マーケ: 幅 `1440` でスクロール可。
- モーダル、パネル、ウィジェット、コンポーネント: 自然なコンテナサイズ。
- 提供スクショ、Figma、モック、参照画像: そのビジュアルから続けるときは寸法とアスペクトを合わせる。
- 詰め込みを避け、現実的な余白、読めるタイポ、クリップなしで寸法に収める。
- 各 Image Gen プロンプトに選んだ寸法を含める。

6. アクセスギャップを確認。

- 認証、権限、期限切れログイン、スコープ不足、空結果、ローカル状態不可でコネクタ・参照・ファイルにアクセスできないときは停止。
- ギャップを明確に名指し、トラブルシュートかそのソースなし続行か聞く。
- 名指し参照を黙って無視している間は生成しない。

7. ユーザー提供画像・モックを Image Gen 呼び出しにデザインブリーフと一緒に添付。

8. 情報ヒエラルキー、レイアウト戦略、インタラクションモデル、プロダクトフレーミングが独立して異なる3オプションを生成。

守るルール:

- 下の Image Gen プロンプトを使う。
- 組み込み Image Gen ツールを使う。
- 各 Image Gen 完了後、返却ファイルをワークスペースルートの `.cursor/assets/` にコピーまたは移動する（`ideate-option-<表示順>-<slug>.png` など）。`.cursor/assets/` が無ければ作成。チャット表示だけに残さない。
- ユーザーが数を上書きしない限り独立画像を厳密に3枚。
- 各 Image Gen 呼び出しを独立起動。`Promise.all` でバッチ、順序配列、リクエスト順再生をしない。
- 各方向は別の Image Gen 結果。1画像に複数アイデアを入れない。
- 生成前に各方向に説明的な名前を付けるが、`option 1` などやプロンプト内の計画番号ラベルは使わない。並列結果は要求順と異なる順で返ることがある。
- 番号はスレッドに generated-image 結果が揃った **後だけ**。正しい順序はスレッド表示順のみ。計画概念順、要求チェーン、送信順、`Promise.all` 結果順、バッチ順、インデックス、リトライ順、想定完了順は無視。
- 全結果後、表示順にオプション番号をバインド。最終選択メッセージでオプションを名前付け・説明しない。
- 利用可能ならスクショ、ファイル、アプリキャプチャ、Figma、ビジュアルソースをムードボードとして添付。
- 既存プロダクトスクショ、類似フロー、Storybook、トークン、コンポーネント参照を接地材料として添付。
- モックデータに日付や時間敏感情報があるときは現在日付を解決し各 Image Gen プロンプトに含める。表示日付はその基準から。ユーザーまたはソースデザインが要求する日付は保持。
- スクショ・画像・ビジュアルファイルがあれば Image Gen に実画像を添付。テキスト説明だけに頼らない。
- 画像を実際に添付したときだけ参照添付を主張。添付できないときは明言し、テキストのみ続行するか聞く。
- ブリーフの硬い制約を各画像で保持。
- オプション生成後、ビルド前にユーザー選択を待つ。
- 後でユーザーがオプション `N` を選んだときは、直近 ideation の **表示順** N 番目の generated-image を解決。計画順からビルドしない。解決できないときは推測せず概念名または画像の再選択を求める。
- 選択オプションは `$image-to-code` のビジュアルターゲット。

## Feedback Loop

オプション後にフィードバックがあれば、そのフィードバックで修正オプションを生成。

オプション選択とフィードバックが同時なら、ビルド前に修正オプションを1枚生成。

複数オプションの良い部分を組み合わせたいときは新 Image Gen デザインにまとめ、ビルド前に見せる。

## Image Gen Prompt

現在のデザインブリーフに合わせてこのプロンプトを調整し、利用可能な画像参照を添付して Image Gen に送る:

```text
Create realistic, production-quality UI designs with clear hierarchy, strong typography, intentional imagery, and purposeful spacing.

Design a focused primary screen, not a feature inventory. The product may support many workflows, but this frame should show the hero use case, one clear primary action, and only one or two supporting actions or content areas. Do not add cards, panels, tabs, badges, metrics, filters, or navigation items merely to advertise every feature. Let the rest of the product exist off-screen. Prefer strong hierarchy and generous whitespace; if the screen feels crammed, remove UI.

### Target Dimensions

Pick the dimensions that best match the user's request and any provided visual reference.

Default to a desktop web-app frame unless the user or reference clearly calls for mobile, tablet, or another format.

 - Mobile app: `390 x 844`
 - Tablet app: `834 x 1194`
 - Desktop app, dashboard, admin, or SaaS: `1440 x 1024`
 - Landing or marketing page: `1440` wide and scrollable
 - Modal, panel, widget, or component: natural container size
 - Provided screenshot, Figma frame, mockup, or reference image: match its dimensions and aspect ratio when the user wants to continue from that visual

Use a natural viewport ratio for the intended surface. Never stretch, squash, or warp the generated screen, imagery, typography, or UI elements to fill the canvas. If the composition does not fit naturally, recompose or simplify the layout instead.

Avoid crowding. Make the design fit the chosen dimensions cleanly, with realistic spacing, readable type, and no clipped content.

### Layout

When deciding how to lay elements out on the page, this should be your priority order for tools to differentiate sections:

1. Use spacing, grouping, alignment, typography, and hierarchy on the same product surface.
2. Use simple dividers or row separators.
3. Use a subtle surface tint only when the base surface is not enough.
4. Use borders only when separation still is not clear.
5. Use shadows/elevation last, and sparingly.

Don'ts:
 - Do not default to a centered "app card" (the whole UI is in a card on the page) on top of a contrasting page background. Use the base page surface first unless the source product or user explicitly asks for a contained app panel.
 - Do not put cards inside cards. Do not make every major section a card. Do not make each list item its own card unless each item is truly a standalone object. A normal list should usually read as one grouped surface with lightweight row separation.
 - Do not make up extraneous features. Add only the things essential to accomplish what the prototype's goal is. Don't make up more features just to fill out a UI.

### Typography

 - Anchor UI typography to readable product sizes. Body text should usually sit between 14px and 16px, with the rest of the type scale built around that baseline.
 - Keep long-form text to a comfortable line length, generally no more than 65 characters per line.
 - Use no more than 2 fonts in a UI. You can use any font available in the project, or fonts provided free on Google Fonts. Pick the font that is best for the goal of the product and that matches with its intended look and feel.

### Presentation

 - For mobile app concepts, output app content only. Do not include a device bezel, phone body, notch, Dynamic Island, OS status bar, clock, signal or battery indicators, home indicator, browser chrome, rounded device mask, or device shadow.
 - Do not put multiple ideas into a single image generation.
 - Vary each idea as much as possible while adhering to the constraints given entirely.

### Data Freshness

When the design includes dates or time-sensitive mock data, use the supplied current date as the anchor. Weekly views must show the real containing week with correct weekday/date pairs. Feeds, charts, notifications, and recent activity must use plausible chronological dates relative to today. Mark today when useful. Preserve dates required by the brief or source design.
```

## Output

ユーザーに選ばせる最終メッセージを送る前に、すべての Image Gen 呼び出しの返却を待つ。

要求枚数の生成画像がメインチャットにそれぞれ1回だけ見えるまで選択メッセージを送らない。

見える Image Gen 出力が要求より少ないときは不足分を再試行。選択メッセージは送らない。

会話コンテキストの **表示順** で Image Gen 出力に番号:

- 1番目 = オプション 1
- 2番目 = オプション 2
- 3番目 = オプション 3

計画概念順、要求チェーン、送信順、`Promise.all` 結果順、バッチ順、インデックス、リトライ順、ツール送信順は無視。

オプションを名前付け・説明しない。デフォルト3枚では次だけ送る:

`Which option should I build: 1, 2, or 3? Or tell me what you'd like to refine or personalize first.`

ユーザーが別枚数を求めたときだけ数字を調整。

ユーザーが番号を選んだら `$image-to-code` にルーティングする前に選択を短く認知（例: `Building option 2!`）。マッピングが明確なとき確認を求めない。

完了とは、要求枚数の独立画像が生成され、ユーザーに選択を求めた状態。

---
name: design-qa
description: "内部プロトタイプ QA ヘルパー。Product Design のプロトタイプ、URL-to-code、image-to-code ビルドがソースビジュアルと実装の両方を持ち、引き渡し前に比較できるときだけ使用。広い UX critique、デザイン critique、プロダクト監査、フローレビューは audit にルーティング。"
---

# Design QA

引き渡し前に、プロトタイプのソースデザインとレンダリング実装を比較する内部ヘルパー。

広い UX critique、デザイン critique、プロダクト監査、フローレビューには使わない。ユーザー向けは [audit](../audit/SKILL.md)。

すべての Product Design ビルド引き渡しの前に使う。

合格 QA には両方必要:

- ソースビジュアル: Figma ノード、画像、スクリーンショット、モック、ソースキャプチャ
- レンダリング実装: ローカル URL、デプロイ URL、アプリ画面、コンポーネント、スクリーンショット

どちらも開けない・キャプチャできない・比較できないときは `design-qa.md` に `final result: blocked` とブロッカーを書く。ビルドスキルは完了引き渡しをしない。

## Critical Overrides

[critical-overrides](../../references/critical-overrides.md) に従う。

## Workflow

意図デザインと実装をプロダクト品質レビュアーとして比較する。出力は両アーティファクトの根拠に基づく優先度付き修正リスト。

メモリ、コード、ファイルパスだけから QA を書かない。先にソースと実装を開くかキャプチャし、見えているものを比較する。

別画像ビューを並列比較と見せかけない。ソース画像と実装スクリーンショットを同じ比較入力に入れ、そこから差分を判断する。

Design QA は反復ループ。初回比較が pass するのは、 actionable な P0/P1/P2 差分が無く、それに対する視覚修正も無いときだけ。

P0/P1/P2 がある比較では:

- finding を記録し blocked のまま。
- 修正を適用。
- 同じビューポート・状態で再キャプチャ。
- 修正後キャプチャをソースと再比較。

後続パスは以前の finding、修正、修正後の視覚根拠を特定する。ビルド、依存、lint、デプロイ、プレビュー障害対応は design-QA 反復に数えない。

1. 比較ターゲットを特定。
   - ソース: Figma ノード、画像、ボード、スクリーンショット、仕様、モック。
   - 実装: ローカル URL、デプロイ URL、画面、コンポーネント、スクリーンショット、コードレンダリング。
   - 判断前に同じビューポート、状態、テーマ、密度、ルート、コンテンツ、認証、インタラクション状態を合わせる。
   - 同じ状態を表していないときは先に明記し、誤った精度を避ける。

2. 根拠をキャプチャ。
   - Figma は利用可能なら design context とスクリーンショットツール。
   - Product Design `mobile-app` テンプレ実装はブラウザページ全体ではなくアプリビューポートをキャプチャ。コンテンツのみ比較は `data-testid="device-screen"` / `[data-phone-screen]`；ベゼル含むソースは `data-testid="phone-frame"`。
   - `mobile-app` キャプチャ前に `npm run check:runtime`。失敗はブロック。チェック回避や、ラスタ化／複製ステータスバー・ベゼル・ホームインジケータをアプリコンテンツとして受け入れない。
   - Web/アプリは [cursor-preview](../../references/cursor-preview.md) と [index](../index/SKILL.md#browser-choice)。意図ビューポートでスクリーンショット。
   - 関連状態も: mobile/desktop、hover/focus/active、empty/loading/error、dark/light、主要ブレークポイント。
   - finding 引用用にスクリーンショットパスや URL を保存。
   - キャプチャだけでは不十分。判断前にソースと実装を同じ比較入力に入れる。

3. 比較前に正規化。
   - クロップ、ビューポート、スケール、デバイスフレームを揃える。フレーム付きモックとフレームなしページを不一致を明記せず比較しない。
   - ブラウザ chrome や周囲キャンバスよりコンテンツ領域を優先。
   - `mobile-app` では 1:1 phone-screen キャプチャを強制または検証。小ビューポートではデバイスが縮小される；Playwright は scale `1` 用に十分大きくし、`[data-phone-screen]` が `393 x 852` CSS px であることを確認。小さいスクリーンショットはスケール済みで 1:1 比較に無効。
   - 要素スクリーンショットまたは明示クリップでキャプチャ。例:

   ```ts
   const page = await browser.newPage({
     viewport: { width: 1400, height: 1200 },
     deviceScaleFactor: 1,
   });
   await page.goto("http://127.0.0.1:8796");
   const screen = page.getByTestId("device-screen");
   await screen.waitFor({ state: "visible" });

   const box = await screen.boundingBox();
   if (!box || Math.abs(box.width - 393) > 1 || Math.abs(box.height - 852) > 1) {
     throw new Error(`Expected unscaled mobile screen at 393 x 852, got ${box?.width} x ${box?.height}`);
   }

   await screen.screenshot({ path: "implementation-mobile-screen.png" });
   ```

   - 密度を正規化。`@2x` などは同サイズに揃えて比較。`design-qa.md` にソースピクセル、実装ピクセル、CSS ビューポート、`deviceScaleFactor` を記録。
   - 密度不一致、ブラウザ chrome、キャンバスパディング、フレーム不一致だけの視覚 finding は出さない。正規化後にタイポ、余白、色、画像、状態を判断。

4. 適切な粒度で比較。
   - 全体ビュー: 構成、ヒエラルキー、レイアウト、密度、レスポンシブ構造。
   - 焦点領域: 全体では小さすぎる重要詳細。
   - タイポ、整列、画像、アイコン、ロゴ、コントロール、フォーム、ナビ、テーブル、密な UI、見えるインタラクション状態で必要なら焦点比較。
   - 不要なら `design-qa.md` で理由を述べる。
   - 重要詳細が読めないときは全体ビューだけで pass しない。

5. 体系的にレビュー。
   - 簡単な視覚チェック以上なら [qa-rubric](./references/qa-rubric.md) を読む。
   - IA、レイアウト、余白、タイポ／フォント、色、画像品質、アイコン、コピー、 affordance、状態、レスポンシブ、アクセシビリティ、仕上げ。
   - 必須5表面を必ず別パス: フォント／タイポ、余白／レイアウトリズム、色／トークン、画像品質、コピー／コンテンツ。
   - モックが扱っていない問題（null 状態など）はモックの不足として別 finding。
   - 実装がモックと「同じくらい良く見えるか」も判断。スタイル問題、プロンプト漏れ（アプリ単体で立たない）も指摘。
   - 意図的なずれの可能性は質問や仮定として述べる。

6. 修正向け QA レポート。
   - finding を先に、深刻度とユーザー影響順。
   - 各 finding: 深刻度、場所、差分、根拠、重要性、具体修正。
   - 実装コンテキストがあれば CSS／コンポーネント／トークン提案。
   - 客観的不一致と主観的 polish を分離。
   - 必須表面を確認し残差を acceptable / expected / actionable に分類するまで「一致」「完了」「これ以上無理」と言わない。
   - 実行可能な実装チェックリストで終える。

## Required Fidelity Surfaces

毎回明示評価:

- Fonts and typography: ファミリ、フォールバック、ウェイト、サイズ、行高、字間、アンチエイリアス、ヒエラルキー、折り返し、省略、display/small UI の光学ウェイト。フォントは特に厳密に（類似書体・画像分析）。
- Spacing and layout rhythm: フレーム、クロップ、整列、マージン、パディング、グリッド、セクション間、コンポーネント間、角丸、シャドウ、垂直リズム。
- Colors and visual tokens: パレット、グラデーション、不透明度、コントラスト、セマンティック色、前景／背景、CSS トークンマップ。
- Image quality and asset fidelity: 被写体、クロップ、スケール、シャープネス、圧縮、透過ハロ、マスク、背景、ラスタ／ベクタ。ロゴ、イラスト、装飾、プロダクト画像、非標準アイコンをインライン SVG、div/CSS、絵文字、プレースホルダーで置換したら fail。
- Copy and content of app-specific text

## Severity

- `P0`: コア利用不能、重大 a11y、レイアウト破損、タスク不可能。
- `P1`: 主要デザイン不一致またはユーザーに気づかれやすい UX 退行。
- `P2`: 中程度の視覚 drift、状態不一致、レスポンシブ、修正可能 polish。
- `P3`: 受け入れを阻まない細部。

永続コントロールを隠すビューポート overflow、ファーストビュー・主要領域比率・折り返し・密度を変える不一致は P2 以上。

## Output Format

ユーザーが別形式を求めない限り:

```markdown
**Findings**
- [P1] Short issue title
  Location: screen/component/selector/file if known.
  Evidence: design does X, implementation does Y.
  Impact: why this matters.
  Fix: concrete change.

**Open Questions**
- Any ambiguity about intentional deviations, unavailable states, or missing artifacts.

**Implementation Checklist**
- Ordered fixes that can be executed directly.

**Follow-up Polish**
- P3 refinements that can improve fidelity after handoff.
```

実質的不一致が無ければ明言し、残るテストギャップを列挙。

引き渡し前使用時は最新 QA をプロジェクトルート `design-qa.md` に保存。

`design-qa.md` 必須項目:

- source visual truth path
- implementation screenshot path
- viewport
- ソース／実装ピクセル、CSS サイズ、密度正規化
- state
- full-view 比較根拠
- focused region 比較根拠、または不要理由
- findings
- 各 P0/P1/P2 反復の比較履歴
- final result

ブラウザレンダリング実装スクリーンショット、ビューポート、主要インタラクション、コンソールエラー、final result を含める。ブラウザ根拠欠如なら `final result` は `blocked`。

`final result` は厳密に `passed` または `blocked`。

`passed`: actionable P0/P1/P2 なし。P3 は follow-up 可。
`blocked`: actionable P0/P1/P2 残存とブロッカー名。

QA レポートのファイルパスを返す。

---
name: brush-up
description: "Product Design プロトタイプの美学リファイン（tighten / polish / ブラッシュアップ）。layout・IA・ルートは原則維持し、テンプレ感・AI 美学・コピー・タイポ・装飾を締める。design-qa 中・忠実クローンのみの依頼では使わない。テンプレ感を減らす・仕上げ・frontend-design 的に締める に使用。"
---

# Brush Up

既存の Product Design プロトタイプ（または同ワークフローで引き渡した runnable 実装）を、**参照フィデリティ QA ではなく美学・コピー・仕上げ**の観点で締める。

全面リデザイン、新ルート追加、ideate の選び直しはここではしない。必要なら `$ideate` または `$image-to-code` に戻す。

## When To Use

- ユーザーが **tighten / polish / brush up / ブラッシュアップ / テンプレ感 / もっと個性的** を求めたとき
- ビルド引き渡し（`critical-overrides` の tighten nudge）への返答として仕上げを求められたとき
- `$image-to-code` 等で **design-qa `passed` 後**、参照一致は十分で **見た目・文案だけ** 上げたいとき

## When Not To Use

- **design-qa 未完了**（`final result` が `passed` でない）— 先に [design-qa](../design-qa/SKILL.md)
- **`$url-to-code` の忠実クローン**が契約で、ユーザーが **ソース一致** のみ求めているとき — [critical-overrides](../../references/critical-overrides.md) の創作禁止
- **アノテーション1点修正** — [index](../index/SKILL.md#browser-annotation-updates) のスコープ付き編集。プロトタイプ全体の再美学化はしない
- **ビジュアルターゲット未選択の新規ビルド** — `$get-context` → `$ideate` → `$image-to-code`

ユーザーが **意図的なリデザイン**（IA 変更・参照から大きく外す）を明示したときは、先に scope を1文確認する。

## Critical Overrides

- 進行前にプラグインルーター [$index](../index/SKILL.md) を参照する。
- [$critical-overrides](../../references/critical-overrides.md) に従う。**忠実モードと brush-up が競合するときは忠実モードが優先。**
- 美学チェックリスト: [aesthetic-refine](./references/aesthetic-refine.md)（frontend-design 抜粋）

## User Context

開始前に [$user-context](../user-context/SKILL.md) を読み、ローカルシェルが使えるときは preflight を実行する。

保存済みブランド、トークン、デザインシステム、タイポ方針があれば **リファインはその範囲内**。保存参照をすべて inspect しない。必要なものだけ。

## Workflow

**重要: チェックリストとして完了する。**

1. **対象を特定** — プロトタイプルート、dev URL、主要画面。動いていなければ [cursor-preview](../../references/cursor-preview.md) で dev を起動しプレビュー可能にする。

2. **モード確認** — 忠実クローン／「モック通り」契約なら、タイポ・コピーの微修正のみ。レイアウト・パレットの大胆変更はしない。

3. **短いリファイン計画**（5 行以内）— [aesthetic-refine](./references/aesthetic-refine.md) の「brush-up 向け短い計画」。ユーザー向けに変更予定を1文で示してから編集してよい。

4. **実装** — 既存コンポーネント・トークン・スタックを尊重。新規フレームワークや全面 CSS 書き換えは避ける。
   - タイポ、色トークン、余白リズム、装飾、モーション、UI コピー（CTA・エラー・空状態）
   - 汎用 AI 美学パターンの削除（aesthetic-refine 参照）
   - インライン SVG 代用・div アートでアセットを **新たに劣化させない**（[critical-overrides](../../references/critical-overrides.md#アセットの扱い)）

5. **検証** — [cursor-preview](../../references/cursor-preview.md) で主要ビューポートとインタラクション。コンソールエラーなし。可能なら `browser_take_screenshot` で自己批評（装飾1つ削る判断）。

6. **引き渡し** — ローカル URL を返す。`design-qa.md` は **自動更新しない**（参照一致の再 QA が必要ならユーザーに `$design-qa` を提案）。

7. **完了メッセージ** — 例: `Brush-up is done on <URL>. Say if you want another pass, design-qa against the original mock, or $share.`

## Relationship To Other Skills

| スキル | 関係 |
| --- | --- |
| `design-qa` | ソース vs 実装の一致。brush-up **後**に元モックと再比較したいときのみユーザー指示で |
| `audit` | UX／フロー critique。美学だけなら brush-up |
| `ideate` / `image-to-code` | 新規方向・新規ビルド |
| `share` | デプロイは別依頼 |

## Output

- 変更したファイルは通常の実装 diff
- ユーザーがレポートを求めない限り、長い美学論は不要。何を締めたか箇条書き 3 点以内

完了とは、リファイン計画に沿った編集が入り、ブラウザで主要画面が問題なく見える状態。

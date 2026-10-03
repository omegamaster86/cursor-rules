# デザイン監査フレームワーク

`audit` ではこの構造を使う。

`audit` は単一アーティファクトのフィードバックではなく、より広い体験の体系的評価向け。

## 監査モード

- `UX audit`
- `Accessibility audit`
- `Combined audit`

## UX 監査のレンズ

- タスクの入口と発見性
- 情報アーキテクチャ
- インタラクションフローと摩擦
- ヒエラルキーと明瞭性
- 信頼と安心
- デフォルト状態と空状態
- コピーと CTA
- 体験全体の一貫性

## アクセシビリティ監査のレンズ

- 感知可能なコンテンツとコントラストリスク
- セマンティック構造と読み上げ順
- キーボード操作とフォーカス挙動
- ターゲットサイズと操作の手がかり
- ラベル、説明、エラー回復
- モーション、タイミング、状態変化の伝達
- レスポンシブのリフローとズーム耐性
- 支援技術向けの明瞭性と堅牢性

## UX 監査の出力構造

1. `Audit scope`
2. `User goal`
3. `Strengths`
4. `Notable risks`
5. `Opportunity areas`
6. `Optional comparison context`
7. `Recommendations`

## アクセシビリティ監査の出力構造

1. `Audit scope`
2. `Accessibility target`
3. `Confirmed strengths`
4. `Likely issues`
5. `WCAG-relevant considerations`
6. `Evidence limits and verification gaps`
7. `Recommendations`

## 複合監査の出力構造

1. `Audit scope`
2. `User goal and accessibility target`
3. `Strengths`
4. `UX risks`
5. `Accessibility risks`
6. `Opportunity areas`
7. `Evidence limits and verification gaps`
8. `Recommendations`

## ガードレール

- ビジネス戦略ではなく体験パターンに焦点を置く。
- 比較プロダクトは任意。監査を鋭くするときだけ使う。
- 構造問題と仕上げ問題を分ける。
- 推奨はユーザーゴール、ワークフロー、アクセシビリティ成果に結びつける。
- ユーザーが実装詳細を十分に提供していない限り、完全 WCAG 準拠を暗示しない。
- 単一画面・コンポーネント・モーダル・限定的インタラクションなら、その表面にスコープを限定する。

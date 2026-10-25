# Structural audit（親・フェーズ 0.5）

サブエージェント起動**前**に、変更ファイルに限定して実施する（リポジトリ全体の既存負債は列挙しない）。

| 観点 | 手順 |
|------|------|
| 新規 import と package.json | 差分の外部 import が dependencies にあるか |
| 解決不能・怪しい import | パス・エイリアスの実在 |
| 二重 export / 未使用の新規 export | export 名の grep |
| 差分内の類似ロジック | 特徴的な文字列で grep |
| レイヤー違反 | `.cursor/rules`・skills・PJ 境界 |
| 複雑度の急増 | 大きな関数・分岐 |

`structural_audit_summary` を親のコンテキストに保持する（**成果物ファイルは書かない**）。統合時は `consolidated.md` の Structural Audit セクションに載せる。`reuse_hints` は Quality レーン（C）に渡す。

クローン候補の行は `reuse_hints` として別途保持する。

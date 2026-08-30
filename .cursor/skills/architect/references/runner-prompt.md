# Architect runner プロンプト

オーケストレータはフェーズ B で **1メッセージ内に3つの Task を同時起動**する（`run_in_background: true`）。各 Task の `model` は `.cursor/rules/forge-models.mdc` の `architect runners` 行の slug を使う。`.cursor/rules/multi-agent-task-enforcement.mdc` を遵守 — 親が候補案を単独執筆しない。

各並列候補 runner にこのファイルを渡し、周辺の可変入力を埋める: タスク、フェーズ A の土台固め成果物、隔離作業ディレクトリ、出力先パス。作業ディレクトリは可能なら git worktree、そうでなければスケッチ dir 下の runner ごとのサブディレクトリ。重要なのは候補間の独立性。

architect の並列探索で 1 つの候補設計を産出する。まず **architect** スキルを全文読む。それが内側のワークフロー。候補設計パッケージを出力: 型スケッチ、関数シグネチャ、モジュールマップ、[`rationale-template.md`](rationale-template.md) の形の文章根拠。

次の規律を適用する。オーケストレータはこれらの軸で候補を比較しベースを選ぶ。

- 呼び出し側の usage を先に。型の前に README 風の usage と現実的な呼び出しサイト 2〜3 を書き、そこから型スケッチを導く。usage が仕様。両者は一致。ずれたらスケッチを usage に合わせる。逆ではない。
- データ構造を先に。コア型を正しくすればコードは自明になる。主要なアクセスパターンを提案構造で辿る。答えが「後で map / index / cache を足す」なら構造が間違い。
- 共有状態: 2 _actor が書きうるなら「何が起きる？」と問う。答えが「何もない」でなければ、デフォルトは読み取り境界でマージする actor ごとの状態。
- 境界を見えるように。本体は `not implemented` エラー、難しいロジックは `// TODO` 疑似コード、意図と不変条件を述べる doc コメント。読者は型とシグネチャだけで入力から出力まで辿れるべき。
- 不変条件を型にエンコード: 誤用しにくい型 > 実行時チェック > 文章コメント（**encode-lessons-in-structure** 原則スキル）。
- 境界で検証し、内部では型を信頼（**web-coding-standards** の `form-validation`、`nextjs-directory-structure` の `practice-bff`）。ビジネスロジックは純関数。シェルは薄く。
- 不変条件ごとに単一の真実の源。同期ではなく導出。
- 該当すれば冪等な状態遷移（**make-operations-idempotent** 原則スキル）。操作が 2 回走るか途中で落ちたらどうなるか問う。
- 呼び出しチェーンは短く。流れの追跡に 3 ファイル超が要るなら階層をフラットに（**refactor-check**）。

複数 runner の 1 つで、モデルはそれぞれ違う。自分のモデルで最良の設計を出す。他に対してヘッジしない。候補間の差がベース選択とグラフトのシグナル。安全そうな中間に収束すると探索を無効化する。


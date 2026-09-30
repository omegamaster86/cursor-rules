# 呼び出しを移して legacy API を削除する

新 API が正しい設計と決まったら、**互換層を残さず**同一 wave で caller を移し旧 API を削除する。

**適用:** 旧 caller が残るまま新 internal API を導入するとき。外部 backward compatibility が不要な repo 内 refactor。

**ルール:**
- internal caller が残るだけで legacy path を維持しない
- caller を inventory → migrate → 旧 API を即 delete
- 一時 adapter は例外で time-box。デフォルトアーキテクチャにしない
- テストは新 contract を assert。refactor 前の実装詳細だけを守るテストは削除

**当てはまる:**
- 外部ユーザーが backward compat を要求しない
- 協調 breaking change を吸収できる
- 新 API が簡素化 initiative の一部

**理由:** 旧新併存は dual-path の複雑さ、cleanup 遅延、append-only な codebase 感を生む。`outcome-oriented-execution.md` と整合。

# 設計する

関数境界を越える変更は形がロックインする前に設計する。

## `/architect`

型・シグネチャ・モジュール境界を `not implemented` スケッチで固め、実装で誤りが出たら捨てて再設計。

- 並列案: **multi-agent-candidates**（3 Task 必須、`multi-agent-task-enforcement.mdc`）
- 統合前: `design-red-flags.md` で shallow module 等を弾く
- 争点が大きいとき: `/review-orchestrator-triple-hybrid`

## `/swarm`

設計 bakeoff ではなく、**カバレッジ分割・レース・探索**向き。

```text
/swarm この 40 ファイルの import 置換を 8 ワーカーで分割。各スライスは typecheck で PASS 報告。
```

モデルは `forge-models.mdc` の `swarm workers`。

次: [作って証明する](./05-build-and-verify.md)

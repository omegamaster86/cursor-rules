# Align と Ship

| フェーズ | 入口 | 役割 |
|----------|------|------|
| **Align** | `/plan-interview`（grilling） | 何を作るか、非ゴール、用語の合意 |
| **Ship** | `/forge-mode` | プレイブック駆動の実装・調査・PR 運用 |

同じターンで両方を混ぜない。

## Intent gate

`/forge-mode` 起動直後、次のいずれか 1 行を残す。

- `alignment: <合意 1 文>` — Ship 続行
- `alignment: skip — <再現済みバグ / 読み取り専用調査 / 実装明示>` — Ship 続行
- `alignment: blocked — plan-interview` — **ここで止める**。`/plan-interview` を案内

「いい感じ」「ちゃんと」だけ、スコープ未決、用語ズレが続くときは blocked。

## forge-mode の使い方

```text
/forge-mode スクロールが 750ms ごとにずれる。idle でも。先に repro。
```

```text
/forge-mode この仕様で実装して。<plan-interview で出た alignment 行を貼る>
```

プレイブックは todo に verbatim コピーされる。原則（`principles/`）は該当 leaf を全文読んでから手を動かす。

次: [理解する](./03-understand.md)

---
name: domain-modeling
description: "プロジェクトのドメインモデルを構築・研ぎ澄ます。コードベースの用語の議論、GLOSSARY.md の作成・編集、ADR の記録・編集に使用。"
disable-model-invocation: true
---

# Domain Modeling

設計しながら **能動的に** ドメインモデルを構築・研ぎ澄ます。用語への挑戦、エッジケースのシナリオ発明、決まった瞬間の glossary / ADR への書き込みが本スキル。（`GLOSSARY.md` を読むだけの一行習慣は本スキルではない — モデルを **変える** ときに使う。）

旧来の `CONTEXT.md` / `CONTEXT-MAP.md` は `GLOSSARY.md` / `GLOSSARY-MAP.md` にリネーム済みとみなす。スキルは新名称のみ参照する。

## File structure

多くの repo は単一コンテキスト：

```
/
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

ルートに `GLOSSARY-MAP.md` があるときは複数コンテキスト。マップが各コンテキストの場所を指す：

```
/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                          ← システム全体の決定
├── src/
│   ├── ordering/
│   │   ├── GLOSSARY.md
│   │   └── docs/adr/
│   └── billing/
│       ├── GLOSSARY.md
│       └── docs/adr/
```

**lazy 作成:** 書くものがあるときだけ。`GLOSSARY.md` が無ければ最初の用語が決まったときに作る。`docs/adr/` も最初の ADR が要るときに作る。

## During the session

### Challenge against the glossary

ユーザーの用語が `GLOSSARY.md` の言語と矛盾するとき、すぐ指摘する。「glossary では cancellation は X だが、今 Y の意味に見える。どちらか？」

### Sharpen fuzzy language

曖昧・多義語には正確な canonical 語を提案。「account と言っているが Customer か User か。別物。」

### Discuss concrete scenarios

関係を議論するとき、具体シナリオでストレステスト。境界を迫るエッジを発明する。

### Cross-reference with code

ユーザーが動き方を述べたらコードと照合。矛盾があれば表面化。「コードは Order 全体を cancel するが、部分 cancel 可能と言った。どちらが正か？」

### Update GLOSSARY.md inline

用語が決まったら **その場で** `GLOSSARY.md` を更新。溜め込まない。形式は [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md)。

`GLOSSARY.md` に **実装詳細を入れない。** spec・scratch pad・実装決定の置き場にしない。glossary のみ。

### Offer ADRs sparingly

次の **三つすべて** が真のときだけ ADR を提案：

1. **逆戻しが難い** — 後から変えるコストが meaningful
2. **文脈なしでは驚く** — 将来の読者が「なぜこう？」となる
3. **本当のトレードオフの結果** — 代替があり、理由で選んだ

どれか欠ければ ADR はスキップ。形式は [ADR-FORMAT.md](./ADR-FORMAT.md)。

## 上流

正本: [mattpocock/skills — engineering/domain-modeling](https://github.com/mattpocock/skills/tree/main/skills/engineering/domain-modeling)。同期メモ: `references/UPSTREAM.md`。

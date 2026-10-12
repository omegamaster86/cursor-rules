---
name: domain-modeling
description: "プロジェクトのドメインモデルを構築・研ぎ澄ます。コードベースの用語、`GLOSSARY.md` の作成・編集、ADR の記録・編集の議論時に使用。"
disable-model-invocation: true
---

# Domain Modeling

設計しながらドメインモデルを **能動的に** 構築・研ぎ澄ます。**能動**な規律：用語への挑戦、エッジケースのシナリオ、決定が固まった瞬間の glossary / ADR への書き込み。（`GLOSSARY.md` を読んで語彙を借りるだけはこのスキルではない。どのスキルでもできる 1 行習慣。モデルを **変える** ときにこのスキル。）

## ファイル構造

多くの repo は単一 context：

```
/
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

ルートに `GLOSSARY-MAP.md` がある場合は複数 context。map が各 context の場所を指す：

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

ファイルは lazy に作る：書くものがあるときだけ。`GLOSSARY.md` が無ければ最初の用語が決まったときに作成。`docs/adr/` も最初の ADR が要るときに作成。

## セッション中

### glossary への挑戦

ユーザーの用語が `GLOSSARY.md` の既存言語と矛盾するとき、すぐ指摘する。「glossary は cancellation を X と定義しているが、今は Y のように聞こえる。どちらか？」

### 曖昧な言葉を尖らせる

曖昧・多義の語には precise な canonical 語を提案。「account と言っているが Customer か User か。別物。」

### 具体シナリオで議論

関係を議論するとき、エッジを突く具体シナリオを invent し、概念の境界を精密にさせる。

### コードと突合

ユーザーが動きを述べたらコードが一致するか確認。矛盾なら表面化：「コードは Order 全体を cancel するが、部分 cancel 可能と言った。どちらが正か？」

### `GLOSSARY.md` を inline 更新

用語が決まったらその場で更新。バッチにまとめない。形式は [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md)。

`GLOSSARY.md` は実装詳細を一切含めない。spec・scratch・実装決定の置き場にしない。**glossary でしかない。**

### ADR は控えめに

次の **3 つすべて** が真のときだけ ADR を提案：

1. **戻しにくい**：後から変えるコストが meaningful
2. **文脈なしでは意外**：将来の読者が「なぜこう？」となる
3. **実 trade-off の結果**：代替があり、理由で 1 つを選んだ

1 つでも欠ければ ADR は skip。形式は [ADR-FORMAT.md](./ADR-FORMAT.md)。

## 上流

正本: [mattpocock/skills — engineering/domain-modeling](https://github.com/mattpocock/skills/tree/main/skills/engineering/domain-modeling)。`references/UPSTREAM.md`。

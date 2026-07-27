---
title: Utility File Naming Convention
impact: LOW
impactDescription: ヘルパー関数の発見しやすさ
tags: naming, utilities, helpers, convention
---

## Utility File Naming Convention

ユーティリティ関数とヘルパーファイルの命名規則です。

配置先は [colocation-utils](colocation-utils.md) を参照（ページ／機能固有は `_utils/`、共通は `src/utils/`。`_lib/` / `lib/` は使わない）。

**Correct（目的を明示・kebab-case）：**

```
utils/
├── class-name.ts     # cn()
├── date.ts
└── ...

app/.../todos/_utils/
└── todo-labels.ts
```

**命名規則：**

| 形式 | 用途 | 例 |
|------|------|-----|
| `kebab-case.ts` | 複数語・共通 util | `class-name.ts`, `todo-labels.ts` |
| 単一語 | そのまま | `date.ts` |

**注意**: Barrel Exports（`utils/index.ts`）は必須ではない。大規模では直接インポートを推奨。

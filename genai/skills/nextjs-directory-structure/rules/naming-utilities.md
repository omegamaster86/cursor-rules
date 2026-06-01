---
title: Utility File Naming Convention
impact: LOW
impactDescription: ヘルパー関数の発見しやすさ
tags: naming, utilities, helpers, convention
---

## Utility File Naming Convention

ユーティリティ関数とヘルパーファイルの命名規則です。

**Incorrect（不明確な命名）:**

```
utils/
├── helpers.ts        # ❌ 何のヘルパーか不明
├── utils.ts          # ❌ 冗長
├── misc.ts           # ❌ 曖昧
└── stuff.ts          # ❌ 意味不明
```

**Correct（目的を明示）:**

```
utils/
├── format.ts         # ✅ フォーマット関連
├── validation.ts     # ✅ バリデーション関連
├── date.ts           # ✅ 日付操作関連
├── string.ts         # ✅ 文字列操作関連
└── class-name.ts     # ✅ クラス名結合（cn関数など）
```

**命名規則：**

| 形式 | 用途 | 例 |
|------|------|-----|
| `camelCase.ts` | 単一目的のファイル | `formatDate.ts` |
| `kebab-case.ts` | 複数関数を含むファイル | `class-name.ts` |
| `index.ts` | エクスポート集約 | `utils/index.ts` |

**ファイル内容の例：**

```typescript
// utils/format.ts
export function formatDate(date: Date): string {
  return date.toLocaleDateString('ja-JP')
}

export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('ja-JP', {
    style: 'currency',
    currency: 'JPY',
  }).format(amount)
}

// utils/validation.ts
export function isValidEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

export function isValidPhoneNumber(phone: string): boolean {
  return /^0\d{9,10}$/.test(phone)
}
```

**エクスポート集約（オプション）：**

```typescript
// utils/index.ts
export * from './format'
export * from './validation'
export * from './date'
```

**注意**: Barrel Exportsはビルド速度に影響する可能性があるため、大規模プロジェクトでは直接インポートを推奨。

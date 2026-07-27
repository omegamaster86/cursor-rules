---
title: Tailwind CSS rem Units
impact: MEDIUM
impactDescription: スペーシング・サイジング系プロパティは rem 単位を使用
tags: tailwind, css, styling, units, accessibility
---

## Tailwind CSS rem Units

Tailwind CSS でスペーシング・サイジング系プロパティを指定する際は、px 単位ではなく rem 単位のユーティリティクラスを使用します。

**理由：**

- rem はルートフォントサイズに相対的なため、ユーザーのブラウザ設定（フォントサイズ変更）に追従する
- アクセシビリティの向上（視覚障害を持つユーザーがフォントサイズを拡大した際にレイアウトが適切にスケールする）

**原則：Tailwind のデフォルトユーティリティクラス（rem ベース）を優先し、任意値が必要な場合は rem 単位を使用する。**

**対象プロパティ：**

| カテゴリ | プロパティ | rem（✅ 推奨） | px（❌ 非推奨） |
|---------|-----------|---------------|----------------|
| サイジング | width / height | `w-4`, `h-4` | `w-[16px]`, `h-[16px]` |
| サイジング | min/max-width / min/max-height | `max-w-md`, `min-h-12` | `max-w-[300px]`, `min-h-[48px]` |
| スペーシング | padding / margin | `p-4`, `m-2` | `p-[16px]`, `m-[8px]` |
| スペーシング | gap | `gap-4`, `gap-x-2` | `gap-[16px]` |
| スペーシング | top / right / bottom / left | `top-4`, `inset-0` | `top-[16px]` |
| スペーシング | scroll-margin / scroll-padding | `scroll-m-4` | `scroll-m-[16px]` |
| テキスト | font-size | `text-base` | `text-[16px]` |
| テキスト | text-indent | `indent-4` | `indent-[16px]` |
| 装飾 | border-radius | `rounded-lg` | `rounded-[8px]` |

**良い例と悪い例：**

```typescript
// ❌ 悪い例：px 単位の任意値
<div className="w-[200px] h-[100px] p-[16px] m-[8px] gap-[12px] text-[14px] rounded-[8px]">
  Content
</div>

// ✅ 良い例：Tailwind のデフォルトクラス（rem ベース）
<div className="w-52 h-24 p-4 m-2 gap-3 text-sm rounded-lg">
  Content
</div>

// ✅ 良い例：任意値が必要な場合も rem を使用
<div className="w-[12.5rem] h-[6.25rem] p-[1rem] m-[0.5rem] gap-[0.75rem] text-[0.875rem] rounded-[0.5rem]">
  Content
</div>
```

**許容される px 使用：**

- `border-width`（`border`, `border-2` など）— 意図的に薄い線でありスケール不要
- `outline-width`（`outline-1` など）
- `box-shadow`（`shadow-*`）— 影のぼかし・オフセット
- 1px の微細な調整（`gap-px` など）

**チェックリスト：**

- [ ] スペーシング・サイジング系の任意値に `[…px]` を使用していない
- [ ] 任意値が必要な場合は rem 単位を使用している
- [ ] Tailwind のデフォルトユーティリティクラス（rem ベース）を優先している

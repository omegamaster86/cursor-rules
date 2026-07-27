---
title: Date Handling with date-fns
impact: MEDIUM
impactDescription: 軽量で関数型な日付処理
tags: date-fns, dates, formatting, parsing
---

## Date Handling with date-fns

date-fns を使用した日付処理のベストプラクティスです。

**インストール：**

```bash
npm install date-fns
```

**基本的なフォーマット：**

```typescript
import { format, formatDistance, formatRelative } from 'date-fns'
import { ja } from 'date-fns/locale'

const date = new Date(2024, 0, 15, 14, 30)

// 基本フォーマット
format(date, 'yyyy年MM月dd日')  // "2024年01月15日"
format(date, 'yyyy/MM/dd HH:mm')  // "2024/01/15 14:30"
format(date, 'M月d日(E)', { locale: ja })  // "1月15日(月)"

// 相対時間
formatDistance(date, new Date(), { locale: ja, addSuffix: true })
// "約1ヶ月前"

// 相対日付
formatRelative(date, new Date(), { locale: ja })
// "先週の月曜日 14:30"
```

**日付の操作：**

```typescript
import {
  addDays,
  addMonths,
  subDays,
  startOfMonth,
  endOfMonth,
  startOfWeek,
  endOfWeek,
} from 'date-fns'

const today = new Date()

// 加算・減算
addDays(today, 7)      // 7日後
addMonths(today, 1)    // 1ヶ月後
subDays(today, 3)      // 3日前

// 範囲の取得
startOfMonth(today)    // 月初
endOfMonth(today)      // 月末
startOfWeek(today, { locale: ja })  // 週初（日曜）
endOfWeek(today, { locale: ja })    // 週末（土曜）
```

**日付の比較：**

```typescript
import {
  isBefore,
  isAfter,
  isSameDay,
  isWithinInterval,
  differenceInDays,
} from 'date-fns'

const date1 = new Date(2024, 0, 15)
const date2 = new Date(2024, 0, 20)

// 比較
isBefore(date1, date2)  // true
isAfter(date1, date2)   // false
isSameDay(date1, date2) // false

// 期間内かどうか
isWithinInterval(new Date(2024, 0, 17), {
  start: date1,
  end: date2,
})  // true

// 差分
differenceInDays(date2, date1)  // 5
```

**パースとバリデーション：**

```typescript
import { parse, parseISO, isValid } from 'date-fns'

// ISO 8601 形式のパース
const isoDate = parseISO('2024-01-15T14:30:00')

// カスタム形式のパース
const customDate = parse('2024/01/15', 'yyyy/MM/dd', new Date())

// バリデーション
isValid(isoDate)        // true
isValid(new Date('invalid'))  // false
```

**React コンポーネントでの使用：**

```tsx
'use client'

import { format, formatDistance } from 'date-fns'
import { ja } from 'date-fns/locale'

type DateDisplayProps = {
  date: Date | string
  format?: 'full' | 'short' | 'relative'
}

export function DateDisplay({ date, format: displayFormat = 'full' }: DateDisplayProps) {
  const dateObj = typeof date === 'string' ? new Date(date) : date

  const formatted = (() => {
    switch (displayFormat) {
      case 'full':
        return format(dateObj, 'yyyy年MM月dd日 HH:mm', { locale: ja })
      case 'short':
        return format(dateObj, 'M/d', { locale: ja })
      case 'relative':
        return formatDistance(dateObj, new Date(), { locale: ja, addSuffix: true })
      default:
        return format(dateObj, 'yyyy-MM-dd')
    }
  })()

  return <time dateTime={dateObj.toISOString()}>{formatted}</time>
}

// 使用例
<DateDisplay date={post.createdAt} format="relative" />
// → "3日前"
```

**チェックリスト：**

- [ ] 日本語ロケールは `date-fns/locale` からインポート
- [ ] ISO 8601 形式は `parseISO` でパース
- [ ] 相対時間には `formatDistance` を使用
- [ ] `<time>` 要素に `dateTime` 属性を設定
- [ ] 必要な関数のみをインポート（ツリーシェイキング）

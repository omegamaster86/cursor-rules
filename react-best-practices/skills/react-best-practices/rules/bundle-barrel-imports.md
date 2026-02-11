---
title: バレルファイル経由の Import を避ける
impact: CRITICAL
impactDescription: 200-800ms import cost, slow builds
tags: bundle, imports, tree-shaking, barrel-files, performance
---

## バレルファイル経由の Import を避ける

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

未使用モジュールを大量に読み込まないため、barrel file ではなくソースファイルから直接 import します。**Barrel file** は複数モジュールを再エクスポートするエントリポイントです（例: `index.js` で `export * from './module'` を行う）。

人気のアイコン/コンポーネントライブラリでは、エントリファイルに **最大 10,000 件**の再エクスポートが含まれることがあります。多くの React パッケージでは import だけで **200-800ms** かかり、開発速度と本番コールドスタートの両方に影響します。

**tree-shaking が効きにくい理由:** ライブラリを external（非バンドル）にすると、バンドラは最適化できません。tree-shaking のためにバンドルすると、モジュールグラフ全体の解析でビルドが大きく遅くなります。

**Incorrect（imports entire library):**

```tsx
import { Check, X, Menu } from 'lucide-react'
// Loads 1,583 modules, takes ~2.8s extra in dev
// Runtime cost: 200-800ms on every cold start

import { Button, TextField } from '@mui/material'
// Loads 2,225 modules, takes ~4.2s extra in dev
```

**Correct（imports only what you need):**

```tsx
import Check from 'lucide-react/dist/esm/icons/check'
import X from 'lucide-react/dist/esm/icons/x'
import Menu from 'lucide-react/dist/esm/icons/menu'
// Loads only 3 modules (~2KB vs ~1MB)

import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
// Loads only what you use
```

**代替案（Next.js 13.5+):**

```js
// next.config.js - use optimizePackageImports
module.exports = {
  experimental: {
    optimizePackageImports: ['lucide-react', '@mui/material']
  }
}

// Then you can keep the ergonomic barrel imports:
import { Check, X, Menu } from 'lucide-react'
// Automatically transformed to direct imports at build time
```

直接 import により、dev 起動 15-70% 高速化、ビルド 28% 高速化、コールドスタート 40% 高速化、HMR も大幅に改善します。

影響を受けやすいライブラリ: `lucide-react`, `@mui/material`, `@mui/icons-material`, `@tabler/icons-react`, `react-icons`, `@headlessui/react`, `@radix-ui/react-*`, `lodash`, `ramda`, `date-fns`, `rxjs`, `react-use`.

参考: [How we optimized package imports in Next.js](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js)

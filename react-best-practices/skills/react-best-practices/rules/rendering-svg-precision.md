---
title: SVG 精度を最適化する
impact: LOW
impactDescription: reduces file size
tags: rendering, svg, optimization, svgo
---

## SVG 精度を最適化する

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

SVG 座標の精度を下げてファイルサイズを削減します。最適精度は viewBox サイズに依存しますが、一般に精度削減は検討すべきです。

**Incorrect（excessive precision):**

```svg
<path d="M 10.293847 20.847362 L 30.938472 40.192837" />
```

**Correct（1 decimal place):**

```svg
<path d="M 10.3 20.8 L 30.9 40.2" />
```

**SVGO で自動化:**

```bash
npx svgo --precision=1 --multipass icon.svg
```

---
title: モジュールを条件付きで読み込む
impact: HIGH
impactDescription: loads large data only when needed
tags: bundle, conditional-loading, lazy-loading
---

## モジュールを条件付きで読み込む

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

大きなデータやモジュールは、機能が有効化されたときだけ読み込みます。

**例（アニメーションフレームを遅延読み込み）:**

```tsx
function AnimationPlayer({ enabled, setEnabled }: { enabled: boolean; setEnabled: React.Dispatch<React.SetStateAction<boolean>> }) {
  const [frames, setFrames] = useState<Frame[] | null>(null)

  useEffect(() => {
    if (enabled && !frames && typeof window !== 'undefined') {
      import('./animation-frames.js')
        .then(mod => setFrames(mod.frames))
        .catch(() => setEnabled(false))
    }
  }, [enabled, frames, setEnabled])

  if (!frames) return <Skeleton />
  return <Canvas frames={frames} />
}
```

`typeof window !== 'undefined'` の判定により、このモジュールが SSR 用にバンドルされるのを防ぎ、サーバーバンドルサイズとビルド速度を最適化できます。

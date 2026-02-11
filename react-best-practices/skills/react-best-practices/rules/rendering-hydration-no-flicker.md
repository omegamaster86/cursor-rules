---
title: チラつきなしで Hydration 不一致を防ぐ
impact: MEDIUM
impactDescription: avoids visual flicker and hydration errors
tags: rendering, ssr, hydration, localStorage, flicker
---

## チラつきなしで Hydration 不一致を防ぐ

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

client-side storage（localStorage / cookies）に依存する内容を描画する場合は、React が hydration する前に DOM を更新する同期スクリプトを注入し、SSR 破綻と hydration 後のチラつきを同時に防ぎます。

**Incorrect（breaks SSR):**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  // localStorage is not available on server - throws error
  const theme = localStorage.getItem('theme') || 'light'
  
  return (
    <div className={theme}>
      {children}
    </div>
  )
}
```

`localStorage` はサーバーでは未定義のため、SSR は失敗します。

**Incorrect（visual flickering):**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState('light')
  
  useEffect(() => {
    // Runs after hydration - causes visible flash
    const stored = localStorage.getItem('theme')
    if (stored) {
      setTheme(stored)
    }
  }, [])
  
  return (
    <div className={theme}>
      {children}
    </div>
  )
}
```

コンポーネントは先にデフォルト値（`light`）で描画され、hydration 後に更新されるため、誤った内容のフラッシュが発生します。

**Correct（no flicker, no hydration mismatch):**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  return (
    <>
      <div id="theme-wrapper">
        {children}
      </div>
      <script
        dangerouslySetInnerHTML={{
          __html: `
            (function() {
              try {
                var theme = localStorage.getItem('theme') || 'light';
                var el = document.getElementById('theme-wrapper');
                if (el) el.className = theme;
              } catch (e) {}
            })();
          `,
        }}
      />
    </>
  )
}
```

inline script が要素表示前に同期実行されるため、DOM は最初から正しい値を持ちます。チラつきも hydration mismatch も発生しません。

このパターンは、テーマ切替・ユーザー設定・認証状態など、デフォルト値のフラッシュなしに即時表示したい client-only データで特に有効です。

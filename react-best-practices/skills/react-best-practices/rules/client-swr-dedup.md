---
title: SWR で自動重複排除を行う
impact: MEDIUM-HIGH
impactDescription: automatic deduplication
tags: client, swr, deduplication, data-fetching
---

## SWR で自動重複排除を行う

このルールの目的はパフォーマンスと保守性の向上です。以下に非推奨例と推奨例を示します。

SWR はコンポーネントインスタンス間で、リクエスト重複排除・キャッシュ・再検証を提供します。

**Incorrect（no deduplication, each instance fetches):**

```tsx
function UserList() {
  const [users, setUsers] = useState([])
  useEffect(() => {
    fetch('/api/users')
      .then(r => r.json())
      .then(setUsers)
  }, [])
}
```

**Correct（multiple instances share one request):**

```tsx
import useSWR from 'swr'

function UserList() {
  const { data: users } = useSWR('/api/users', fetcher)
}
```

**不変データの場合:**

```tsx
import { useImmutableSWR } from '@/lib/swr'

function StaticContent() {
  const { data } = useImmutableSWR('/api/config', fetcher)
}
```

**ミューテーションの場合:**

```tsx
import { useSWRMutation } from 'swr/mutation'

function UpdateButton() {
  const { trigger } = useSWRMutation('/api/user', updateUser)
  return <button onClick={() => trigger()}>Update</button>
}
```

参考: [https://swr.vercel.app](https://swr.vercel.app)

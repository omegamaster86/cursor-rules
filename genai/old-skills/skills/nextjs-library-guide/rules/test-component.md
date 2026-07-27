---
title: Component Testing with React Testing Library
impact: HIGH
impactDescription: コンポーネントの振る舞いを検証するテスト
tags: react-testing-library, component-test, testing
---

## Component Testing with React Testing Library

React Testing Library を使用したコンポーネントテストのベストプラクティスです。

**インストール：**

```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

**基本的なコンポーネントテスト：**

```tsx
// components/Button/Button.tsx
type ButtonProps = {
  children: React.ReactNode
  onClick?: () => void
  disabled?: boolean
}

export function Button({ children, onClick, disabled }: ButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled} className="btn">
      {children}
    </button>
  )
}

// components/Button/Button.test.tsx
import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Button } from './Button'

describe('Button', () => {
  it('should render children', () => {
    render(<Button>Click me</Button>)
    
    expect(screen.getByRole('button', { name: 'Click me' })).toBeInTheDocument()
  })

  it('should call onClick when clicked', async () => {
    const user = userEvent.setup()
    const handleClick = vi.fn()
    
    render(<Button onClick={handleClick}>Click me</Button>)
    
    await user.click(screen.getByRole('button'))
    
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('should not call onClick when disabled', async () => {
    const user = userEvent.setup()
    const handleClick = vi.fn()
    
    render(<Button onClick={handleClick} disabled>Click me</Button>)
    
    await user.click(screen.getByRole('button'))
    
    expect(handleClick).not.toHaveBeenCalled()
  })
})
```

**フォームのテスト：**

```tsx
// components/LoginForm/LoginForm.test.tsx
import { describe, it, expect, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { LoginForm } from './LoginForm'

describe('LoginForm', () => {
  it('should show validation errors', async () => {
    const user = userEvent.setup()
    render(<LoginForm onSubmit={vi.fn()} />)
    
    // 空のまま送信
    await user.click(screen.getByRole('button', { name: '送信' }))
    
    await waitFor(() => {
      expect(screen.getByText('メールアドレスは必須です')).toBeInTheDocument()
    })
  })

  it('should submit with valid data', async () => {
    const user = userEvent.setup()
    const handleSubmit = vi.fn()
    render(<LoginForm onSubmit={handleSubmit} />)
    
    await user.type(screen.getByLabelText('メールアドレス'), 'test@example.com')
    await user.type(screen.getByLabelText('パスワード'), 'Password123')
    await user.click(screen.getByRole('button', { name: '送信' }))
    
    await waitFor(() => {
      expect(handleSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'Password123',
      })
    })
  })
})
```

**非同期コンポーネントのテスト：**

```tsx
import { describe, it, expect, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { TodoList } from './TodoList'

// APIモック
vi.mock('@/services/api', () => ({
  fetchTodos: vi.fn().mockResolvedValue([
    { id: '1', title: 'Todo 1' },
    { id: '2', title: 'Todo 2' },
  ]),
}))

describe('TodoList', () => {
  it('should render loading state', () => {
    render(<TodoList />)
    
    expect(screen.getByText('読み込み中...')).toBeInTheDocument()
  })

  it('should render todos after loading', async () => {
    render(<TodoList />)
    
    await waitFor(() => {
      expect(screen.getByText('Todo 1')).toBeInTheDocument()
      expect(screen.getByText('Todo 2')).toBeInTheDocument()
    })
  })
})
```

**クエリの優先順位：**

```typescript
// 推奨順（アクセシビリティ重視）
screen.getByRole('button', { name: 'Submit' })  // 1. ロール + 名前
screen.getByLabelText('Email')                   // 2. ラベル
screen.getByPlaceholderText('Enter email')       // 3. プレースホルダー
screen.getByText('Welcome')                      // 4. テキスト
screen.getByTestId('custom-element')             // 5. data-testid（最後の手段）
```

**チェックリスト：**

- [ ] `userEvent` でユーザー操作をシミュレート
- [ ] `waitFor` で非同期処理を待機
- [ ] ロールベースのクエリを優先
- [ ] `data-testid` は最後の手段
- [ ] 実装詳細ではなく振る舞いをテスト

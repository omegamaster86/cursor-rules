---
title: E2E Testing with Playwright
impact: HIGH
impactDescription: ブラウザ自動化によるエンドツーエンドテスト
tags: playwright, e2e-test, browser-automation
---

## E2E Testing with Playwright

Playwright を使用した E2E テストのベストプラクティスです。

**インストール：**

```bash
npm install --save-dev @playwright/test
npx playwright install
```

**設定（playwright.config.ts）：**

```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

**基本的な E2E テスト：**

```typescript
// tests/e2e/todo.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Todo List', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/todos')
  })

  test('should display todo list', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'Todo List' })).toBeVisible()
    await expect(page.getByRole('list')).toBeVisible()
  })

  test('should create a new todo', async ({ page }) => {
    // フォームに入力
    await page.getByLabel('タイトル').fill('New Todo')
    await page.getByRole('button', { name: '追加' }).click()

    // 新しいTodoが表示される
    await expect(page.getByText('New Todo')).toBeVisible()
  })

  test('should delete a todo', async ({ page }) => {
    // 既存のTodoを確認
    const todoItem = page.getByRole('listitem').first()
    const todoText = await todoItem.textContent()

    // 削除ボタンをクリック
    await todoItem.getByRole('button', { name: '削除' }).click()

    // 確認ダイアログ
    await page.getByRole('button', { name: '確認' }).click()

    // Todoが削除されている
    await expect(page.getByText(todoText!)).not.toBeVisible()
  })
})
```

**認証が必要なテスト：**

```typescript
// tests/e2e/auth.setup.ts
import { test as setup, expect } from '@playwright/test'

const authFile = 'tests/.auth/user.json'

setup('authenticate', async ({ page }) => {
  await page.goto('/login')
  await page.getByLabel('メールアドレス').fill('test@example.com')
  await page.getByLabel('パスワード').fill('password123')
  await page.getByRole('button', { name: 'ログイン' }).click()

  await expect(page).toHaveURL('/dashboard')
  
  await page.context().storageState({ path: authFile })
})

// playwright.config.ts に追加
// projects: [
//   { name: 'setup', testMatch: /.*\.setup\.ts/ },
//   {
//     name: 'chromium',
//     use: { storageState: 'tests/.auth/user.json' },
//     dependencies: ['setup'],
//   },
// ]
```

**ページオブジェクトパターン：**

```typescript
// tests/e2e/pages/TodoPage.ts
import type { Page, Locator } from '@playwright/test'

export class TodoPage {
  readonly page: Page
  readonly titleInput: Locator
  readonly addButton: Locator
  readonly todoList: Locator

  constructor(page: Page) {
    this.page = page
    this.titleInput = page.getByLabel('タイトル')
    this.addButton = page.getByRole('button', { name: '追加' })
    this.todoList = page.getByRole('list')
  }

  async goto() {
    await this.page.goto('/todos')
  }

  async addTodo(title: string) {
    await this.titleInput.fill(title)
    await this.addButton.click()
  }

  async getTodoItems() {
    return this.todoList.getByRole('listitem')
  }
}

// 使用例
test('should create todo', async ({ page }) => {
  const todoPage = new TodoPage(page)
  await todoPage.goto()
  await todoPage.addTodo('New Todo')
  
  const items = await todoPage.getTodoItems()
  await expect(items).toHaveCount(1)
})
```

**package.json スクリプト：**

```json
{
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:debug": "playwright test --debug"
  }
}
```

**チェックリスト：**

- [ ] テストは独立して実行可能
- [ ] 認証状態はセットアップで共有
- [ ] ページオブジェクトパターンで再利用性を向上
- [ ] CI では retries を設定
- [ ] スクリーンショットは失敗時のみ

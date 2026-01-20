---
description: PlaywrightでE2Eテストを生成・実行する。テストジャーニー作成、実行、スクショ/動画/トレースの取得、アーティファクトのアップロードを行う。
---

# E2E コマンド

このコマンドは **e2e-runner** エージェントを起動し、PlaywrightでE2Eテストの生成/保守/実行を行います。

## このコマンドが行うこと

1. **テストジャーニー生成** - ユーザーフロー向けPlaywrightテストを作成
2. **E2Eテスト実行** - 複数ブラウザで実行
3. **アーティファクト取得** - 失敗時のスクショ/動画/トレース
4. **結果アップロード** - HTMLレポートとJUnit XML
5. **フレイキー特定** - 不安定テストを隔離

## 使用タイミング

`/e2e` を使うケース:
- 重要なユーザージャーニー（ログイン、取引、支払い）の検証
- 複数ステップのフローがE2Eで動くことの確認
- UI操作やナビゲーションのテスト
- フロントとバックの統合確認
- 本番デプロイ前の検証

## 仕組み

e2e-runner エージェントが:

1. **ユーザーフローを分析**し、テストシナリオを特定
2. **Page Object Model**でPlaywrightテストを生成
3. **複数ブラウザ**（Chrome/Firefox/Safari）で実行
4. **失敗時の証跡**をスクショ/動画/トレースで取得
5. **結果レポート**とアーティファクトを生成
6. **フレイキー検出**と修正提案

## 使用例

```
User: /e2e Test the market search and view flow

Agent (e2e-runner):
# E2E Test Generation: Market Search and View Flow

## Test Scenario Identified

**User Journey:** Market Search → View Results → Click Market → View Details

**Test Coverage:**
1. Navigate to markets page
2. Perform semantic search
3. Verify search results
4. Click on first result
5. Verify market details page loads
6. Verify chart renders

## Generated Test Code

```typescript
// tests/e2e/markets/search-and-view.spec.ts
import { test, expect } from '@playwright/test'
import { MarketsPage } from '../../pages/MarketsPage'
import { MarketDetailsPage } from '../../pages/MarketDetailsPage'

test.describe('Market Search and View Flow', () => {
  test('user can search markets and view details', async ({ page }) => {
    // 1. Navigate to markets page
    const marketsPage = new MarketsPage(page)
    await marketsPage.goto()

    // Verify page loaded
    await expect(page).toHaveTitle(/Markets/)
    await expect(page.locator('h1')).toContainText('Markets')

    // 2. Perform semantic search
    await marketsPage.searchMarkets('election')

    // Wait for API response
    await page.waitForResponse(resp =>
      resp.url().includes('/api/markets/search') && resp.status() === 200
    )

    // 3. Verify search results
    const marketCards = marketsPage.marketCards
    await expect(marketCards.first()).toBeVisible()
    const resultCount = await marketCards.count()
    expect(resultCount).toBeGreaterThan(0)

    // Take screenshot of search results
    await page.screenshot({ path: 'artifacts/search-results.png' })

    // 4. Click on first result
    const firstMarketTitle = await marketCards.first().textContent()
    await marketCards.first().click()

    // 5. Verify market details page loads
    await expect(page).toHaveURL(/\/markets\/[a-z0-9-]+/)

    const detailsPage = new MarketDetailsPage(page)
    await expect(detailsPage.marketName).toBeVisible()
    await expect(detailsPage.marketDescription).toBeVisible()

    // 6. Verify chart renders
    await expect(detailsPage.priceChart).toBeVisible()

    // Verify market name matches
    const detailsTitle = await detailsPage.marketName.textContent()
    expect(detailsTitle?.toLowerCase()).toContain(
      firstMarketTitle?.toLowerCase().substring(0, 20) || ''
    )

    // Take screenshot of market details
    await page.screenshot({ path: 'artifacts/market-details.png' })
  })

  test('search with no results shows empty state', async ({ page }) => {
    const marketsPage = new MarketsPage(page)
    await marketsPage.goto()

    // Search for non-existent market
    await marketsPage.searchMarkets('xyznonexistentmarket123456')

    // Verify empty state
    await expect(page.locator('[data-testid="no-results"]')).toBeVisible()
    await expect(page.locator('[data-testid="no-results"]')).toContainText(
      /no.*results|no.*markets/i
    )

    const marketCount = await marketsPage.marketCards.count()
    expect(marketCount).toBe(0)
  })

  test('can clear search and see all markets again', async ({ page }) => {
    const marketsPage = new MarketsPage(page)
    await marketsPage.goto()

    // Initial market count
    const initialCount = await marketsPage.marketCards.count()

    // Perform search
    await marketsPage.searchMarkets('trump')
    await page.waitForLoadState('networkidle')

    // Verify filtered results
    const filteredCount = await marketsPage.marketCards.count()
    expect(filteredCount).toBeLessThan(initialCount)

    // Clear search
    await marketsPage.searchInput.clear()
    await page.waitForLoadState('networkidle')

    // Verify all markets shown again
    const finalCount = await marketsPage.marketCards.count()
    expect(finalCount).toBe(initialCount)
  })
})
```

## Running Tests

```bash
# Run the generated test
npx playwright test tests/e2e/markets/search-and-view.spec.ts

Running 3 tests using 3 workers

  ✓  [chromium] › search-and-view.spec.ts:5:3 › user can search markets and view details (4.2s)
  ✓  [chromium] › search-and-view.spec.ts:52:3 › search with no results shows empty state (1.8s)
  ✓  [chromium] › search-and-view.spec.ts:67:3 › can clear search and see all markets again (2.9s)

  3 passed (9.1s)

Artifacts generated:
- artifacts/search-results.png
- artifacts/market-details.png
- playwright-report/index.html
```

## Test Report

```
╔══════════════════════════════════════════════════════════════╗
║                    E2E Test Results                          ║
╠══════════════════════════════════════════════════════════════╣
║ Status:     ✅ ALL TESTS PASSED                              ║
║ Total:      3 tests                                          ║
║ Passed:     3 (100%)                                         ║
║ Failed:     0                                                ║
║ Flaky:      0                                                ║
║ Duration:   9.1s                                             ║
╚══════════════════════════════════════════════════════════════╝

Artifacts:
📸 Screenshots: 2 files
📹 Videos: 0 files (only on failure)
🔍 Traces: 0 files (only on failure)
📊 HTML Report: playwright-report/index.html

View report: npx playwright show-report
```

✅ E2E test suite ready for CI/CD integration!
```

## テストアーティファクト

テスト実行時に以下のアーティファクトが取得される:

**全テスト共通:**
- タイムラインと結果を含むHTMLレポート
- CI連携用JUnit XML

**失敗時のみ:**
- 失敗時点のスクリーンショット
- テスト動画
- デバッグ用トレース（ステップ再生）
- ネットワークログ
- コンソールログ

## アーティファクトの閲覧

```bash
# View HTML report in browser
npx playwright show-report

# View specific trace file
npx playwright show-trace artifacts/trace-abc123.zip

# Screenshots are saved in artifacts/ directory
open artifacts/search-results.png
```

## フレイキー検出

テストが断続的に失敗する場合:

```
⚠️  FLAKY TEST DETECTED: tests/e2e/markets/trade.spec.ts

Test passed 7/10 runs (70% pass rate)

Common failure:
"Timeout waiting for element '[data-testid=\"confirm-btn\"]'"

Recommended fixes:
1. Add explicit wait: await page.waitForSelector('[data-testid="confirm-btn"]')
2. Increase timeout: { timeout: 10000 }
3. Check for race conditions in component
4. Verify element is not hidden by animation

Quarantine recommendation: Mark as test.fixme() until fixed
```

## ブラウザ設定

デフォルトで複数ブラウザで実行:
- ✅ Chromium (Desktop Chrome)
- ✅ Firefox (Desktop)
- ✅ WebKit (Desktop Safari)
- ✅ Mobile Chrome (optional)

`playwright.config.ts` で調整可能。

## CI/CD統合

CIパイプラインに追加:

```yaml
# .github/workflows/e2e.yml
- name: Install Playwright
  run: npx playwright install --with-deps

- name: Run E2E tests
  run: npx playwright test

- name: Upload artifacts
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: playwright-report
    path: playwright-report/
```

## PMX固有の重要フロー

PMXでは次のE2Eを優先:

**🔴 CRITICAL (必ず通るべき):**
1. ユーザーがウォレット接続できる
2. ユーザーがマーケットを閲覧できる
3. ユーザーがマーケットを検索できる（セマンティック検索）
4. ユーザーがマーケット詳細を閲覧できる
5. ユーザーが取引できる（テスト資金）
6. マーケットが正しく決済される
7. ユーザーが資金を引き出せる

**🟡 IMPORTANT:**
1. マーケット作成フロー
2. ユーザープロフィール更新
3. リアルタイム価格更新
4. チャート描画
5. マーケットのフィルタ/ソート
6. モバイルのレスポンシブレイアウト

## ベストプラクティス

**DO:**
- ✅ 保守性のためにPage Object Modelを使う
- ✅ data-testidでセレクタを安定化
- ✅ 任意の待機ではなくAPIレスポンスを待つ
- ✅ 重要ユーザージャーニーをE2Eでテスト
- ✅ mainマージ前にテストを実行
- ✅ 失敗時にアーティファクトを確認

**DON'T:**
- ❌ 壊れやすいセレクタ（CSSクラス）を使う
- ❌ 実装詳細をテストする
- ❌ 本番環境でテストしない
- ❌ フレイキーを放置しない
- ❌ 失敗時のアーティファクト確認を省略
- ❌ すべてのエッジケースをE2Eで（ユニットで）

## 重要事項

**PMX向けCRITICAL:**
- 実資金のE2Eテストはテストネット/ステージングのみ
- 本番に対して取引テストは絶対に実行しない
- 金融テストは `test.skip(process.env.NODE_ENV === 'production')` を設定
- テストウォレットは少額のテスト資金のみ使用

## 他コマンドとの連携

- `/plan` で重要ジャーニーを特定
- `/tdd` でユニットテスト（高速・粒度）
- `/e2e` で統合/ユーザージャーニー
- `/code-review` でテスト品質確認

## 関連エージェント

このコマンドは次の `e2e-runner` エージェントを呼び出します:
`~/.claude/agents/e2e-runner.md`

## クイックコマンド

```bash
# Run all E2E tests
npx playwright test

# Run specific test file
npx playwright test tests/e2e/markets/search.spec.ts

# Run in headed mode (see browser)
npx playwright test --headed

# Debug test
npx playwright test --debug

# Generate test code
npx playwright codegen http://localhost:3000

# View report
npx playwright show-report
```

---
name: security-review
description: 認証追加、ユーザー入力の取り扱い、シークレットの扱い、APIエンドポイント作成、決済/機密機能実装時に使用するスキル。包括的なセキュリティチェックリストとパターンを提供。
---

# セキュリティレビュー・スキル

このスキルは、すべてのコードがセキュリティのベストプラクティスに従うことを保証し、潜在的な脆弱性を特定します。

## 有効化のタイミング

- 認証/認可の実装
- ユーザー入力やファイルアップロードの取り扱い
- 新しいAPIエンドポイントの作成
- シークレットや資格情報の取り扱い
- 決済機能の実装
- 機密データの保存/送信
- サードパーティAPIの統合

## セキュリティチェックリスト

### 1. シークレット管理

#### ❌ 絶対にやってはいけない
```typescript
const apiKey = "sk-proj-xxxxx"  // ハードコードされたシークレット
const dbPassword = "password123" // ソース内
```

#### ✅ 常にやること
```typescript
const apiKey = process.env.OPENAI_API_KEY
const dbUrl = process.env.DATABASE_URL

// シークレットの存在確認
if (!apiKey) {
  throw new Error('OPENAI_API_KEY not configured')
}
```

#### 検証ステップ
- [ ] ハードコードされたAPIキー/トークン/パスワードがない
- [ ] すべてのシークレットは環境変数
- [ ] `.env.local` が .gitignore にある
- [ ] git履歴にシークレットがない
- [ ] 本番シークレットはホスティング側（Vercel/Railway）で管理

### 2. 入力検証

#### 常にユーザー入力を検証
```typescript
import { z } from 'zod'

// バリデーションスキーマ
const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().min(0).max(150)
})

// 処理前に検証
export async function createUser(input: unknown) {
  try {
    const validated = CreateUserSchema.parse(input)
    return await db.users.create(validated)
  } catch (error) {
    if (error instanceof z.ZodError) {
      return { success: false, errors: error.errors }
    }
    throw error
  }
}
```

#### ファイルアップロードの検証
```typescript
function validateFileUpload(file: File) {
  // サイズチェック（最大5MB）
  const maxSize = 5 * 1024 * 1024
  if (file.size > maxSize) {
    throw new Error('File too large (max 5MB)')
  }

  // タイプチェック
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif']
  if (!allowedTypes.includes(file.type)) {
    throw new Error('Invalid file type')
  }

  // 拡張子チェック
  const allowedExtensions = ['.jpg', '.jpeg', '.png', '.gif']
  const extension = file.name.toLowerCase().match(/\.[^.]+$/)?.[0]
  if (!extension || !allowedExtensions.includes(extension)) {
    throw new Error('Invalid file extension')
  }

  return true
}
```

#### 検証ステップ
- [ ] すべてのユーザー入力はスキーマで検証
- [ ] ファイルアップロードが制限されている（サイズ/タイプ/拡張子）
- [ ] ユーザー入力をクエリへ直接使用しない
- [ ] ブラックリストではなくホワイトリスト検証
- [ ] エラーメッセージに機密情報が含まれない

### 3. SQLインジェクション防止

#### ❌ SQLを連結しない
```typescript
// 危険 - SQLインジェクション
const query = `SELECT * FROM users WHERE email = '${userEmail}'`
await db.query(query)
```

#### ✅ パラメータ化クエリを使う
```typescript
// 安全 - パラメータ化クエリ
const { data } = await supabase
  .from('users')
  .select('*')
  .eq('email', userEmail)

// または生SQL
await db.query(
  'SELECT * FROM users WHERE email = $1',
  [userEmail]
)
```

#### 検証ステップ
- [ ] すべてのDBクエリがパラメータ化されている
- [ ] SQL文字列連結がない
- [ ] ORM/クエリビルダを正しく使用
- [ ] Supabaseクエリが適切にサニタイズされている

### 4. 認証と認可

#### JWTトークンの取り扱い
```typescript
// ❌ WRONG: localStorage（XSSに弱い）
localStorage.setItem('token', token)

// ✅ CORRECT: httpOnly cookie
res.setHeader('Set-Cookie',
  `token=${token}; HttpOnly; Secure; SameSite=Strict; Max-Age=3600`)
```

#### 認可チェック
```typescript
export async function deleteUser(userId: string, requesterId: string) {
  // 常に先に認可確認
  const requester = await db.users.findUnique({
    where: { id: requesterId }
  })

  if (requester.role !== 'admin') {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 403 }
    )
  }

  // 削除を実行
  await db.users.delete({ where: { id: userId } })
}
```

#### Row Level Security（Supabase）
```sql
-- 全テーブルでRLSを有効化
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- ユーザーは自分のデータのみ閲覧
CREATE POLICY "Users view own data"
  ON users FOR SELECT
  USING (auth.uid() = id);

-- ユーザーは自分のデータのみ更新
CREATE POLICY "Users update own data"
  ON users FOR UPDATE
  USING (auth.uid() = id);
```

#### 検証ステップ
- [ ] トークンはhttpOnly cookieに保存（localStorageは使わない）
- [ ] 機密操作前に認可チェック
- [ ] SupabaseのRLSが有効
- [ ] RBAC（ロール制御）を実装
- [ ] セッション管理が安全

### 5. XSS防止

#### HTMLのサニタイズ
```typescript
import DOMPurify from 'isomorphic-dompurify'

// ユーザー提供HTMLは必ずサニタイズ
function renderUserContent(html: string) {
  const clean = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p'],
    ALLOWED_ATTR: []
  })
  return <div dangerouslySetInnerHTML={{ __html: clean }} />
}
```

#### Content Security Policy
```typescript
// next.config.js
const securityHeaders = [
  {
    key: 'Content-Security-Policy',
    value: `
      default-src 'self';
      script-src 'self' 'unsafe-eval' 'unsafe-inline';
      style-src 'self' 'unsafe-inline';
      img-src 'self' data: https:;
      font-src 'self';
      connect-src 'self' https://api.example.com;
    `.replace(/\s{2,}/g, ' ').trim()
  }
]
```

#### 検証ステップ
- [ ] ユーザーHTMLがサニタイズされている
- [ ] CSPヘッダが設定されている
- [ ] 検証なしの動的コンテンツ描画がない
- [ ] ReactのXSS保護を活用

### 6. CSRF対策

#### CSRFトークン
```typescript
import { csrf } from '@/lib/csrf'

export async function POST(request: Request) {
  const token = request.headers.get('X-CSRF-Token')

  if (!csrf.verify(token)) {
    return NextResponse.json(
      { error: 'Invalid CSRF token' },
      { status: 403 }
    )
  }

  // Process request
}
```

#### SameSite Cookie
```typescript
res.setHeader('Set-Cookie',
  `session=${sessionId}; HttpOnly; Secure; SameSite=Strict`)
```

#### 検証ステップ
- [ ] 状態変更操作にCSRFトークン
- [ ] 全CookieにSameSite=Strict
- [ ] Double-submit cookieパターン

### 7. レート制限

#### APIレート制限
```typescript
import rateLimit from 'express-rate-limit'

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: 'Too many requests'
})

// Apply to routes
app.use('/api/', limiter)
```

#### 高コスト操作
```typescript
// 検索は厳しめに制限
const searchLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 10, // 10 requests per minute
  message: 'Too many search requests'
})

app.use('/api/search', searchLimiter)
```

#### 検証ステップ
- [ ] 全APIにレート制限
- [ ] 高コスト操作は厳しめ
- [ ] IPベース制限
- [ ] ユーザーベース制限（認証済み）

### 8. 機密データ露出

#### ログ
```typescript
// ❌ WRONG: 機密ログ
console.log('User login:', { email, password })
console.log('Payment:', { cardNumber, cvv })

// ✅ CORRECT: マスキング
console.log('User login:', { email, userId })
console.log('Payment:', { last4: card.last4, userId })
```

#### エラーメッセージ
```typescript
// ❌ WRONG: 内部情報露出
catch (error) {
  return NextResponse.json(
    { error: error.message, stack: error.stack },
    { status: 500 }
  )
}

// ✅ CORRECT: 汎用メッセージ
catch (error) {
  console.error('Internal error:', error)
  return NextResponse.json(
    { error: 'An error occurred. Please try again.' },
    { status: 500 }
  )
}
```

#### 検証ステップ
- [ ] パスワード/トークン/シークレットがログにない
- [ ] ユーザー向けエラーは汎用
- [ ] 詳細エラーはサーバーログのみ
- [ ] スタックトレースをユーザーに出さない

### 9. ブロックチェーンセキュリティ（Solana）

#### ウォレット検証
```typescript
import { verify } from '@solana/web3.js'

async function verifyWalletOwnership(
  publicKey: string,
  signature: string,
  message: string
) {
  try {
    const isValid = verify(
      Buffer.from(message),
      Buffer.from(signature, 'base64'),
      Buffer.from(publicKey, 'base64')
    )
    return isValid
  } catch (error) {
    return false
  }
}
```

#### トランザクション検証
```typescript
async function verifyTransaction(transaction: Transaction) {
  // 受取先の確認
  if (transaction.to !== expectedRecipient) {
    throw new Error('Invalid recipient')
  }

  // 金額確認
  if (transaction.amount > maxAmount) {
    throw new Error('Amount exceeds limit')
  }

  // 残高確認
  const balance = await getBalance(transaction.from)
  if (balance < transaction.amount) {
    throw new Error('Insufficient balance')
  }

  return true
}
```

#### 検証ステップ
- [ ] ウォレット署名の検証
- [ ] トランザクション詳細の検証
- [ ] 送金前の残高確認
- [ ] 盲目的な署名をしない

### 10. 依存関係のセキュリティ

#### 定期更新
```bash
# Check for vulnerabilities
npm audit

# Fix automatically fixable issues
npm audit fix

# Update dependencies
npm update

# Check for outdated packages
npm outdated
```

#### ロックファイル
```bash
# 必ずロックファイルをコミット
git add package-lock.json

# CI/CDで再現性あるビルド
npm ci  # Instead of npm install
```

#### 検証ステップ
- [ ] 依存関係が最新
- [ ] 既知脆弱性なし（npm audit clean）
- [ ] ロックファイルがコミット済み
- [ ] GitHubでDependabot有効
- [ ] 定期的なセキュリティ更新

## セキュリティテスト

### 自動セキュリティテスト
```typescript
// 認証テスト
test('requires authentication', async () => {
  const response = await fetch('/api/protected')
  expect(response.status).toBe(401)
})

// 認可テスト
test('requires admin role', async () => {
  const response = await fetch('/api/admin', {
    headers: { Authorization: `Bearer ${userToken}` }
  })
  expect(response.status).toBe(403)
})

// 入力検証
test('rejects invalid input', async () => {
  const response = await fetch('/api/users', {
    method: 'POST',
    body: JSON.stringify({ email: 'not-an-email' })
  })
  expect(response.status).toBe(400)
})

// レート制限
test('enforces rate limits', async () => {
  const requests = Array(101).fill(null).map(() =>
    fetch('/api/endpoint')
  )

  const responses = await Promise.all(requests)
  const tooManyRequests = responses.filter(r => r.status === 429)

  expect(tooManyRequests.length).toBeGreaterThan(0)
})
```

## 本番前セキュリティチェックリスト

本番デプロイ前に必ず:

- [ ] **Secrets**: ハードコードなし、環境変数化
- [ ] **Input Validation**: すべて検証済み
- [ ] **SQL Injection**: すべてパラメータ化
- [ ] **XSS**: ユーザーコンテンツをサニタイズ
- [ ] **CSRF**: 対策有効
- [ ] **Authentication**: トークン取り扱い適切
- [ ] **Authorization**: 役割チェック
- [ ] **Rate Limiting**: 全エンドポイントで有効
- [ ] **HTTPS**: 本番で強制
- [ ] **Security Headers**: CSP, X-Frame-Options
- [ ] **Error Handling**: 機密情報を含まない
- [ ] **Logging**: 機密ログなし
- [ ] **Dependencies**: 更新済みで脆弱性なし
- [ ] **Row Level Security**: Supabaseで有効
- [ ] **CORS**: 適切に設定
- [ ] **File Uploads**: サイズ/タイプ検証
- [ ] **Wallet Signatures**: 検証済み（ブロックチェーン）

## リソース

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Next.js Security](https://nextjs.org/docs/security)
- [Supabase Security](https://supabase.com/docs/guides/auth)
- [Web Security Academy](https://portswigger.net/web-security)

---

**Remember**: セキュリティは必須。1つの脆弱性がプラットフォーム全体を危険にする。迷ったら安全側に倒す。

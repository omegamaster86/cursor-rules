# セキュリティガイドライン

## 必須セキュリティチェック

すべてのコミット前に:
- [ ] ハードコードされたシークレットがない（APIキー、パスワード、トークン）
- [ ] すべてのユーザー入力を検証
- [ ] SQLインジェクション防止（パラメータ化クエリ）
- [ ] XSS防止（サニタイズHTML）
- [ ] CSRF保護を有効化
- [ ] 認証/認可を検証
- [ ] すべてのエンドポイントにレート制限
- [ ] エラーメッセージが機密情報を漏らさない

## シークレット管理

```typescript
// NEVER: Hardcoded secrets
const apiKey = "sk-proj-xxxxx"

// ALWAYS: Environment variables
const apiKey = process.env.OPENAI_API_KEY

if (!apiKey) {
  throw new Error('OPENAI_API_KEY not configured')
}
```

## セキュリティ対応プロトコル

セキュリティ問題を見つけた場合:
1. ただちに停止
2. **security-reviewer** エージェントを使用
3. CRITICALを修正してから続行
4. 露出したシークレットはローテーション
5. 類似問題がないかコードベース全体を確認

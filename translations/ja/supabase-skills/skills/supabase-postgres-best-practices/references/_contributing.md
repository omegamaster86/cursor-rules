# Postgres リファレンス執筆ガイドライン

このドキュメントは、AI エージェントや LLM で使いやすい Postgres ベストプラクティス・リファレンスを作るための指針を示します。

## 主要原則

### 1. 具体的な変換パターン

SQL の書き換えを正確に示してください。理念的な助言は避けます。

**良い例:** "`WHERE id = ANY(ARRAY[...])` を `WHERE id IN (SELECT ...)` の代わりに使う"  
**悪い例:** "良いスキーマを設計する"

### 2. エラー先行の構成

必ず問題のあるパターンを先に示し、その後に解決策を示します。これにより、エージェントがアンチパターンを認識しやすくなります。

```markdown
**Incorrect (sequential queries):** [bad example]

**Correct (batched query):** [good example]
```

### 3. 定量化された効果

具体的な指標を含めます。エージェントが優先順位を判断しやすくなります。

**良い例:** "クエリが 10 倍高速化", "インデックスサイズ 50% 削減", "N+1 を解消"  
**悪い例:** "速くなる", "より良い", "より効率的"

### 4. 自己完結した例

例は完全に実行可能（またはそれに近い）にします。文脈が必要なら `CREATE TABLE` を含めます。

```sql
-- Include table definition when needed for clarity
CREATE TABLE users (
  id bigint PRIMARY KEY,
  email text NOT NULL,
  deleted_at timestamptz
);

-- Now show the index
CREATE INDEX users_active_email_idx ON users(email) WHERE deleted_at IS NULL;
```

### 5. 意味のある命名

意味が伝わるテーブル名・列名を使います。名前そのものが LLM に意図を伝えます。

**良い例:** `users`, `email`, `created_at`, `is_active`  
**悪い例:** `table1`, `col1`, `field`, `flag`

---

## コード例の基準

### SQL フォーマット

```sql
-- Use lowercase keywords, clear formatting
CREATE INDEX CONCURRENTLY users_email_idx
  ON users(email)
  WHERE deleted_at IS NULL;

-- Not cramped or ALL CAPS
CREATE INDEX CONCURRENTLY USERS_EMAIL_IDX ON USERS(EMAIL) WHERE DELETED_AT IS NULL;
```

### コメント

- _何をしているか_ ではなく _なぜそうするか_ を説明する
- 性能への影響を明示する
- よくある落とし穴を示す

### 言語タグ

- `sql` - 標準 SQL クエリ
- `plpgsql` - ストアドプロシージャ/関数
- `typescript` - アプリケーションコード（必要な場合）
- `python` - アプリケーションコード（必要な場合）

---

## アプリケーションコードを含める条件

**基本方針: SQL のみ**

ほとんどのリファレンスは純粋な SQL パターンに集中してください。これにより可搬性が上がります。

**アプリケーションコードを含めるべきケース:**

- 接続プーリング設定
- アプリケーション文脈でのトランザクション管理
- ORM のアンチパターン（Prisma/TypeORM の N+1 など）
- Prepared statement の利用

**混在例のフォーマット:**

````markdown
**Incorrect (N+1 in application):**

```typescript
for (const user of users) {
  const posts = await db.query("SELECT * FROM posts WHERE user_id = $1", [
    user.id,
  ]);
}
```
````

**Correct (batch query):**

```typescript
const posts = await db.query("SELECT * FROM posts WHERE user_id = ANY($1)", [
  userIds,
]);
```

---

## 影響レベルのガイドライン

| Level | Improvement | Use When |
|-------|-------------|----------|
| **CRITICAL** | 10-100x | インデックス不足、接続枯渇、大規模テーブルでの Seq Scan |
| **HIGH** | 5-20x | 不適切なインデックス種別、悪いパーティショニング、カバリングインデックス不足 |
| **MEDIUM-HIGH** | 2-5x | N+1 クエリ、非効率なページネーション、RLS 最適化 |
| **MEDIUM** | 1.5-3x | 冗長インデックス、クエリプラン不安定 |
| **LOW-MEDIUM** | 1.2-2x | VACUUM チューニング、設定微調整 |
| **LOW** | Incremental | 高度なパターン、エッジケース |

---

## リファレンス基準

**一次情報源:**

- Postgres 公式ドキュメント
- Supabase ドキュメント
- Postgres wiki
- 実績ある技術ブログ（2ndQuadrant, Crunchy Data）

**形式:**

```markdown
Reference:
[Postgres Indexes](https://www.postgresql.org/docs/current/indexes.html)
```

---

## レビューチェックリスト

リファレンス提出前に確認:

- [ ] タイトルが明確でアクション指向
- [ ] 影響レベルが性能改善幅と整合している
- [ ] impactDescription に定量表現がある
- [ ] 説明が簡潔（1-2 文）
- [ ] **Incorrect** の SQL 例が最低 1 つある
- [ ] **Correct** の SQL 例が最低 1 つある
- [ ] SQL が意味のある命名を使っている
- [ ] コメントが _何を_ ではなく _なぜ_ を説明している
- [ ] 必要に応じてトレードオフに触れている
- [ ] 参照リンクが含まれている
- [ ] `npm run validate` が成功する
- [ ] `npm run build` が正しい出力を生成する

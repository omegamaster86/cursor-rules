# Postgres Reference の執筆ガイドライン

このドキュメントは、AI エージェント/LLM と相性の良い Postgres ベストプラクティスの reference を作成するためのガイドラインを示します。

## 主要原則

### 1. 具体的な変換パターン

SQL の書き換えを正確に示してください。抽象的・哲学的な助言は避けます。

**Good:** "`WHERE id IN (SELECT ...)` の代わりに `WHERE id = ANY(ARRAY[...])` を使う"  
**Bad:** "良いスキーマ設計をする"

### 2. エラー先行の構成

必ず問題のあるパターンを先に示し、その後に解決策を示します。これにより、エージェントがアンチパターンを認識できるようになります。

```markdown
**Incorrect (sequential queries):** [bad example]

**Correct (batched query):** [good example]
```

### 3. 影響の数値化

具体的なメトリクスを含めます。エージェントが修正優先度を判断しやすくなります。

**Good:** "10x faster queries", "50% smaller index", "Eliminates N+1" 
**Bad:** "Faster", "Better", "More efficient"

### 4. 自己完結した例

例は完結していて実行可能（またはほぼ実行可能）である必要があります。文脈が必要な場合は `CREATE TABLE` を含めます。

```sql
-- 明確にするため、必要に応じてテーブル定義を含める
CREATE TABLE users (
  id bigint PRIMARY KEY,
  email text NOT NULL,
  deleted_at timestamptz
);

-- その後にインデックスを示す
CREATE INDEX users_active_email_idx ON users(email) WHERE deleted_at IS NULL;
```

### 5. 意味のある命名

テーブル/カラム名は意味のあるものを使ってください。名前が LLM に意図を伝えます。

**Good:** `users`, `email`, `created_at`, `is_active`  
**Bad:** `table1`, `col1`, `field`, `flag`

---

## コード例の基準

### SQL フォーマット

```sql
-- 小文字キーワードと明確な整形を使う
CREATE INDEX CONCURRENTLY users_email_idx
  ON users(email)
  WHERE deleted_at IS NULL;

-- 詰め込みや ALL CAPS は避ける
CREATE INDEX CONCURRENTLY USERS_EMAIL_IDX ON USERS(EMAIL) WHERE DELETED_AT IS NULL;
```

### コメント

- _what_ ではなく _why_ を説明する
- パフォーマンスへの影響を強調する
- ありがちな落とし穴を指摘する

### 言語タグ

- `sql` - 標準 SQL クエリ
- `plpgsql` - ストアドプロシージャ/関数
- `typescript` - アプリケーションコード（必要な場合）
- `python` - アプリケーションコード（必要な場合）

---

## アプリケーションコードを含める場面

**デフォルト: SQL のみ**

ほとんどの reference は純粋な SQL パターンに集中すべきです。例の移植性が保たれます。

**アプリケーションコードを含める条件:**

- 接続プーリングの設定
- アプリケーション文脈でのトランザクション管理
- ORM のアンチパターン（Prisma/TypeORM の N+1）
- プリペアドステートメントの利用

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

## 影響度レベルのガイドライン

| Level | Improvement | Use When |
|-------|-------------|----------|
| **CRITICAL** | 10-100x | インデックス不足、接続枯渇、大規模テーブルの順次スキャン |
| **HIGH** | 5-20x | 不適切なインデックス種類、低品質なパーティショニング、カバリングインデックス不足 |
| **MEDIUM-HIGH** | 2-5x | N+1 クエリ、非効率なページング、RLS 最適化 |
| **MEDIUM** | 1.5-3x | 冗長なインデックス、クエリプランの不安定性 |
| **LOW-MEDIUM** | 1.2-2x | VACUUM チューニング、設定の微調整 |
| **LOW** | Incremental | 高度なパターン、エッジケース |

---

## Reference の基準

**一次情報源:**

- 公式 Postgres ドキュメント
- Supabase ドキュメント
- Postgres wiki
- 実績あるブログ（2ndQuadrant、Crunchy Data）

**フォーマット:**

```markdown
Reference:
[Postgres Indexes](https://www.postgresql.org/docs/current/indexes.html)
```

---

## レビューチェックリスト

Reference を提出する前に:

- [ ] タイトルが明確で行動指向
- [ ] 影響度がパフォーマンス改善に一致
- [ ] impactDescription に数値が含まれている
- [ ] 説明が簡潔（1-2 文）
- [ ] **Incorrect** SQL 例が少なくとも 1 つある
- [ ] **Correct** SQL 例が少なくとも 1 つある
- [ ] SQL で意味のある命名を使用
- [ ] コメントが _what_ ではなく _why_ を説明
- [ ] 可能ならトレードオフが記載されている
- [ ] 参考リンクが含まれている
- [ ] `npm run validate` が通る
- [ ] `npm run build` が正しく生成される

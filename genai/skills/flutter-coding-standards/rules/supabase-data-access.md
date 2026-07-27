---
title: Supabase Data Access
impact: CRITICAL
impactDescription: Repository 直呼び + Edge Functions
tags: supabase, data-access, flutter
---

## Supabase Data Access

**標準レイヤー:**

```
Widget → Controller/Provider → Repository → supabase.functions.invoke
```

**Repository は具象クラスでよい**（domain インターフェース / `*_impl` 必須ではない）。

```dart
// features/todos/data/todo_repository.dart
@riverpod
TodoRepository todoRepository(Ref ref) => TodoRepository();

class TodoRepository {
  Future<List<Todo>> fetchTodos() async {
    final response = await SupabaseClientManager.client.functions.invoke(
      'get-todos',
      method: HttpMethod.get,
    );
    _assertSuccess(response);
    // parse JSON → Freezed Todo
  }
}
```

**エラー:** `Either<Failure, T>` / dartz は必須ではない。`AppException` / `EdgeFunctionException` を throw する。

**チェックリスト:**

- [ ] UI から直接 Edge を呼ばない
- [ ] Repository が Edge Function を呼ぶ
- [ ] 例外は core/exceptions.dart の型を使う

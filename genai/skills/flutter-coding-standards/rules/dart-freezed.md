---
title: Freezed Models
impact: HIGH
impactDescription: Freezed によるモデル定義
tags: freezed, dart, flutter
---

## Freezed Models

```dart
// features/todos/data/models/todo.dart
@freezed
class Todo with _$Todo {
  const factory Todo({
    required String id,
    required String title,
    // ...
  }) = _Todo;

  factory Todo.fromJson(Map<String, dynamic> json) => _$TodoFromJson(json);
}
```

- Entity（domain）と `UserModel` + `toEntity()` 分離は **オプション**
- starter 標準は data/models の Freezed のみ
- enum は `core/enums/` + `@JsonEnum` / `@JsonValue` 可

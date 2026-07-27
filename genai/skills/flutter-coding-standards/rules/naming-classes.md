---
title: Class Naming (Coding Standards)
impact: MEDIUM
impactDescription: クラス命名
tags: naming, classes, flutter
---

## Class Naming

| 種類 | 例 |
|------|-----|
| Screen | `LoginScreen` |
| Controller | `LoginController`（AsyncNotifier） |
| Repository | `TodoRepository` |
| Model | `Todo`, `CreateTodoRequest` |

`*Notifier` より `*Controller` を正式パターンとする（starter 準拠）。

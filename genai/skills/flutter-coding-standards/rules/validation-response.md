---
title: Response Validation / Exceptions
impact: HIGH
impactDescription: 例外モデルとレスポンス検証
tags: validation, exceptions, flutter
---

## Response Validation / Exceptions

**例外配置:** `lib/core/exceptions.dart`

- `AppException`
- `EdgeFunctionException`
- `EmailNotVerifiedException` 等

`core/errors/failures.dart` / Either 階層は必須ではない。

レスポンス検証は Repository 内で status と JSON パースを行う（[supabase-edge-function](supabase-edge-function.md)）。

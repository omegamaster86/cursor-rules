---
title: Riverpod Placement
impact: HIGH
impactDescription: Riverpod プロバイダーの配置
tags: riverpod, state, flutter
---

## Riverpod Placement

| 種類 | 配置 |
|------|------|
| 機能横断（Auth 等） | `features/*/providers/` |
| 画面 Controller | `presentation/<flow>/*_controller.dart` |
| Repository | `data/*_repository.dart` 内の `@riverpod` |
| Router | `config/routes/router.dart`（手書き `Provider<GoRouter>` 可） |

`core/providers/` や `presentation/providers/` への強制配置はしない（starter 実態に合わせる）。

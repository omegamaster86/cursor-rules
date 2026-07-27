---
title: Overall Directory Structure
impact: HIGH
impactDescription: プロジェクト全体の見通しと保守性
tags: structure, directories, flutter
---

## Overall Directory Structure

```
frontend/mobile/
├── lib/
│   ├── main.dart
│   ├── app.dart
│   ├── core/
│   │   ├── constants.dart          # AppConstants（env 読み取り）
│   │   ├── exceptions.dart
│   │   ├── supabase_client.dart    # SupabaseClientManager
│   │   ├── enums/
│   │   ├── notifications/
│   │   └── widgets/                # フラットな共通ウィジェット
│   ├── config/
│   │   ├── env/                    # テンプレ等（実行時は AppConstants が正）
│   │   └── routes/
│   │       └── router.dart
│   └── features/
│       ├── auth/
│       ├── todos/
│       └── settings/
├── env.example.json
├── env.local.json                  # gitignore
└── test/
```

Supabase バックエンドはモノレポの `backend/supabase/`（mobile 配下には置かない）。

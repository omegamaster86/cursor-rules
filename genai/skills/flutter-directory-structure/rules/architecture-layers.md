---
title: Architecture Layers
impact: HIGH
impactDescription: 簡略レイヤー構成
tags: architecture, layers, flutter
---

## Architecture Layers

| 層 | 役割 |
|----|------|
| presentation | Screen / Controller / widgets |
| providers | 機能横断状態（Auth 等） |
| data | Repository（Edge Function 呼び出し）+ Freezed models |

フル Clean Architecture（domain / usecase / datasource / Either）は **大規模時オプション**。starter 標準ではない。

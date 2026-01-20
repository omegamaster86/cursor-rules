---
description: 要件を言い換え、リスクを評価し、手順ごとの実装計画を作成する。ユーザーの確認を得るまでコードに触れない。
---

# Plan コマンド

このコマンドは **planner** エージェントを起動し、コードを書く前に包括的な実装計画を作成します。

## このコマンドが行うこと

1. **要件の言い換え** - 何を作る必要があるかを明確化
2. **リスクの特定** - 潜在的な問題やブロッカーを洗い出す
3. **手順の作成** - 実装をフェーズに分解
4. **確認待ち** - 必ずユーザー承認を得てから進行

## 使用タイミング

`/plan` を使うケース:
- 新機能の開始
- 大きなアーキテクチャ変更
- 複雑なリファクタ
- 複数ファイル/コンポーネントに影響
- 要件が不明瞭/曖昧

## 仕組み

planner エージェントが:

1. **依頼内容を分析**し、明確な要件に言い換え
2. **フェーズ分解**し、具体的で実行可能なステップを提示
3. **依存関係**を整理
4. **リスク評価**と潜在ブロッカーの洗い出し
5. **難易度見積り**（High/Medium/Low）
6. **計画提示**後、明確な確認を待つ

## 使用例

```
User: /plan I need to add real-time notifications when markets resolve

Agent (planner):
# Implementation Plan: Real-Time Market Resolution Notifications

## Requirements Restatement
- Send notifications to users when markets they're watching resolve
- Support multiple notification channels (in-app, email, webhook)
- Ensure notifications are delivered reliably
- Include market outcome and user's position result

## Implementation Phases

### Phase 1: Database Schema
- Add notifications table with columns: id, user_id, market_id, type, status, created_at
- Add user_notification_preferences table for channel preferences
- Create indexes on user_id and market_id for performance

### Phase 2: Notification Service
- Create notification service in lib/notifications.ts
- Implement notification queue using BullMQ/Redis
- Add retry logic for failed deliveries
- Create notification templates

### Phase 3: Integration Points
- Hook into market resolution logic (when status changes to "resolved")
- Query all users with positions in market
- Enqueue notifications for each user

### Phase 4: Frontend Components
- Create NotificationBell component in header
- Add NotificationList modal
- Implement real-time updates via Supabase subscriptions
- Add notification preferences page

## Dependencies
- Redis (for queue)
- Email service (SendGrid/Resend)
- Supabase real-time subscriptions

## Risks
- HIGH: Email deliverability (SPF/DKIM required)
- MEDIUM: Performance with 1000+ users per market
- MEDIUM: Notification spam if markets resolve frequently
- LOW: Real-time subscription overhead

## Estimated Complexity: MEDIUM
- Backend: 4-6 hours
- Frontend: 3-4 hours
- Testing: 2-3 hours
- Total: 9-13 hours

**WAITING FOR CONFIRMATION**: Proceed with this plan? (yes/no/modify)
```

## 重要な注意

**CRITICAL**: planner エージェントは、明確に "yes" や "proceed" などの肯定的な回答があるまでコードを書きません。

変更したい場合は以下で回答:
- "modify: [your changes]"
- "different approach: [alternative]"
- "skip phase 2 and do phase 3 first"

## 他コマンドとの連携

計画の後:
- 実装は `/tdd` でTDD方式
- ビルドエラー時は `/build-and-fix`
- 実装完了後に `/code-review`

## 関連エージェント

このコマンドは次の `planner` エージェントを呼び出します:
`~/.claude/agents/planner.md`

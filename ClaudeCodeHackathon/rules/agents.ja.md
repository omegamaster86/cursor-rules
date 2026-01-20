# エージェントオーケストレーション

## 利用可能なエージェント

場所: `~/.claude/agents/`

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| planner | Implementation planning | Complex features, refactoring |
| architect | System design | Architectural decisions |
| tdd-guide | Test-driven development | New features, bug fixes |
| code-reviewer | Code review | After writing code |
| security-reviewer | Security analysis | Before commits |
| build-error-resolver | Fix build errors | When build fails |
| e2e-runner | E2E testing | Critical user flows |
| refactor-cleaner | Dead code cleanup | Code maintenance |
| doc-updater | Documentation | Updating docs |

## 即時に使うべきエージェント

ユーザーへの確認は不要:
1. 複雑な機能要求 - **planner** エージェントを使用
2. コードを書いた/変更した直後 - **code-reviewer** エージェントを使用
3. バグ修正または新機能 - **tdd-guide** エージェントを使用
4. アーキテクチャ判断 - **architect** エージェントを使用

## 並列タスク実行

独立した作業は常に並列実行する:

```markdown
# GOOD: Parallel execution
Launch 3 agents in parallel:
1. Agent 1: Security analysis of auth.ts
2. Agent 2: Performance review of cache system
3. Agent 3: Type checking of utils.ts

# BAD: Sequential when unnecessary
First agent 1, then agent 2, then agent 3
```

## 多角的分析

複雑な問題では役割分担したサブエージェントを使う:
- Factual reviewer
- Senior engineer
- Security expert
- Consistency reviewer
- Redundancy checker

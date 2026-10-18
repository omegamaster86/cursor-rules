---
title: TypeScript boundary patterns
impact: HIGH
impactDescription: 境界での parse と非法状態の排除（pstack typescript-best-practices 相当）
tags: typescript, types, boundary, branded-types
---

## TypeScript boundary patterns

原則は `forge-mode/principles/type-system-discipline.md` と `boundary-discipline.md`。ここは TypeScript の具体例。

### Branded types

プリミティブに brand を付け、境界で一度だけ検証する。下流は型を信頼する。

```typescript
type AgentId = string & { readonly __brand: "AgentId" };

function isAgentId(input: string): input is AgentId {
  return isUUID(input);
}

function parseAgentId(input: string): AgentId {
  if (!isAgentId(input)) throw new Error(`Invalid agent id: ${input}`);
  return input;
}

function focusAgent(id: AgentId): void {
  /* input is trusted */
}
```

`readonly __brand: "X"` の形に合わせる。独自 convention は増やさない。`as AgentId` で黙らせない。

### Discriminated unions

リテラル discriminant で variant を表す。不可能な組み合わせを型に載せない。

```typescript
// Don't. Boolean + optionals lets contradictory states exist.
type DiffState = { loading: boolean; diff?: GitDiff; error?: string };

// Do. Only valid states exist.
type DiffState =
  | { kind: "loading" }
  | { kind: "ready"; diff: GitDiff }
  | { kind: "error"; error: string };
```

discriminant 名（`kind` / `type` / `tag`）は 1 つに固定する。

---
title: Component Design Best Practices
impact: HIGH
impactDescription: コンポーネントの保守性と再利用性
tags: components, design, single-responsibility, refactoring
---

## Component Design Best Practices

コンポーネント設計の原則とベストプラクティスです。

**単一責任の原則：**

1つのコンポーネントは1つの責務のみを持つ。

**Incorrect（責務が多すぎる）:**

```tsx
function RegisterPage() {
  const [formData, setFormData] = useState({})
  const [errors, setErrors] = useState({})
  const [step, setStep] = useState(1)
  
  // 個人情報のバリデーション
  function validatePersonalInfo() { /* ... */ }
  
  // 住所のバリデーション
  function validateAddress() { /* ... */ }
  
  // 支払い情報のバリデーション
  function validatePayment() { /* ... */ }
  
  // 200行以上のJSX...
  return (
    <div>
      {step === 1 && <div>{/* 個人情報フォーム */}</div>}
      {step === 2 && <div>{/* 住所フォーム */}</div>}
      {step === 3 && <div>{/* 支払いフォーム */}</div>}
    </div>
  )
}
```

**Correct（責務ごとに分割）:**

```tsx
// page.tsx
function RegisterPage() {
  return (
    <div>
      <h1>会員登録</h1>
      <RegisterForm />
    </div>
  )
}

// _components/RegisterForm/index.tsx
function RegisterForm() {
  const [step, setStep] = useState(1)
  
  return (
    <div>
      {step === 1 && <PersonalInfoSection onNext={() => setStep(2)} />}
      {step === 2 && <AddressSection onNext={() => setStep(3)} />}
      {step === 3 && <PaymentSection onSubmit={handleSubmit} />}
    </div>
  )
}

// _components/PersonalInfoSection/index.tsx
function PersonalInfoSection({ onNext }: Props) {
  // 個人情報に関するロジックのみ
}
```

**コンポーネントサイズの目安：**

| 状態 | 対応 |
|------|------|
| 100行以下 | ✅ 適切 |
| 100-200行 | ⚠️ 分割を検討 |
| 200行以上 | ❌ 分割が必要 |

**分割の判断基準：**

1. 独立してテストできるか？
2. 別のページで再利用できるか？
3. 責務を一言で説明できるか？
4. プロップが5つ以上ないか？

# セクション

このファイルは、すべてのセクション定義（順序、影響度、説明）を管理します。
セクション ID（括弧内）は、ルールをグルーピングするファイル名プレフィックスです。

---

## 1. コンポーネント設計 (architecture)

**Impact:** HIGH  
**Description:** props の増殖を防ぎ、柔軟なコンポジションを可能にするための基本的なコンポーネント設計パターン。

## 2. 状態管理 (state)

**Impact:** MEDIUM  
**Description:** 合成されたコンポーネント間で、state のリフトアップと共有 context 管理を行うためのパターン。

## 3. 実装パターン (patterns)

**Impact:** MEDIUM  
**Description:** 複合コンポーネントや context provider を実装するための具体的なテクニック。

## 4. React 19 APIs (react19)

**Impact:** MEDIUM  
**Description:** React 19+ 専用。`forwardRef` は使わず、`useContext()` の代わりに `use()` を使う。

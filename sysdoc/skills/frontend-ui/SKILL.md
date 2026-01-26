---
name: frontend-ui
description: Next.js フロントエンドUI向けスキル。`src/app/` と `src/components/` 配下の React コンポーネント、Tailwind、Hooks、UI挙動を編集する場合に使用。
---

## 概要

React/Next.js の UI 実装で、UI/UX、Tailwind、Hooks、コンポーネント分割規約を一貫適用する。

## 必須参照

UI変更前に `references/rules-map.md` を読む。

## UI実装ワークフロー

1. レイアウト/余白/色/フォント変更が含まれないか確認する。
2. Tailwind、Hooks、コンポーネント分割規約を読む。
3. 既存の類似コンポーネントを確認し、重複を避ける。
4. 命名/型の規約に従って実装する。
5. コンポーネント境界と共通UI利用を検証する。

## 品質チェック

- Tailwind の記述をプロジェクトのスタイルに合わせる。
- 不要な新規コンポーネントは作らず、既存を再利用する。
- Hooks の使い方が規約に沿っているか確認する。


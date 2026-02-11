---
name: web-design-guidelines
description: Web Interface Guidelines 準拠の観点で UI コードをレビューします。"review my UI"、"check accessibility"、"audit design"、"review UX"、"check my site against best practices" などの依頼で使用します。
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

# Web Interface Guidelines

Web Interface Guidelines への準拠状況をレビューします。

## 動作手順

1. 下記ソース URL から最新ガイドラインを取得する
2. 指定されたファイルを読む（未指定ならユーザーに対象ファイル/パターンを確認する）
3. 取得したガイドライン内の全ルールに照らしてチェックする
4. 指摘は簡潔な `file:line` 形式で出力する

## ガイドライン取得元

レビューごとに最新ガイドラインを取得します。

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

最新ルールの取得には WebFetch を使用します。取得内容には、全ルールと出力形式の指示が含まれます。

## 使い方

ユーザーがファイルまたはパターンを指定した場合:
1. 上記ソース URL からガイドラインを取得する
2. 指定ファイルを読む
3. 取得した全ルールを適用する
4. ガイドライン指定の形式で指摘を出力する

対象ファイルが指定されていない場合は、レビュー対象をユーザーに確認します。

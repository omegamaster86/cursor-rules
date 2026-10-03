---
name: share
description: "ユーザーが好むデプロイツールで runnable プロトタイプを共有する。"
---

# Share

ユーザーの runnable プロトタイプをデプロイし、他者と共有できるようにする。

## Critical Overrides

- 進行前にプラグインルーター [$index](../index/SKILL.md) を参照する。
- [$critical-overrides](../../references/critical-overrides.md) に従う。

## User Context

開始前に [$user-context](../user-context/SKILL.md) を読み、ローカルシェルが使えるときは preflight スクリプトを実行する。

保存済みプロダクト URL、Figma、スクリーンショット、参照画像、コードベースパス、Storybook、トークン、デザインシステム、ブランドアセット、コンポーネント参照、ブラウザ設定、共有先を、関連するときの接地材料として使う。

保存参照をすべて inspect しない。現在のタスクに必要なものだけ。

## Workflow

1. プロトタイプディレクトリとユーザーが好むデプロイ先を確認する。
2. ユーザーがデプロイ先（Vercel、GitHub Pages、Cloudflare、既存 CI、リポに OpenAI Sites スタックがある場合の Sites）を名指ししたら、それを選択済みホスティング先とする。
3. 未選択なら1問:

> どこにデプロイしますか: Vercel、GitHub Pages、それとも既に使っている別の先？

4. 新規 Product Design プロトタイプで Sites を使う前に、既存プロジェクトを保持する。`npm run build` と `npm run test:sites` を実行する。`mobile-app` なら先に `npm run check:runtime`。`dist/client/index.html`、`dist/server/index.js`、`dist/.openai/hosting.json`、ソースの `.openai/hosting.json` の存在を確認する。検証済みプロジェクトを `sites-hosting` に渡す。`sites-building` を呼ばない。`init-site.sh` を走らせず、Product Design ランタイムを Vinext スタータに置き換えない。
5. 選択ツールが利用可能ならそれを使う。
6. 利用不可なら明言し、別先を使うか聞く。
7. 可能ならデプロイを実行する。自分で完了できるのにセットアップ手順だけ渡さない。
8. 共有可能な URL を返す。
9. ユーザーがまだ手動で必要な不足やフォローアップを述べる。

## Rules

- ユーザーが選ぶまたは確認する前にデプロイしない。
- 動く URL があるまで共有済みと言わない。
- 選択ツールが使えないときは明言し、別先を使うか聞く。

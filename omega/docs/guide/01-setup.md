# セットアップ

正本は `cursor-rules/omega`。各 PJ は symlink で参照します（[omega README](../../README.md) の手順）。

## ローカル Desktop

```bash
chmod +x /path/to/cursor-rules/omega/scripts/omega-link
/path/to/cursor-rules/omega/scripts/omega-link /path/to/your-project
```

Cursor で `/forge-mode` と `/plan-interview` が選べれば OK。

## Cloud Agent

```bash
/path/to/cursor-rules/omega/scripts/omega-cloud-init /path/to/your-project
```

`.cursor/environment.json` と `install-omega.sh` を commit し、環境を Rebuild。

## モデル設定

```text
/setup-forge
```

利用可能な Task モデルを検出し、`forge-models.mdc` にロール別の割当と budget を書きます。手編集も可（`.cursor/rules/forge-models.mdc`）。

## 動作確認レシピ（任意）

アプリをユーザー操作で証明する `verify-<app>` が無い場合:

```text
/create-verification-skill
```

完了ゲートは常に `/verify-done`。

次: [Align と Ship](./02-align-and-forge.md)

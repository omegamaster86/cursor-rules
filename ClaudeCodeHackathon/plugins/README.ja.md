# プラグインとマーケットプレイス

プラグインはClaude Codeに新しいツールや機能を追加します。このガイドはインストールのみを扱います。使用タイミングや理由については[全文記事](https://x.com/affaanmustafa/status/2012378465664745795)を参照してください。

---

## マーケットプレイス

マーケットプレイスはインストール可能なプラグインのリポジトリです。

### マーケットプレイスの追加

```bash
# 公式Anthropicマーケットプレイスを追加
claude plugin marketplace add https://github.com/anthropics/claude-plugins-official

# コミュニティマーケットプレイスを追加
claude plugin marketplace add https://github.com/mixedbread-ai/mgrep
```

### 推奨マーケットプレイス

| Marketplace | Source |
|-------------|--------|
| claude-plugins-official | `anthropics/claude-plugins-official` |
| claude-code-plugins | `anthropics/claude-code` |
| Mixedbread-Grep | `mixedbread-ai/mgrep` |

---

## プラグインのインストール

```bash
# プラグインブラウザを開く
/plugins

# 直接インストール
claude plugin install typescript-lsp@claude-plugins-official
```

### 推奨プラグイン

**開発:**
- `typescript-lsp` - TypeScriptのインテリジェンス
- `pyright-lsp` - Pythonの型チェック
- `hookify` - 会話でフックを作成
- `code-simplifier` - コードのリファクタ

**コード品質:**
- `code-review` - コードレビュー
- `pr-review-toolkit` - PR自動化
- `security-guidance` - セキュリティチェック

**検索:**
- `mgrep` - 高度な検索（ripgrepより優れる）
- `context7` - ライブドキュメント参照

**ワークフロー:**
- `commit-commands` - Gitワークフロー
- `frontend-design` - UIパターン
- `feature-dev` - 機能開発

---

## クイックセットアップ

```bash
# マーケットプレイスを追加
claude plugin marketplace add https://github.com/anthropics/claude-plugins-official
claude plugin marketplace add https://github.com/mixedbread-ai/mgrep

# /plugins を開いて必要なものをインストール
```

---

## プラグインファイルの場所

```
~/.claude/plugins/
|-- cache/                    # ダウンロード済みプラグイン
|-- installed_plugins.json    # インストール済み一覧
|-- known_marketplaces.json   # 追加済みマーケットプレイス
|-- marketplaces/             # マーケットプレイスのデータ
```

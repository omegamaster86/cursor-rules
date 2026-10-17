# Upstream（codex-security × claude-security）

| 正本 | 用途 |
|------|------|
| [openai/plugins — plugins/codex-security](https://github.com/openai/plugins/tree/main/plugins/codex-security) | Codex CLI プラグイン。MCP workbench・`security-scan` スキル |
| [anthropics/claude-plugins-official — plugins/claude-security](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-security) | Claude Code プラグイン。Workflow スキャン・パッチ提案 |
| [anthropics/claude-plugins-official — plugins/security-guidance](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/security-guidance) | Claude Code 常時フック（本 omega スキルとは別。併用可） |
| cursor-rules `openai-plugins/` submodule | Codex プラグインのローカル参照用ミラー |

## omega に含めるもの

- `SKILL.md` — ホスト判定・委譲・Cursor 単体レビュー・統一レポート形式
- `references/checklist.md` — Cursor 単体の横断チェックリスト
- `references/codex-security.md` — Codex 向け委譲手順（抜粋）
- `references/claude-security.md` — Claude Code 向け委譲手順（抜粋）
- `references/report-format.md` — 成果物テンプレ

## omega に含めないもの

- workbench / MCP ランチャー / Workflow 実装本体
- 公式プラグイン SKILL の全文コピー（更新追従が重い）

## 同期メモ

```bash
# submodule 更新（任意）
git submodule update --remote openai-plugins

# 公式 README や SKILL の差分を見て、委譲節・UPSTREAM を手マージ
```

各 PJ では `omega-link` で `.cursor/skills/code-security` にリンクされる（skills ディレクトリ一括リンク）。

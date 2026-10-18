# 上流参照（メンテ用）

omega の `code-security` は Cursor 上で自己完結する。設計の参照元:

| 上流 | パス（cursor-rules ルート） |
|------|---------------------------|
| OpenAI Codex | `openai-plugins/plugins/`（submodule [openai/plugins](https://github.com/openai/plugins)） |
| Anthropic Claude | `claude-plugins-official/plugins/claude-security/`（submodule [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)） |

ジョブ名・panel / investigator の分割は omega 独自。上流を取り込むときは `jobs/` と `references/threat-model.md` を diff し、日本語レポート形式は維持する。

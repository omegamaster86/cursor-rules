# cursor-rules

Cursor 用ルール・スキル・omega の正本リポジトリ。

## Git submodule（上流追従）

| パス | 上流 | omega からの参照 |
|------|------|------------------|
| `supabase-skills/` | [omegamaster86/agent-skills](https://github.com/omegamaster86/agent-skills) | （別用途） |
| `yomiyasu/` | [nanaism/yomiyasu](https://github.com/nanaism/yomiyasu) | 上流全文。Cursor 用は `omega/skills/yomiyasu/` に**抜粋**（`references/UPSTREAM.md`） |

初回 clone 後:

```bash
git submodule update --init --recursive
```

### 上流の更新を確認する

```bash
git submodule foreach 'git fetch origin 2>/dev/null; echo "=== $name ==="; git -C $toplevel/$sm_path log --oneline HEAD..origin/main 2>/dev/null | head -20 || true'
```

`yomiyasu` だけ:

```bash
git -C yomiyasu fetch origin
git -C yomiyasu log --oneline HEAD..origin/main
```

### 上流を取り込む（cursor-rules 側で pin を進める）

全 submodule を `.gitmodules` の `branch` 追従で更新:

```bash
git submodule update --remote --merge
git status   # yomiyasu などの gitlink 変更を確認
git add yomiyasu .gitmodules
git commit -m "chore: bump yomiyasu submodule"
```

`yomiyasu` だけ:

```bash
git submodule update --remote yomiyasu
omega/skills/yomiyasu/scripts/sync-from-upstream.sh
# 必要なら omega/skills/yomiyasu/SKILL.md と references/writing-rules.md を手マージ
git add yomiyasu omega/skills/yomiyasu
git commit -m "chore: bump yomiyasu upstream and sync omega excerpt"
```

特定コミットに pin する場合:

```bash
git -C yomiyasu checkout <sha>
git add yomiyasu
git commit -m "chore: pin yomiyasu at <sha>"
```

### omega 経由でスキルを使う

`omega/scripts/omega-link` は `omega/skills/yomiyasu/` を PJ の `.cursor/skills/yomiyasu` にリンクする。正本を更新したあと、各 PJ で `omega-link` を再実行。

**運用:** yomiyasu は **明示依頼時** の推敲用（Cursor のみの抜粋版）。forge-mode 常時適用や他の日本語校正スキルとの同時有効化は避ける。

`product-design` は **Cursor 専用**（`omega/skills/product-design/`）。Codex CLI のスキルパスには載せない。`omega-link` で各 PJ の `.cursor/skills/product-design` にリンクされる。



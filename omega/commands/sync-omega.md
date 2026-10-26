# omega 正本の差分を取り込む

[omegamaster86/cursor-rules](https://github.com/omegamaster86/cursor-rules) の `main` を pull し、この PJ の `.cursor` を再リンクする。symlink 運用のため **PJ 側の git commit は不要**（`.cursor/` は多くの PJ で gitignore）。

## 手順（エージェント）

1. **PJ ルート**で次を実行する（sandbox で `git pull` が失敗したら `all` 権限で再実行）。

```bash
OMEGA_ROOT="$(dirname "$(readlink .cursor/commands)")"
bash "$OMEGA_ROOT/scripts/omega-sync" .
```

`.cursor/commands` が symlink でない（旧コピー運用）ときは、ユーザーが持つ `cursor-rules` clone へのパスを聞くか、環境変数 `CURSOR_RULES` / `OMEGA` を指定して実行する。

```bash
bash /path/to/cursor-rules/omega/scripts/omega-sync .
```

2. pull 結果を報告する（`Already up to date` でも明記）。取り込めた場合は `git -C "$CURSOR_RULES" log -5 --oneline` を要約する。
3. `omega-sync` 完了後、変更が symlink 経由で見える主要差分（例: `agent-review`、`forge-models`）があれば一言触れる。
4. **コミット・push はユーザーが依頼したときだけ**（PJ および `cursor-rules` 双方）。

## 人間向け（ターミナル）

```bash
chmod +x /path/to/cursor-rules/omega/scripts/omega-sync
/path/to/cursor-rules/omega/scripts/omega-sync /path/to/your-project
```

`omega/scripts/projects.txt` に PJ を書いておけば、全 PJ 一括は `omega/scripts/omega-sync-all` を実行する。

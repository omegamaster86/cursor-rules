# フックシステム

## フック種別

- **PreToolUse**: ツール実行前（検証、パラメータ変更）
- **PostToolUse**: ツール実行後（自動フォーマット、チェック）
- **Stop**: セッション終了時（最終確認）

## 現在のフック（~/.claude/settings.json）

### PreToolUse
- **tmux reminder**: 長時間コマンド（npm, pnpm, yarn, cargoなど）にtmuxを提案
- **git push review**: push前にZedでレビューを開く
- **doc blocker**: 不要な .md/.txt 作成をブロック

### PostToolUse
- **PR creation**: PR URLとGitHub Actionsステータスを記録
- **Prettier**: 編集後にJS/TSを自動フォーマット
- **TypeScript check**: .ts/.tsx編集後にtscを実行
- **console.log warning**: 編集ファイル内のconsole.logを警告

### Stop
- **console.log audit**: セッション終了前に変更ファイルのconsole.logを確認

## Auto-Accept権限

注意して使用:
- 信頼できる明確な計画にのみ有効化
- 探索的作業では無効化
- dangerously-skip-permissionsフラグは絶対に使わない
- `~/.claude.json` の `allowedTools` を設定

## TodoWriteベストプラクティス

TodoWriteツールを使う目的:
- 複数ステップ作業の進捗管理
- 指示理解の検証
- リアルタイムの舵取り
- 粒度の細かい実装ステップ提示

Todoリストから見えること:
- 手順の順番ミス
- 抜け漏れ
- 不要な項目
- 粒度の不適切さ
- 要求の誤解

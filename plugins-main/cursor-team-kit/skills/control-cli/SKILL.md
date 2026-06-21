---
name: control-cli
description: 外部サービスを使わずに、対話型 CLI や TUI を駆動・検査・プロファイルするローカルハーネスを構築・適応する。CLI UX の確認、起動リグレッション、メモリリーク、ハング、プロンプトフロー、端末デモに使用する。
---

# Control CLI

手動で触る代わりに、対話型 CLI を再現性のあるローカルハーネスで検証します。まずリポジトリに既存のテスト/デモハーネスがあれば再利用し、なければ標準のローカルツールで一時ハーネスを作る。

## 利用用途

- 決定的な入力で CLI/TUI の不具合を再現。
- キーボードフロー、プロンプト、割り込み、リサイズ、端末レイアウトの確認。
- バグ修正用に before/after のトランスクリプトを収集。
- 起動時間、遅い処理、ハング、メモリ増加をプロファイル。
- 出力説明より実行結果が伝わりやすい場合、短い端末デモを録画。

## ハーネスループ

1. テスト対象のコマンドと最小再現可能ワークスペースを特定。
2. 既存のローカルハーネスを発見: package scripts、e2e テスト、デモレコーダ、expect スクリプト、PTY 補助。
3. ハーネスがなければ、決定的な環境変数を付与して CLI を分離端末セッションで起動。
4. 操作前に現在の画面を取得。
5. 1 回ごとに 1 つの操作を実行: テキスト、Enter、矢印、Escape、Ctrl-C、リサイズ。
6. 次アクションの前に具体的な画面パターンまたはプロンプトを待つ。
7. トランスクリプトとプロファイル成果物を保存。
8. セッションを適切に終了。

## ハーネス候補

- リポジトリ標準ハーネス: アプリの起動条件・環境・プロンプトを知っているため優先。
- `tmux`: 管理対象セッション、`capture-pane`、`send-keys`、attach/detach。
- PTY プローブ: tmux が使えない場合、短い Python/Node/Expect スクリプトを使用。
- ランタイムインスペクタ: Node または Bun のインスペクタで CPU プロファイル、ヒープスナップショット、ライブ評価を実行。
- 端末録画: リポジトリのデモツールか asciinema 互換ツールを使用（ユーザー指定のデモ時）。

## 最小 tmux ハーネス

```bash
SESSION="cli-harness-$(date +%s)"
tmux new-session -d -s "$SESSION" -- <command-under-test>
tmux capture-pane -pt "$SESSION"
tmux send-keys -t "$SESSION" "help" Enter
tmux capture-pane -pt "$SESSION"
tmux kill-session -t "$SESSION"
```

Node CLI の場合:

```bash
NODE_OPTIONS="--inspect=127.0.0.1:0" tmux new-session -d -s "$SESSION" -- <node-cli-command>
```

端末出力からインスペクタ URL を見つけ、必要なら Chrome DevTools 互換のツールで解析する。

## 最小 PTY ハーネス

リポジトリに tmux もデモハーネスもない場合、決定的待機が必要なときに PTY スクリプトを使う。再利用可能なテストを追加する要件がない限り一時的に留める。

```python
import os
import pty
import select
import subprocess
import time

master_fd, slave_fd = pty.openpty()
proc = subprocess.Popen(
    ["<command>", "<arg>"],
    stdin=slave_fd,
    stdout=slave_fd,
    stderr=slave_fd,
    close_fds=True,
)
os.close(slave_fd)

deadline = time.time() + 30
buffer = b""
while time.time() < deadline:
    ready, _, _ = select.select([master_fd], [], [], 0.25)
    if not ready:
        continue
    chunk = os.read(master_fd, 4096)
    buffer += chunk
    if b"<ready text>" in buffer:
        os.write(master_fd, b"help\n")
        break

print(buffer.decode(errors="replace"))
proc.terminate()
os.close(master_fd)
```

CLI がより高度な端末制御を必要とする場合、`pty.fork()` または既存の PTY ライブラリを使う。

## プロファイル手順

- 起動回帰: 同じマシン、同環境、同じコマンドでベースラインと比較対象の起動時間を取得。
- 遅い処理: CPU プロファイルを開始し、処理を実行、停止して、上位 self-time 関数を比較。
- メモリリーク: 可能なら GC 強制→ヒープスナップショット取得→処理を繰り返し実行→再度 GC 強制→再取得。
- ハング: 画面、アクティブハンドル/リソース、割り込み前のスタック/CPU サンプルを収集。

## ガードレール

- sleep より確定待機を優先。sleep を使う場合は理由を明示。
- 認証情報や破壊的コマンドを制御セッションに送らない。
- リポジトリに既存ハーネスがない場合は `/tmp` に保管。
- パスは他リポジトリのものをハードコードしない。現在のリポジトリの scripts/ランタイムに合わせる。
- 不要になった tmux セッション、作業ディレクトリ、インスペクタ、デモ成果物は、保持要求がない限り削除。

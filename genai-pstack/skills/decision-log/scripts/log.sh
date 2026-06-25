#!/usr/bin/env bash
# decision-log（意思決定ログ）の Markdown ログに整形済みブロックを追記する。
# 使い方: log.sh <logfile> <決定詳細> <決定理由>
# 決定理由は原因・課題・背景を書く（「ユーザーが依頼したため」だけは不可）
set -euo pipefail

if [ "$#" -ne 3 ]; then
	printf 'usage: log.sh <logfile> <決定詳細> <決定理由>\n' >&2
	exit 1
fi

logfile="$1"
decision="$2"
reason="$3"

logdir="$(dirname "$logfile")"
if [ -n "$logdir" ] && [ "$logdir" != "." ] && [ ! -d "$logdir" ]; then
	mkdir -p "$logdir"
fi

if [ ! -f "$logfile" ]; then
	printf '# 決定ログ\n' > "$logfile"
fi

ts="$(date +%Y-%m-%d)"

clean() {
	printf '%s' "$1" | tr '\r' ' '
}

printf '\n## %s\n\n### 決定詳細\n%s\n\n### 決定理由\n%s\n' \
	"$ts" "$(clean "$decision")" "$(clean "$reason")" >> "$logfile"

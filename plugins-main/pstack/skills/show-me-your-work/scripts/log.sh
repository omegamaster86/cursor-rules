#!/usr/bin/env bash
# show-me-your-work の意思決定ログ（TSV）に整形済みの行を追記する。
# 使い方: log.sh <logfile> <phase> <decision> <why> <evidence> <result>
set -euo pipefail

if [ "$#" -ne 6 ]; then
	printf 'usage: log.sh <logfile> <phase> <decision> <why> <evidence> <result>\n' >&2
	exit 1
fi

logfile="$1"
shift

logdir="$(dirname "$logfile")"
if [ -n "$logdir" ] && [ "$logdir" != "." ] && [ ! -d "$logdir" ]; then
	mkdir -p "$logdir"
fi

if [ ! -f "$logfile" ]; then
	printf 'ts\tphase\tdecision\twhy\tevidence\tresult\n' > "$logfile"
fi

ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
# タブ・改行・CR を除去してセルを1行に保ち、スプレッドシートが数式として
# 解釈する先頭文字（=, +, -, @）のセルには先頭にシングルクォートを付ける。
# このスキルはログをスプレッドシートで読むことを想定しているため、
# 攻撃者制御の evidence（PR タイトル、ファイル名、生成テキスト）が
# レビュアーがファイルを開いたときに数式実行にならないようにする。
clean() {
	local v
	v=$(printf '%s' "$1" | tr '\t\n\r' '   ')
	case "$v" in
		=*|+*|-*|@*) printf "'%s" "$v" ;;
		*) printf '%s' "$v" ;;
	esac
}
printf '%s\t%s\t%s\t%s\t%s\t%s\n' \
	"$ts" "$(clean "$1")" "$(clean "$2")" "$(clean "$3")" "$(clean "$4")" "$(clean "$5")" \
	>> "$logfile"

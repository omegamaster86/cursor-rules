---
name: pr-review-canvas
disable-model-invocation: true
description: 対話型の PR レビューウォークスルーを HTML で生成する。gh API で PR データを取得し、コア/機械的変更を分類、レビュワー向け注釈を追加し、移動コード検出付きで差分を描画する。GitHub PR URL を貼り付けてレビュー・ウォークスルー・要約要請、または "review this PR" と要求されたときに使用。
---

# PR Review Canvas

重要点だけをピアレビューのように説明する、GitHub PR の対話型 HTML レビューを生成します。

## ワークフロー

### 1. PR データ取得

以下の `gh api` を並列実行:

```bash
gh api repos/{owner}/{repo}/pulls/{number} --jq '{title, body, user: .user.login, state, additions, deletions, changed_files, base: .base.ref, head: .head.ref}'
gh api repos/{owner}/{repo}/pulls/{number}/files --paginate --jq '.[] | {filename, status, additions, deletions, patch}'
gh api repos/{owner}/{repo}/pulls/{number}/comments --jq '.[] | {user: .user.login, body, path, line}'
```

### 2. PR 分析と body HTML 作成

差分を読み、PR を理解したうえで `<body>` 内容を直接 HTML で記述する。実装形式の自由は高く、レビューの分かりやすさが最優先。

**典型構成**（必要に応じて調整）:
- タイトル、PR 番号、作成者、統計を含むヘッダ
- PR 内容を平易語で説明するサマリボックス
- 注釈付きのコアファイルセクションと差分
- 機械的・定型ファイルをデフォルト折りたたみ
- 下部にレビュー用チェックリスト

**追加してよい要素:**
- 冗長コードの**擬似コード要約**（実際の差分は折りたたむ）。`.bp-section` カードで "Show full implementation" 表示。
- 図（インライン SVG、CDN 経由の mermaid、`<pre>` 中の ASCII アート）
- 前後の制御フローを示すフローチャート
- 挙動の Before/After 比較表
- 警告・質問・落とし穴を示す注意ボックス
- 有用なら対話ウィジェット
- 読解を助ける他の表現

**擬似コード例:**
```html
<div class="file-card">
  <div class="file-hdr" onclick="toggle(this)">
    <span class="fname">retryClient.ts</span>
    <div class="fstats"><span class="pill add">+173</span><span class="pill del">&minus;11</span><span class="chev open">&#9654;</span></div>
  </div>
  <div class="file-body open">
    <div class="file-note">
      <strong>このファイルの要点:</strong>
      <pre style="margin-top:8px;color:var(--text);font-size:12px;line-height:1.6;">
fetch(url):
  if circuit breaker is open → fail fast
  retry up to N times:
    try fetch with timeout
    on success → close circuit breaker, return
    on retryable error → wait (exponential backoff + jitter)
    on non-retryable error → throw
  circuit breaker records failure</pre>
    </div>
    <div class="bp-section" style="margin:0;border:0;border-radius:0;">
      <div class="bp-hdr" onclick="toggleBP(this)">
        <span>実装全体を表示 (+173 lines)</span><span class="chev">&#9654;</span>
      </div>
      <div class="bp-body"><div data-diff="retryClient"></div></div>
    </div>
  </div>
</div>
```

### 3. 利用可能な CSS クラスと JS ユーティリティ

このスキルディレクトリ内の [styles.css](styles.css) と [renderer.js](renderer.js) を参照。ダークテーマの既存 UI をそのまま [template.html](template.html) に注入する。

**利用可能な CSS クラス:**

| Class | Purpose |
|-------|---------|
| `.header`, `.header h1`, `.header-meta` | ページヘッダ |
| `.pill.add`, `.pill.del`, `.pill.files` | 統計バッジ（+N, -N, N files） |
| `.content` | 中央寄せコンテンツラッパ（最大幅 900px） |
| `.summary` | サマリ/TL;DR ボックス |
| `.section-title` | 下線付きセクション見出し |
| `.ic` | インラインコード参照（等幅・ダーク背景） |
| `.file-card`, `.file-hdr`, `.file-body` | 折りたたみ式ファイルカード（`.file-hdr` に `onclick="toggle(this)"`） |
| `.file-note` | ファイルカード内の固定注釈 |
| `.bp-section`, `.bp-hdr`, `.bp-body` | 折りたたみ式ボイラープレートカード（`onclick="toggleBP(this)"`） |
| `.bp-note` | ボイラープレート内の注釈 |
| `.verdict` | レビュー用チェックリスト |

**利用可能な JS 関数:**

| Function | Usage |
|----------|-------|
| `toggle(hdrElement)` | `.file-body` を開閉 |
| `toggleBP(hdrElement)` | `.bp-body` を開閉 |
| `renderDiff(target, diffInput)` | unified diff を描画。`target` は DOM 要素/文字列 ID/CSS セレクタ、`diffInput` は文字列または行配列。自動的に import 行を除外、空白のみ差分は折りたたみ、移動コードを検出（青/紫）。 |
| `esc(string)` | 文字列を HTML エスケープ |

**差分描画**: `data-diff` 属性を使って自動発見します。
`<div data-diff="KEY"></div>` を必要箇所へ追加すると、DOM 読み込み後にレンダラが `<script id="pr-diffs-json" type="application/json">` から補完します（template.html）。

**重要:** パッチ文字列には改行、バックスラッシュ、引用符に加え `</script>` が含まれる可能性があります。`json.dumps(...)` だけでは `<script>` 解析が途中終了する場合があるため、JS/JSON へ生文字列を直接埋めない。以下の安全な手順を使う。

1. 取得時に `jq` でパッチを JSON ファイルへ保存する（正しくエスケープ）。
```bash
gh api repos/{owner}/{repo}/pulls/{number}/files --paginate \
  --jq '[.[] | {key: (.filename | gsub("[^a-zA-Z0-9]"; "_")), value: (.patch // "")} ] | from_entries' \
  > /tmp/pr-patches-{number}.json
```

2. 組み立て時に Python で安全に `template.html` へ注入。
```bash
python3 <<'PY'
import json
from pathlib import Path

patches = json.loads(Path('/tmp/pr-patches-{number}.json').read_text())
html = Path('/tmp/pr-review-{number}-body.html').read_text()
css = Path('styles.css').read_text()
js = Path('renderer.js').read_text()
tmpl = Path('template.html').read_text()

# リテラルの </script> が script タグを早期終了しないようにする。
safe_json = json.dumps(patches).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')

out = (
  tmpl.replace('/* INJECT_CSS */', css)
      .replace('/* INJECT_JS */', js)
      .replace('<!-- INJECT_BODY -->', html)
      .replace('{"__PR_DIFFS_PLACEHOLDER__":true}', safe_json)
)

Path('/tmp/pr-review-{number}.html').write_text(out)
PY
```

これで JSON と HTML が安全な形で埋め込まれる。エージェントは body HTML を一時ファイルに書き出し、Python で最終 HTML を組み立てます。

`data-diff` 属性値は HTML のキーと一致させる。
```html
<div data-diff="path_to_file_ts"></div>
```

`renderer.js` は `<head>` で読み込まれるため、必要ならインライン `<script>` から `renderDiff(target, lines)` を直接呼べます（引数: DOM 要素/ID/CSS 文字列, 文字列または配列）。

**この枠に縛られる必要はありません。** 追加の `<style>` や `<script>`、SVG、図表を自由に追加してください。既製部品は作業時間短縮のためで制約ではありません。

### 4. 組み立てと公開

1. `<body>` 全体を `/tmp/pr-review-{number}-body.html` に書き出す。
2. `jq` 手順で `/tmp/pr-patches-{number}.json` を保存。
3. スタイル/レンダラを読み込む Python 組み立てスクリプトを実行し、最終 HTML を生成。
4. 固定ポートでローカルサーバ起動:
   ```bash
   cd /tmp && python3 -m http.server 8432 --bind 127.0.0.1
   ```
   バックグラウンド化し、`http://127.0.0.1:8432/pr-review-{number}.html` へアクセス。

   **固定ポート・`cd /tmp` を使う理由:** バックグラウンドシェルには TTY がないため Python は起動メッセージをバッファし続ける。ポート 0 は選択された番号を読めない。一方 `--directory /tmp` も使えるが、Python 環境差異に対して `cd /tmp` の方が堅牢。
   ポート 8432 が使用中なら 8433、8434 を試す。

### Diff features（renderer.js 側で自動処理）

- import 行のみをフィルタ
- 空白差分をコンテキストとして折りたたみ
- 3 行以上連続して削除→他箇所に同一追加がある移動コードを検出し、赤緑ではなく青紫で表示
- 追加/削除に小規模な編集がある場合は別の紫系表示

### スタイルノート

- ダークテーマ: `#1a1a1a` 背景、本文 `Inter`、コード `IBM Plex Mono`
- `var(--warning)` をオレンジ、`var(--success)` を緑、`var(--danger)` を赤、`var(--accent)` を青に使用
- スクロール時に固定されるファイルヘッダ（`position: sticky; top: 0`）と注釈（`top: 35px`）
- コアファイルを既定で展開（`.file-body.open`）、機械的ファイルは折りたたみ

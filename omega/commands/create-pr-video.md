# 依頼内容

- 今作業しているブランチのPRを作成します（**本文込みで自動作成**）。
- **検証用の録画またはスクリーンショットを PR 本文に添付**して作成する（`create-pr` の動画版）。
- プッシュ済みなので、リモートの履歴から情報を取得してください。
- 変更履歴や変更コードを確認し、下記のテンプレートを埋めてください。
- **最後に `gh pr create` を実行してPRを作成**してください（対話プロンプトは禁止）。
- PR作成済みの場合は **既存PRのURLを出力**してください（重複PRを作らない）。
- 作成できたら **PRのURLを出力**してください（最終出力に必ず含める）。

## 前提・制約

- 依頼範囲外の実装や、UI/UX（レイアウト、色、フォント、間隔など）の変更はしない。
- `gh` 未ログインの場合は、権限なしで実行してください。
- 「プッシュ済み」が前提。未push（upstream未設定）なら、pushが必要と明示して終了する（勝手にpushしない）。

# テンプレート（この形でPR本文を生成）

---

## やったこと

- このプルリクで何をしたのか？

## やらないこと

- このプルリクでやらないことは何か？（あれば。無いなら「無し」でOK）（やらない場合は、いつやるのかを明記する。）

## 課題

- 悩んでいること
- とくにレビューしてほしいところ

## できるようになること（ユーザ目線）

- 何ができるようになるのか？（あれば。無いなら「無し」でOK）

## できなくなること（ユーザ目線）

- 何ができなくなるのか？（あれば。無いなら「無し」でOK）

## 動作確認

- どのような動作確認を行ったのか？　結果はどうか？

## 本番反映手順

- 本番反映時の手順を記載してください。（.env追記、php artisan migrate、composer installなど）

## その他

- レビュワーへの参考情報（実装上の懸念点や注意点などあれば記載）

## 動作確認の録画・スクリーンショット

- （UI変更がある場合は必須。動画またはスクリーンショットを添付する）
- 録画: `![](pr-artifacts/verification_demo.mp4)` のように本文に参照を書き、`--attach` でアップロードする（下記手順）

---

# 検証用録画・スクリーンショットの作成（PR作成前に行う）

PR本文に載せる検証用メディアは、**PR作成前に**動作確認の最中で用意する。PR作成コマンド実行時点で `pr-artifacts/` にファイルが無い場合は、先に録画・撮影を行ってからPRを作成する。

## 保存場所

リポジトリ直下の `pr-artifacts/` に保存する（**gitにはコミットしない**。`gh pr create --attach` でGitHubにアップロードする）。

```
pr-artifacts/
  verification_demo.mp4      # 動作確認の録画（推奨）
  before_login.png           # スクリーンショット（必要な場合）
  after_login.png
```

ファイル名は `snake_case` で内容が分かる名前にする（例: `verification_profile_upload.mp4`）。

## 録画の作成方法

### UI変更がある場合（推奨: 画面録画）

1. 動作確認用にアプリを起動し、変更箇所の画面を開く
2. **録画開始** → 変更が動くところを実際に操作して見せる → **録画終了**
3. 保存先: `pr-artifacts/verification_<機能名>.mp4`

**Cursor Cloud Agent / computer use 利用時:**

1. `computerUse` サブエージェントでUIを操作し、検証対象の画面を開く
2. `RecordScreen` で `START_RECORDING` → 操作・検証 → `SAVE_RECORDING`（`save_as_filename` で `verification_<機能名>` など）
3. 保存された録画を `pr-artifacts/` にコピーする（Cloud Agent の artifacts ディレクトリから）

**ローカル（Mac）で手動録画する場合:**

- QuickTime Player: ファイル → 新規画面録画
- または `screencapture` / OBS 等で `.mp4` / `.mov` を保存

### UI変更がない場合

- コマンド出力・ログ・テスト結果を「動作確認」セクションにテキストで記載すればよい（録画は不要）

### スクリーンショットのみで十分な場合

- 変更前後の1〜2枚に絞る（冗長な枚数は避ける）

## 録画の内容（良い例 / 悪い例）

**良い録画:**

- 変更した機能が end-to-end で動くところだけ（30秒〜2分程度）
- 操作の結果（成功・表示変化）がはっきり見える

**悪い録画（載せない）:**

- テスト失敗の録画（直してから再録画）
- 環境構築・ログイン待ちなどの長い前置き
- 同じ内容の重複録画

## 技術要件

- `gh` **v2.99.0 以上**（`--attach` フラグが必要）
- 対応形式: 画像（PNG, JPEG, GIF, WebP, SVG）、動画（MP4, MOV, WebM）
- サイズ上限: 画像 10MB、動画は Free 10MB / 有料プラン 100MB（GitHubのWeb UIと同じ）

---

# 実行要件（必ず満たす）

1. 現在ブランチ名を取得: `git branch --show-current`
2. upstream が設定済みか確認: `git rev-parse --abbrev-ref --symbolic-full-name @{u}`
3. `gh` が存在するか確認: `gh --version`（**v2.99.0 以上**であること）
4. `gh` にログイン済みか確認: `gh auth status`
5. 既存PR有無を確認: `gh pr list --head <current-branch> --state all`
6. 検証用メディアの確認: `pr-artifacts/` 内の `.mp4`, `.mov`, `.webm`, `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp` を列挙し、UI変更がある場合は録画またはスクリーンショットが1件以上あること

# PR作成（非対話で完走させる）

以下の方針で **実際にコマンドを実行**してPRを作成すること：

## baseブランチの決め方

- 原則 `develop`
- `origin/develop` が無い場合は `origin` のデフォルトブランチ（`git remote show origin` の `HEAD branch`）を使う

## title

- タイトルは原則「現在ブランチ名」（例: `feature/create/login`）

## body

- 上のテンプレを埋めたMarkdown本文を生成して、それを `gh pr create --body-file -` で stdin から渡す
- 本文は必ず「取得した差分」を根拠に具体的に埋める（例: `git log origin/<base>..HEAD` / `git diff origin/<base>...HEAD`）
- UI変更がある場合、「動作確認の録画・スクリーンショット」セクションにローカルパス参照を書く（`--attach` がアップロードURLに置換する）

### メディアの本文への埋め込み方

**動画**（段落内にこれだけを書く。文中に混ぜるとリンク表示になる）:

```markdown
![](pr-artifacts/verification_demo.mp4)
```

**画像**（altテキスト付き）:

```markdown
![ログイン画面の変更後](pr-artifacts/after_login.png)
```

## attach（検証用メディアの添付）

- `pr-artifacts/` にファイルがある場合、本文で参照しているファイルと同じパスを `--attach` で渡す
- 本文に参照が無いファイルは、本文末尾に自動追記される（参照を書く方が望ましい）
- 複数ファイルは `--attach` を繰り返す
- `pr-artifacts/` が空、またはUI変更がない場合は `--attach` を付けない

## 実行例（この形で実行する）

```bash
# 1) base判定
BASE_BRANCH="develop"
if ! git show-ref --verify --quiet "refs/remotes/origin/${BASE_BRANCH}"; then
  BASE_BRANCH="$(git remote show origin | sed -n 's/.*HEAD branch: //p')"
fi

# 2) 現在ブランチとタイトル
CURRENT_BRANCH="$(git branch --show-current)"
TITLE="${CURRENT_BRANCH}"

# 3) 既存PRがあるならURLを出して終了（重複PRを作らない）
EXISTING_URL="$(gh pr list --head "$CURRENT_BRANCH" --state all --json url --jq '.[0].url' 2>/dev/null || true)"
if [ -n "$EXISTING_URL" ]; then
  echo "$EXISTING_URL"
  exit 0
fi

# 4) 検証用メディアを収集（pr-artifacts/ があれば）
ATTACH_ARGS=()
if [ -d pr-artifacts ]; then
  while IFS= read -r -d '' f; do
    ATTACH_ARGS+=(--attach "$f")
  done < <(find pr-artifacts -maxdepth 1 -type f \( \
    -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' -o \
    -iname '*.gif' -o -iname '*.webp' -o -iname '*.svg' -o \
    -iname '*.mp4' -o -iname '*.mov' -o -iname '*.webm' \
  \) -print0 | sort -z)
fi

# 5) ここであなたがテンプレを埋めた本文を生成して BODY に入れる（例: heredoc）
#    UI変更がある場合は「動作確認の録画・スクリーンショット」に ![](pr-artifacts/xxx.mp4) 等を書く
BODY="$(cat <<'EOF'
（ここにテンプレ本文を出力）
EOF
)"

# 6) PR作成（非対話）。メディアがあれば --attach でGitHubにアップロード
if [ "${#ATTACH_ARGS[@]}" -gt 0 ]; then
  printf "%s" "$BODY" | gh pr create \
    --base "$BASE_BRANCH" \
    --head "$CURRENT_BRANCH" \
    --title "$TITLE" \
    --body-file - \
    "${ATTACH_ARGS[@]}"
else
  printf "%s" "$BODY" | gh pr create \
    --base "$BASE_BRANCH" \
    --head "$CURRENT_BRANCH" \
    --title "$TITLE" \
    --body-file -
fi

# 7) 作成後、PR URL を必ず出力（最終出力に含める）
gh pr view --head "$CURRENT_BRANCH" --json url --jq '.url'
```

## 注意

- `gh pr create` の対話プロンプトが出ないように、必ず `--title` と `--body-file -` を指定すること。
- `gh auth status` がNGなら、権限無しで実行すること。
- `gh` がネットワーク/TLS等で失敗する場合は、実行環境の制約の可能性があるため、**同じコマンドを権限制限なしで再実行して切り分け**すること（勝手な設定変更はしない）。
- `pr-artifacts/` は `.gitignore` に追加すること（動画はリポジトリにコミットしない）。
- UI変更があるのに `pr-artifacts/` が空の場合は、PR作成を中断し、先に検証録画を作成してから再実行すること。
- 既存PRに後からメディアを追加する場合: `gh pr edit <番号> --body-file <file> --attach pr-artifacts/xxx.mp4`

# 依頼内容

- 今作業しているブランチのPRを作成します（**本文込みで自動作成**）。
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

## 画面の画像など

---

# 実行要件（必ず満たす）

1. 現在ブランチ名を取得: `git branch --show-current`
2. upstream が設定済みか確認: `git rev-parse --abbrev-ref --symbolic-full-name @{u}`
3. `gh` が存在するか確認: `gh --version`
4. `gh` にログイン済みか確認: `gh auth status`
5. 既存PR有無を確認: `gh pr list --head <current-branch> --state all`

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

# 4) ここであなたがテンプレを埋めた本文を生成して BODY に入れる（例: heredoc）
BODY="$(cat <<'EOF'
（ここにテンプレ本文を出力）
EOF
)"

# 5) PR作成（非対話）
printf "%s" "$BODY" | gh pr create \
  --base "$BASE_BRANCH" \
  --head "$CURRENT_BRANCH" \
  --title "$TITLE" \
  --body-file -

# 6) 作成後、PR URL を必ず出力（最終出力に含める）
gh pr view --head "$CURRENT_BRANCH" --json url --jq '.url'
```

## 注意

- `gh pr create` の対話プロンプトが出ないように、必ず `--title` と `--body-file -` を指定すること。
- `gh auth status` がNGなら、権限無しで実行すること。
- `gh` がネットワーク/TLS等で失敗する場合は、実行環境の制約の可能性があるため、**同じコマンドを権限制限なしで再実行して切り分け**すること（勝手な設定変更はしない）。


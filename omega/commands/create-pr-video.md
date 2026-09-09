---
name: create-pr-video
model: inherit
description: 検証用録画・スクリーンショットを用意し、gh pr create --attach で PR 本文に埋め込んで PR を作成する。UI 変更の完了ゲート兼 PR 作成コマンド。
---

# PR 作成（検証録画付き）

**動作確認の録画またはスクリーンショットを PR に載せて** PR を作成する。

- 本文の生成・`gh pr create` の実行手順は `現在使用中のルール/.cursor/commands/create-pr.md`（または対象 PJ の `.cursor/commands/create-pr.md`）を正本とする。
- 本コマンドは **検証メディアの作成 → `pr-artifacts/` への保存 → `--attach` でアップロード** の追加要件を定義する。
- **直前に `/verify-done` を PASS してから** 実行する（`commands/verify-done.md`）。UI 変更がある場合、verify-done の proof に録画作成を含めてもよい。

## いつ使う

| 入口 | タイミング |
|------|------------|
| `/create-pr-video` | UI 変更ありで、レビュアーに動作を見せたい PR を開くとき |
| `forge-mode` | `opening-a-pr.md` の代わりに検証録画付き PR が必要なとき |
| `create-pr` の前段 | 録画が無い状態で create-pr が中断されたとき |

UI 変更がない PR は通常の `create-pr` で足りる（録画不要）。

## 実行環境（重要）

- **対象 PJ 内**で完結する。proof は実際に実行・録画する（説明だけで終わらせない）。
- `pr-artifacts/` のメディアは **git にコミットしない**（`.gitignore` に追加）。
- `gh` **v2.99.0 以上**（`--attach` 必須）。`gh auth status` が NG なら権限なしで実行。

---

# 検証用録画・スクリーンショットの作成（PR 作成前）

PR 本文に載せる検証用メディアは、**PR 作成前に**動作確認の最中で用意する。`pr-artifacts/` が空で UI 変更がある場合は、先に録画・撮影してから PR を作成する。

## 保存場所

リポジトリ直下の `pr-artifacts/`:

```
pr-artifacts/
  verification_demo.mp4      # 動作確認の録画（推奨）
  before_login.png           # スクリーンショット（必要な場合）
  after_login.png
```

ファイル名は `snake_case` で内容が分かる名前（例: `verification_profile_upload.mp4`）。

## 録画の作成方法

### UI 変更がある場合（推奨: 画面録画）

1. 動作確認用にアプリを起動し、変更箇所の画面を開く
2. **録画開始** → 変更が動くところを実際に操作 → **録画終了**
3. 保存先: `pr-artifacts/verification_<機能名>.mp4`

**Cursor Cloud Agent / computer use 利用時:**

1. `computerUse` サブエージェントで UI を操作し、検証対象の画面を開く
2. `RecordScreen` で `START_RECORDING` → 操作・検証 → `SAVE_RECORDING`（`save_as_filename` で `verification_<機能名>` など）
3. 保存された録画を `pr-artifacts/` にコピー（Cloud Agent の artifacts ディレクトリから）

**ローカル（Mac）で手動録画する場合:**

- QuickTime Player: ファイル → 新規画面録画
- または `screencapture` / OBS 等で `.mp4` / `.mov` を保存

**PJ に verify スキルがある場合:**

- `.cursor/skills/verify-*/` の Launch / Doctor / Drive で操作し、その最中に録画する（`commands/create-verification-skill.md`）

### UI 変更がない場合

- 「動作確認」セクションにテキスト（コマンド出力・ログ・テスト結果）のみ。録画不要。通常の `create-pr` を使う。

### スクリーンショットのみで十分な場合

- 変更前後の 1〜2 枚に絞る（冗長な枚数は避ける）

## 録画の内容（良い例 / 悪い例）

**良い録画:**

- 変更した機能が end-to-end で動くところだけ（30 秒〜2 分程度）
- 操作の結果（成功・表示変化）がはっきり見える

**悪い録画（載せない）:**

- テスト失敗の録画（直してから再録画）
- 環境構築・ログイン待ちなどの長い前置き
- 同じ内容の重複録画

## 技術要件

- 対応形式: 画像（PNG, JPEG, GIF, WebP, SVG）、動画（MP4, MOV, WebM）
- サイズ上限: 画像 10MB、動画は Free 10MB / 有料プラン 100MB（GitHub Web UI と同じ）

---

# PR 本文への埋め込みと作成

`create-pr.md` のテンプレートを使い、**「動作確認の録画・スクリーンショット」** セクションにローカルパス参照を書く。`--attach` がアップロード URL に置換する。

### メディアの本文への埋め込み方

**動画**（段落内にこれだけを書く。文中に混ぜるとリンク表示になる）:

```markdown
![](pr-artifacts/verification_demo.mp4)
```

**画像**（alt テキスト付き）:

```markdown
![ログイン画面の変更後](pr-artifacts/after_login.png)
```

### attach ルール

- `pr-artifacts/` にファイルがある場合、本文で参照しているファイルと同じパスを `--attach` で渡す
- 本文に参照が無いファイルは本文末尾に自動追記される（参照を書く方が望ましい）
- 複数ファイルは `--attach` を繰り返す

## 実行要件（必ず満たす）

1. `/verify-done` が **PASS**（UI 変更時）
2. `gh --version` が **v2.99.0 以上**
3. `pr-artifacts/` 内のメディアを列挙し、UI 変更がある場合は 1 件以上あること
4. 以降は `create-pr.md` の実行要件（ブランチ、upstream、`gh auth status`、既存 PR 確認）に従う

## 実行例（`gh pr create` 部分）

`create-pr.md` のシェル例に以下が含まれること（要約）:

```bash
# 検証用メディアを収集
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

# PR 作成（メディアがあれば --attach）
if [ "${#ATTACH_ARGS[@]}" -gt 0 ]; then
  printf "%s" "$BODY" | gh pr create \
    --base "$BASE_BRANCH" \
    --head "$CURRENT_BRANCH" \
    --title "$TITLE" \
    --body-file - \
    "${ATTACH_ARGS[@]}"
else
  # UI 変更があるのにここに来たら中断（録画未作成）
  echo "ERROR: pr-artifacts/ is empty but UI changes require verification media." >&2
  exit 1
fi
```

完全な base 判定・既存 PR チェック・本文生成は **`create-pr.md` の実行例をそのまま使う**。

## 注意

- UI 変更があるのに `pr-artifacts/` が空の場合は **PR 作成を中断**し、先に検証録画を作成してから再実行する。
- 既存 PR に後からメディアを追加: `gh pr edit <番号> --body-file <file> --attach pr-artifacts/xxx.mp4`
- 録画はリポジトリにコミットしない（`pr-artifacts/` を `.gitignore` に追加）。

## 関連

- PR 本文テンプレ・完全な `gh pr create` 手順: `現在使用中のルール/.cursor/commands/create-pr.md`
- 完了前検証: `commands/verify-done.md`
- forge-mode PR フロー: `skills/forge-mode/playbooks/opening-a-pr.md`
- ユーザー操作レシピ: `commands/create-verification-skill.md`

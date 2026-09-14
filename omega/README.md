# genai-pstack

genai（Next.js / Supabase ドメイン規約）と pstack（厳密エンジニアリングワークフロー）を統合した Cursor ルールセットの試作版です。

## 構成

```
omega/
├── commands/          # ユーザーが叩く入口
├── skills/            # ドメイン規約 + ワークフロー（フラット配置）
├── agents/            # forge-agent サブエージェント
├── rules/
│   ├── global.mdc           # 通常モード（常時適用）
│   ├── forge-models.mdc              # モデル設定テンプレート（Task runner の正）
│   └── multi-agent-task-enforcement.mdc  # multi-agent の Task 3並列必須
└── scripts/
    ├── omega-link             # PJ へ symlink インストール（ローカル Desktop）
    ├── omega-link-all         # projects.txt の全 PJ を一括リンク
    ├── omega-cloud-init       # Cloud 用テンプレを PJ にコピー
    ├── install-omega-cloud.sh # Cloud VM 上で omega を展開（core）
    └── projects.txt           # リンク対象 PJ の一覧
└── templates/
    └── cloud/.cursor/         # PJ に commit する Cloud 用テンプレ
        ├── environment.json
        └── install-omega.sh
```

## 各 PJ でのセットアップ手順

正本は `cursor-rules/omega` です。**ローカル Desktop** と **Cloud Agent** でインストール方法が異なります。新しい PJ では次の順で進めてください。

### 前提

- `cursor-rules` リポジトリをローカルに clone 済みであること
- 以降 `/path/to/cursor-rules` はその clone 先に読み替える

### Step 0: スクリプトに実行権限を付ける（初回のみ）

```bash
chmod +x /path/to/cursor-rules/omega/scripts/omega-link
chmod +x /path/to/cursor-rules/omega/scripts/omega-link-all
chmod +x /path/to/cursor-rules/omega/scripts/omega-cloud-init
```

### Step 1: ローカル Desktop 用 — `omega-link`

PJ ルートで symlink を張る。**commit 不要**（`.cursor/` が gitignore されていてもよい）。

```bash
/path/to/cursor-rules/omega/scripts/omega-link /path/to/your-project
```

PJ ルートから実行する場合:

```bash
cd /path/to/your-project
/path/to/cursor-rules/omega/scripts/omega-link .
```

**確認:** Cursor Desktop を開き、Customize または `/forge-mode` が使えること。

### Step 2: Cloud Agent 用 — テンプレを PJ に置く

Cloud Agent は repo 外 symlink を読めない。**2 ファイルだけ commit** する。

```bash
/path/to/cursor-rules/omega/scripts/omega-cloud-init /path/to/your-project
```

生成されるファイル:

| ファイル | 役割 |
|----------|------|
| `.cursor/environment.json` | Cloud Build の install フック |
| `.cursor/install-omega.sh` | `cursor-rules` を clone して omega を VM に展開 |

### Step 3: commit & push

```bash
cd /path/to/your-project
git add .cursor/environment.json .cursor/install-omega.sh
git commit -m "chore: add omega Cloud Agent install hook"
git push
```

### Step 4: Cloud Agent 環境を再 Build

1. [Cloud Agents Dashboard](https://cursor.com/agents) または Desktop の Agents Window を開く
2. 対象 PJ の環境を選択
3. **Rebuild**（または初回 Build）を実行

Build 完了後、VM 上に omega の commands / skills / rules / agents がリンクされる。

**確認:** Cloud Agent を起動し、`/forge-mode` や `/verify-done` が slash から選べること。

### Step 5: PJ 固有の設定（任意）

| ファイル | いつ | 内容 |
|----------|------|------|
| `.cursor/rules/forge-models.mdc` | モデル割当を PJ ごとに変えたい | `omega-link` または Cloud install でテンプレがコピーされる。編集して commit 可 |
| `.cursor/skills/verify-<app>/` | 動作確認レシピがある | PJ 固有。omega には含めない。repo に直接置く |

### Step 6: 複数 PJ を一括セットアップ（任意）

`scripts/projects.txt` に PJ パスを1行ずつ書く:

```text
/path/to/project-a
/path/to/project-b
```

ローカル symlink の一括:

```bash
/path/to/cursor-rules/omega/scripts/omega-link-all
```

Cloud テンプレは PJ ごとに `omega-cloud-init` を実行する（一括スクリプトは未提供）。

### セットアップ後の `.cursor/` の形

| パス | ローカル | Cloud | 備考 |
|------|----------|-------|------|
| `.cursor/commands/` | omega への symlink | VM 上で omega へリンク | 共有 |
| `.cursor/agents/` | 同上 | 同上 | 共有 |
| `.cursor/rules/global.mdc` 等 | 同上 | 同上 | 共有 |
| `.cursor/rules/forge-models.mdc` | 初回コピー | 初回コピー | PJ 固有 |
| `.cursor/skills/<共有>/` | omega への symlink | VM 上でリンク | 共有 |
| `.cursor/skills/verify-*/` | PJ 固有 | PJ 固有 | omega 対象外 |
| `.cursor/environment.json` | — | commit 必須 | Cloud のみ |
| `.cursor/install-omega.sh` | — | commit 必須 | Cloud のみ |

### omega 更新時

| 環境 | 操作 |
|------|------|
| ローカル Desktop | 不要（symlink のため即反映）。skill 追加時は `omega-link` を再実行 |
| Cloud Agent | 各 PJ の commit **不要**。次回 Build で `OMEGA_REF`（デフォルト `main`）の最新を取得 |

### Cloud 用環境変数（任意）

Dashboard → Cloud Agents → Secrets に設定するか、`.cursor/environment.json` の Build 環境で渡す。

| 変数 | デフォルト | 用途 |
|------|------------|------|
| `OMEGA_REPO` | `https://github.com/omegamaster86/cursor-rules.git` | omega 正本 repo |
| `OMEGA_REF` | `main` | ブランチ / tag |
| `GITHUB_TOKEN` | （なし） | private repo clone 用 |

---

## インストール（PJ へ symlink）— 詳細

正本は `cursor-rules/omega` です。各 PJ では **コピーせず symlink** で参照します。omega を更新するとリンク済み PJ に即反映されます。

### 1. スクリプトに実行権限を付ける（初回のみ）

```bash
chmod +x /path/to/cursor-rules/omega/scripts/omega-link
chmod +x /path/to/cursor-rules/omega/scripts/omega-link-all
chmod +x /path/to/cursor-rules/omega/scripts/omega-cloud-init
```

### 2. PJ へリンク

```bash
/path/to/cursor-rules/omega/scripts/omega-link /path/to/your-project
```

PJ ルートから実行する場合:

```bash
/path/to/cursor-rules/omega/scripts/omega-link .
```

### 3. 複数 PJ を一括リンク（任意）

`scripts/projects.txt` に PJ パスを1行ずつ書いて:

```bash
/path/to/cursor-rules/omega/scripts/omega-link-all
```

### リンク後の `.cursor/` の形

| パス | 種類 |
|------|------|
| `.cursor/commands/` | omega への symlink |
| `.cursor/agents/` | omega への symlink |
| `.cursor/rules/global.mdc` 等 | omega への symlink |
| `.cursor/rules/forge-models.mdc` | 初回のみコピー（PJ ごとに編集可） |
| `.cursor/skills/<共有 skill>/` | omega への symlink |
| `.cursor/skills/verify-*/` | PJ 固有（リンクしない） |
| omega に無いローカル skill | そのまま残る |

omega に skill を追加したら、既存 PJ で `omega-link` を再実行してください。

## インストール（Cloud Agent）— 詳細

Cloud Agent は Mac の home や repo 外 symlink を読めない。手順の概要は [各 PJ でのセットアップ手順](#各-pj-でのセットアップ手順) を参照。

### 1. PJ に Cloud テンプレを置く

```bash
/path/to/cursor-rules/omega/scripts/omega-cloud-init /path/to/your-project
```

### 2. commit & push

```bash
git add .cursor/environment.json .cursor/install-omega.sh
git commit -m "chore: add omega Cloud Agent install hook"
git push
```

### 3. Cloud Agent 環境を再 Build

Dashboard または Agents Window から環境を再 Build する。

### カスタム

| 変数 | デフォルト | 用途 |
|------|------------|------|
| `OMEGA_REPO` | `https://github.com/omegamaster86/cursor-rules.git` | omega 正本 repo |
| `OMEGA_REF` | `main` | ブランチ / tag |
| `GITHUB_TOKEN` | （なし） | private repo clone 用（Cloud Secrets に設定） |

`forge-models.mdc` は repo に無ければ omega テンプレからコピー。PJ 固有の `verify-*` skill は repo の `.cursor/skills/` に置き、install では触らない。

### 旧 cp 方式から移行する場合

`.cursor/commands` や `.cursor/agents` が **実ディレクトリ**（旧コピー）のままだと symlink がネストする可能性があります。共有分を退避または削除してから `omega-link` を実行してください。`verify-*` と omega に無いローカル skill は残して問題ありません。

## 使い方

| シーン | 使うもの |
|--------|----------|
| 軽い修正・質問 | 通常チャット（`global.mdc` のみ） |
| 本格的な実装・調査 | `/forge-mode`（プロダクト方向が未確定なら先に `/plan-interview`） |
| 計画・用語のすり合わせ | `/plan-interview` |
| ファイル調査 | `/file-brief` |
| 流用チェック | `/reuse-check` |
| リファクタ・削減チェック | `/refactor-check` |
| 完了前検証 | `/verify-done` |
| PJ の動作確認レシピ | `/create-verification-skill`（初回） / `/maintain-verification-skill`（更新） |
| PR レビュー | `/review-orchestrator-triple-hybrid` |
| モデル設定 | `rules/forge-models.mdc` を編集 |

## モードの関係

- **通常モード**: `global.mdc` が適用。タスク分析・実行結果報告フォーマットあり。
- **forge-mode**: `/forge-mode` コマンド起動時、`commands/forge-mode.md` と `skills/forge-mode/`（原則は `skills/forge-mode/principles/`）が `global.mdc` より優先。起動直後に **Intent gate**（Align vs Ship）。`blocked` ならプレイブックに入らず `/plan-interview` へ。原則14本 + プレイブック + 検証重視。完了前検証は **`/verify-done`** が正本。ユーザー操作の証明レシピは **`/create-verification-skill`**。検証・層配線は genai ドメインスキル、リファクタ調査は `/refactor-check` が正本。

コマンド（入口）とスキル（原則・プレイブック本体）はどちらも **forge-mode** という名前で統一しています。

## genai と pstack、mattpocock の統合方針

| 衝突 | 解決 |
|------|------|
| `typescript-best-practices` | 採用せず **`web-coding-standards`** を使用 |
| pstack `interrogate` | 未採用。**`/review-orchestrator-triple-hybrid`** コマンドを使用 |
| `poteto-agent` | **`forge-agent`** にリネーム |
| `cursor-team-kit`（deslop, control-*） | 未導入時は skip、手動 verify で代替 |
| grilling vs never-block | **Intent gate。** Align は `/plan-interview`、Ship は `/forge-mode`。同じターンで両方オンにしない |

詳細は `skills/forge-mode/SKILL.md` の **ルーティング** と **Intent gate** を参照。

## スキル一覧

`skills/README.md` を参照。

## 由来

- `genai/` — Next.js / Supabase コーディング規約
- `plugins-main/pstack/` — poteto のエンジニアリングワークフロー（日本語訳済み）

参考
https://github.com/mattpocock/skills/tree/main/skills 
https://github.com/cursor/plugins/tree/main/pstack 

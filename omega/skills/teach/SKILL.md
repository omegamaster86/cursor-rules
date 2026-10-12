---
name: teach
description: "ワークスペース内でトピックを複数セッションで教える（レッスン・MISSION・リソース）。コードや変更を平易に説明する（内部で how + why）。「これを教えて」「X を理解したい」「この変更を説明して」に使用。"
disable-model-invocation: true
argument-hint: "何について学びたいですか？ / 何を説明しますか？"
---

ユーザーは何かを教わりたい、または理解したい。状態を持つ依頼になりうる（複数セッションの学習）。**説明だけ**の依頼なら末尾の **コード・変更の説明** に従う。

## Teaching Workspace

**`/teach` を実行したディレクトリ** を teaching workspace とみなす。ワークスペース相対パス（`./lessons/` など）はそのディレクトリ基準で解決する。**このスキルフォルダ基準** なのは `*-FORMAT.md` へのリンクだけ。

学習状態はこのディレクトリのファイルに載る：

- `MISSION.md`：学ぶ **理由**。すべての教育判断の根。形式は [MISSION-FORMAT.md](./MISSION-FORMAT.md)。
- `./reference/*.html`：圧縮された参照（チートシート、アルゴリズム、構文、glossary 等）。印刷向きの美しい quick reference。
- `RESOURCES.md`：信頼できる外部リソース一覧。形式は [RESOURCES-FORMAT.md](./RESOURCES-FORMAT.md)。
- `./learning-records/*.md`：学んだことの記録（ADR 相当）。`0001-<dash-case>.md` で連番。形式は [LEARNING-RECORD-FORMAT.md](./LEARNING-RECORD-FORMAT.md)。
- `./lessons/*.html`：**レッスン**（1 ファイル 1 トピック、mission に結びつく HTML）。主要な教育単位。
- `./assets/*`：レッスン間で再利用する **コンポーネント**（[Assets](#assets)）。
- `NOTES.md`：好みや作業メモ。

ワークスペース用の用語集は `GLOSSARY.md`（形式 [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md)）。repo ルートの `GLOSSARY.md`（domain-modeling 正本）とは別物。

## Philosophy

深く学ぶには三つ：

- **Knowledge**（高信頼リソースから）
- **Skills**（あなたが設計するインタラクティブレッスン）
- **Wisdom**（他の学習者・実務者との交流）

`RESOURCES.md` がまだ薄いときは、parametric 知識を信じず高品質リソース探索を優先。トピックにより knowledge 偏重か skills 偏重かは変わる。

### Fluency vs Storage Strength

- **Fluency**：その場の想起
- **Storage**：長期保持（真の目標）

Fluency だけだと錯覚的な mastery。desirable difficulty（retrieval practice、spacing、skills 練習向けの interleaving）を設計する。

## Lessons

`./lessons/0001-<dash-case>.html`（連番）。短く、すぐ終わる。working memory 内。mission と ZPD に直結した **1 つの具体的成功**。

美しい typography（Tufte 的）。可能なら CLI でレッスンを開く。HTML anchor で他レッスン・参照へリンク。各レッスンに primary source（読む／見る）を推奨。不明点は agent に follow-up を促す文言を入れる。

## Assets

`./assets/` に stylesheet、quiz、simulator 等。**再利用がデフォルト**。新規は component として `assets/` に置き、インライン複製はしない。共有 stylesheet は最初に作り、コースとして見えるようにする。

## Mission

レッスンは mission に結ぶ。`MISSION.md` が空なら、まず **なぜ学ぶか** を質問。mission が変わったら `MISSION.md` と learning record を更新し、ユーザー確認を取る。

## Zone Of Proximal Development

常に「ちょうど良い」難易度。指定がなければ learning-records と mission から次を選ぶ。

## Knowledge / Skills

レッスンは **1 スキル** 中心。知識はそのスキルに必要な分だけ。外部 citation を厚く。知識獲得では difficulty は敵。

スキル獲得では difficulty は道具。quiz・軽い in-browser タスク・実世界ステップ（ヨガポーズ等）。**feedback loop** を最短に。

**Quiz**：各選択肢は可能なら **同じ語数（できれば文字数も）**。正解位置を問ごとに変える。書式や順序で答えにヒントを出さない。

## Wisdom

実世界での試行が wisdom。forum / subreddit / クラス等の **community** を探す。参加を望まないなら尊重。

## Reference Documents

`./reference/` に圧縮 essence。レッスンよりここが後から読まれる。glossary は特に重要。作ったら全レッスンで用語を守る。

## `NOTES.md`

教え方の好みを記録。

## コード・変更の説明（omega / pstack）

**サブシステムや diff を理解させる** 依頼は、上のワークスペースではなくこの節。**何かを変えることではなく理解** が目的。

`how` と `why` の上に位置する。全体像を掴んだら `how` で動き、`why` で理由（実スキル起動）。1 本の平易な説明に溶かし、相手に重要なところから入り、聞かれたら深掘り。`why` の confidence 表現はそのまま。

1. 持ち帰り要点を少数決める（変更前・レビュー・デバッグ・初見と既知から。クイズしない）。
2. `how` / `why` に任せ、二重にやらない。並列可。`why` はデフォルト狭く。
3. 平易な定義 → 手前の事例 → 動き・理由・エッジ。枠ラベル（TL;DR 等）は出さない。最小の完結答えを先に。
4. 会話調。クイズ・Pause 演出・言い返し要求なし。
5. 見せる。3 以上の動く部分は図を段階的に積む（mermaid / 画像生成の使い分けは既存 omega 規律どおり）。

**unslop** スキルがあれば通す。

**Reply:** 説明そのもの。報告ではない。

## 上流

ワークスペース教學の正本: [mattpocock/skills — productivity/teach](https://github.com/mattpocock/skills/tree/main/skills/productivity/teach)。`references/UPSTREAM.md`。コード説明節は pstack 由来を omega で維持。

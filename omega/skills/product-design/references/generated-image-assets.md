# Product Design 生成画像の保存先

Image Gen / `GenerateImage` で作ったラスタ（ideate の3案、image-to-code の個別アセットなど）は、**作業ワークスペース（該当 PJ）ルート**の次に置く。

```text
<workspace-root>/.cursor/assets/
```

## ルール

- 初回保存前に `mkdir -p .cursor/assets` する。
- 生成ツールの一時パスやチャット添付だけに留めない。必ず `.cursor/assets/` にコピーまたは移動する。
- プロトタイプをサブフォルダに bootstrap しても、生成ラスタは **ワークスペースルート** の `.cursor/assets/` に置く。プロトタイプフォルダ直下の `assets/` やスキル正本ディレクトリには書き込まない。
- テンプレの `public/assets/`（モバイルデバイス chrome 等の保護ランタイム）は別物。上書き・混同しない。

## ファイル名

| 用途 | 例 |
| --- | --- |
| ideate オプション | `ideate-option-<表示順>-<slug>.png` |
| 実装用アセット | `<slug>.png`（コンポーネント／用途が分かる slug） |

## コードから参照

`src/` から import する。プロトタイプがワークスペース直下にあるとき:

```js
import hero from "../.cursor/assets/hero-background.png";
```

プロトタイプがサブディレクトリ（例 `prototypes/demo/`）のときは、ワークスペースルートへの相対パスで import する（例 `../../../.cursor/assets/hero-background.png`）。

Vite が親ディレクトリのファイルを拒否したら、当該プロトタイプの `vite.config` にワークスペースルートを `server.fs.allow` に足す。ビルドに含めるため import パスは実ファイルを指す。

## user-context の assets との違い

| パス | 用途 |
| --- | --- |
| `.cursor/assets/` | 本セッションの Image Gen 出力（ideate / 実装アセット） |
| `.cursor/product-design/assets/` または `~/.cursor/product-design/assets/` | user-context に保存する参照スクショ・ブランド素材 |

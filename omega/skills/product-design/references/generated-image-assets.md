# Product Design 生成画像の保存先

**product-design スキル（全サブスキル）で Image Gen / `GenerateImage` 等により生成したラスタは、例外なくすべて** 作業ワークスペース（該当 PJ）ルートの次に置く（ideate の案・リミックス、image-to-code の個別アセット、url-to-code の ImageGen 置換など）。

```text
<workspace-root>/.cursor/assets/
```

## ルール

- 初回保存前にシェルで `mkdir -p .cursor/assets` し、ディレクトリが無ければ必ず作成する。
- `GenerateImage` 等が一時パスだけ返す場合も、保存直後に `.cursor/assets/<slug>.png` へコピーまたは移動する。
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


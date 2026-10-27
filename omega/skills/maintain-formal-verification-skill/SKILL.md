---
name: maintain-formal-verification-skill
description: "コード変更後、形式的検証を再びコードと一致させる。/maintain-formal-verification-skill、モデルはまだ正しいか、merge/refactor 後。"
disable-model-invocation: true
---

# Maintain a formal verification skill

形式的チェックは、描写しているものの性質を証明する。コードだけ変わり検証が変わらないと、存在しないコードを描写しながら pass し続けることがある。その pass は証明に見えて危険。このスキルは `/create-formal-verification-skill` が生成した verify スキル、または named コードに対するモデルチェッカ・証明・コード検証を走らせる project-local スキルの**保守ループ**。project-local スキルはエージェントがスキル使用中にした変更を扱う。本スキルはスキルを通さなかった変更：merge、スキル無し編集、複数 commit の drift。

## 結果

各チェックに 1 つの outcome を付け、どれかを述べる：

- **in sync**: 最後の sync 以降、描写を変える変更が無く、チェックは pass。
- **updated**: コードが変わり、検証が新コードを描写し、チェックは pass。
- **bug**: 検証は現コードを描写し、コードが性質を破る。コードに関する発見であり drift ではない。
- **blocked**: 一致に戻せない、または走らせられない。理由を exact に。

updated と bug は両立しうる：更新で再びコードを描写したあと、性質が失敗する。

## 編集範囲

検証だけ編集：モデル、harness、property ファイル、verify スキル本体。ユーザーが求めない限りプロダクトコードは編集しない。現コードで性質が失敗したら、通るまで性質やモデルを弱めない。失敗を報告する。

## 手順

1. **チェックを見つける。** verify スキルは固定名が無い。named コードに対してモデルチェッカ・証明・検証器を走らせる project スキルを探す。ユーザーが名指したものまたは見つけた各件について、性質、カバー、境界・仮定、実行コマンド、描写を最後に確認した commit を読む。無ければ `/create-formal-verification-skill` を指して止める。sync commit が無ければ検証ファイルの最後の変更 commit を使い、そうしたと述べる。

2. **そのまま 1 回走らせる。** 何も変える前に各チェックを 1 回。pass はコードが正しいとは言わない。古い描写がまだ成り立つと言う。失敗は drift か bug。step 5 まで決めない。

3. **カバーされたコードの全変更を読む。** sync commit から現 commit までカバー file を diff し、各 commit message を読む。rename・分割・移動もカバー。ガードする state に触れる新コードも見る。各変更は次のどれか：
   - **No effect.** 描写に影響しない（format、コメント、検証がカバーしない経路）。commit message ではなくモデル/harness で確認。
   - **描写がコードとずれた。** 1 ステップが 2 つになった、分岐の増減、チェックの移動、ガード state への新経路、値域の変化。モデル/harness を変える。
   - **約束が意図的に変わった。** doc、テスト、changelog、message などの evidence がある。性質を変え、evidence を引用。
   - **約束が壊れた可能性。** evidence 無しのコード変更。続く失敗は bug 候補。

4. **結果ではなくコードから更新。** 変更部分が再び開けるコードを指し、コードの 1 ステップは検証の 1 ステップ。rerun 前にコードから書き、pass する形に合わせない。意図的な約束変更だけ性質を変える。旧・新 wording と evidence を書く。境界は変化が境界を誤らせるときだけ縮め、縮めたら報告に書く。

5. **rerun と判定。**
   - **Pass:** 新コードで性質の守り方を壊し（チェック削除、順序入れ替えなど）、チェックが捕まえることを確認してから壊しを戻す。
   - **Fail:** 反例を実コードに 1 ステップずつ replay。起きないステップなら検証が誤り。直し何が誤りだったか述べる。すべて起きうるなら bug。導入 commit、コードの言葉での手順列、害を 1 文。安い再現があれば報告に添える（プロダクトには commit しない）。

6. **verify スキルを更新。** カバー、コマンド、境界、仮定、sync commit。確認した commit を sync に。blocked は sync を動かさず報告に書く。次のエージェントと同様に verify スキルを 1 回たどり、手順がまだ走ることを確認。

## 報告

各チェックについてユーザーに：

- outcome と読んだ commit；
- 検証で何をなぜ変えたか（形の変化か意図的な約束変更か、evidence 付き）；
- rerun 結果と、更新後も失敗できることを示した break；
- 各 bug を平易語（手順列、害、導入 commit）；
- まだカバーしないもの（カバーすべき新コードを含む）。

検証の drift とコードの bug を明示。更新前 pass・更新後 fail なら、古い pass は stale 描写だったと述べる。

検証の更新はプロダクト修正とは別 changeset にする。

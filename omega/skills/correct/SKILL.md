---
name: correct
description: "この repo でエージェントが繰り返すミスを見つけ、再発不能にする。architecture → 型 → lint → テスト → ドキュメントの順。各チェックが過去の実ミスで失敗することを証明。オペレーターが直したら都度実行。/correct に使用。"
disable-model-invocation: true
---

# Correct

オペレーターがこの repo でエージェントに同じ修正を繰り返しさせている。次のエージェントが同じミスをできない形に repo を変える。

contributor はすべて、開いたファイルだけ見て、最寄りの例をコピーし、コンパイルが通る最短経路を取るエージェントと仮定する。1 ファイルから正しく見える変更が repo 全体で正しいように設計する。

## ミスクラスを見つける

最近の commit、revert、レビューコメント、`.cursor/rules/`・`AGENTS.md`・スキル内の workaround 説明を読む。ミスをクラスにまとめる。同じクラスが 2 回起きたらカウントする。

## 各クラスを効く最高レベルで直す

1. **architecture で消す。** 状態に 1 owner、タスクに 1 つの supported なやり方。internals を隠し、誤 import を失敗させる。手同期リストを単一の source of truth に。エージェントがコピーする旧経路と dead code を削除。
2. **型で bad state を書けなくする。** まだコンパイルするなら、lint または CI で「代わりに使う file / type / function」を error に書く。パターンが既に広いなら、増やした変更だけ fail。
3. **振る舞いをテストする。** import 先がすべて undefined でも通るテストは直すか削除。
4. **ドキュメントと agent 規則は最後。** 判断が要るものだけ。スキップしても fail しないもの。

## 直して証明する

いま最頻のクラスを 1 commit ずつ直す。各新チェックが過去の実ミスで fail することを証明する。同じコマンドを local と CI で走らせる。例外は offending 行に reason・expiry・人の承認。

## ルール表を維持する

`.cursor/rules/` またはプロジェクトの agent 指示ファイルに、**ルール ↔ 強制手段** の表を残す。オペレーターが直したらミスを直しルールを足す。ルールがあるが何も強制していないなら repeat なので、同じ変更で最高レベルを直す。ミスが起きなくなったらルールを落とす。

**Reply:** 各クラスと evidence、選んだレベル、より高いレベルが効かなかった理由。

# Design red flags

synthesis 前にすべての candidate をスクリーンする。red flag は形状を見直す・拒否する理由。

## Shallow module

shallow module は複雑さをほとんど隠さず大きな interface を露出する。depth は public surface のサイズに対してその背後に隠れた capability と policy で判断する。実質的な振る舞いに支えられた単純な interface を選ぶ。

deep module と deep call chain を混同しない。deep call chain は理解をレイヤに散らす。deep module は 1 interface の背後に capability を集中させる。

次の兆候を探す:

- caller が 1 操作完了のために複数 method を調整する。
- public option が内部 stage や実装選択を露出する。
- interface を学んでも caller を実装の学習から救わない。

## Information leakage

information leakage は複数 module が同じ内部決定に依存する状態にする。表現・policy・protocol 詳細が複数箇所に現れ、変更に coordinated edit が要る。

transport や wire 型の public re-export は leakage。interface の背後で外部データを domain 型に parse する。storage schema、framework オブジェクト、protocol 詳細は private に。

## Temporal decomposition

temporal decomposition は所有する知識ではなく実行順で module を組む。load・validate・transform・save を分けると、同じ表現と invariant が複数境界で繰り返されることが多い。

domain 知識と ownership でコードをまとめる。異なる時刻で走る method でも同じ決定を守るなら 1 module に属せる。

## Pass-through method

pass-through method は同じ形状の別 method に同じ引数をそのまま forward する。複雑さを隠さずレイヤを足すだけ。

除去するか、操作を完了できる module に責務を移す。forward 境界は policy・adaptation・明確な abstraction を足すときだけ残す。

## Split ownership

複数 module が同じ state を書く、または各自コピーを持つ。1 writer を編集するエージェントは他が見えず、ルールが乖離する。

各 state に 1 owner。他 module は読むか owner に変更を依頼する。

## Two ways to do one task

設計が同じタスクを複数のやり方で支える。エージェントは最初に見つけた方をコピーし、すべての経路に caller が増える。

1 通りだけ残す。他から caller を移し、同じ変更で削除する。

## Importable internals

caller が module の internals を import できる。エージェントはコンパイルが通る最短経路を取り、直接 import して interface の一部にする。

module 外から internals に到達不能にし、外からの import で build を fail させる。

## Hand-synced list

2 箇所以上が同じ項目をリストし、項目追加はすべてのリスト編集を意味する。1 リストだけ見たエージェントはそこだけ更新する。

1 リストを正とし他を derive する。derive できないなら、リスト不一致で build を fail させる。

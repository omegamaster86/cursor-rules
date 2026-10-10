---
name: blast-radius
description: "ship 前に変更が別所で壊す可能性を diff 以外から見つけ、安全だと言う根拠の 1 事実を実コード実行で証明する（書き上げだけはしない）。'blast radius of X'、'what could this break'、信頼できない小 diff のレビュー向け。"
disable-model-invocation: true
---

# Blast radius

ship 前に変更が別所で何を壊すかを見つける。「blast radius of X」「what could this break」、まだ信頼できない小 diff のレビュー向け。

`how` と `why` の companion。`how` はコードの動き、`why` はその形状の理由。blast radius は別所での破壊。

caller 列挙が仕事ではない。エージェントは grep で秒で取れる。grep が示さない破壊が仕事。

## Don't trust your own writeup

正しく聞こえる blast-radius writeup は無価値。真偽に関わらず説得力がある。writeup を返さない。全体が依存する 1〜2 事実を見つけ、コード実行で証明する。

### How sure are you

変更の安全が依存する各事実を、安いところまでこのリストを下げ、どこで止まったか言う。

1. そう言っただけ。単体では無価値。
2. 行を指した。実 `file:line`、またはライブラリ自身の source。
3. bad case が起きないことを示した。失敗を step by step 辿り到達しない。
4. 走らせた。実コードを呼ぶ script または test で、誤りなら loud に fail。
5. 動いている app で再現した。

Step 4 は通常、app が ship する同じ library を import し、心配な関数を呼ぶ小さな script 1 つ。

## Steps

1. 変更を読む。diff、追加・変更・削除した symbol、diff が書かない部分も含めて何が違うか。PR と commit を引くには `why` step 2。
2. 安全だと言う 1 事実を見つける。risky に見える変更の多くは 1 事実で安全、例:「この呼び出しは既に dead の cache entry を落とすだけで他はしない」。それが成り立てば risky case の多くは一気に clear。長い maybe リストではなくここに時間を使う。
3. grep が止まる所を見る。呼ぶ library の source を読み、pin 版と local patch を確認。いつ走るか: microtask、unmount と teardown、Solid vs React。symbol search が逃すものを辿る: API が返す JSON、DB column、wire format、同じ bytes を読む別言語、feature flag、3 hop 下の code。
4. 各 risk を正直に。起きる実 chance と起きたらの実 cost。確認した risk だけ残す。調べて clear したものは別列。`why` と同じルール。実 `file:line`、何も見つからない search も答え。caller や API を捏造しない。
5. 1 事実を証明。実コードを走らせる script または test を書き、実行し、起きたことを貼る。
6. 大きく広い変更なら `multi-agent-candidates` で走らせる。複数モデルに同じ問いをし答えを merge。モデルごとに違う real bug を捕まえる。

## What to hand back

- **What it does.** 何が変わったか、自明でない部分も含む。
- **The one fact it's safe because of.** 述べ、どの step まで行ったか、証明を示す。証明できなければ unproven と書く。
- **Risks.** 各々がどう壊すか、`file:line`、likelihood と severity、確認方法。重要なものは証明を貼る。
- **Cleared.** 何を調べ、なぜ問題ないか。
- **Before you merge.** real bug を捕まえる最安の test または repro。書いた script を含む。

`unslop` で書き、実コードを引用し、public に出す前に private を strip。

**Reply:** 上の writeup。1 つの安全 fact は proven または unproven 明示。

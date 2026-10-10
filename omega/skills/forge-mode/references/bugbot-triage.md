# Bugbot triage

Babysit プレイブック（`../playbooks/babysit.md`）が Bugbot またはレビュー自動化コメントを扱うときの参照。

Bugbot やレビュー自動化コメントを Babysit が扱うときは本参照を使う。目的は Bugbot をデフォルトで無視することではない。すべてのコメントを必須のコード変更とみなすのをやめること。

## 判断ルーブリック

動く前に Bugbot の各スレッドを分類する。

- `fix`: コメントが、妥当な正しさ・セキュリティ・プライバシー・データ損失・認可・課金・マイグレーション・冪等性・レース・リリース済み挙動の問題を指している。所有 PR の最下層で直し、commit SHA で返信してスレッドを resolve する。
- `dismiss`: コメントが文書化済みの低リスクなノイズパターンに一致し、現コード／文脈で変更不要と証明できる。短い理由で返信して resolve する。
- `ask`: コメントが新規、高 severity、セキュリティ／プライバシー／データ関連、または曖昧。推測せずユーザーに聞く。

迷ったら `ask`。ノイズなコード品質コメントを飛ばすコストは小さい。本物のデータ／セキュリティバグを飛ばすコストは大きい。

## 学習パターンの書式

将来のパターンは次の形で追記する。

```markdown
### <短いパターン名>

- Confidence: candidate | recurring | strong
- Skip when: <満たすべき条件>
- Do not skip when: <リスク境界>
- Example signal: <パターンを示す文言やコード文脈>
- Source: <PR/コメント URL または短い履歴メモ>
```

`candidate` は 1〜2 例。実 dismiss が複数回なら `recurring`。パターンが狭く繰り返し検証済みで低リスクのときだけ `strong`。

## 繰り返し skip 候補

### 意図的な UI またはデザインシステムのビジュアル変更

- Confidence: candidate
- Skip when: PR 説明・スクリーンショット・デザインレビュー・近傍コードでビジュアル変更が明示され、Bugbot コメントが共有ビジュアルデフォルトの変更を言い直しているだけ。
- Do not skip when: アクセシビリティ、フォーカス可視性、キーボード操作、コントラスト、PR が意図していないコンポーネント API 契約を指している。
- Example signal: フォーカス枠、ボタンサイズ、余白、共有コンポーネントのビジュアルデフォルトについてのコメントで、オーナーが「intentional」「意図的」と返している。

### アップスタックやスタック局所の利用を Bugbot が見えない

- Confidence: candidate
- Skip when: Bugbot が export・コンポーネント・ヘルパー・ファイルを未使用とし、稼働中 forge の PR 一覧と diff、上段スタックの diff、PR 文脈でスタック後続 PR が使っていると示せる。
- Do not skip when: 現 PR がスタックの一部でない、シンボルが public API、上段利用を検証できない。
- Example signal: 「Exported component is never used」に人が「used upstack」と返す。

### 並行実装中の一時的な重複

- Confidence: candidate
- Skip when: PR が小さな重複を意図的に入れ、削除・置換・検証中の旧経路と新経路を並行させている。
- Do not skip when: 重複がセキュリティ・課金・データアクセス・API 挙動を変える、または長寿命の共有抽象化が明らかにリスクを下げる。
- Example signal: 「Significant duplication」「duplicated validation logic」で、オーナーが旧経路削除予定または意図的ローカル重複と説明している。

### フレームワーク／コンポーネントの既存 invariant が警告をカバー

- Confidence: candidate
- Skip when: 懸念が共有コンポーネント、フレームワーク契約、型 invariant、現 diff または近傍で見える単一の正本で既に保証されている。
- Do not skip when: invariant は仮定のみで強制されていない、タイミング依存、async／状態境界で値が乖離しうる。
- Example signal: 内側 popover の max-height 欠如だが共有 popover が viewport を強制、nullable で局所 checked 値と渡し値が同じソース。

### オーナー宣言のフォローアップまたは延期クリーンアップ

- Confidence: candidate
- Skip when: PR オーナーが既知フォローアップと明示し、現 PR で悪化していない、高リスク領域ではない。
- Do not skip when: オーナー入力なしでエージェントが動く、中〜高 severity のプロダクト挙動、延期すると新 regression が merge される。
- Example signal: 「あとで対応」「eventually 削除」。

### 自己撤回または明示 false positive ルールコメント

- Confidence: recurring
- Skip when: コメント本文または後続 Bugbot 返信が finding 撤回・ compliant・ false positive と明示し、関連ルールをローカルで検証できる。
- Do not skip when: 高リスク issue で人が「false positive」とだけ言い理由がない。
- Example signal: ファイル命名ルールコメントの本文が既に compliant と書いている。

## デフォルトで ask

過去 PR で似た dismiss があっても、次は自動 skip しない。

- セキュリティ、プライバシー、認可、課金、データ保持、学習データ、権限境界の finding。
- 高 severity の finding。
- マイグレーション、スキーマ、冪等性、並行、システム横断挙動の finding。
- 提案修正が小さく、プロダクト intent を変えずに明らかにリスクを下げるコメント。

履歴では人がセキュリティ／データフロー系を dismiss することもある。それはチーム全体の skip ルールではなく、オーナー判断として扱う。

## 最近の babysit からの候補学習

チームに有用だが未成熟に見えるものは babysit 中・後にここへ追記。複数 PR で確認できたら上のセクションへ昇格。

### ネイティブブラウザ挙動の手実装

- Confidence: candidate
- Skip when: 実質ほぼ never。diff がネイティブを手実装に置き換える（sticky → JS クローン、scroll targeting → wheel/touch 転送、ペイント順 → mask/clip-path）とき、そのコードへの Bugbot のロジックバグ finding は一貫して正当だった。
- Do not skip when: event 転送の穴（wheel deltaMode、touch pan、端での scroll chaining、tap slop）、mask/clip の hit-test 乖離、IntersectionObserver と React 状態のタイミングレース。デフォルトは fix。
- Example signal: 「masks do not affect hit-testing」「overlay blocks wheel scroll」「ignores deltaMode」「runs in the IntersectionObserver callback before React applies state」。
- Source: sticky occlusion PR 1 件: Bugbot 6 pass、約 18 finding、すべて fix、dismiss なし。

### 契約テストの drift 主張は安く検証できる — 先にテストを走らす

- Confidence: candidate
- Skip when: 検証自体は skip しない。1 コマンドのコスト。PR がプロトコルやドキュメント文言を pin する契約テスト（SKILL.md への regex、doc 文言スナップショット）を載せ、Bugbot が「テストが doc と合わない」（または逆）と言うとき、分類前に PR tip でそのテストを走らせる。red は主張を実証、green は dismiss 返信の反証。
- Do not skip when: n/a — これは検証短縮であり dismiss パターンではない。繰り返し pass の lean-dismiss ヒューリスティックはここで外れる。prose pin テストは fix ラウンドで prose を編集するから drift する。
- Example signal: 「Contract test omits the pre-fix wait」で、以前の fix commit が pin 箇所を言い換えた PR。tip でテストが引用 assertion で fail。
- Source: prose pin PR 1 件、Bugbot 8 pass。pass 7 の主張は実在（以前はすべて fix-and-resolve）。

### 同一 PR 内の後続 commit で既に直した古いセキュリティレビュー finding

- Confidence: candidate
- Skip when: エージェント型セキュリティレビューが authz/validation 欠如を主張し、PR tip にその gate（テスト付き）が明確にある。多くはレビュー実行後の hardening commit。
- Do not skip when: 引用ヘルパーが当該 principal で no-op、チェックが副作用の後、主張 principal のカバレッジ欠如。
- Example signal: HIGH「missing authorization check」だが tip で副作用前に guard 呼び出し済み。
- Source: webhook endpoint PR。hardening がレビュー実行より後。

### 意図的に狭いエラー条件を広げると本当のエラーが隠れる

- Confidence: candidate
- Skip when: finding が狭いエラー条件（特定 `errno`、エラーコード、status クラス）を catch-all に広げるよう求め、その狭さが実 distinction を表す。典型は依存フォールバックが `ENOENT` 限定:「バイナリ未インストール」と「コマンド実行失敗」は別状況。非ゼロ終了すべてでリトライすると正当失敗（not found、期限切れ auth、ネットワーク）をフォールバックに再実行し、フォールバックのエラーを報告して真因を隠す。
- Do not skip when: 狭い条件が同カテゴリの別ケースを逃す（`EACCES` など別の「バイナリ使えない」errno、別のトランスポート失敗）、未処理経路でデータ損失や部分状態、リトライが冪等かつ元エラーを依然 surface。
- Example signal: 「only retries when X fails with ENOENT … never tries the fallback even when a working Y exists」が、フォールバックが欠如バイナリ用で失敗コマンド用ではないコードを指す。
- Source: CLI rename PR。フォールバックは欠如バイナリ用。

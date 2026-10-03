# Product Design セットアップ

保存ユーザーコンテキストが無いとき、Product Design が何を記憶できるか聞かれたとき、セットアップを求められたとき、プロダクト／デザイン参照を保存するために使う。

セットアップ開始前に [$user-context](../SKILL.md) の永続化可否チェックを実行する。永続コンテキストが使えないときは下のオンボーディングプロンプトを出さない。参照は今の会話では使えるが将来の会話には保存できないと説明する。

セットアップは短い。アンケートでも正式オンボーディング状態機械でもない。

## Step 1: オリエンテーション

これを最初に出す。このメッセージの前にファイル書き込み、ツール inspect、URL 閲覧、Figma 開く、プロトタイプ作成、画像生成、監査をしない。

```md
Product Design は、よく使うプロダクト画面とデザインソースを記憶し、次の作業を正しい場所から始められます。

保存に便利なもの:
1. プロダクト URL
2. Figma ファイル
3. スクリーンショットまたは参照画像
4. コードベースパス
5. Storybook またはコンポーネントドキュメント
6. デザインシステム参照
7. ブランドとアセットソース
8. 好みのツールと共有先

今すぐ送るか、`skip` と言えば各タスクのソースだけから進めます。
```

## Step 2: コンテキスト保存

ユーザーが参照を渡したら保存先:

```text
~/.cursor/product-design/user-context.md
```

プロジェクトスコープ（任意）:

```text
.cursor/product-design/user-context.md
```

必要なら先にファイルを作る:

```bash
python3 scripts/init_user_context.py
```

カテゴリ構造は `../SKILL.md` に従う。

スクリーンショットや参照画像は次にコピー:

```text
~/.cursor/product-design/assets/
```

保存画像には内容が分かる名前を付ける（例: `assets/payment-sheet-mobile-error-state.png`）。

秘密、API キー、認証情報、私有トークン、未サポートの主張は保存しない。

保存後の要約:

```md
Product Design コンテキストを保存しました:
- {Category}: {what was saved}

将来の Product Design 作業の起点マップとして使います。タスクで渡すソースが常に優先されます。
```

## Step 3: コンテキスト読み出し

Product Design が何を知っているか聞かれたら `user-context.md` を読み、保存エントリだけ要約する。

保存が無ければ明言し、Step 1 のセットアッププロンプトを提案する。

# フロントエンド コーディングルール

## 1. コーディングスタイル
### 1.1. 命名規則

-   **変数・関数:** キャメルケース (`exampleVariable`, `getUserData`) を使用します。
-   **コンポーネント・クラス・型・インターフェース:** パスカルケース (`ExampleComponent`, `UserData`, `IUserService`) を使用します。
-   **定数:** 大文字スネークケース (`MAX_CONNECTIONS`, `ACCESS_TOKEN_KEY`) を使用します。
-   **ファイル名:** ケバブケース (`button.tsx`, `use-theme-color.ts`) を使用します。コンポーネントディレクトリ内のエントリーファイルは `index.tsx` とします。Expo Router のルートファイルは規約に従います (`(routes)/index.tsx`, `post/_layout.tsx` など)。
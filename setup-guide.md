---
marp: true
theme: default
paginate: false
header: "研修環境セットアップガイド"
footer: "© 2024 RuntimeStudio Inc."
style: |
  section {
    font-family: 'Hiragino Kaku Gothic ProN', 'Noto Sans JP', sans-serif;
    background-color: #FAFAFA;
  }
  header {
    font-size: 14px;
    color: #666;
  }
  footer {
    font-size: 12px;
    color: #666;
  }
  h1 {
    color: #D92B2B;
  }
  h2 {
    color: #2D2926;
  }
  a {
    color: #D92B2B;
  }
  code {
    background-color: #f5f5f5;
    color: #333;
  }
  pre {
    background-color: #2D2926;
    color: #f8f8f2;
    font-size: 0.75em;
  }
  pre code {
    background-color: transparent;
    color: #f8f8f2;
  }
  table {
    font-size: 0.85em;
  }
  th {
    background-color: #D92B2B;
    color: white;
  }
  strong {
    color: #D92B2B;
  }
  section.title {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  section.title h1 {
    font-size: 2.5em;
  }
  section::after {
    content: "";
  }
  img[alt="logo"] {
    position: absolute;
    top: 25px;
    right: 30px;
    width: 120px;
    height: auto;
  }
---

<!-- _class: title -->

![w:180](./assets/logos/logo_yoko.png)

# 研修環境セットアップガイド
## 〜uvでPython環境を構築しよう〜

---

![logo](./assets/logos/logo_yoko.png)

# この資料の目的

研修を始める前に、全員が**同じ開発環境**で作業できるようにセットアップを行います。

## やること

1. Pythonバージョンの確認
2. uvのセットアップ
3. 研修リポジトリの取得
4. 依存関係のインストール
5. 動作確認

---

![logo](./assets/logos/logo_yoko.png)

# uvとは？

**Pythonの高速パッケージマネージャー**

## メリット

- **超高速**: pipより10〜100倍速い
- **簡単**: 1コマンドでインストール可能
- **便利**: Python仮想環境の管理も自動
- **信頼性**: プロジェクトごとに依存関係を分離

---

![logo](./assets/logos/logo_yoko.png)

# Step 1: Pythonバージョンの確認

## ターミナルを開く

- Mac: Spotlight検索で「ターミナル」と入力
- Windows: 「コマンドプロンプト」または「PowerShell」を起動

## バージョン確認

```bash
python3 --version
```

**Python 3.11.x** または **3.12.x** と表示されればOK！

---

![logo](./assets/logos/logo_yoko.png)

# Step 2: uvのインストール

## Mac / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

インストール後、**ターミナルを再起動**してください。

---

![logo](./assets/logos/logo_yoko.png)

# uvのインストール確認

## バージョン確認

```bash
uv --version
```

`uv x.x.x` と表示されればインストール成功！

## もし `command not found` と出たら

ターミナルを閉じて、もう一度開いてください。

---

![logo](./assets/logos/logo_yoko.png)

# Step 3: 研修リポジトリの取得

## 方法1: Git経由（推奨）

```bash
# Gitがインストールされている場合
git clone https://github.com/YOUR_ORG/ai-agent-training.git
cd ai-agent-training
```

## 方法2: ZIPダウンロード

講師から配布されたZIPファイルを展開して、フォルダに移動してください。

```bash
cd ai-agent-training
```

---

![logo](./assets/logos/logo_yoko.png)

# Step 4: 依存関係のインストール

## uvで環境構築

```bash
uv sync
```

これだけで完了！uvが自動的に：

1. 仮想環境（`.venv`）を作成
2. 必要なパッケージをインストール

---

![logo](./assets/logos/logo_yoko.png)

# Step 5: Google AI APIキーの取得

## Google AI Studioにアクセス

https://aistudio.google.com/apikey

1. Googleアカウントでログイン
2. 「Create API key」をクリック
3. APIキーをコピー

---

![logo](./assets/logos/logo_yoko.png)

# Step 6: 環境変数の設定

## .envファイルの作成

```bash
cp .env.example .env
```

## .envファイルの編集

お好きなエディタで `.env` ファイルを開いて編集してください。

```bash
# Google AI API Key
GOOGLE_API_KEY=your_api_key_here
```

**注意**: `.env`ファイルはGitにコミットしないでください

---

![logo](./assets/logos/logo_yoko.png)

# Step 7: 動作確認

## 確認スクリプトを実行

```bash
uv run python check.py
```

すべて ✅ が表示されれば、環境構築完了です！

```
============================================
🔍 研修環境チェック
============================================
✅ Python バージョン: 3.11.x
✅ uv バージョン: x.x.x
✅ 仮想環境: .venv
✅ 依存パッケージ: インストール済み
============================================
🎉 環境構築完了！研修を始めましょう！
============================================
```

---

![logo](./assets/logos/logo_yoko.png)

# よく使うuvコマンド

| コマンド | 説明 |
|:--|:--|
| `uv sync` | 依存関係をインストール |
| `uv add パッケージ名` | パッケージを追加 |
| `uv run python ファイル.py` | Pythonファイルを実行 |
| `uv run python` | Python対話モードを起動 |

---

![logo](./assets/logos/logo_yoko.png)

# トラブルシューティング

## `uv: command not found`

ターミナルを再起動してください。それでも解決しない場合：

```bash
# Mac/Linux: パスを通す
source $HOME/.local/bin/env
```

## APIキーエラー

```
GOOGLE_API_KEY environment variable not set
```
→ `.env` ファイルに `GOOGLE_API_KEY` を設定してください

---

![logo](./assets/logos/logo_yoko.png)

# トラブルシューティング

## 依存関係エラー

環境を作り直したい場合：

```bash
# .venvを削除
rm -rf .venv

# 再度インストール
uv sync
```

## パッケージが見つからない

```bash
# lockファイルを更新
uv lock
uv sync
```

---

<!-- _class: title -->

![w:180](./assets/logos/logo_yoko.png)

# 準備完了！

## 研修本編へ進みましょう

困ったらこの資料に戻ってきてください

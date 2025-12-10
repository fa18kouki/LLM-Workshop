---
marp: true
theme: default
paginate: false
header: "Python基礎 〜フロントエンドエンジニアのための速習ガイド〜"
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
  pre code .hljs-keyword { color: #ff79c6; }
  pre code .hljs-string { color: #f1fa8c; }
  pre code .hljs-number { color: #bd93f9; }
  pre code .hljs-comment { color: #6272a4; }
  pre code .hljs-function { color: #50fa7b; }
  pre code .hljs-class { color: #8be9fd; }
  pre code .hljs-title { color: #50fa7b; }
  pre code .hljs-params { color: #ffb86c; }
  pre code .hljs-built_in { color: #8be9fd; }
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

# Python基礎
## 〜フロントエンドエンジニアのための速習ガイド〜

---

![logo](./assets/logos/logo_yoko.png)

# この資料の目的

普段JavaScript/TypeScriptを使っているエンジニアが、
**LLM演習をスムーズに進められる**ようにPythonの基礎を解説

## 対象者

- フロントエンドエンジニア（React, Vue, etc.）
- バックエンドでもNode.js/Go/Java等を使っている方
- Pythonは「なんとなく読める」程度の方

---

![logo](./assets/logos/logo_yoko.png)

# JS/TS vs Python: 基本構文の違い

| 項目 | JavaScript/TypeScript | Python |
|:--|:--|:--|
| 文末 | セミコロン `;` | **不要**（改行で区切り） |
| ブロック | `{ }` で囲む | **インデント**で表現 |
| 変数宣言 | `const`, `let`, `var` | そのまま `x = 1` |
| 型注釈 | `: string` | `: str`（任意） |
| コメント | `//` or `/* */` | `#` |

---

![logo](./assets/logos/logo_yoko.png)

# 変数と型

```python
# Pythonでは型宣言不要（でも型ヒントは書ける）
name = "田中"           # str（文字列）← JSのstring
age = 25               # int（整数）← JSのnumber
price = 19.99          # float（小数）← JSのnumber
is_active = True       # bool ← JSのboolean（大文字始まり注意！）
items = ["a", "b"]     # list ← JSの配列
user = {"name": "太郎"} # dict ← JSのオブジェクト

# 型ヒント付き（TypeScriptライクに書きたい人向け）
name: str = "田中"
age: int = 25
```

**ポイント**: `True`/`False`/`None` は大文字始まり（JSの`true`/`false`/`null`と違う）

---

![logo](./assets/logos/logo_yoko.png)

# 文字列操作

```python
name = "田中"
message = f"こんにちは、{name}さん"  # JSの `こんにちは、${name}さん`

# 複数行文字列（JSのバッククォートに相当）
prompt = """
あなたは優秀なアシスタントです。
以下の質問に答えてください。
"""

# メソッド
text = "  hello world  "
text.strip()    # 空白削除 ← .trim()
text.split(" ") # 分割 ← 同じ
text.replace("hello", "hi")  # 置換 ← 同じ
```

---

![logo](./assets/logos/logo_yoko.png)

# リスト（配列）操作

```python
fruits = ["apple", "banana", "cherry"]  # JSの配列と同じ

fruits[0]              # "apple"
fruits.append("orange") # 末尾に追加 ← JSの .push()
len(fruits)            # 長さ ← JSの .length

# スライス（JSにはない便利機能！）
fruits[1:3]   # ["banana", "cherry"]
fruits[-1]    # 最後の要素 ← JSの .at(-1)

# リスト内包表記 ← JSの .map()
doubled = [n * 2 for n in [1,2,3]]  # [2, 4, 6]
```

---

![logo](./assets/logos/logo_yoko.png)

# 辞書（オブジェクト）操作

```python
user = {"name": "田中", "age": 25}  # JSのオブジェクトと同じ

user["name"]       # "田中" ← JSのuser.nameだがPythonは[]のみ
user.get("email", "未設定")  # キーがなくてもエラーにならない

user["email"] = "tanaka@example.com"  # 追加・更新

user.keys()    # キー一覧 ← Object.keys(user)
user.values()  # 値一覧 ← Object.values(user)
user.items()   # (キー, 値)のペア ← Object.entries(user)
```

---

![logo](./assets/logos/logo_yoko.png)

# 条件分岐

```python
score = 85

if score >= 90:
    print("優")
elif score >= 70:    # ← JSの else if
    print("良")
else:
    print("可")

# 三項演算子: JSの score >= 60 ? "合格" : "不合格"
result = "合格" if score >= 60 else "不合格"

# None判定: JSの value === null
if value is None:
    print("値がありません")
```

---

![logo](./assets/logos/logo_yoko.png)

# ループ

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:        # JSの for (const fruit of fruits)
    print(fruit)

for i, fruit in enumerate(fruits):   # インデックス付き
    print(f"{i}: {fruit}")  # JSの fruits.forEach((fruit, i) => ...)

for i in range(5):          # 0,1,2,3,4 ← JSの for(let i=0; i<5; i++)
    print(i)
```

---

![logo](./assets/logos/logo_yoko.png)

# 関数

```python
# 基本的な関数
def greet(name):
    return f"こんにちは、{name}さん"

# デフォルト引数
def greet(name, greeting="こんにちは"):
    return f"{greeting}、{name}さん"

# 型ヒント付き（TypeScriptっぽく書きたい人向け）
def greet(name: str, greeting: str = "こんにちは") -> str:
    return f"{greeting}、{name}さん"

# 呼び出し
greet("田中")                    # "こんにちは、田中さん"
greet("田中", greeting="おはよう")  # キーワード引数
```

**JSとの違い**: `function`キーワードの代わりに`def`を使う

---

![logo](./assets/logos/logo_yoko.png)

# クラス（Pydanticの前提知識）

```python
# 通常のクラス
class User:
    def __init__(self, name: str, age: int):  # ← constructor相当
        self.name = name
        self.age = age

    def greet(self):  # ← メソッド（selfが必須）
        return f"私は{self.name}です"

user = User("田中", 25)
print(user.name)    # "田中"
print(user.greet()) # "私は田中です"
```

**注意**: メソッドの第一引数には必ず`self`が必要（JSの`this`に相当）

---

![logo](./assets/logos/logo_yoko.png)

# Pydantic: 構造化出力で使う重要ライブラリ

```python
from pydantic import BaseModel, Field
from typing import Literal

# BaseModelを継承してデータ構造を定義（TypeScriptのinterfaceに近い）
class CommentAnalysis(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"] = Field(
        description="感情分析の結果"
    )
    score: int = Field(description="スコア", ge=1, le=5)  # ge=以上, le=以下
    keywords: list[str] = Field(description="キーワードリスト")

# TypeScriptで書くと...
# interface CommentAnalysis {
#   sentiment: "positive" | "negative" | "neutral";
#   score: number; // 1〜5
#   keywords: string[];
# }
```

LLMに「この形式で出力して」と指示するときに使用

---

![logo](./assets/logos/logo_yoko.png)

# import文

```python
# モジュール全体をインポート
import json
data = json.loads('{"name": "田中"}')

# 特定の関数/クラスだけインポート
from json import loads
data = loads('{"name": "田中"}')

# 別名でインポート
import numpy as np  # npとして使える

# 複数インポート
from typing import Literal, Optional, List
```

**JSとの対応**:
- `import json` ← `import * as json from 'json'`
- `from json import loads` ← `import { loads } from 'json'`

---

![logo](./assets/logos/logo_yoko.png)

# 非同期処理（async/await）

```python
import asyncio

async def fetch_data():           # JSとほぼ同じ！
    await asyncio.sleep(1)
    return {"data": "result"}

async def main():
    results = await asyncio.gather(  # ← Promise.all() に相当
        fetch_data(), fetch_data(), fetch_data()
    )
    return results

asyncio.run(main())  # 実行
```

演習C1で並列実行する際に使用

---

![logo](./assets/logos/logo_yoko.png)

# エラーハンドリング

```python
# try-except（JSのtry-catchに相当）
try:
    result = 10 / 0
except ZeroDivisionError as e:  # ← catch (e)
    print(f"エラー: {e}")
except Exception as e:  # すべての例外をキャッチ
    print(f"予期しないエラー: {e}")
finally:
    print("終了処理")

# 例外を発生させる
def validate(value):
    if value < 0:
        raise ValueError("負の値は不正です")  # ← throw new Error(...)
```

---

![logo](./assets/logos/logo_yoko.png)

# 演習で使うパターン集

## LLMのAPI呼び出し

```python
from google import genai

client = genai.Client()
response = client.models.generate_content(
    model="gemini-2.5-flash", contents="質問内容",
)
print(response.text)  # JSの console.log(response.text) と同じ
```

---

![logo](./assets/logos/logo_yoko.png)

# 演習で使うパターン集

## f-string でプロンプトを組み立てる

```python
user_input = "サッカー観戦が好きです"
prompt = f"""
以下の文章から趣味を抽出してください。
入力文: {user_input}
"""
```

```javascript
// JSで書くと:
const prompt = `以下の文章から趣味を抽出してください。
入力文: ${userInput}`;
```

`f"..."`がJSのテンプレートリテラル`` `...` ``に対応

---

![logo](./assets/logos/logo_yoko.png)

# 演習で使うパターン集

## 構造化出力（LLMの出力を型安全に）

```python
from pydantic import BaseModel, Field
from typing import Literal

class AnalysisResult(BaseModel):
    sentiment: Literal["positive", "negative"]
    reason: str = Field(description="判定理由")

# LLMにこの構造で出力させる
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="このコメントを分析: 最高でした！",
    config=GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=AnalysisResult,  # ← ここで型を指定
    ),
)
```

---

![logo](./assets/logos/logo_yoko.png)

# よくあるエラーと解決法

| エラー | 原因 | 解決法 |
|:--|:--|:--|
| `IndentationError` | インデントが揃っていない | スペース4つで統一 |
| `NameError: name 'xxx' is not defined` | 変数が未定義 | スペルミス確認、import確認 |
| `TypeError: 'NoneType'` | Noneに対して操作 | None判定を追加 |
| `KeyError` | 辞書にキーがない | `.get()`を使う |
| `ModuleNotFoundError` | パッケージ未インストール | `uv add パッケージ名` |

---

![logo](./assets/logos/logo_yoko.png)

# 実行方法

```bash
# 仮想環境でPythonファイルを実行（uvを使用）
uv run python practice/genai_ver/a1.py

# 対話モードで試す
uv run python
>>> print("Hello")
Hello
>>> exit()
```

## VSCodeでの実行

1. `.py`ファイルを開く
2. 右上の再生ボタン or `F5`キー
3. ターミナルに結果が表示される

---

![logo](./assets/logos/logo_yoko.png)

# クイックリファレンス

| やりたいこと | JavaScript | Python |
|:--|:--|:--|
| 配列の長さ | `arr.length` | `len(arr)` |
| 配列に追加 | `arr.push(x)` | `arr.append(x)` |
| 配列をマップ | `arr.map(x => x*2)` | `[x*2 for x in arr]` |
| 配列をフィルタ | `arr.filter(x => x>0)` | `[x for x in arr if x>0]` |
| オブジェクトのキー | `Object.keys(obj)` | `obj.keys()` |
| JSON→オブジェクト | `JSON.parse(str)` | `json.loads(str)` |
| オブジェクト→JSON | `JSON.stringify(obj)` | `json.dumps(obj)` |
| コンソール出力 | `console.log(x)` | `print(x)` |

---

<!-- _class: title -->

![w:180](./assets/logos/logo_yoko.png)

# 準備完了！

## 研修本編へ進みましょう

困ったらこの資料に戻ってきてください

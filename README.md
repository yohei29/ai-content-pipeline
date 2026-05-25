# README
---
## 環境構築

1. venvのインストール
2. Python環境構築
```
py -3.12 -m venv .venv
```
起動
```
# PowerShellの場合
.venv\Scripts\Activate.ps1

# コマンドプロンプト(cmd)の場合
.venv\Scripts\activate.bat
```

3. python モジュールインストール
```
pip install -r requirements.txt
```

---
## 実行

実行はrootでおこなう。

memo .venv_gpu312\Scripts\Activate.ps1

## 実行順序

1. 動画ID一覧取得
```
python -m src.pipelines.get_movie_metadata.get_movie_ids
```

2. 動画取得
```
python -m src.pipelines.youtube_work.youtube_download
```

---
## ディレクトリ構成ガイドライン

### ディレクトリ構成

```text
project/
├─ src/
├─ data/
│   ├─ raw/
│   ├─ processed/
│   └─ exports/
├─ logs/
├─ temp/
└─ archive/
```

---

## src/

```
src/
├─ workflows/  # システム全体の処理順制御
│               # pipelineを組み合わせ目的を達成する/
│
├─ pipelines/  # データ加工処理
│               # 入力→変換→出力の直列処理
│
├─ prompts/    # LLMへ渡すPrompt管理
│               # 要約・記事化・分類など用途別に分離
│
├─ models/     # データ構造定義(将来的に使用)
│               # dataclass / pydantic 等
│
├─ services/   # 外部サービス接続(将来的に使用)
│               # YouTube / Whisper / Gemini / DB等
│
├─ utils/      # 汎用関数
│               # 文字列・ファイル・日時処理など
│
└─ config/     # 定数・環境設定・パス管理
                # API_KEY / DIRECTORY / MODEL設定等

workflow
  ↓
pipeline
  ↓
service
  ↓
external API

----------------------------------------

workflow
  「何をするか」

pipeline
  「どうデータを加工するか」

service
  「どう外部と通信するか」

model
  「どんなデータを扱うか」

prompt
  「AIへどう指示するか」

----------------------------------------
```

## data/

```text
data/
```
データ保存領域。


---

## data/raw/

```text
data/raw/
```

加工前生データ。

---

## data/raw/videos/

```text
data/raw/videos/
```
動画。


## data/raw/metadata/

```text
data/raw/metadata/
```

動画情報メタデータ。

---

## data/processed/

```text
data/processed/
```

A関連連処理出力データ。

---

### data/processed/transcripts/

```text
data/processed/transcripts/
```

文字起こし結果。


---

### data/processed/summaries/

```text
data/processed/summaries/
```

AI動画要約結果。

---

## data/processed/analysis/

```text
data/processed/analysis/
```

AI解析結果。

### 内容例

- 感情分析
- ジャンル分類
- keyword抽出
- topic分類
- 品質判定

---

## data/exports/

```text
data/exports/
```

外部利用向け成果物。

---

## logs/

```text
logs/
```

ログ保存領域。

---

## temp/

```text
temp/
```

処理中に使用する一時ファイル領域。

---

## archive/

```text
archive/
```

旧データ・退避領域。

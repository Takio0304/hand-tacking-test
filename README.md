# Hand Tracking Mouse Control

Webカメラで手の動きを検出し、マウス操作を行うプログラムです。MediaPipeとOpenCVを使用して、手のジェスチャーでPCを操作できます。

## 機能

- **マウス移動**: 手首の位置でカーソルを移動
- **左クリック**: 親指と人差し指をピンチ（つまむ）
- **右クリック**: 親指と中指をピンチ
- **スムージング**: カーソル移動を滑らかに

## 必要な環境

- Python 3.7以上（Python 3.11推奨）
- Webカメラ
- Windows / macOS / Linux

## セットアップ（初回のみ）

### 1. Pythonがインストールされているか確認

```bash
python --version
```

Python 3.7以上がインストールされていることを確認してください。

### 2. リポジトリをクローン

```bash
git clone git@github.com:Takio0304/hand-tacking-test.git
cd hand-tacking-test
```

### 3. 仮想環境を作成

Pythonの仮想環境を作成します（プロジェクト専用の独立した環境）。

```bash
python -m venv venv
```

### 4. 仮想環境を有効化

作成した仮想環境を有効化します。

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

仮想環境が有効化されると、コマンドプロンプトの先頭に `(venv)` と表示されます。

### 5. 依存パッケージをインストール

仮想環境内に必要なパッケージをインストールします。

```bash
pip install -r requirements.txt
```

これで、OpenCV、MediaPipe、PyAutoGUIなどの必要なライブラリがインストールされます。

## 実行方法

### 初回実行または環境をリセットした後

1. プロジェクトディレクトリに移動
```bash
cd hand-tacking-test
```

2. 仮想環境を有効化
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. プログラムを実行
```bash
python hand_control.py
```

### 2回目以降の実行

すでにセットアップが完了している場合は、仮想環境を有効化して実行するだけです。

```bash
# 仮想環境を有効化
venv\Scripts\activate  # Windows
# または
source venv/bin/activate  # macOS/Linux

# プログラムを実行
python hand_control.py
```

### 仮想環境を終了する場合

```bash
deactivate
```

## 使い方

1. プログラムを実行すると、カメラ映像のウィンドウが開きます
2. カメラに手をかざします（片手のみ検出）
3. **手首を動かす** → マウスカーソルが移動
4. **親指と人差し指をつまむ** → 左クリック
5. **親指と中指をつまむ** → 右クリック
6. **'q'キーを押す** → プログラム終了

## 調整方法

`hand_control.py` の以下のパラメータで動作を調整できます：

```python
pinch_threshold = 0.05      # ピンチ検出の感度（小さいほど敏感）
pinch_duration = 5          # クリック判定までのフレーム数
max_buffer = 5              # カーソルのスムージング量
```

## トラブルシューティング

### カメラが起動しない
- 他のアプリケーションがカメラを使用していないか確認してください
- カメラのアクセス許可を確認してください

### 検出精度が低い
- 明るい場所で使用してください
- カメラとの距離を調整してください（50cm〜1m程度推奨）
- 背景をシンプルにすると精度が向上します

### カーソルの動きが不安定
- `max_buffer` の値を大きくするとスムージングが強くなります
- カメラの解像度を変更する（`cap.set()`の値を調整）

## 依存パッケージ

- OpenCV (`opencv-python`)
- MediaPipe (`mediapipe`)
- PyAutoGUI (`pyautogui`)
- NumPy
- その他（`requirements.txt` を参照）

## ライセンス

このプロジェクトは自由に使用・改変できます。

## 注意事項

- このプログラムはマウス操作を自動で行います。予期しない動作を防ぐため、重要な作業中の使用は避けてください
- カメラへのアクセス許可が必要です

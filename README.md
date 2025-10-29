# Hand Tracking Mouse Control

Webカメラで手の動きを検出し、マウス操作を行うプログラムです。MediaPipeとOpenCVを使用して、手のジェスチャーでPCを操作できます。

## 機能

- **マウス移動**: 手首の位置でカーソルを移動
- **左クリック**: 親指と人差し指をピンチ（つまむ）
- **右クリック**: 親指と中指をピンチ
- **スムージング**: カーソル移動を滑らかに

## 必要な環境

- Python 3.11
- Webカメラ
- Windows / macOS / Linux

## セットアップ

### 1. リポジトリをクローン

```bash
git clone git@github.com:Takio0304/hand-tacking-test.git
cd hand-tacking-test
```

### 2. 仮想環境を作成

```bash
python -m venv hand_env
```

### 3. 仮想環境を有効化

**Windows:**
```bash
hand_env\Scripts\activate
```

**macOS/Linux:**
```bash
source hand_env/bin/activate
```

### 4. 依存パッケージをインストール

```bash
pip install -r requirements.txt
```

## 実行方法

```bash
python hand_control.py
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

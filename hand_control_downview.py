import cv2
import mediapipe as mp
import pyautogui
import math
import numpy as np

# 必要なライブラリのインストールコマンド（ターミナルで実行）:
# pip install opencv-python mediapipe pyautogui

def main():
    # 画面サイズを取得
    screen_width, screen_height = pyautogui.size()
    print(f"Screen size: {screen_width}x{screen_height}")

    # MediaPipe Hand トラッキングの初期化
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
    mp_draw = mp.solutions.drawing_utils

    # Webカメラの起動
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera could not be opened.")
        return

    cam_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cam_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # --- Y軸（高さ）キャリブレーションのための設定 ---
    # これらの値は、実行して表示される "Hand Size" を見ながら調整が必須です。
    
    # 例: 手を机に置いた時 (一番遠い) のサイズ
    MIN_HAND_SIZE = 0.15 
    # 例: 手をカメラに近づけた時 (一番近い) のサイズ
    MAX_HAND_SIZE = 0.35

    # --- X軸（左右）の操作領域 ---
    frame_reduction_x = 150 

    # スムージング
    prev_x, prev_y = 0, 0
    smoothing_factor = 0.4 # 0 (遅い) ~ 1 (速い)

    # --- クリックのための設定 (ピンチ) ---
    CLICK_DISTANCE_THRESHOLD = 0.04 # 人差し指と親指の距離の閾値 (正規化座標)

    print("X-Z (Height) Hand tracking started.")
    print("Move hand Left/Right for X-axis.")
    print("Move hand Up/Down (Height) for Y-axis.")
    print("Pinch index and thumb to click.")
    print("Press 'q' to quit.")

    try:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            image.flags.writeable = False
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)
            image.flags.writeable = True
            
            # image = cv2.flip(image, 1) # 必要に応じて反転

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                
                mp_draw.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                # --- ランドマークの座標取得 ---
                # (0.0 ~ 1.0 の正規化された座標)
                
                # 人差し指の先端 (Index Finger Tip) - Landmark 8
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                # 親指の先端 (Thumb Tip) - Landmark 4
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                
                # --- Y軸（高さ）のためのランドマーク ---
                # 手首 (Wrist) - Landmark 0
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                # 中指の付け根 (Middle Finger MCP) - Landmark 9
                mcp_middle = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]

                # --- 1. マウスカーソルのY軸（高さ） ---
                # 手首(0)と中指付け根(9)の間の「見かけの大きさ」を計算
                # (正規化座標系で計算する)
                hand_size = math.hypot(wrist.x - mcp_middle.x, wrist.y - mcp_middle.y)

                # デバッグ用にサイズを表示
                cv2.putText(image, f"Hand Size (Y): {hand_size:.4f}", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # 手の大きさを画面のY座標にマッピング
                # (np.interp は範囲外の値を丸めてくれるので便利)
                # マッピング: 小さい(遠い) -> 下, 大きい(近い) -> 上
                target_y = np.interp(hand_size, 
                                   (MIN_HAND_SIZE, MAX_HAND_SIZE), 
                                   (screen_height, 0)) # Y軸を反転

                # --- 2. マウスカーソルのX軸（左右） ---
                # 人差し指の先端のX座標を画面のX座標にマッピング
                target_x = np.interp(index_tip.x, 
                                   (frame_reduction_x / cam_width, 1.0 - frame_reduction_x / cam_width), 
                                   (0, screen_width))

                # スムージング
                current_x = prev_x + (target_x - prev_x) * smoothing_factor
                current_y = prev_y + (target_y - prev_y) * smoothing_factor

                pyautogui.moveTo(current_x, current_y, duration=0) 
                
                prev_x, prev_y = current_x, current_y

                # --- 3. クリック動作 (ピンチ) ---
                # 人差し指(8)と親指(4)の距離を計算
                pinch_distance = math.hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)

                # デバッグ用に距離を表示
                cv2.putText(image, f"Pinch (Click): {pinch_distance:.4f}", (10, 60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                if pinch_distance < CLICK_DISTANCE_THRESHOLD:
                    # ピクセル座標に変換 (描画用)
                    index_x_cam = int(index_tip.x * cam_width)
                    index_y_cam = int(index_tip.y * cam_height)
                    
                    cv2.circle(image, (index_x_cam, index_y_cam), 10, (0, 0, 255), cv2.FILLED)
                    pyautogui.click()
                    print(f"Click! (Pinch Distance: {pinch_distance})")
                    cv2.waitKey(200) # 連続クリック防止

            # 結果を表示
            cv2.imshow('X-Z (Height) Mouse Control', image)

            if cv2.waitKey(5) & 0xFF == ord('q'):
                print("Quitting...")
                break

    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        hands.close()

if __name__ == "__main__":
    pyautogui.FAILSAFE = True
    main()

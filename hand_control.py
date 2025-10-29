import cv2
import mediapipe as mp
import pyautogui
import math

# MediaPipe Handsの初期化
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.3
)

# 画面サイズ
screen_width, screen_height = pyautogui.size()

# カメラの初期化
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# ピンチ検出の設定
pinch_threshold = 0.05  # 調整可能
pinch_count = 0
pinch_duration = 5  # 5フレーム継続でクリック
mouse_positions = []
max_buffer = 5  # スムージング用バッファ

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("カメラから画像を取得できませんでした。")
        break

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # マウス移動（スムージング）
            wrist = hand_landmarks.landmark[0]
            mouse_x = int((1 - wrist.x) * screen_width)
            mouse_y = int(wrist.y * screen_height)
            mouse_positions.append((mouse_x, mouse_y))
            if len(mouse_positions) > max_buffer:
                mouse_positions.pop(0)
            avg_x = sum(pos[0] for pos in mouse_positions) / len(mouse_positions)
            avg_y = sum(pos[1] for pos in mouse_positions) / len(mouse_positions)
            pyautogui.moveTo(avg_x, avg_y)

            # ピンチ検出
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            middle_tip = hand_landmarks.landmark[12]
            dist_index = math.hypot(thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y)
            dist_middle = math.hypot(thumb_tip.x - middle_tip.x, thumb_tip.y - middle_tip.y)

            # デバッグ表示
            cv2.putText(image, f"Index Dist: {dist_index:.4f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            if dist_index < pinch_threshold:
                cv2.circle(image, (int(index_tip.x * image.shape[1]), int(index_tip.y * image.shape[0])), 10, (0, 255, 0), -1)

            # ピンチ持続時間チェック
            if dist_index < pinch_threshold and dist_middle >= pinch_threshold:
                pinch_count += 1
                if pinch_count >= pinch_duration:
                    pyautogui.click()
                    pinch_count = 0
            elif dist_middle < pinch_threshold and dist_index >= pinch_threshold:
                pinch_count += 1
                if pinch_count >= pinch_duration:
                    pyautogui.rightClick()
                    pinch_count = 0
            else:
                pinch_count = 0

    cv2.imshow('Hand Tracking', image)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
import cv2
import mediapipe as mp
import numpy as np
import time
import math

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Canvas
canvas = None
prev_x, prev_y = None, None

# Colors (BGR)
colors = [
    (255, 0, 255),  # Purple
    (255, 0, 0),    # Blue
    (0, 255, 0),    # Green
    (0, 255, 255),  # Yellow
    (0, 0, 0)       # Eraser
]
color_names = ["PURPLE", "BLUE", "GREEN", "YELLOW", "ERASER"]
current_color = colors[0]

# Palette visibility
palette_visible = True
palm_hold_start = None
PALETTE_TOGGLE_TIME = 1.0  # seconds

# Smoothing (Exponential Moving Average)
alpha = 0.7
smooth_x, smooth_y = None, None

# FPS
prev_time = 0

def fingers_up(hand):
    lm = hand.landmark
    return {
        "index": lm[8].y < lm[6].y,
        "middle": lm[12].y < lm[10].y,
        "ring": lm[16].y < lm[14].y,
        "pinky": lm[20].y < lm[18].y
    }

def is_open_palm(f):
    return all(f.values())

def draw_palette(img):
    h, w, _ = img.shape
    box_w = w // len(colors)
    for i, col in enumerate(colors):
        x1 = i * box_w
        x2 = (i + 1) * box_w
        cv2.rectangle(img, (x1, 0), (x2, 60), col, -1)
        cv2.putText(
            img, color_names[i],
            (x1 + 10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6, (0, 0, 0), 2
        )

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    if canvas is None:
        canvas = np.zeros((h, w, 3), dtype=np.uint8)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    mode = "NONE"

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        f = fingers_up(hand)

        x = int(hand.landmark[8].x * w)
        y = int(hand.landmark[8].y * h)

        # EMA smoothing
        if smooth_x is None:
            smooth_x, smooth_y = x, y
        else:
            smooth_x = int(alpha * smooth_x + (1 - alpha) * x)
            smooth_y = int(alpha * smooth_y + (1 - alpha) * y)

        x, y = smooth_x, smooth_y

        # Palette toggle (open palm hold)
        if is_open_palm(f):
            if palm_hold_start is None:
                palm_hold_start = time.time()
            elif time.time() - palm_hold_start > PALETTE_TOGGLE_TIME:
                palette_visible = not palette_visible
                palm_hold_start = None
        else:
            palm_hold_start = None

        # Selection mode
        if f["index"] and f["middle"]:
            mode = "SELECT"
            prev_x, prev_y = None, None

            if palette_visible and y < 60:
                box_w = w // len(colors)
                idx = x // box_w
                if idx < len(colors):
                    current_color = colors[idx]

            cv2.circle(frame, (x, y), 15, current_color, cv2.FILLED)

        # Draw mode
        elif f["index"] and not f["middle"]:
            mode = "DRAW"
            cv2.circle(frame, (x, y), 10, current_color, cv2.FILLED)

            if prev_x is None:
                prev_x, prev_y = x, y

            thickness = 40 if current_color == (0, 0, 0) else 8
            cv2.line(canvas, (prev_x, prev_y), (x, y), current_color, thickness)
            prev_x, prev_y = x, y

        else:
            prev_x, prev_y = None, None

    # Merge canvas
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, inv)
    frame = cv2.bitwise_or(frame, canvas)

    if palette_visible:
        draw_palette(frame)

    # FPS
    curr_time = time.time()
    fps = int(1 / (curr_time - prev_time)) if prev_time else 0
    prev_time = curr_time

    cv2.putText(frame, f"FPS: {fps}", (10, h - 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.putText(frame, f"Mode: {mode}", (10, h - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Air Canvas (Improved)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

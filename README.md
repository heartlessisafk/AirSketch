
# Air Canvas: Virtual Drawing Board 🎨

### What It Is
This is an augmented reality drawing tool that turns the air in front of you into a digital canvas. Using just your webcam and your fingers, you can draw, erase, and switch colors in real-time. It’s like having a touchscreen, but without the screen—you just wave your finger in the air to paint.

### What Skills It Made Me Learn
* **Signal Smoothing:** I learned how to use the Exponential Moving Average (EMA) algorithm to filter out the natural "jitter" of a webcam, turning shaky hand inputs into smooth, professional-looking curves.
* **UI Masking:** I mastered the technique of overlaying digital graphics (like the color palette) onto a live video feed using bitwise masking operations.
* **Coordinate Mapping:** I learned to translate the normalized coordinates from the AI model (0.0 to 1.0) into specific pixel locations (1920x1080) for accurate drawing.

### How It Works
1.  **Tracking:** The system tracks the tip of your index finger.
2.  **Mode Switching:** It checks your hand configuration:
    * **Index Finger Only:** Drawing Mode (creates a line).
    * **Index + Middle Finger:** Selection Mode (moves the cursor without drawing).
3.  **Drawing Engine:** As you move your finger, the code draws lines between your previous position and your current position on a black canvas.
4.  **Compositing:** Finally, it merges the black canvas with your live webcam feed so it looks like the ink is floating in the air.

### If You Want To Use It, Here It Is
**Clone the repository:**
```bash
git clone [https://github.com/heartlessisafk/air-canvas-cv.git](https://github.com/heartlessisafk/air-canvas-cv.git)
Install the requirement
:

Bash
pip install opencv-python mediapipe numpy
Run the application:

Bash
python air_canvas.py
```
Controls:

☝️ Index Finger: Draw.

✌️ Two Fingers: Hover/Select Colors.

✋ Open Palm: Toggle Palette On/Off.

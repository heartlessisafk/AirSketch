A computer vision project that turns your webcam into a virtual canvas. Built with OpenCV and MediaPipe, this application tracks your hand landmarks to let you draw, erase, and change colors in mid-air.

🌟 Features
Gesture-Based Drawing: Use your index finger as a brush and two fingers to navigate.

Virtual Palette: Select colors (Purple, Blue, Green, Yellow) or an Eraser from a menu at the top of the screen.

Stabilization: Implements Exponential Moving Average (EMA) smoothing to ensure lines are clean and not jittery.

Smart UI: Toggle the color palette on/off by holding an open palm to keep your view clean.

🎮 Controls
Gesture	Mode	Action
Index Finger Up	(DRAW)	Draws on the canvas with the selected color.
Index + Middle Up	(SELECT)	Moves the cursor without drawing. Use this to hover over the top menu to change colors.
Open Palm (Hold 1s)	(TOGGLE)	Hides or shows the color palette.
🛠️ Tech Stack
Python 3.x

OpenCV (cv2) - Image processing and canvas overlay.

MediaPipe - Real-time hand landmark detection.

NumPy - Handling image arrays and masks.

🚀 How to Run
Clone the repository:

Bash
git clone https://github.com/YOUR-USERNAME/air-canvas-cv.git
Install dependencies:

Bash
pip install opencv-python mediapipe numpy
Run the application:

Bash
python air_canvas.py
Tip: Ensure you have good lighting so the camera can detect your hand clearly. Press 'q' to quit.

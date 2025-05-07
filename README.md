# RPS Gesture Detector 🎮🖐️

`rps-gesture-detector` is a computer vision-based game that allows users to play Rock-Paper-Scissors by showing hand gestures in front of a webcam. Built with Python and OpenCV, the system processes the live video stream, detects the user's gesture, and determines the winner by generating a gesture from the AI.

## 🔍 Features
- Real-time hand gesture detection
- Background removal and preprocessing visualization
- Classic Rock-Paper-Scissors game logic
- AI opponent with random move generation
- User-friendly and responsive interface
- Optionally extendable to RPSLS (Lizard & Spock)

## 🛠️ Technologies
- Python
- OpenCV
- NumPy
- Matplotlib (for step-by-step visualizations)

## 🚀 Installation

Follow these steps to set up the project on your local machine:

1. **Clone the Repository**  
   Clone this repository to your local machine using Git:
   ```bash
   git clone https://github.com/your-username/rpsls-gesture-detector.git
   cd rpsls-gesture-detector
   ```

2. **Set Up a Virtual Environment**  
   Create and activate a Python virtual environment to isolate dependencies:
   ```bash
   python -m venv .venv
   ```

   - On **Windows**:
     ```bash
     .venv\Scripts\activate
     ```

   - On **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```

3. **Install Dependencies**  
   Install the required Python packages listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables (Windows Only)**  
   If you encounter issues with `tkinter`, set the `TCL_LIBRARY` environment variable:
   ```bash
   $env:TCL_LIBRARY="C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
   ```

5. **Run the Application**  
   Start the Rock-Paper-Scissors gesture detector:
   ```bash
   python main.py
   ```

6. **Optional: Extend to RPSLS**  
   To extend the game to include Lizard and Spock, modify the game logic in [`gui/game.py`](gui/game.py).

You're all set! Enjoy playing Rock-Paper-Scissors with gesture detection! 🎮🖐️

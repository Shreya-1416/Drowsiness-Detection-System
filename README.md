# AI-Based Drowsiness Detection System
Real-time computer vision system for detecting driver fatigue and preventing accidents.

## Features
- Real-time face detection
- Eye movement tracking
- Blink detection
- Alert system for fatigue detection

## Tech Stack
- Python
- OpenCV
- MediaPipe

## Algorithm / Logic
The system uses MediaPipe to detect facial landmarks and track eye movement.
When the eyes remain closed for a certain duration, it identifies drowsiness and triggers an alert.

## Topics
- python
- opencv
- mediapipe
- computer-vision
- AI-project
- drowsiness-detection

## How It Works
The system captures live video using a webcam, detects facial landmarks, and monitors eye movement patterns. If signs of drowsiness (like prolonged eye closure) are detected, an alert is triggered.

## Run Project
pip install -r requirements.txt  
python main.py

## Future Improvements
- Add sound alerts
- Improve accuracy
- Deploy as web app

## Author
Shreya Gupta

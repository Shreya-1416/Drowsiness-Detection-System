# Drowsiness Detection Project

## Requirements
- Python 3.8+
- OpenCV: pip install opencv-python
- Mediapipe: pip install mediapipe
- Pygame: pip install pygame

## How to Run
1. Place your clean alarm WAV as `alarm.wav` in the project folder.
2. Run main.py:
    python main.py
3. Press 'q' to quit.

## Features
- 1-second eyes-closed detection
- EAR smoothing to avoid false alarms
- Automatic WAV fix for glitch-free alarm sound
- Easily replace alarm.wav to change sound

## Optional Scripts
- fix_wave.py: Fix corrupt WAV files
- compare_wav.py: Compare two WAV files
- compare_audio.py: Check WAV file properties

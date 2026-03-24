import cv2
import mediapipe as mp
import pygame
import math
from collections import deque
import wave
import os

# -----------------------------
# WAV Fix Function
# -----------------------------
def fix_wav(input_file, output_file):
    try:
        with wave.open(input_file, 'rb') as wf:
            params = wf.getparams()
            audio_data = wf.readframes(params.nframes)
        with wave.open(output_file, 'wb') as wf:
            wf.setparams(params)
            wf.writeframes(audio_data)
        print(f"WAV file fixed and saved as {output_file}")
    except wave.Error as e:
        print("Error fixing WAV:", e)

# -----------------------------
# Alarm Sound Setup
# -----------------------------
ALARM_FILE = "alarm.wav"        # <-- Replace with your clean alarm file
FIXED_ALARM_FILE = "alarm_fixed.wav"

# Auto-fix WAV if needed
fix_wav(ALARM_FILE, FIXED_ALARM_FILE)

pygame.mixer.init(frequency=44100, size=-16, channels=2)
pygame.mixer.music.load(FIXED_ALARM_FILE)
pygame.mixer.music.set_volume(1.0)  # Full volume

# -----------------------------
# Mediapipe Face Mesh
# -----------------------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Eye landmark indexes (MediaPipe 468-point model)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# -----------------------------
# Functions
# -----------------------------
def euclidean_dist(p1, p2):
    return math.dist(p1, p2)

def eye_aspect_ratio(eye_points, landmarks, image_w, image_h):
    p = [(int(landmarks[i].x * image_w), int(landmarks[i].y * image_h)) for i in eye_points]
    vertical1 = euclidean_dist(p[1], p[5])
    vertical2 = euclidean_dist(p[2], p[4])
    horizontal = euclidean_dist(p[0], p[3])
    EAR = (vertical1 + vertical2) / (2.0 * horizontal)
    return EAR

# -----------------------------
# Settings
# -----------------------------
EAR_THRESHOLD = 0.20       # Ignore normal blink
EAR_CONSEC_FRAMES = 30     # 1 second at 30 FPS
frame_counter = 0

EAR_QUEUE_LENGTH = 5       # Moving average for smoothing
ear_history = deque(maxlen=EAR_QUEUE_LENGTH)

# -----------------------------
# Capture video
# -----------------------------
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape

            left_ear = eye_aspect_ratio(LEFT_EYE, face_landmarks.landmark, w, h)
            right_ear = eye_aspect_ratio(RIGHT_EYE, face_landmarks.landmark, w, h)
            ear = (left_ear + right_ear) / 2.0

            # Smoothing
            ear_history.append(ear)
            smoothed_ear = sum(ear_history) / len(ear_history)

            # Display EAR
            cv2.putText(frame, f"EAR: {smoothed_ear:.2f}", (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Check drowsiness
            if smoothed_ear < EAR_THRESHOLD:
                frame_counter += 1
                if frame_counter >= EAR_CONSEC_FRAMES:
                    if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.play()
            else:
                frame_counter = 0
                pygame.mixer.music.stop()

    cv2.imshow("Drowsiness Detection (EAR)", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

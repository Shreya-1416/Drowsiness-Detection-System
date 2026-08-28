import cv2
import mediapipe as mp
import pygame
import math
from collections import deque

ALARM_FILE = "alarm_fixed.wav"

pygame.mixer.init(frequency=44100, size=-16, channels=2)
pygame.mixer.music.load(ALARM_FILE)
pygame.mixer.music.set_volume(1.0)

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]


def euclidean_dist(p1, p2):
    return math.dist(p1, p2)


def eye_aspect_ratio(eye_points, landmarks, image_w, image_h):
    points = [
        (int(landmarks[i].x * image_w), int(landmarks[i].y * image_h))
        for i in eye_points
    ]

    vertical1 = euclidean_dist(points[1], points[5])
    vertical2 = euclidean_dist(points[2], points[4])
    horizontal = euclidean_dist(points[0], points[3])

    return (vertical1 + vertical2) / (2.0 * horizontal)


EAR_THRESHOLD = 0.20
EAR_CONSEC_FRAMES = 30

frame_counter = 0
ear_history = deque(maxlen=5)

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

            left_ear = eye_aspect_ratio(
                LEFT_EYE, face_landmarks.landmark, w, h
            )

            right_ear = eye_aspect_ratio(
                RIGHT_EYE, face_landmarks.landmark, w, h
            )

            ear = (left_ear + right_ear) / 2.0

            ear_history.append(ear)
            smoothed_ear = sum(ear_history) / len(ear_history)

            cv2.putText(
                frame,
                f"EAR: {smoothed_ear:.2f}",
                (30, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            if smoothed_ear < EAR_THRESHOLD:
                frame_counter += 1

                if frame_counter >= EAR_CONSEC_FRAMES:
                    if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.play()
            else:
                frame_counter = 0
                pygame.mixer.music.stop()

    cv2.imshow("Drowsiness Detection (EAR)", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
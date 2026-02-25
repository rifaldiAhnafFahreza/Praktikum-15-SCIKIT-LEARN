import cv2
import mediapipe as mp
import numpy as np
import math
# Inisialisasi MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
# Fungsi menghitung sudut
def hitung_sudut(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    sudut = np.abs(radians * 180.0 / np.pi)
    if sudut > 180.0:
        sudut = 360 - sudut
    return sudut
while True:
    success, frame = cap.read()
    if not success:
        break
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    if results.pose_landmarks:
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        h, w, c = frame.shape

        # Ambil landmark
        lm = results.pose_landmarks.landmark

        shoulder = [int(lm[11].x * w), int(lm[11].y * h)]
        hip = [int(lm[23].x * w), int(lm[23].y * h)]
        knee = [int(lm[25].x * w), int(lm[25].y * h)]
        # Hitung sudut
        sudut = hitung_sudut(shoulder, hip, knee)
        # Klasifikasi
        if sudut > 150:
            status = "BERDIRI"
            warna = (0, 255, 0)
        else:
            status = "DUDUK"
            warna = (0, 0, 255)
        # Tampilkan teks
        cv2.putText(frame, status, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, warna, 3)

        cv2.putText(frame, f"Sudut: {int(sudut)}",
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (255, 255, 255), 2)

    cv2.imshow("Deteksi Berdiri / Duduk", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
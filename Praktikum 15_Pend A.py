import os
from time import sleep
import cv2

DATA_DIR = 'C:\\Rifaldi\\KULIAH\\aa Tugas smt 6\\Praktikum Kontrol Cerdas\\Program Pycharm\\DATA'

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

number_of_classes = 2
dataset_size = 100

cap = cv2.VideoCapture(0)

for j in range(number_of_classes):

    # Membuat folder untuk tiap class (0, 1, dst)
    class_dir = os.path.join(DATA_DIR, str(j))
    if not os.path.exists(class_dir):
        os.makedirs(class_dir)

    print(f'Collecting data for class {j}')

    # Tampilan awal sebelum mulai capture
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.putText(frame, 'Ready? Press "Q"!',
                    (100, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    sleep(1)

    counter = 0

    # Proses pengambilan gambar
    while counter < dataset_size:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Video', frame)
        cv2.waitKey(10)

        cv2.imwrite(os.path.join(class_dir, f'{counter}.jpg'), frame)
        counter += 1

cap.release()
cv2.destroyAllWindows()
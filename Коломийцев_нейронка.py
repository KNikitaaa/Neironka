import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

# Загрузка каскада Хаара для распознавания лиц
haarcascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(haarcascade_path)

# Список для хранения уникальных лиц
known_faces = []


def detect_and_recognize_faces(image_path):
    global known_faces

    # Загрузка изображения
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Распознавание лиц
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Показ результата
    for (x, y, w, h) in faces:
        face = gray[y:y + h, x:x + w]
        face_resized = cv2.resize(face, (100, 100))  # Приведение лица к фиксированному размеру

        # Проверка на совпадение с известными лицами
        match_found = False
        for known_face in known_faces:
            if np.linalg.norm(face_resized - known_face) < 2000:  # Сравнение по Евклидовой норме
                match_found = True
                break

        # Добавление нового лица в базу, если оно неизвестно
        if not match_found:
            known_faces.append(face_resized)

    # Возвращаем количество лиц
    return len(faces)


def open_image_and_detect_faces():
    # Открытие диалогового окна для выбора файла изображения
    file_path = filedialog.askopenfilename(title="Выберите изображение",
                                           filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])

    if file_path:
        faces_count = detect_and_recognize_faces(file_path)

        # Отображение сообщения с количеством найденных лиц
        message = f"Обнаружено лиц: {faces_count}" if faces_count > 0 else "Лица не обнаружены."
        messagebox.showinfo("Результат распознавания", message)


def create_main_window():
    # Создание главного окна
    root = tk.Tk()
    root.title("Распознавание лиц")

    # Устанавливаем размер окна
    root.geometry("300x150")

    # Кнопка выбора изображения
    select_button = tk.Button(root, text="Выбрать изображение", command=open_image_and_detect_faces, height=2, width=20)
    select_button.pack(pady=20)

    # Кнопка выхода
    exit_button = tk.Button(root, text="Выход", command=root.quit, height=2, width=20)
    exit_button.pack()

    # Запуск главного цикла интерфейса
    root.mainloop()


if __name__ == "__main__":
    create_main_window()

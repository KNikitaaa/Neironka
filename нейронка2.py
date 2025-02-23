import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from mtcnn import MTCNN

# Инициализация детектора MTCNN
detector = MTCNN()

# Список для хранения уникальных лиц
known_faces = []


def detect_and_recognize_faces(image_path):
    global known_faces

    # Загрузка изображения
    img = cv2.imread(image_path)

    # Проверка, что изображение успешно загружено
    if img is None:
        messagebox.showerror("Ошибка", "Не удалось загрузить изображение.")
        return 0

    # Преобразуем изображение в RGB (MTCNN работает с RGB)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Детекция лиц с использованием MTCNN
    faces = detector.detect_faces(img_rgb)

    # Показ результата
    new_faces = []  # Список для хранения новых лиц
    for face in faces:
        x, y, w, h = face['box']
        # Проверка на корректные размеры лиц
        if w < 10 or h < 10:
            continue  # Пропускаем слишком маленькие лица

        face_resized = cv2.resize(img_rgb[y:y + h, x:x + w], (100, 100))  # Приведение лица к фиксированному размеру

        # Проверка на совпадение с известными лицами
        match_found = False
        for known_face in known_faces:
            if np.linalg.norm(face_resized - known_face) < 2000:  # Сравнение по Евклидовой норме
                match_found = True
                break

        # Добавление нового лица в базу, если оно неизвестно
        if not match_found:
            known_faces.append(face_resized)
            new_faces.append(face)

    # Возвращаем количество лиц
    return len(new_faces)


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

    # Устанавливаем размер окна и позицию в центре экрана
    window_width, window_height = 400, 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_x = (screen_width - window_width) // 2
    position_y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

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

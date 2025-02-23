import tkinter as tk
from tkinter import messagebox
import re

# Определение данных для чисел
tens = {
    "zwanzig": 20, "dreissig": 30, "vierzig": 40, "funfzig": 50,
    "sechzig": 60, "siebzig": 70, "achtzig": 80, "neunzig": 90
}

from_10_to_19 = {
    "zehn": 10, "elf": 11, "zwolf": 12, "dreizehn": 13, "vierzehn": 14,
    "funfzehn": 15, "sechzehn": 16, "siebzehn": 17, "achtzehn": 18, "neunzehn": 19
}

units = {
    "ein": 1, "eins": 1, "zwei": 2, "drei": 3, "vier": 4,
    "funf": 5, "sechs": 6, "sieben": 7, "acht": 8, "neun": 9
}

zero = {
    "null": 0
}


# Функция для преобразования текста в число
def parse_number(text: str):
    number = 0
    exam = ""
    previous_category = None  # Переменная для отслеживания категории предыдущего слова

    for part in text.lower().strip().split():
        if previous_category in ["zero"]:
            raise ValueError("После нуля ничего быть не может.")

        elif part == "und":
            if previous_category == "hundreds":
                raise ValueError("После hundert не может идти und.")
            if not previous_category or (previous_category in ["hundreds", "tens", "from_10_to_19"]):
                raise ValueError("Перед und должны быть единицы.")
            if exam == "eins":
                raise ValueError("eins перед und недопустим")
            if previous_category in ["und"]:
                raise ValueError("und не может идти после другого und.")
            previous_category = "und"


        elif part == "hundert":
            if not previous_category or (previous_category in ["tens", "from_10_to_19", "und"]):
                raise ValueError("Перед hundert должны быть числа от 1 до 9.")
            if exam == "eins":
                raise ValueError("eins перед hundert недопустим")
            if number >= 100:
                raise ValueError("Сотни не могут идти после других сотен.")
            number *= 100
            previous_category = "hundreds"

        elif part in tens:
            if previous_category and (previous_category in ["tens"]):
                raise ValueError("Десятки не могут идти после других десятков.")
            if previous_category and (previous_category in ["from_10_to_19"]):
                raise ValueError("Десятки могут идти только вместо чисел от 10 до 19.")
            if previous_category and previous_category not in ["hundreds", "und"]:
                raise ValueError("Десятки должны идти отдельно или после und или hundreds.")

            number += tens[part]
            previous_category = "tens"

        elif part in from_10_to_19:
            if previous_category and (previous_category in ["units", "tens", "und"]):
                raise ValueError("Числа от 10 до 19 могут идти только после сотен.")
            if previous_category and (previous_category in ["from_10_to_19"]):
                raise ValueError("Числа от 10 до 19 не могут идти после других чисел от 10 до 19.")
            number += from_10_to_19[part]
            previous_category = "from_10_to_19"

        elif part in units:
            if previous_category and (previous_category in ["tens", "und"]):
                raise ValueError("Числа единичного формата не могут идти после und.")
            if previous_category and (previous_category in ["units"]):
                raise ValueError("Единицы не могут идти после других единиц.")
            if previous_category and (previous_category in ["from_10_to_19"]):
                raise ValueError("Числа от 1 до 9 могут идти только вместо чисел от 10 до 19.")
            number += units[part]
            previous_category = "units"
            exam = part

        elif part in zero:
            if previous_category:
                raise ValueError("Перед нулем ничего быть не может.")
            previous_category = "zero"

        else:
            raise ValueError(f"Некорректное слово: {part}, перепишите и попробуйте снова")

    if previous_category and previous_category == "und":
        raise ValueError("und не может быть последним словом")

    return number



# Функция конвертации
def convert(text: str):
    try:
        return parse_number(text)
    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))


# Основной интерфейс
root = tk.Tk()
root.title("Конвертер чисел на немецком языке")
root.geometry("600x300")

# Заголовок с пояснением
instruction_label = tk.Label(root, text="Введите число на немецком языке:", font=("Arial", 14))
instruction_label.pack(pady=10)

# Поле ввода текста
Entry = tk.Entry(root, width=55, font=("Consolas", 18))
Entry.pack(pady=10)
Entry.focus_set()

# Кнопка "Конвертировать" на русском
button = tk.Button(root, text="Конвертировать", font=("Arial", 16), command=lambda: label.configure(text=convert(Entry.get())))
button.pack(pady=10)

# Место для вывода результата
label = tk.Label(root, font=("Arial", 14))
label.pack(pady=10)

root.resizable(False, False)
root.mainloop()
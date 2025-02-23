import tkinter as tk
from tkinter import font

# Расширенный словарь для преобразования немецких чисел в числовой формат
num_dict = {
    'null': 0, 'eins': 1, 'zwei': 2, 'drei': 3, 'vier': 4, 'fünf': 5,
    'sechs': 6, 'sieben': 7, 'acht': 8, 'neun': 9, 'zehn': 10,
    'elf': 11, 'zwölf': 12, 'dreizehn': 13, 'vierzehn': 14, 'fünfzehn': 15,
    'sechzehn': 16, 'siebzehn': 17, 'achtzehn': 18, 'neunzehn': 19,
    'zwanzig': 20, 'dreißig': 30, 'vierzig': 40,св 'fünfzig': 50,
    'sechzig': 60, 'siebzig': 70, 'achtzig': 80, 'neunzig': 90,
    'hundert': 100, 'zweihundert': 200, 'dreihundert': 300,
    'vierhundert': 400, 'fünfhundert': 500, 'sechshundert': 600,
    'siebenhundert': 700, 'achthundert': 800, 'neunhundert': 900
}


def replace_special_chars(event=None):
    """Обработчик событий для замены 1, 2 и 3 на ü, ö и ß, с сохранением позиции курсора."""
    cursor_pos = input_entry.index(tk.INSERT)  # Запоминаем позицию курсора
    text = input_entry.get()
    text = text.replace('1', 'ü').replace('2', 'ö').replace('3', 'ß')
    input_entry.delete(0, tk.END)
    input_entry.insert(0, text)
    input_entry.icursor(cursor_pos)  # Восстанавливаем позицию курсора



def check_format_errors(words):
    """Проверка ошибок формата по указанным правилам."""
    single_digit = {key: val for key, val in num_dict.items() if val < 10}
    teens = {key: val for key, val in num_dict.items() if 10 <= val < 20}
    tens = {key: val for key, val in num_dict.items() if 20 <= val < 100}

    # Проверка: "und" не должно быть последним словом
    if "und" in words and words[-1] == "und":
        return "Слово 'und' не может быть последним в строке"

    for i in range(len(words) - 1):
        current_word = words[i]
        next_word = words[i + 1]

        # Проверка: после десятков не могут идти десятки
        if current_word in tens and next_word in tens:
            return "После десятков не могут идти десятки"
        # Проверка: после единиц не могут идти единицы
        elif current_word in single_digit and next_word in single_digit:
            return "После единиц не могут идти единицы"
        # Проверка: после десятков не могут идти числа 10-19
        elif current_word in tens and next_word in teens:
            return "После десятков не могут идти числа формата 10-19"
        # Проверка: после чисел 10-19 не могут идти десятки
        elif current_word in teens and next_word in tens:
            return "После чисел формата 10-19 не могут идти десятки"
        # Проверка: после единиц не могут идти числа 10-19
        elif current_word in single_digit and next_word in teens:
            return "После единиц не могут идти числа формата 10-19"
        # Проверка: после чисел 10-19 не могут идти единицы
        elif current_word in teens and next_word in single_digit:
            return "После чисел формата 10-19 не могут идти единицы"
        # Проверка: после десятков не может идти "und" и единица
        # Проверка: после десятков не может идти "und" и единица
        elif current_word in tens and i + 2 < len(words) and words[i + 1] == "und" and words[i + 2] in single_digit:
            return "После десятков не может идти 'und' и единица"

    return None


def parse_number(text):
    """Конвертирует введённое число словами в числовой формат."""
    words = text.split()
    total = 0
    current = 0

    for word in words:
        if word in num_dict:
            value = num_dict[word]
            if value == 100:  # Если слово "hundert", умножаем текущую часть
                current *= value
            else:
                current += value
        elif word == 'und':  # Пропускаем "und" как соединительное слово
            continue
        else:
            return "Ошибка: неизвестное слово"

        if current >= 100:  # Если достигли сотни, добавляем к общему результату
            total += current
            current = 0

    total += current  # Добавляем оставшееся число
    return total


def convert_to_number():
    """Конвертирует введённое число словами в числовой формат с проверкой ошибок."""
    text = " ".join(input_entry.get().lower().strip().split())
    words = text.split()
    errors = check_format_errors(words)
    if errors:
        result_label.config(text=f"Ошибка: {errors}")
        return
    result = parse_number(text)
    result_label.config(text=f"Результат: {result}")


# Создание основного окна
root = tk.Tk()
root.title("Конвертер чисел на немецком")
root.geometry("500x300")  # Увеличение размера окна

# Настройка шрифта
app_font = font.Font(family="Helvetica", size=14)  # Задание размера шрифта

# Поле для ввода
input_label = tk.Label(root, text="Введите число на немецком (1=ü, 2=ö, 3=ß):", font=app_font)
input_label.pack(pady=10)
input_entry = tk.Entry(root, font=app_font, width=40)
input_entry.pack(pady=10)
input_entry.bind("<KeyRelease>", replace_special_chars)

# Кнопка для конвертации
convert_button = tk.Button(root, text="Конвертировать", command=convert_to_number, font=app_font)
convert_button.pack(pady=10)

# Метка для результата
result_label = tk.Label(root, text="Результат: ", font=app_font)
result_label.pack(pady=10)

# Запуск приложения
root.mainloop()

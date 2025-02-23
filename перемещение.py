import tkinter as tk
from tkinter import messagebox

def move_words_to_beginning():
    text = text_input.get("1.0", tk.END).strip()
    try:
        x1 = int(input_x1.get())
        x2 = int(input_x2.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числовые значения для x1 и x2.")
        return

    words = text.split()

    if x2 > len(words):
        messagebox.showerror("Ошибка", "Значение x2 больше количества слов в тексте.")
        return

    if x1 < 1:
        messagebox.showerror("Ошибка", "Значение x1 не может быть отрицательным или равным нулю.")
        return

    if x2 < 1:
        messagebox.showerror("Ошибка", "Значение x2 не может быть отрицательным или равным нулю.")
        return

    if x1 > x2:
        messagebox.showerror("Ошибка", "Значение x1 не может быть больше значения x2.")
        return

    selected_words = words[x1 - 1:x2]
    remaining_words = words[:x1 - 1] + words[x2:]

    new_text = ' '.join(selected_words + remaining_words)
    result_output.config(state=tk.NORMAL)
    result_output.delete("1.0", tk.END)
    result_output.insert(tk.END, new_text)
    result_output.config(state=tk.DISABLED)

# Создание окна
window = tk.Tk()
window.title("Move Words to Beginning")
window.geometry("500x350")

# Поле для ввода текста
label_text = tk.Label(window, text="Введите текст:")
label_text.pack()

text_input = tk.Text(window, height=5, width=50)
text_input.pack()

# Поля для ввода x1 и x2
label_x1 = tk.Label(window, text="Введите x1:")
label_x1.pack()

input_x1 = tk.Entry(window)
input_x1.pack()

label_x2 = tk.Label(window, text="Введите x2:")
label_x2.pack()

input_x2 = tk.Entry(window)
input_x2.pack()

# Кнопка для выполнения операции
button = tk.Button(window, text="Переместить слова", command=move_words_to_beginning)
button.pack(pady=10)

# Поле для вывода результата
result_output = tk.Text(window, height=5, width=50, state=tk.DISABLED)
result_output.pack()

# Запуск окна
window.mainloop()
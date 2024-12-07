import tkinter as tk
from tkinter import *

class DraggableLabel(tk.Label):
    def __init__(self, master, text):
        super().__init__(master, text=text, relief="raised", width=20, bg="lightblue", font=("Arial", 12))
        self.text = text
        self.bind("<Button-1>", self.start_drag)
        self.bind("<B1-Motion>", self.do_drag)

    def start_drag(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def do_drag(self, event):
        x = self.winfo_x() + event.x - self.offset_x
        y = self.winfo_y() + event.y - self.offset_y
        self.place(x=x, y=y)

class Game:
    def __init__(self, master):
        self.master = master
        self.master.title("Обучение Python")
        self.master.geometry("800x600")
        self.master.configure(bg="lightgray")

        self.levels = [self.level1]
        self.current_level = 0

        self.start_button = tk.Button(master, text="Играть", command=self.start_game, font=("Arial", 14), bg="lightgreen")
        self.start_button.pack(pady=20)

        self.level_selection = tk.Frame(master, bg="lightgray")
        self.level_selection.pack(pady=20)

        self.level_buttons = []

        for i in range(len(self.levels)):
            label = tk.Label(self.level_selection, text=f"Уровень {i + 1}", font=("Arial", 12))
            label.grid(row=0, column=i, padx=5)

    def start_game(self):
        self.start_button.pack_forget()
        self.levels[self.current_level]()

    def load_level(self, level_index):
        self.current_level = level_index
        self.clear_level()
        self.levels[self.current_level]()

    def clear_level(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.start_button.pack_forget()
        self.level_selection.pack()

    def level1(self):
        self.level_window = tk.Frame(self.master, bg="lightgray")
        self.level_window.pack(pady=20)

        self.code_parts = [
            "print(",
            '"Hello, world"',
            ")"
        ]

        self.correct_code = 'print("Hello, world")'

        self.labels = []
        for i, part in enumerate(self.code_parts):
            label = DraggableLabel(self.level_window, part)
            label.grid(row=i, column=0, padx=10, pady=5)
            self.labels.append(label)

        # Кнопка проверки кода
        self.submit_button = tk.Button(self.level_window, text="Проверить", command=self.check_code, font=("Arial", 12), bg="lightblue")
        self.submit_button.grid(row=len(self.code_parts), column=0, pady=20)

        # Поле ввода кода
        self.code_input = tk.Entry(self.level_window, width=50, font=("Arial", 14))
        self.code_input.grid(row=len(self.code_parts) + 1, column=0, pady=10)

        # Метка для вывода результата
        self.result_label = tk.Label(self.level_window, text="", font=("Arial", 12), bg="lightgray")
        self.result_label.grid(row=len(self.code_parts) + 2, column=0, pady=10)

        # Добавляем возможность перетаскивать части кода в поле ввода
        for label in self.labels:
            label.bind("<Button-1>", self.add_to_code)

    def add_to_code(self, event):
        part = event.widget.text
        current_code = self.code_input.get()
        self.code_input.delete(0, tk.END)  # Очищаем поле ввода
        self.code_input.insert(tk.END, current_code + part)  # Добавляем перетаскиваемую часть

    def check_code(self):
        if self.code_input.get() == self.correct_code:
            self.result_label.config(text="Вы правильно собрали код!", fg="green")
            self.show_back_button()  # Показать кнопку "Назад на главную"
        else:
            self.result_label.config(text="Попробуйте снова!", fg="red")

    def show_back_button(self):
        self.back_button = tk.Button(self.level_window, text="Назад на главную", command=self.back_to_main, font=("Arial", 12), bg="lightcoral")
        self.back_button.grid(row=len(self.code_parts) + 3, column=0, pady=10)

    def back_to_main(self):
        print("Потом")

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.geometry("1920x960")
    root.mainloop()
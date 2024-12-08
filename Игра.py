import tkinter as tk
from tkinter import messagebox, ttk, simpledialog, filedialog
import sqlite3
import random
import hashlib
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import uuid
import json
import base64


class LearningGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Образовательная платформа: Программирование и Электроника")
        self.master.geometry("1400x900")
        self.master.configure(bg="#F0F4F8")

        # Защита личных данных
        self.current_user = None
        self.session_token = None

        # Инициализация базы данных
        self.init_database()

        # Уровни для программирования
        self.programming_levels = [
            {
                "id": 1,
                "name": "Привет, Мир!",
                "description": "Научись выводить первое сообщение",
                "theory": "В программировании первая программа - вывод текста на экран. Print() - это функция для вывода.",
                "static_parts": [
                    {"text": "print(", "type": "function"},
                    {"text": '"Hello, World!"', "type": "string"},
                    {"text": ")", "type": "close"}
                ],
                "correct_code": 'print("Hello, World!")',
                "hint": "Помести текст в кавычки внутри print()"
            },
            {
                "id": 2,
                "name": "Переменные",
                "description": "Создай и выведи переменную",
                "theory": "Переменные - это контейнеры для хранения данных. Они имеют имя и значение.",
                "static_parts": [
                    {"text": "age =", "type": "variable"},
                    {"text": "25", "type": "number"},
                    {"text": "\nprint(age)", "type": "output"}
                ],
                "correct_code": "age = 25\nprint(age)",
                "hint": "Сначала создай переменную, потом выведи её"
            },
            # Добавить еще уровней...
        ]

        # Уровни для электроники
        self.electronics_levels = [
            {
                "id": 1,
                "name": "Основы электрической цепи",
                "description": "Создание простой последовательной цепи",
                "theory": """
                Электрическая цепь - замкнутый путь протекания электрического тока.
                Основные компоненты:
                1. Источник питания (батарея)
                2. Проводники
                3. Нагрузка (лампочка, резистор)
                """,
                "task": "Нарисуйте принципиальную схему последовательной цепи с батареей и лампочкой",
                "correct_solution": "Батарея -> Провод -> Лампочка -> Провод -> Батарея"
            },
            # Добавить еще уровней...
        ]

        # Пользовательские задания
        self.custom_levels = []

        # Текущие уровни и тема
        self.current_levels = self.programming_levels
        self.current_topic = "Программирование"
        self.current_level_index = 0

        self.create_login_screen()

    def show_theory_screen(self, level):
        """Экран для отображения теоретической части уровня"""
        for widget in self.master.winfo_children():
            widget.destroy()

        theory_frame = tk.Frame(self.master, bg="#F0F4F8")
        theory_frame.pack(expand=True, fill="both", padx=20, pady=20)

        tk.Label(theory_frame, text=f"Теория: {level['name']}", font=("Arial", 18, "bold"), bg="#F0F4F8").pack(pady=20)

        theory_text = tk.Text(theory_frame, wrap="word", font=("Arial", 14), bg="#F0F4F8", relief="flat", height=15)
        theory_text.insert("1.0", level["theory"])
        theory_text.config(state="disabled")  # Делает текстовое поле только для чтения
        theory_text.pack(padx=20, pady=20, fill="both", expand=True)

        # Кнопки для управления
        button_frame = tk.Frame(theory_frame, bg="#F0F4F8")
        button_frame.pack(pady=10, fill="x")  # Используем fill="x", чтобы растянуть кнопки по ширине

        # Кнопка "Главное меню"
        main_menu_button = tk.Button(button_frame, text="Главное меню", font=("Arial", 14),
                                     bg="#F39C12", fg="white", command=self.create_start_menu)
        main_menu_button.pack(side="left", padx=10)

        # Кнопка "Далее"
        next_button = tk.Button(button_frame, text="Далее", font=("Arial", 14),
                                bg="#2ECC71", fg="white", command=lambda: self.start_level())
        next_button.pack(side="right", padx=10)


    def create_login_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        login_frame = tk.Frame(self.master, bg="#F0F4F8")
        login_frame.pack(expand=True, fill='both', padx=20, pady=20)

        tk.Label(login_frame, text="Образовательная платформа",
                 font=("Arial", 24, "bold"), bg="#F0F4F8").pack(pady=20)

        username_label = tk.Label(login_frame, text="Логин:", font=("Arial", 14), bg="#F0F4F8")
        username_label.pack()
        username_entry = tk.Entry(login_frame, font=("Arial", 14), width=30)
        username_entry.pack(pady=10)

        password_label = tk.Label(login_frame, text="Пароль:", font=("Arial", 14), bg="#F0F4F8")
        password_label.pack()
        password_entry = tk.Entry(login_frame, show="*", font=("Arial", 14), width=30)
        password_entry.pack(pady=10)

        def login():
            username = username_entry.get()
            password = password_entry.get()
            if self.authenticate_user(username, password):
               self.create_start_menu()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")

        def register():
            username = username_entry.get()
            password = password_entry.get()
            email = simpledialog.askstring("Регистрация", "Введите email:")

            if email and self.register_user(username, password, email):
                messagebox.showinfo("Регистрация", "Пользователь успешно зарегистрирован")
            else:
                messagebox.showerror("Ошибка", "Не удалось зарегистрировать пользователя")

        login_btn = tk.Button(login_frame, text="Войти", command=login,
                              font=("Arial", 14), bg="#3498DB", fg="white")
        login_btn.pack(pady=10)

        register_btn = tk.Button(
            self.master,
            text="Регистрация",
            command=self.register_user,
            font=("Arial", 14),
            bg="#58D68D",
            fg="white"
        )

        register_btn.pack(pady=10)

    def authenticate_user(self, username, password):
        """Аутентификация пользователя"""
        try:
            # Поиск пользователя в базе данных
            self.cursor.execute("SELECT password_hash, salt FROM users WHERE username = ?", (username,))
            user_data = self.cursor.fetchone()

            if not user_data:
                messagebox.showerror("Ошибка", "Пользователь с таким именем не найден.")
                return False

            stored_password_hash, salt = user_data

            # Проверка введённого пароля
            import hashlib
            input_password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()

            if input_password_hash == stored_password_hash:
                self.current_user = username
                messagebox.showinfo("Успех", f"Добро пожаловать, {username}!")
                return True
            else:
                messagebox.showerror("Ошибка", "Неверный пароль.")
                return False
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
            return False


    def create_start_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        start_frame = tk.Frame(self.master, bg="#F0F4F8")
        start_frame.pack(expand=True, fill='both', padx=20, pady=20)

        tk.Label(start_frame, text=f"Добро пожаловать, {self.current_user}!",
                 font=("Arial", 24, "bold"), bg="#F0F4F8").pack(pady=20)

        def select_programming():
            self.current_levels = self.programming_levels
            self.current_topic = "Программирование"
            self.start_level(0)

        def select_electronics():
            self.current_levels = self.electronics_levels
            self.current_topic = "Электроника"
            self.start_level(0)

        def show_custom_levels():
            self.show_custom_level_menu()

        def show_progress():
            self.show_user_progress()

        programming_btn = tk.Button(start_frame, text="Программирование",
                                    command=select_programming,
                                    font=("Arial", 16), bg="#3498DB", fg="white")
        programming_btn.pack(pady=10, fill='x')

        electronics_btn = tk.Button(start_frame, text="Электроника",
                                    command=select_electronics,
                                    font=("Arial", 16), bg="#2ECC71", fg="white")
        electronics_btn.pack(pady=10, fill='x')

        custom_levels_btn = tk.Button(start_frame, text="Пользовательские задания",
                                      command=show_custom_levels,
                                      font=("Arial", 16), bg="#9B59B6", fg="white")
        custom_levels_btn.pack(pady=10, fill='x')

        progress_btn = tk.Button(start_frame, text="Мой прогресс",
                                 command=show_progress,
                                 font=("Arial", 16), bg="#F39C12", fg="white")
        progress_btn.pack(pady=10, fill='x')

        logout_btn = tk.Button(start_frame, text="Выйти",
                               command=self.create_login_screen,
                               font=("Arial", 16), bg="#E74C3C", fg="white")
        logout_btn.pack(pady=10, fill='x')

    def start_programming_level(self):
        """Начало уровня программирования"""
        self.current_levels = self.programming_levels
        self.current_level_index = 0
        self.start_level()

    def start_electronics_level(self):
        """Начало уровня электроники"""
        self.current_levels = self.electronics_levels
        self.current_level_index = 0
        self.start_level()

    def start_level(self, level_index):
        """Запуск уровня: сначала показываем теорию, потом задание"""
        self.current_level_index = level_index
        level = self.current_levels[level_index]

        # Показ теоретической части
        self.show_theory_screen(level)
        #
        # for widget in self.master.winfo_children():
        #     widget.destroy()
        #
        # level_frame = tk.Frame(self.master, bg="#F0F4F8")
        # level_frame.pack(expand=True, fill='both', padx=20, pady=20)
        #
        # tk.Label(level_frame,
        #          text=f"{self.current_topic}: Уровень {level['id']} - {level['name']}",
        #          font=("Arial", 20, "bold"), bg="#F0F4F8").pack(pady=10)
        #
        # tk.Label(level_frame, text=level['description'],
        #          font=("Arial", 14), bg="#F0F4F8").pack(pady=5)
        #
        # # Теоретическая часть
        # theory_text = tk.Text(level_frame, height=5, width=80,
        #                       font=("Arial", 12), wrap=tk.WORD)
        # theory_text.insert(tk.END, level.get('theory', 'Теория отсутствует'))
        # theory_text.config(state=tk.DISABLED)
        # theory_text.pack(pady=10)
        #
        # # Реализация для разных типов уровней
        # if self.current_topic == "Программирование":
        #     self.create_programming_level_ui(level_frame, level)
        # else:
        #     self.create_electronics_level_ui(level_frame, level)


    def create_programming_level_ui(self, frame, level):
        # UI для уровней программирования с кодом
        code_input = tk.Text(frame, height=5, width=50, font=("Consolas", 12))
        code_input.pack(pady=10)

        def check_code():
            user_code = code_input.get("1.0", tk.END).strip()
            if user_code == level['correct_code']:
                self.update_level_progress(True)
                messagebox.showinfo("Успех", "Уровень пройден!")
                if self.current_level_index < len(self.current_levels) - 1:
                    self.start_level(self.current_level_index + 1)
            else:
                messagebox.showwarning("Ошибка", level.get('hint', 'Попробуйте еще раз'))

        tk.Button(frame, text="Проверить", command=check_code,
                  font=("Arial", 14), bg="#2ECC71", fg="white").pack(pady=10)

    def create_electronics_level_ui(self, frame, level):
        # UI для уровней электроники с текстовым вводом
        solution_input = tk.Text(frame, height=5, width=50, font=("Arial", 12))
        solution_input.pack(pady=10)

        def check_solution():
            user_solution = solution_input.get("1.0", tk.END).strip()
            if user_solution == level['correct_solution']:
                self.update_level_progress(True)
                messagebox.showinfo("Успех", "Уровень пройден!")
                if self.current_level_index < len(self.current_levels) - 1:
                    self.start_level(self.current_level_index + 1)
            else:
                messagebox.showwarning("Ошибка", "Неверное решение")

        tk.Button(frame, text="Проверить", command=check_solution,
                  font=("Arial", 14), bg="#2ECC71", fg="white").pack(pady=10)

    def update_level_progress(self, completed):
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO user_progress 
                (username, topic, level_id, completed, attempts) VALUES 
                (?, ?, ?, ?, COALESCE(
                    (SELECT attempts FROM user_progress 
                     WHERE username = ? AND topic = ? AND level_id = ?) + 1, 
                    1)
                )
            ''', (
                self.current_user, self.current_topic,
                self.current_levels[self.current_level_index]['id'],
                1 if completed else 0,
                self.current_user, self.current_topic,
                self.current_levels[self.current_level_index]['id']
            ))
            self.conn.commit()
        except Exception as e:
            print(f"Ошибка обновления прогресса: {e}")

    def show_user_progress(self):
        progress_window = tk.Toplevel(self.master)
        progress_window.title("Мой прогресс")
        progress_window.geometry("800x600")

        # Получение прогресса
        self.cursor.execute('''
            SELECT topic, level_id, completed 
            FROM user_progress 
            WHERE username = ?
        ''', (self.current_user,))
        progress_data = self.cursor.fetchall()

        # Создание графика
        plt.figure(figsize=(10, 6))
        topics = {}
        for topic, _, completed in progress_data:
            topics[topic] = topics.get(topic, 0) + completed

        plt.bar(topics.keys(), topics.values())
        plt.title("Прогресс по темам")
        plt.xlabel("Темы")
        plt.ylabel("Пройденные уровни")

        canvas = FigureCanvasTkAgg(plt.gcf(), master=progress_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def show_custom_level_menu(self):
        custom_window = tk.Toplevel(self.master)
        custom_window.title("Пользовательские задания")
        custom_window.geometry("600x400")

        def create_custom_level():
            custom_level = {
                "id": len(self.custom_levels) + 1,
                "name": simpledialog.askstring("Новое задание", "Название задания:"),
                "description": simpledialog.askstring("Новое задание", "Описание задания:"),
                "theory": simpledialog.askstring("Новое задание", "Теоретическая часть:"),
                "topic": "Пользовательское"
            }

            if self.current_topic == "Программирование":
                custom_level["correct_code"] = simpledialog.askstring("Новое задание", "Правильный код:")
            else:
                custom_level["correct_solution"] = simpledialog.askstring("Новое задание", "Правильное решение:")

            self.custom_levels.append(custom_level)
            messagebox.showinfo("Успех", "Задание создано!")
            self.refresh_custom_levels()

    def start_custom_level(level):
            self.current_levels = [level]
            self.current_topic = level.get("topic", "Пользовательское")
            self.start_level(0)

            def start_custom_level(level):
                self.current_levels = [level]
                self.current_topic = level.get("topic", "Пользовательское")
                self.start_level(0)

            create_btn = tk.Button(custom_window, text="Создать задание",
                                   command=create_custom_level,
                                   font=("Arial", 14), bg="#3498DB", fg="white")
            create_btn.pack(pady=10)

            levels_frame = tk.Frame(custom_window)
            levels_frame.pack(fill='both', expand=True, padx=20, pady=10)

            def refresh_custom_levels():
                for widget in levels_frame.winfo_children():
                    widget.destroy()

                for level in self.custom_levels:
                    level_btn = tk.Button(
                        levels_frame,
                        text=f"{level['name']} ({level.get('topic', 'Пользовательское')})",
                        command=lambda l=level: start_custom_level(l),
                        font=("Arial", 12)
                    )
                    level_btn.pack(fill='x', pady=5)

            self.refresh_custom_levels = refresh_custom_levels
            refresh_custom_levels()

    def init_database(self):
        # Предыдущая реализация метода осталась без изменений
        # Подключение к базе данных
        self.conn = sqlite3.connect('learning_platform.db')
        self.cursor = self.conn.cursor()

        # Таблица пользователей с безопасным хэшированием паролей
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password_hash TEXT,
                    salt TEXT,
                    email TEXT
                )
            ''')

        # Таблица прогресса
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_progress (
                    username TEXT,
                     topic TEXT,
                     level_id INTEGER,
                     completed INTEGER DEFAULT 0,
                       score REAL DEFAULT 0,
                    attempts INTEGER DEFAULT 0,
                    FOREIGN KEY(username) REFERENCES users(username),
                    PRIMARY KEY(username, topic, level_id)
                )
            ''')

        # Таблица для пользовательских заданий
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS custom_levels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    name TEXT,
                    description TEXT,
                    theory TEXT,
                    topic TEXT,
                    correct_solution TEXT,
                    FOREIGN KEY(username) REFERENCES users(username)
                )
            ''')
        self.conn.commit()

    def register_user(self):
        """Регистрация нового пользователя"""
        username = simpledialog.askstring("Регистрация", "Введите имя пользователя:")
        email = simpledialog.askstring("Регистрация", "Введите вашу электронную почту:")
        password = simpledialog.askstring("Регистрация", "Введите пароль:", show="*")
        confirm_password = simpledialog.askstring("Регистрация", "Подтвердите пароль:", show="*")

        if not username or not email or not password:
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения.")
            return

        if password != confirm_password:
            messagebox.showerror("Ошибка", "Пароли не совпадают.")
            return

        # Генерация соли и хэширование пароля
        import hashlib, os
        salt = os.urandom(16).hex()
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()

        try:
            self.cursor.execute('''
                INSERT INTO users (username, password_hash, salt, email)
                VALUES (?, ?, ?, ?)
            ''', (username, password_hash, salt, email))
            self.conn.commit()
            messagebox.showinfo("Успех", "Регистрация завершена! Теперь вы можете войти.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует.")
        try:
            self.cursor.execute('''
                    INSERT INTO users (username, password_hash, salt, email)
                    VALUES (?, ?, ?, ?)
                ''', (username, key, salt, email))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def save_custom_level_to_database(self, level):
            """Сохранение пользовательского задания в базу данных"""
            try:
                self.cursor.execute('''
                        INSERT INTO custom_levels 
                        (username, name, description, theory, topic, correct_solution) 
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                    self.current_user,
                    level['name'],
                    level.get('description', ''),
                    level.get('theory', ''),
                    level.get('topic', 'Пользовательское'),
                    level.get('correct_solution', '') or level.get('correct_code', '')
                ))
                self.conn.commit()
                return True
            except Exception as e:
                print(f"Ошибка сохранения задания: {e}")
                return False

    def load_custom_levels(self):
            """Загрузка пользовательских заданий из базы данных"""
            try:
                self.cursor.execute('''
                        SELECT name, description, theory, topic, correct_solution 
                        FROM custom_levels 
                        WHERE username = ?
                    ''', (self.current_user,))
                custom_levels = self.cursor.fetchall()

                self.custom_levels = [
                    {
                        "id": idx + 1,
                        "name": level[0],
                        "description": level[1],
                        "theory": level[2],
                        "topic": level[3],
                        "correct_solution": level[4]
                    } for idx, level in enumerate(custom_levels)
                ]
            except Exception as e:
                print(f"Ошибка загрузки заданий: {e}")

def main():
    root = tk.Tk()
    game = LearningGame(root)
    game.init_database()
    root.mainloop()

if __name__ == "__main__":
    main()
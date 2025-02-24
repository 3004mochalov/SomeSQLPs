import tkinter as tk
from tkinter import messagebox
import psycopg2

def connect_db():
    return psycopg2.connect(
        dbname="users",
        user="postgres",
        password="4134",
        host="localhost",
        port="1337"
    )

def register_user():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Ошибка", "Пожалуйста, введите имя пользователя и пароль.")
        return

    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        messagebox.showinfo("Успех", "Регистрация прошла успешно!")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))
    finally:
        cur.close()
        conn.close()

def login_user():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Ошибка", "Пожалуйста, введите имя пользователя и пароль.")
        return

    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cur.fetchone()
        if result and result[0] == password:
            messagebox.showinfo("Успех", "Вход выполнен успешно!")
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль.")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))
    finally:
        cur.close()
        conn.close()

# Создание интерфейса
root = tk.Tk()
root.title("Регистрация и вход")

# Поля ввода
label_username = tk.Label(root, text="Имя пользователя:")
label_username.pack()
entry_username = tk.Entry(root)
entry_username.pack()

label_password = tk.Label(root, text="Пароль:")
label_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

# Кнопки
button_register = tk.Button(root, text="Зарегистрироваться", command=register_user)
button_register.pack()

button_login = tk.Button(root, text="Войти", command=login_user)
button_login.pack()

# Запуск приложения
root.mainloop()
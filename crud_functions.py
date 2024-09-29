import sqlite3


def initiate_db():
    connection = sqlite3.connect("bd.db")     # подключение к базе данных
    cursor = connection.cursor()    # создание курсора
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_title ON Products (title)")     # создание индекса
    cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                   ("5w20", "maxima_5w20_5l", "100"))    # добавление данных
    cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                   ("10w30", "maxima_10w30_5l", "200"))    # добавление данных
    cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                   ("10w40_plus", "maxima_10w40_plus_5l", "300"))    # добавление данных
    cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                   ("auto_lpg_10w40", "maxima_auto_lpg_10w40_4l", "400"))    # добавление данных

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users (email)")     # создание индекса
    connection.commit()     # подключение
    connection.close()      # закрываем подключение


def add_user(username, email, age):
    connection = sqlite3.connect("bd.db")     # подключение к базе данных
    cursor = connection.cursor()    # создание курсора
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (f"{username}", f"{email}", f"{age}", "1000"))    # добавление данных
    connection.commit()     # подключение


def is_included(username):
    connection = sqlite3.connect("bd.db")     # подключение к базе данных
    cursor = connection.cursor()    # создание курсора
    users_list = cursor.execute("SELECT * FROM Users")
    name_f = 0
    for user in users_list:
        if username == user[1]:
            name_f = 1
    return name_f


def get_all_products():     # возвращает все записи из таблицы
    connection = sqlite3.connect('bd.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    all_entries = cursor.fetchall()
    return all_entries

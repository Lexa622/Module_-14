import sqlite3

connection = sqlite3.connect("not_telegram.db")     # подключение к базе данных
cursor = connection.cursor()    # создание курсора
"""Для создания базы данных мы должны указать некоторую табличку. Для этого мы пишем «CREATE TABLE»
и ещё добавим одну проверку «IF NOT EXISTS», чтобы мы с вами случайно ничего не сломали.
И дальше пишем название нашей таблички «Users» («CREATE» это создание таблицы, если её не существует)
Укажем поля «id», «username», «email» и «age». Но этого на самом деле недостаточно.
Давайте мы с вами ещё одну вещь добавим. А именно то, какого они будут типа.
«id» это у нас целый тип данных «INTEGER», то есть просто число.
И мы ему ещё добавляем специальный ключ «PRIMARY KEY», чтобы мы понимали, что это просто номер.
«username»- это у нас текстовый тип «TEXT». И для того, чтобы мы точно знали, что поле не пустое,
указываем, что это поле не может быть пустым, пишем «NOT NULL». С «email» то же самое «TEXT NOT NULL».
А с возрастом мы можем позволить, чтобы оно было пустым, поэтому делаем просто «INTEGER»"""
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
""")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users (email)")     # создание индекса
for i in range(1, 11):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (f"User{i}", f"example{i}@gmail.com", f"{i * 10}", "1000"))    # добавление кучей данных
for i in range(1, 11):
    cursor.execute("UPDATE Users SET balance = ? WHERE id % 2", (500, ))  # обновление данных ячеек
for i in range(1, 11, 3):
    cursor.execute("DELETE FROM Users WHERE username = ?", (f"User{i}",))  # удаление данных
cursor.execute("SELECT username, email, age, balance FROM Users WHERE not age == ?", (60,))
users = cursor.fetchall()
for user in users:
    print(f"Имя: {user[0]} | Почта: {user[1]} | Возраст: {user[2]} | Баланс: {user[3]}")
connection.commit()     # подключение
connection.close()      # закрываем подключение

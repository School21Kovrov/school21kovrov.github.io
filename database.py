import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Создаем таблицу Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
org_key TEXT NOT NULL,
fio TEXT NOT NULL,
class TEXT NOT NULL,
login TEXT NOT NULL,
password TEXT NOT NULL,
status BOOLEAN NOT NULL DEFAULT 0
)
''')



connection.commit()
connection.close()
import sqlite3
connect = sqlite3.connect('database.db') # создает подключение к базе данных database.db
cursor = connect.cursor() 

create_tabl_task = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    task TEXT,
    done TEXT
    );
"""
create_tabl_user = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    chat_id INTEGER
    );
"""
cursor.execute(create_tabl_task) # выполняет SQL запрос на создание базы данных
cursor.execute(create_tabl_user)
connect.commit() # Сохранить изменения в базе данных.


def get_user(id):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute("SELECT id FROM users")
    users = cursor.fetchall()
    connect.close()
    return users

def add_task(task):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    connect.commit()
    connect.close()

def get_tasks():
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM tasks")
    task = cursor.fetchall()
    connect.close()
    return task
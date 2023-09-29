import telebot
import sqlite3
from database import add_task, get_tasks, get_user

bot = telebot.TeleBot("6202225034:AAF0vrVfx20dKJxggtY-ZcihVhnXlPDu1uA")

@bot.message_handler(commands=["start"])
def start_handelr(message):
    bot.send_message(chat_id=message.chat.id, text="Бот запущен")

@bot.message_handler(commands=["register"])
def register_handler(message):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    user = (message.from_user.first_name, message.from_user.id)
    cursor.execute("INSERT INTO users (name, chat_id) VALUES (?, ?)", user)
    connect.commit()
    connect.close()
    bot.reply_to(message, "Вы зарегистрированы")

@bot.message_handler(commands=['del'])
def deletetask_handler(message):
    
    try:

        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        chat_id = (message.from_user.id,)
        cursor.execute("SELECT * FROM users WHERE chat_id=?", chat_id)
        user = cursor.fetchone()
        if user is None:
            bot.reply_to(message, "Вы не зарегистрированы в системе!")
        else:
            task_id = message.text.split("/del")[1]
            task_id = (int(task_id),)
            user = (int(user[0]),)
            cursor.execute("SELECT * FROM tasks WHERE id=? AND user_id=?", task_id + user)
            task = cursor.fetchone()
            if task is None:
                bot.reply_to(message, "Такой записи нету")
            else:
                cursor.execute("DELETE FROM tasks WHERE id=?", task_id)
                connect.commit()
                connect.close()
                bot.reply_to(message, "Ваша запись удалина")
    except ValueError:
        bot.reply_to(message, "Вы не ввели номер задачи")

@bot.message_handler(commands=["add"])
def add_task_handler(message):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    chat_id = (message.from_user.id,)
    cursor.execute("SELECT * FROM users WHERE chat_id=?", chat_id)
    user = cursor.fetchone()
    if user is None:
        bot.reply_to(message, "Вы не зареегистрированы")
    else:
        task = message.text.split('/add')[1]
        task_data = (user[0], task, "X")
        cursor.execute("INSERT INTO tasks (user_id, task, done) VALUES (?, ?, ?)", task_data)
        connect.commit()
        bot.reply_to(message, "Задача добавлена.")
    connect.close()


@bot.message_handler(commands=["list"])
def get_tasks_hendler(message):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    chat_id = (message.from_user.id,)
    cursor.execute("SELECT * FROM users WHERE chat_id=?", chat_id)
    user = cursor.fetchone()
    if user is None:
        bot.reply_to(message, 'Ты не зарегистрирован')
    else:
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        if tasks:
            task = ''
            for i in tasks:
                task += f'ID записи: {i[0]}\nОписание задачи: {i[2]}\nСостояние задачи: {i[3]}\n\n'
            bot.reply_to(message, task)
        else:
            bot.reply_to(message, "У вас нет задач")

@bot.message_handler(commands=["win"])
def add_winner_handler(message):
    try:
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        chat_id = (message.from_user.id,)
        cursor.execute("SELECT * FROM users WHERE chat_id=?", chat_id)
        user = cursor.fetchone()
        if user is None:
            bot.reply_to(message, "Вы не зарегистрированы")
        else:
            task_number = message.text.split('/win ')[1]
            try:
                task_number = int(task_number)
            except ValueError:
                bot.reply_to(message, "Введите правильный номер задачи")
                return
            try:
                cursor.execute("SELECT * FROM tasks WHERE id=? AND user_id=?", (task_number, user[0]))
                task = cursor.fetchone()
                if task is None:
                    bot.reply_to(message, "Такой задачи не существует или она не принадлежит вам")
                else:
                    cursor.execute("UPDATE tasks SET done='✓' WHERE id=?", (task_number,))
                    connect.commit()
                    bot.reply_to(message, "Статус задачи изменен.")
            except IndexError:
                bot.reply_to(message, "Вы не ввели ничего или такой задачи нет")
                return
            except:
                bot.reply_to(message, "Произошла ошибка")
                return
        connect.close()
    except:
        bot.reply_to(message, "Произошла ошибка")
    
    
@bot.message_handler(commands=["rout"])
def add_rout_handler(message):
    try:
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        chat_id = (message.from_user.id,)
        cursor.execute("SELECT * FROM users WHERE chat_id=?", chat_id)
        user = cursor.fetchone()
        if user is None:
            bot.reply_to(message, "Вы не зарегистрированы")
        else:
            task_number = message.text.split('/rout ')[1]
            try:
                task_number = int(task_number)
            except ValueError:
                bot.reply_to(message, "Введите правильный номер задачи")
                return
            try:
                cursor.execute("SELECT * FROM tasks WHERE id=? AND user_id=?", (task_number, user[0]))
                task = cursor.fetchone()
                if task is None:
                    bot.reply_to(message, "Такой задачи не существует или она не принадлежит вам")
                else:
                    cursor.execute("UPDATE tasks SET done='X' WHERE id=?", (task_number,))
                    connect.commit()
                    bot.reply_to(message, "Статус задачи изменен.")
            except IndexError:
                bot.reply_to(message, "Вы не ввели ничего или такой задачи нет")
                return
            except:
                bot.reply_to(message, "Произошла ошибка")
                return
        connect.close()
    except:
        bot.reply_to(message, "Произошла ошибка")
  
  
            
    connect.close()

bot.set_my_commands([
    telebot.types.BotCommand("/start", "Перезапустить бота"),
    telebot.types.BotCommand("/list", "Список всех задач"),
    telebot.types.BotCommand("/add", "Добавить задачу"),
    telebot.types.BotCommand("/del", "Удалить задачу - введите номер задач"),
    telebot.types.BotCommand("/win", "Пометить задачу выполненной - введите номер задачи"),
    telebot.types.BotCommand("/rout", "Пометить задачу не выполненной - введите номер задачи"),
    telebot.types.BotCommand("/register", "Зарегистрироваться")
])
    
bot.polling()
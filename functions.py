import mysql.connector
from mysql.connector import Error
from config import *
conn = mysql.connector.connect(host="!", user="!", password="!", database="!")

cursor = conn.cursor()

# general filling function

def all_commands_func(info, some_command, user_id):
    cursor.execute('update ' + table_name + ' set ' + some_command + ' = %s where telegram_id = %s', (info, user_id))
    conn.commit()

# fio delete

def db_fio_del(user_id):
    cursor.execute('update ' + table_name + ' set ФИО = %s where telegram_id = %s', (' ', user_id))
    conn.commit()

#creat basic DataBase table

def db_base_table(telegram_id: str, fio: str, user_name: str, user_surname: str, username: str):
    cursor.execute('INSERT INTO ' + table_name + ' (telegram_id, ФИО, Имя, Фамилия, НИК) VALUES (%s, %s, %s, %s, %s)', (telegram_id, fio, user_name, user_surname, username))
    conn.commit()
#creat DataBase comment collumn

def db_comment_column(comment, user_id):
    cursor.execute('update ' + table_name + ' set Комментарий = %s where telegram_id = %s', (comment, user_id))
    conn.commit()

#creat DataBase photo collumn

def db_photo_column(photo, user_id):
    cursor.execute('update ' + table_name + ' set Фото = %s where telegram_id = %s', (photo, user_id))
    conn.commit()

#comment delete

def db_comment_del(user_id):
    cursor.execute('update ' + table_name + ' set Комментарий = %s where telegram_id = %s', (' ', user_id))   
    conn.commit()

#photo delete

def db_photo_del(user_id):
    cursor.execute('update ' + table_name + ' set Фото = %s where telegram_id = %s', (' ', user_id)) 
    conn.commit()

# delete some column

def db_some_column_delete(data, user_id):
    cursor.execute('update ' + table_name + ' set ' + data + '= %s where telegram_id = %s', (' ', user_id))
    conn.commit()

# delete all

def delete(user_id):
    cursor.execute('DELETE FROM ' + table_name + ' WHERE telegram_id = %s', (user_id, ))
    conn.commit()
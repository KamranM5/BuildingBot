import telebot
from telebot import types
import time
import os
from functions import *
from config import *

bot = telebot.TeleBot(token)

data = """CREATE TABLE IF NOT EXISTS """ + table_name + """(
    id INTEGER NOT NULL PRIMARY KEY DEFAULT 0,
    telegram_id BIGINT PRIMARY KEY ,
    ФМО TEXT,
    Имя text,
    Фамилия text,
    НИК text,
    Комментарий LONGTEXT,
    Фото LONGBLOB,
    """ + data1 + """ LONGTEXT,
    """ + data2 + """ LONGTEXT,
    """ + data3 + """ LONGTEXT,
    """ + data4 + """ LONGTEXT)"""
cursor.execute(data)

def nextStepHandler(message):
    def nextStepHandlerImplementation(func):
        def onMessage(message):
            if message.content_type == 'text' and message.text in commands.values():
                bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
                textMessageHandler(message)
                return
            if func(message):
                bot.register_next_step_handler(message, onMessage)
        bot.register_next_step_handler(message, onMessage)
    return nextStepHandlerImplementation

def createPathIfNotExists(path):
    if not os.path.exists(path):
        os.makedirs(path)
def botPolling():
    while True:
        try:
            print('starting bot...')
            bot.polling(none_stop=True, interval=0.1)
        except Exception as ex:
            print('bot error... restarting...', ex)
            bot.stop_polling()
            time.sleep(0.1)

# cteat commands list

if __name__ == '__main__':
    bot = telebot.TeleBot(token)
    commands = {
        'fio': 'Ввести ФИО',
        'comment': 'Отправить комментарий',
        'delete comment': 'Удалить комментарий',
        'photo': 'Отправить фото',
        'delete photo': 'Удалить фото',
        command1 : button_name1,
        command1_del: button_name1_del,
        command2 : button_name2,
        command2_del: button_name2_del,
        command3 : button_name3,
        command3_del: button_name3_del,
        command4 : button_name4,
        command4_del: button_name4_del,
        'delete all': 'Удалить всё',
    }
    
    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        for value in commands.values():
            markup.row(value)
        bt = types.KeyboardButton(text="Отправить местоположение", request_location=True)
        markup.row(bt)
        textMsg = f'Привет , {message.from_user.first_name} {message.from_user.last_name or ""}. Я - бот от команды университета РИНХ #1. Моя задача - оптимизация и автоматизация процесса внедрения объекта в экплуатацию. Выберите одно из действий из меню'
        bot.send_message(message.chat.id, textMsg, reply_markup=markup)
        
    @bot.message_handler(content_types=['location'])
    def check_location(message):
        loc = message.location
        print(loc)
    
    @bot.message_handler(content_types=['text'])
    def textMessageHandler(message):
        if message.text == commands['fio']:
            bot.send_message(message.chat.id, 'Ожидается ФИО (введите"отмена" - для отмены)')
            @nextStepHandler(message)
            def askForFio(message):
                if message.content_type == 'text' and message.text.lower() == 'отмена':
                    bot.send_message(message.chat.id, 'Действие отменено')
                    return

                if message.content_type != 'text':
                    bot.send_message(message.chat.id, 'Принимается только текст!')
                    return True

                if len(message.text) > 60:
                    bot.send_message(message.chat.id, 'Фио слишком длинное!')
                    return True

                fio = message.text

                db_base_table(message.from_user.id, fio, message.from_user.first_name, message.from_user.last_name, message.from_user.username) # фио успешно записано

                bot.send_message(message.chat.id, 'Здравствуйте, ' + fio)
                
        elif message.text == commands['comment']:
            bot.send_message(message.chat.id, 'Ожидается комментарий (введите "отмена" - для отмены)')
            @nextStepHandler(message)
            def askForComment(message):
                comment = message.text
                if message.content_type == 'text' and message.text.lower() == 'отмена':
                    bot.send_message(message.chat.id, 'Действие отменено!')
                    return

                if message.content_type != 'text':
                    bot.send_message(message.chat.id, 'Принимается только текст!')
                    return True

                db_comment_column(comment, message.from_user.id) # comment was successfully recorded

                bot.send_message(message.chat.id, 'Записано')

        elif message.text == commands['delete comment']:
            db_comment_del(message.chat.id) # comment deleted

            bot.send_message(message.chat.id, 'Комментарий удалён')

        elif message.text == commands[command1_del]:
            db_some_column_delete(data1, message.from_user.id)

            bot.send_message(message.chat.id, button_name1_del)

        elif message.text == commands[command2_del]:
            db_some_column_delete(data2, message.from_user.id)

            bot.send_message(message.chat.id, button_name2_del)

        elif message.text == commands[command3_del]:
            db_some_column_delete(data3, message.from_user.id)

            bot.send_message(message.chat.id, button_name3_del)

        elif message.text == commands[command4_del]:
            db_some_column_delete(data4, message.from_user.id)

            bot.send_message(message.chat.id, button_name4_del)


        elif message.text == commands['photo']:
            bot.send_message(message.chat.id, 'Отправьте фото (введите "отмена" - для отмены)')
            @nextStepHandler(message)
            def askForPhoto(message):
                if message.content_type == 'text' and message.text.lower() == 'отмена':
                    bot.send_message(message.chat.id, 'Действие отменено')
                    return

                if message.content_type != 'photo':
                    bot.send_message(message.chat.id, 'Нужно фото!')
                    return True
                
                fileInfo = bot.get_file(message.photo[len(message.photo) - 1].file_id)
                downloadedFile = bot.download_file(fileInfo.file_path)

                
                db_photo_column(downloadedFile, message.from_user.id) # photo successfully saved

                bot.send_message(message.chat.id, 'Сохранено')
                
        elif message.text == commands['delete photo']:
            db_photo_del(message.chat.id) # photo deleted

            bot.send_message(message.chat.id, 'Фото удалено')

        elif message.text == commands[command1]:
            bot.send_message(message.chat.id, 'Происходит заполнение параметра: ' + button_name1)
            @nextStepHandler(message)
            def askForCommand1(message):
                all_commands_func(message.text, command1, message.from_user.id)
                bot.send_message(message.chat.id, 'Данные записаны')

        elif message.text == commands[command2]:
            bot.send_message(message.chat.id, 'Происходит заполнение параметра: ' +  button_name2)
            @nextStepHandler(message)
            def askForCommand2(message):
                all_commands_func(message.text, command2, message.from_user.id)
                bot.send_message(message.chat.id, 'Данные записаны')
        
        elif message.text == commands[command3]:
            bot.send_message(message.chat.id, 'Происходит заполнение параметра: ' + button_name3)
            @nextStepHandler(message)
            def askForCommand3(message):
                all_commands_func(message.text, command3, message.from_user.id)
                bot.send_message(message.chat.id, 'Данные записаны')

        elif message.text == commands[command4]:
            bot.send_message(message.chat.id, 'Происходит заполнение параметра: ' + button_name4)
            @nextStepHandler(message)
            def askForCommand4(message):
                all_commands_func(message.text, command4, message.from_user.id)
                bot.send_message(message.chat.id, 'Данные записаны')

        elif message.text == commands['delete all']:
            delete(message.chat.id) # all information deleted

            bot.send_message(message.chat.id, 'Всё данные удалены. Начните заполнение заново')
    botPolling()
#импорт библиотеки telebot
import telebot 
from telebot import types

#Импорт файлов конфигурации
import config
import markup

#Импорт встроенных библиотек python
from getpass import getpass
import codecs
import random

#Импорт библиотеки logging и ее конфигураций
import logging
from logging.handlers import RotatingFileHandler

import psycopg2 #Импорт библиотеки для работы с psql

logging.basicConfig( #Настройка формата вывода сообщений в лог файл
    format = '[%(asctime)s] [%(levelname)s]: %(message)s',  
    datefmt = '%d/%m/%Y %H:%M:%S',
    filename = 'bot For DND\example.log',  
    filemode = 'w',
    level = logging.DEBUG,
    encoding='utf-8'
)
logger = logging.getLogger(__name__) #Создание экземпляра logger

while True: #Инициализация базы данных
    try:
        DBpassword = getpass("Введите пароль от базы данных\n")
        conn = psycopg2.connect(dbname='users', user='postgres', password='{}'.format(DBpassword), host='localhost')
        logger.info("Выполненно подключение к базе данных" + " пароль (" + "*" * len(DBpassword) + ")")
        print("Пароль принят (" + "*" * len(DBpassword) + ")")
        break
    except:
        logger.info("Введен неверный пароль (" + DBpassword + ")")
        print("Введен неверный пароль (", DBpassword, ")")
cursor = (conn.cursor()) #Создание курсора для работы с базой данных

#Лист фотографий для случайной подборки
creatorPhotoList = ["bot For DND\content\photo\_firstPhotoForCreator.png", 
                        "bot For DND\content\photo\_secondPhotoForCreator.jpg", 
                        "bot For DND\content\photo\_thirdPhotoForCreator.jpg", 
                        "bot For DND\content\photo\_fourthPhotoForCreator.png"]

try: #Обработка собщений ботом
    hierarchyButForm = ['start']
    bot = telebot.TeleBot(config.TOKEN) #Инициализируем бота
    
    @bot.message_handler(commands=["start"]) #Команда start
    def welcome(message):
        bot.delete_message(message.chat.id, message.message_id - 0)
        sti=open("bot For DND\content\photo\_milk-inside-a-bag-of-milk_000.webp", "rb")
        bot.send_sticker(message.chat.id, sti)
        bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - MilkChan".format(message.from_user, bot.get_me()),
                        parse_mode="html", reply_markup=markup.startMarkup())
        logger.info("/start [message - %s] [user_id - %s]",message.text, message.from_user.id)
        cursor.execute("SELECT exists(SELECT 1 FROM users WHERE user_id = %s);", [message.from_user.id]) #Проверяем нету ли id пользователя в базе данных
        exists = bool(cursor.fetchone()[0])  #Получаем результат запроса
        if exists:  #Если строка найдена
            logger.info("Пользователь успешно авторизован [user_id - %s] [username - %s]", message.from_user.id, message.from_user.username)  #Пользователь авторизован
        else: #Иначе (если строка не найдена)
            cursor.execute("INSERT INTO users(user_id, username) VALUES (%s, %s);", [message.from_user.id, message.from_user.username])  #Пользователь регестрируется (автоматически)
            conn.commit() #Комит в базу данных
            logger.info("Пользователь успешно зарегистрирован [user_id - %s] [username - %s]", message.from_user.id, message.from_user.username)  #Пользователь регестрируется (автоматически) (отчет в логи)
        
    @bot.message_handler(commands=["creator"]) #Команда creator
    def creatorCard(message):
        bot.delete_message(message.chat.id, message.message_id - 0)
        photo=open(random.choice(creatorPhotoList), "rb")
        bot.send_sticker(message.chat.id, photo)
        bot.send_message(message.chat.id, "Я - Autumn_Phos\nКод бота можно увидеть сдесь - https://github.com/Autumn-Phos/tgBotForDND"),
        logger.info("/creator [message - %s] [user_id - %s]",message.text, message.from_user.id)
        
    @bot.message_handler(commands=["help"]) #Команда help
    def helpCommandsList(message):
        bot.delete_message(message.chat.id, message.message_id - 0)
        #bot.send_message(message.chat.id, "Обязательно при каждом использовании бота пропишите заново /start, "
        #                 "чтобы автоматически пройти авторизацию, или если вы не разу не "
        #                 "пользовались ботом то пройти автоматическую регистрацию")
        bot.send_message(message.chat.id, "###Список всех доступных комманд###\n"
                        "/start - Приветствие\n"
                        "/creator - Карточка создателя бота\n"
                        "/help - Список команд\n"
                        "#################INFO#################\n"
                        "Если не работает какая либо кнопка то пропишите заново /start"
                        "##################################")
        logger.info("/help [message - %s] [user_id - %s]",message.text, message.from_user.id)

    @bot.message_handler(content_types=["text"]) #Обработка сообщений пользователя
    def ButtonForm(message):
            global hierarchyButForm
            #Обработка кнопок с главной формы
            if message.text == "DND": #Кнопочная форма для игры в DND
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id, "---DND Menu---", 
                                reply_markup=markup.DNDMarkup())
                logger.info("'DND' [message - %s] [user_id - %s]",message.text, message.from_user.id)
                hierarchyButForm = ['start', 'DND']
            elif message.text == "DND_HK": #Кнопочная форма для игры в DND Hollow Knight
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id, "We have nothing for it")
                logger.info("'DND_HK' [message - %s] [user_id - %s]",message.text, message.from_user.id)
            elif message.text == "Roll": #Кнопочная форма для бросков кубиков
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id, "---Roll Menu---",
                                reply_markup=markup.rollMarkup())
                logger.info("'Roll' [message - %s] [user_id - %s]",message.text, message.from_user.id)
                hierarchyButForm = ['start', 'Roll']
            elif message.text == "back": #Кнопока назад (back)
                bot.delete_message(message.chat.id, message.message_id - 0)
                if hierarchyButForm[len(hierarchyButForm)-1] == 'DND' or hierarchyButForm[len(hierarchyButForm)-1] == 'Roll': #Переход на startMarkup
                    bot.send_message(message.chat.id, "ВЫПОЛНЕНИЕ КОМАНДЫ - 'back'", 
                                    reply_markup=markup.startMarkup())
                    hierarchyButForm.pop(len(hierarchyButForm)-1)
                elif hierarchyButForm[len(hierarchyButForm)-1] == 'Мои персонажи' or hierarchyButForm[len(hierarchyButForm)-1] == 'Мои игры': #Переход на DNDMarkup
                    bot.send_message(message.chat.id, "ВЫПОЛНЕНИЕ КОМАНДЫ - 'back'", 
                                    reply_markup=markup.DNDMarkup())
                    hierarchyButForm.pop(len(hierarchyButForm)-1)
                elif hierarchyButForm[len(hierarchyButForm)-1] == 'Удалить персонажа': #Переход на charMarkup
                    bot.send_message(message.chat.id, "ВЫПОЛНЕНИЕ КОМАНДЫ - 'back'", 
                                    reply_markup=markup.charMarkup(character_finder(message.from_user.id)))
                    hierarchyButForm.pop(len(hierarchyButForm)-1)
                logger.info("'back' [hierarchy - %s] [message - %s] [user_id - %s]", hierarchyButForm,message.text, message.from_user.id)
            #Обработка кнопок с Roll формы
            elif message.text == "d4": #Бросок куда d4
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id,"d4: " + str(random.randint(1,4)))
                logger.info("'d4' [message - %s] [user_id - %s]",message.text, message.from_user.id)
            elif message.text == "d6": #Бросок куда d6
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id,"d6: " + str(random.randint(1,6)))
                logger.info("'d6' [message - %s] [user_id - %s]",message.text, message.from_user.id)
            elif message.text == "d8": #Бросок куда d8
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id,"d8: " + str(random.randint(1,8)))
                logger.info("'d8' [message - %s] [user_id - %s]",message.text, message.from_user.id)
            elif message.text == "d10": #Бросок куда d10
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id,"d10: " + str(random.randint(1,10)))
                logger.info("'d10' [message - %s] [user_id - %s]",message.text, message.from_user.id)
            elif message.text == "d12": #Бросок куда d12
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id,"d12: " + str(random.randint(1,12)))
                logger.info("'d12' [message - %s] [user_id - %s]",message.text, message.from_user.id)
            elif message.text == "d16": #Бросок куда d16
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id,"d16: " + str(random.randint(1,16)))
                logger.info("'d16' [message - %s] [user_id - %s]",message.text, message.from_user.id)
            elif message.text == "d20": #Бросок куда d20
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id,"d20: " + str(random.randint(1,20)))
                logger.info("'d20' [message - %s] [user_id - %s]",message.text, message.from_user.id)
            #Обработка кнопок с DND формы
            elif message.text == "Мои персонажи": #Персонажи игрока
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id,"---characters---", reply_markup=markup.charMarkup(character_finder(message.from_user.id)))
                logger.info("'Мои персонажи' [message - %s] [user_id - %s]",message.text, message.from_user.id)
                hierarchyButForm = ['start', 'DND', 'Мои персонажи']
            elif message.text == "Мои игры": #Комнаты созданные игроком и в которых он состоит
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id,"---rooms---", reply_markup=markup.roomsMarkup())
                logger.info("'Мои игры' [message - %s] [user_id - %s]",message.text, message.from_user.id)
                hierarchyButForm = ['start', 'DND', 'Мои игры']
            elif message.text == "Удалить персонажа": #Удаление персонажей
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id,"---delete character---", reply_markup=markup.deleteChar(character_finder(message.from_user.id)))
                logger.info("'Удалить персонажа' [message - %s] [user_id - %s]",message.text, message.from_user.id)
                hierarchyButForm = ['start', 'DND', 'Мои персонажи', 'Удалить персонажа']
            else: #Если введено значение которого нет в списке
                try: #Если это имя персонажа
                    #Распаковка данных из базы данных
                    if hierarchyButForm[len(hierarchyButForm)-1] == 'Удалить персонажа': #Проверка действия совершаемового игроком
                        character = delete_character_finder_with_name(message.text, message.from_user.id) #Удаление персонажа
                        if character != '': #Если удалился оповещение об этом
                            bot.send_message(message.chat.id, character + " - удален", reply_markup=markup.deleteChar(character_finder(message.from_user.id))) #Обновление клавиатуры после удаления персонажа
                            logger.info("'Был удален персонаж - %s' [message - %s] [user_id - %s]",character, message.text, message.from_user.id) 
                        else:
                            logger.error("Введена несуществующая текстовая команда [message - %s] [user_id - %s]", message.text, message.from_user.id)
                    else:
                        bot.send_message(message.chat.id, character_finder_with_name(message.text, message.from_user.id))
                        bot.delete_message(message.chat.id, message.message_id - 0)
                        logger.info("'a character search engine was used' [message - %s] [user_id - %s]",message.text, message.from_user.id)
                except:
                    logger.error("Введена несуществующая текстовая команда [message - %s] [user_id - %s]", message.text, message.from_user.id)
    
    def delete_character_finder_with_name(name, id): #Удаление персонажа по имени персонажа
        cursor.execute("SELECT * FROM characters WHERE char_name = %s AND user_id = %s;", [name, id])
        character = ''
        for row in cursor:
            character = str(row[2])
        cursor.execute("DELETE FROM characters WHERE char_name = %s AND user_id = %s;", [name, id])
        conn.commit() #Комит в базу данных
        return character
    def character_finder_with_name(name, id): #Поиск персонажей пользователя по имени персонажа
        cursor.execute("SELECT * FROM characters WHERE char_name = %s AND user_id = %s;", [name, id])
        character = ''
        for row in cursor:
            character = str(row)
        return character
    def character_finder(id): #Поиск персонажей пользователя
        character = []
        try:
            #Распаковка данных из базы данных
            cursor.execute("SELECT char_name FROM characters WHERE user_id = %s;", [id])
            for row in cursor:
                character.append(row[0]+' ')
        except:
            character.append('пусто')
        return character

except Exception: #Если произошла ошибка при общения с ботом
    logger.error(Exception) 

if __name__ == '__main__':
        bot.polling(none_stop=True)
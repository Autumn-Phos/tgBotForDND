#импорт библиотеки telebot
import telebot
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
#Импорт библиотеки для работы с psql
import psycopg2

#Настройка формата вывода сообщений в лог файл
logging.basicConfig(
    format = '[%(asctime)s] [%(levelname)s]: %(message)s',  
    datefmt = '%d/%m/%Y %H:%M:%S',
    filename = 'bot For DND\example.log',  
    filemode = 'w',
    level = logging.DEBUG,
    encoding='utf-8'
)
#Создание экземпляра logger
logger = logging.getLogger(__name__)
#Инициализация базы данных
def dbForUsers():
    while True:
        try:
            DBpassword = getpass("Введите пароль от базы данных\n")
            conn = psycopg2.connect(dbname='users', user='postgres', password='{}'.format(DBpassword), host='localhost')
            logger.info("Выполненно подключение к базе данных" + " пароль (" + "*" * len(DBpassword) + ")")
            print("Пароль принят (" + "*" * len(DBpassword) + ")")
            break
        except:
            logger.info("Введен неверный пароль (" + DBpassword + ")")
            print("Введен неверный пароль (", DBpassword, ")")
    return(conn.cursor())
#Создание курсора для работы с базой данных
cursor = dbForUsers()
#Лист фотографий для случайной подборки
creatorPhotoList = ["bot For DND\content\photo\_firstPhotoForCreator.png", 
                        "bot For DND\content\photo\_secondPhotoForCreator.jpg", 
                        "bot For DND\content\photo\_thirdPhotoForCreator.jpg", 
                        "bot For DND\content\photo\_fourthPhotoForCreator.png"]
#Обработка общения с ботом
try:
    #Инициализируем бота
    bot = telebot.TeleBot(config.TOKEN)
    #Команда start
    @bot.message_handler(commands=["start"])
    def welcome(message):
        bot.delete_message(message.chat.id, message.message_id - 0)
        sti=open("bot For DND\content\photo\_milk-inside-a-bag-of-milk_000.webp", "rb")
        bot.send_sticker(message.chat.id, sti)
        bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - MilkChan".format(message.from_user, bot.get_me()),
                        parse_mode="html", reply_markup=markup.startMarkup())
        bot.send_message(message.chat.id, message.from_user.id)
        logger.info("/start")
    #Команда creator
    @bot.message_handler(commands=["creator"])
    def creatorCard(message):
        bot.delete_message(message.chat.id, message.message_id - 0)
        photo=open(random.choice(creatorPhotoList), "rb")
        bot.send_sticker(message.chat.id, photo)
        bot.send_message(message.chat.id, "Я - Autumn_Phos\nКод бота можно увидеть сдесь - https://github.com/Autumn-Phos/tgBotForDND"),
        logger.info("/creator")
    #Команда help
    @bot.message_handler(commands=["help"])
    def helpCommandsList(message):
        bot.delete_message(message.chat.id, message.message_id - 0)
        bot.send_message(message.chat.id, "---Список всех доступных комманд---\n"
                        "/start - Приветствие\n"
                        "/creator - Карточка создателя бота\n"
                        "/help - Список комманд\n"
                        "-------------------------------------------------")
        logger.info("/help")

    #Обработка сообщений пользователя
    @bot.message_handler(content_types=["text"])
    def ButtonForm(message):
            #Обработка кнопок с главной формы
            if message.text == "DND":
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id, "---DND Menu---", 
                                reply_markup=markup.DNDMarkup())
                logger.info("'DND'")
            elif message.text == "DND_HK":
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id, "We have nothing for it")
                logger.info("'DND_HK'")
            elif message.text == "Roll":
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id, "---Roll Menu---",
                                reply_markup=markup.rollMarkup())
                logger.info("'Roll'")
            elif message.text == "back to button form":
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id, "ВЫПОЛНЕНИЕ КОМАНДЫ - 'back to button form'", 
                                reply_markup=markup.startMarkup())
                logger.info("'back to button form'")
            #Обработка кнопок с Roll формы
            elif message.text == "d4":
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id,"d4: " + str(random.randint(1,4)))
                logger.info("'d4'")
            elif message.text == "d6":
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id,"d6: " + str(random.randint(1,6)))
                logger.info("'d6'")
            elif message.text == "d8":
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id,"d8: " + str(random.randint(1,8)))
                logger.info("'d8'")
            elif message.text == "d10":
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id,"d10: " + str(random.randint(1,10)))
                logger.info("'d10'")
            elif message.text == "d12":
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id,"d12: " + str(random.randint(1,12)))
                logger.info("'d12'")
            elif message.text == "d16":
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id,"d16: " + str(random.randint(1,16)))
                logger.info("'d16'")
            elif message.text == "d20":
                bot.delete_message(message.chat.id, message.message_id - 0)
                bot.send_message(message.chat.id,"d20: " + str(random.randint(1,20)))
                logger.info("'d20'")
            
            #Если введено значение которого нет в списке
            else:
                logger.error("Введена несуществующая текстовая команда - '" + message.text + "'")
#Если произошла ошибка при общения с ботом
except Exception:
    logger.error(Exception) 
if __name__ == '__main__':
        bot.polling(none_stop=True)
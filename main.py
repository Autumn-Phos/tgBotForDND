#импорт библиотеки telebot и ее конфигураций
import telebot
from telebot import types

from functionForBD import DB #Импорт самописных библиотек

import config, markup #Импорт файлов конфигурации

import random, threading #Импорт встроенных библиотек python

#Импорт библиотек для логирования
import logging, sys
from logging.handlers import RotatingFileHandler
import os

print("\n\n            ██████╗  █████╗ ████████╗  ███████╗ █████╗ ██████╗   ██████╗ ███╗  ██╗██████╗\n"
          "            ██╔══██╗██╔══██╗╚══██╔══╝  ██╔════╝██╔══██╗██╔══██╗  ██╔══██╗████╗ ██║██╔══██╗\n"
          "            ██████╦╝██║  ██║   ██║     █████╗  ██║  ██║██████╔╝  ██║  ██║██╔██╗██║██║  ██║\n"
          "            ██╔══██╗██║  ██║   ██║     ██╔══╝  ██║  ██║██╔══██╗  ██║  ██║██║╚████║██║  ██║\n"
          "            ██████╦╝╚█████╔╝   ██║     ██║     ╚█████╔╝██║  ██║  ██████╔╝██║ ╚███║██████╔╝\n"
          "            ╚═════╝  ╚════╝    ╚═╝     ╚═╝      ╚════╝ ╚═╝  ╚═╝  ╚═════╝ ╚═╝  ╚══╝╚═════╝")
bot = telebot.TeleBot(config.TOKEN)

grey = '\x1b[38;20m'
red = '\x1b[1;31m'
green = '\x1b[1;32m'
yellow = '\x1b[1;33m'
magenta = '\x1b[1;35m'

logging.basicConfig( #Настройка формата вывода сообщений в лог файл
    format = yellow + '[%(asctime)s]\x1b[0m ' + red + '[%(levelname)s]\x1b[0m %(message)s\x1b[0m',  
    datefmt = '%d/%m/%Y %H:%M:%S',
    stream=sys.stdout,
    filemode = 'w',
    level = logging.INFO,
    encoding='utf-8'
)
logger = logging.getLogger(__name__) #Создание экземпляра logger

#Лист фотографий для случайной подборки
creatorPhotoList = ["content\photo\_firstPhotoForCreator.png", 
                    "content\photo\_secondPhotoForCreator.jpg", 
                    "content\photo\_thirdPhotoForCreator.jpg", 
                    "content\photo\_fourthPhotoForCreator.png"]

def work_in_background():
    def analytics(func: callable):
        def analytick_wrapper(message):
            logger.info(green + "[user_id - %s]\x1b[0m: " + magenta + "[message - %s]\x1b[0m", message.from_user.id, message.text)
            return func(message)
        return analytick_wrapper

    def create_list_button_form(id):
        #Все возможные положения пользователя в иерархии кнопочных форм
        list_button_form = [[markup.startMarkup(), 'start', 'DND'],
                            [markup.startMarkup(), 'start', 'Roll'],
                            [markup.DNDMarkup(), 'DND', 'Мои персонажи'],
                            [markup.DNDMarkup(), 'DND', 'Мои игры'],
                            [markup.charMarkup(DB.character.finder(id)), 'Мои персонажи', 'Создать персонажа'],
                            [markup.charMarkup(DB.character.finder(id)), 'Мои персонажи', 'Удалить персонажа'],
                            [markup.roomsMarkup(DB.room.finder(id)), 'Мои игры', 'Создать комнату'],
                            [markup.roomsMarkup(DB.room.finder(id)), 'Мои игры', 'Удалить комнату'],
                            [markup.roomsMarkup(DB.room.finder(id)), 'Мои игры', 'Выйти из комнаты']]
        return list_button_form

    @bot.message_handler(commands=["start"])
    @analytics
    def welcome(message):
        sti=open("content\photo\_milk-inside-a-bag-of-milk_000.webp", "rb")
        bot.send_sticker(message.chat.id, sti)
        bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - MilkChan".format(message.from_user, bot.get_me()),
                        parse_mode="html", reply_markup=markup.startMarkup()) #Сообщение приветствие
        exists = DB.user.finder(message.from_user.id)
        if not exists:
            DB.user.register(message.from_user.id, message.from_user.username)
            #logger.info(green + "[user_id - %s]\x1b[0m: " + magenta + "[%s] [username - %s]", 
            #            message.from_user.id, , message.from_user.username) 

    @bot.message_handler(commands=["creator"])
    @analytics
    def creatorCard(message):
        photo=open(random.choice(creatorPhotoList), "rb")
        bot.send_sticker(message.chat.id, photo)
        bot.send_message(message.chat.id, "Я - Autumn_Phos\nКод бота можно увидеть сдесь - https://github.com/Autumn-Phos/tgBotForDND"),

    @bot.message_handler(commands=["help"])
    @analytics
    def helpCommandsList(message):
        bot.send_message(message.chat.id, "-Список всех доступных комманд-\n"
                        "/start - Приветствие\n"
                        "/creator - Карточка создателя бота\n"
                        "/help - Список команд\n"
                        "---INFO---\n"
                        "Если не работает какая либо кнопка то пропишите заново /start\n"
                        "------")

    @bot.message_handler(content_types=["text"])
    @analytics
    def ButtonForm(message):
        bot.delete_message(message.chat.id, message.message_id - 0)
        #Обработка кнопок с главной формы
        if message.text == "DND": #Кнопочная форма для игры в DND
            DB.hierarchy.change(message.from_user.id, message.text) #Изменения положения в иерархии кнопок
            bot.send_message(message.chat.id, "---DND Menu---", reply_markup=markup.DNDMarkup())
        elif message.text == "DND_HK": #Кнопочная форма для игры в DND Hollow Knight
            bot.send_message(message.chat.id, "We have nothing for it")
        elif message.text == "Roll": #Кнопочная форма для бросков кубиков
            DB.hierarchy.change(message.from_user.id, message.text) #Изменения положения в иерархии кнопок
            bot.send_message(message.chat.id, "---Roll Menu---", reply_markup=markup.rollMarkup())
        elif message.text == "back": #Кнопока назад (back)
            buttonHierarchy_list = create_list_button_form(message.chat.id) #Получение всех возможных маршрутов
            buttonHierarchy = DB.hierarchy.receiving(message.from_user.id) #Получение местонахождения пользователя в иерархии
            for i in range(len (buttonHierarchy_list)): #Проверка всех возможных положений пользователя
                if buttonHierarchy[len(buttonHierarchy)-1].replace('_', ' ') == buttonHierarchy_list[i][2]: #Сравнение всех возможных маршрутов и местонахождения пользователя
                    bot.send_message(message.chat.id, "ВЫПОЛНЕНИЕ КОМАНДЫ - 'back'", reply_markup=buttonHierarchy_list[i][0]) #Смена клавиатуры
                    DB.hierarchy.change(message.from_user.id, buttonHierarchy_list[i][1]) #Изменение местонахождения пользователя в иерархии
        #Обработка кнопок с Roll формы
        elif message.text == "d4": #Бросок куда d4
            bot.send_message(message.chat.id,"d4: " + str(random.randint(1,4)))
        elif message.text == "d6": #Бросок куда d6
            bot.send_message(message.chat.id,"d6: " + str(random.randint(1,6)))
        elif message.text == "d8": #Бросок куда d8
            bot.send_message(message.chat.id,"d8: " + str(random.randint(1,8)))
        elif message.text == "d10": #Бросок куда d10
            bot.send_message(message.chat.id,"d10: " + str(random.randint(1,10)))
        elif message.text == "d12": #Бросок куда d12
            bot.send_message(message.chat.id,"d12: " + str(random.randint(1,12)))
        elif message.text == "d16": #Бросок куда d16
            bot.send_message(message.chat.id,"d16: " + str(random.randint(1,16)))
        elif message.text == "d20": #Бросок куда d20
            bot.send_message(message.chat.id,"d20: " + str(random.randint(1,20)))
        #Обработка кнопок с DND формы
        elif message.text == "Мои персонажи": #Персонажи игрока
            DB.hierarchy.change(message.from_user.id, message.text) #Изменения положения в иерархии кнопок
            bot.send_message(message.chat.id,"---characters---", reply_markup=markup.charMarkup(DB.character.finder(message.from_user.id)))
        elif message.text == "Мои игры": #Комнаты созданные игроком и в которых он состоит
            DB.hierarchy.change(message.from_user.id, message.text) #Изменения положения в иерархии кнопок
            bot.send_message(message.chat.id,"---rooms---", reply_markup=markup.roomsMarkup(DB.room.finder(message.from_user.id)))
        elif message.text == "Удалить персонажа": #Удаление персонажей
            DB.hierarchy.change(message.from_user.id, message.text) #Изменения положения в иерархии кнопок
            bot.send_message(message.chat.id,"---delete character---", reply_markup=markup.deleteChar(DB.character.finder(message.from_user.id)))
        elif message.text == "Создать персонажа": #Создание персонажей
            DB.hierarchy.change(message.from_user.id, message.text) #Изменения положения в иерархии кнопок
            bot.send_message(message.chat.id,"---create character---", reply_markup=markup.createChar())
        elif message.text == "Удалить комнату": #Удаление персонажей
            DB.hierarchy.change(message.from_user.id, message.text) #Изменения положения в иерархии кнопок
            bot.send_message(message.chat.id,"---delete room---", reply_markup=markup.deleteRooms(DB.room.finder(message.from_user.id)))
        elif message.text == "Создать комнату": #Создание персонажей
            DB.hierarchy.change(message.from_user.id, message.text) #Изменения положения в иерархии кнопок
            bot.send_message(message.chat.id,"---create room---", reply_markup=markup.createRooms())
        elif message.text == "Присоединиться к комнате": #Удаление персонажей
            send = bot.send_message(message.chat.id, "Введите код команты и пароль через пробел")
            bot.register_next_step_handler(send, connect_to_room)
        elif message.text == "Выйти из комнаты": #Создание персонажей
            DB.hierarchy.change(message.from_user.id, message.text) #Изменения положения в иерархии кнопок
            bot.send_message(message.chat.id,"---disconnect of room---", reply_markup=markup.disconnectOfRoom(DB.room.finder_user_isConnectedTo(message.from_user.id)))
        else: #Если введено значение которого нет в списке                
            buttonHierarchy = DB.hierarchy.receiving(message.from_user.id) #Распаковка данных из базы данных
            if buttonHierarchy[len(buttonHierarchy)-1].replace('_', ' ') == 'Удалить персонажа': #Проверка действия совершаемового игроком
                character = DB.character.delete_finder_with_name(message.text, message.from_user.id) #Удаление персонажа
                if character != '': #Если удалился оповещение об этом
                    bot.send_message(message.chat.id, character + " - удален", reply_markup=markup.deleteChar(DB.character.finder(message.from_user.id))) #Обновление клавиатуры после удаления персонажа
            elif buttonHierarchy[len(buttonHierarchy)-1].replace('_', ' ') == 'Мои персонажи':
                bot.send_message(message.chat.id, DB.character.finder_with_name(message.text, message.from_user.id))
            elif buttonHierarchy[len(buttonHierarchy)-1].replace('_', ' ') == 'Мои игры':
                bot.send_message(message.chat.id, DB.room.finder_with_name(message.text, message.from_user.id))

    def connect_to_room(message):
        notificationOfTheResult = DB.room.connectToRoom(message.text, message.from_user.id)
        logger.info(green + "[user_id - %s]\x1b[0m: " + magenta + "[%s] [message - %s]", message.from_user.id, notificationOfTheResult, message.text)
        bot.send_message(message.chat.id, notificationOfTheResult)

    if __name__ == '__main__':
        bot.polling(none_stop=True)

threading.Thread(target=work_in_background).start()

while True:
    command = input()
    if command == 'cls':
        os.system('cls')
        print("\n\n            ██████╗  █████╗ ████████╗  ███████╗ █████╗ ██████╗   ██████╗ ███╗  ██╗██████╗\n"
                  "            ██╔══██╗██╔══██╗╚══██╔══╝  ██╔════╝██╔══██╗██╔══██╗  ██╔══██╗████╗ ██║██╔══██╗\n"
                  "            ██████╦╝██║  ██║   ██║     █████╗  ██║  ██║██████╔╝  ██║  ██║██╔██╗██║██║  ██║\n"
                  "            ██╔══██╗██║  ██║   ██║     ██╔══╝  ██║  ██║██╔══██╗  ██║  ██║██║╚████║██║  ██║\n"
                  "            ██████╦╝╚█████╔╝   ██║     ██║     ╚█████╔╝██║  ██║  ██████╔╝██║ ╚███║██████╔╝\n"
                  "            ╚═════╝  ╚════╝    ╚═╝     ╚═╝      ╚════╝ ╚═╝  ╚═╝  ╚═════╝ ╚═╝  ╚══╝╚═════╝")
import telebot
from telebot import types

#Keyboard for start markup
def startMarkup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("DND", "DND_HK", "Roll")
    return markup
#Keyboard for DND
def DNDMarkup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Мои персонажи", "Мои игры")
    markup.row("back")
    return markup
#Keyboard for roll
def rollMarkup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("d4", "d6", "d8", "d10", "d12", "d16", "d20")
    markup.row("back")
    return markup
#Keyboard for characters
def charMarkup(character):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(character)):
        markup.row(character[i])
    markup.row("Создать персонажа", "Удалить персонажа")
    markup.row("back")  
    return markup
#Keyboard for rooms
def roomsMarkup(room):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(room)):
        markup.row(room[i])
    markup.row("Присоединиться к комнате", "Выйти из комнаты")
    markup.row("Создать комнату", "Удалить комнату")
    markup.row("back")
    return markup
#Keyboard for delete characters
def deleteChar(character):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(character)):
        markup.row(character[i])
    markup.row("back")  
    return markup
#Keyboard for delete rooms
def deleteRooms(rooms):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(rooms)):
        markup.row(rooms[i])
    markup.row("back")  
    return markup
#Keyboard for create rooms
def createRooms():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("None")  
    markup.row("back")  
    return markup
#Keyboard for add character
def createChar():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("None")  
    markup.row("back")  
    return markup
#Keyboard for disconnect of other room
def disconnectOfRoom(rooms):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(rooms)):
        markup.row(rooms[i])  
    markup.row("back")  
    return markup
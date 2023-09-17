import telebot
from telebot import types

#Главная кнопочная форма
def startMarkup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("DND", "DND_HK", "Roll")
    return markup
#Форма для расчета формул DND
def DNDMarkup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("расчет дамага", "расчет дамага", "расчет дамага", "расчет дамага", "расчет дамага", "расчет дамага")
    markup.row("back to button form")
    return markup
#Форма для броска кубиков
def rollMarkup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("d4", "d6", "d8", "d10", "d12", "d16", "d20")
    markup.row("back to button form")
    return markup
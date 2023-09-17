import telebot
import config
import random
from telebot import types

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=["start"])
def welcome(message):
    bot.delete_message(message.chat.id, message.message_id - 0)
    sti=open("bot For DND\content\milk-inside-a-bag-of-milk_000.webp", "rb")
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - MilkChan".format(message.from_user, bot.get_me()),
    parse_mode="html", reply_markup=startMarkup())

def startMarkup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("DND", "DND_HK", "Roll")
    return markup

def DNDMarkup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("расчет дамага", "расчет дамага", "расчет дамага", "расчет дамага", "расчет дамага", "расчет дамага")
    markup.row("back to button form")
    return markup

def rollMarkup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("d4", "d6", "d8", "d10", "d12", "d16", "d20")
    markup.row("back to button form")
    return markup

@bot.message_handler(content_types=["text"])
def ButtonForm(message):
    if message.text == "DND":
        bot.delete_message(message.chat.id, message.message_id - 0)
        bot.send_message(message.chat.id, "---DND Menu---", reply_markup=DNDMarkup())
    elif message.text == "DND_HK":
        bot.delete_message(message.chat.id, message.message_id - 0)
        bot.send_message(message.chat.id, "We have nothing for it")
    elif message.text == "Roll":
        bot.delete_message(message.chat.id, message.message_id - 0)
        bot.send_message(message.chat.id, "---Roll Menu---",reply_markup=rollMarkup())
    elif message.text == "back to button form":
        bot.delete_message(message.chat.id, message.message_id - 0)
        bot.send_message(message.chat.id, "ВЫПОЛНЕНИЕ КОМАНДЫ - 'back to button form'", reply_markup=startMarkup())

    if message.text == "d4":
        bot.delete_message(message.chat.id, message.message_id - 0)
        bot.send_message(message.chat.id,"d4: " + str(random.randint(1,4)))
    elif message.text == "d6":
        bot.delete_message(message.chat.id, message.message_id - 0)
        bot.send_message(message.chat.id,"d6: " + str(random.randint(1,6)))
    elif message.text == "d8":
        bot.delete_message(message.chat.id, message.message_id - 0)
        bot.send_message(message.chat.id,"d8: " + str(random.randint(1,8)))
    elif message.text == "d10":
        bot.delete_message(message.chat.id, message.message_id - 0)
        bot.send_message(message.chat.id,"d10: " + str(random.randint(1,10)))
    elif message.text == "d12":
        bot.delete_message(message.chat.id, message.message_id - 0)
        bot.send_message(message.chat.id,"d12: " + str(random.randint(1,12)))
    elif message.text == "d16":
        bot.delete_message(message.chat.id, message.message_id - 0)
        bot.send_message(message.chat.id,"d16: " + str(random.randint(1,16)))
    elif message.text == "d20":
        bot.delete_message(message.chat.id, message.message_id - 0)
        bot.send_message(message.chat.id,"d20: " + str(random.randint(1,20)))

bot.polling(none_stop=True)     
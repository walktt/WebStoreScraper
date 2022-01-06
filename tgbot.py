# https://thecode.media/python-bot/
# pip install pytelegrambotapi
import os
import telebot
import time
from dotenv import load_dotenv,find_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv('TELEBOT_TOKEN'))

chatid = 277180656
bot.send_message(chatid, 'hihi')

#
# @bot.message_handler(commands=['chatid'])
# def Greet(message):
#     print(message)
#     bot.reply_to(message,' your chat id is: ' + str(message.chat.id))
#
# @bot.message_handler(content_types=['text'])
# def send_text(message):
#     print(message)
#     if message.text.lower() == '1':
#         img = open('Смайлики и люди 1.png', 'rb')
#         bot.send_document(message.chat.id, img)
#     else:
#         bot.send_message(message.chat.id, 'Nope')
#
# print ('Telegram bot starting...')
#
# bot.polling(none_stop=True)
#




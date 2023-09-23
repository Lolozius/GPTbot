import os
import time
import requests
from dotenv import load_dotenv
from telebot import telebot, types
import logging
from logging.handlers import RotatingFileHandler

load_dotenv()
bot_token = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(bot_token)
logger = logging.getLogger(__name__)


@bot.message_handler(commands=['start'])
def welcome_message(message):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Перейти на Яндекс", url="https://ya.ru")
    keyboard.add(button)
    bot.send_message(message.chat.id, 'Убить всех человеков', reply_markup=keyboard)


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception:
            time.sleep(4)
            logger.error(Exception)

import os
import time
import openai
from dotenv import load_dotenv
from telebot import telebot, types
import logging
from logging.handlers import RotatingFileHandler

load_dotenv()
BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
openai.api_key = os.getenv('API_TOKEN_CHATGPT')
bot = telebot.TeleBot(BOT_TOKEN)
logger = logging.getLogger(__name__)


@bot.message_handler(commands=['start'])
def welcome_message(message):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Open ChatGPT", url="https://chat.openai.com/")
    keyboard.add(button)
    bot.send_message(message.chat.id, 'Убить всех человеков', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def hey_chatgpt(message):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "assistant", "content": message.text}
        ]
    )
    bot.send_message(message.chat.id, completion.choices[0].message.content)


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception:
            time.sleep(4)
            logger.error(Exception)

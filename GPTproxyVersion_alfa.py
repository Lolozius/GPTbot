import os
import time
import requests
#from openai import OpenAI
from dotenv import load_dotenv
from telebot import telebot, types
import logging

load_dotenv()
BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
api_key = os.getenv('API_TOKEN_CHATGPT')
proxy_url = '8.219.97.248:80'  # Замените на ваш реальный URL прокси

# Инициализируем OpenAI
#client = OpenAI(api_key=api_key)

bot = telebot.TeleBot(BOT_TOKEN)
logger = logging.getLogger(__name__)

# Определим сессию с настройкой прокси
session = requests.Session()
session.proxies = {'http': proxy_url, 'https': proxy_url}


def make_openai_request(message_text):
    """Делаем запрос к OpenAI с использованием настроенной сесси"""
    response = session.post(
        'https://api.openai.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {api_key}'},
        json={
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'system', 'content': message_text}]
        },
        timeout=10
    )
    return response.json()


@bot.message_handler(commands=['start'])
def welcome_message(message):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Open ChatGPT", url="https://chat.openai.com/")
    keyboard.add(button)
    bot.send_message(message.chat.id, 'Убить всех человеков', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def hey_chatgpt(message):
    completion = make_openai_request(message.text)
    bot.send_message(message.chat.id, completion)
    print(completion)


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception:
            time.sleep(4)
            logger.error(Exception)
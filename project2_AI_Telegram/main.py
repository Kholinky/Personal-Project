from openai import OpenAI
from telebot import TeleBot
from telebot import types
import os


client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",    
    api_key = "API_KEY",
)


tele_key = "TELEGRAM_KEY"
bot = TeleBot(tele_key)


def handle_command(chat_id, text):
    bot.send_message(chat_id, "Please use /start to start the chat with me!")

@bot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.first_name
    bot.send_message(message.chat.id, f'Hello {username}! I am Chippy! Ask me anything!')
    
@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    text = message.text.strip().lower()

    if text.startswith('/'):
        handle_command(chat_id, text)
    else:
        handle_user_message(chat_id, text)

def handle_user_message(chat_id, text):
    response = chat_with_openai(text)
    bot.send_message(chat_id, response)


def chat_with_openai(text):
    messages = [
        {
            "role": "user",
            "content": text
        }
    ]
    response = client.chat.completions.create(
    model='deepseek/deepseek-r1:free',
    messages=messages
    )

    return response.choices[0].message.content


bot.polling(none_stop=True)

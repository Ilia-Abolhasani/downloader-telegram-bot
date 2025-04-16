import os
import re
import telebot
import requests
import yt_dlp
from dotenv import load_dotenv

load_dotenv()

# Replace with your actual Telegram bot token
BOT_TOKEN = os.getenv("bot_api_key")

bot = telebot.TeleBot(BOT_TOKEN)

if __name__ == "__main__":
    message = ""
    message_id = 66067655
    bot.send_message(chat_id=message_id, text=message)

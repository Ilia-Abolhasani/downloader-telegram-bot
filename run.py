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


def is_valid_url(url):
    youtube_regex = r"(?:https?:\/\/)?(?:www\.|m\.)?(youtube\.com|youtu\.be)"
    instagram_regex = r"(?:https?:\/\/)?(?:www\.)?instagram\.com"
    return re.search(youtube_regex, url) or re.search(instagram_regex, url)


def download_video(url):
    ydl_opts = {
        "format": "best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Send me a YouTube or Instagram link, and I'll download the video for you!",
    )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()
    if not is_valid_url(url):
        bot.reply_to(message, "Please send a valid YouTube or Instagram link.")
        return

    bot.reply_to(message, "Downloading... Please wait.")
    try:
        video_path = download_video(url)
        with open(video_path, "rb") as video:
            bot.send_video(message.chat.id, video)
        os.remove(video_path)  # Clean up after sending
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")


if __name__ == "__main__":
    bot.polling()

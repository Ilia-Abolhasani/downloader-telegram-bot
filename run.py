import os
import re
import telebot
import requests
import yt_dlp
from dotenv import load_dotenv

load_dotenv()

# Replace with your actual Telegram bot token
BOT_TOKEN = os.getenv("bot_api_key")
LOG_CHAT_ID = os.getenv("log_chat_id")
LOG_TOPIC_ID = int(os.getenv("log_topic_id"))
COOKIE_SESSION_ID = os.getenv("cookie_session_id")

bot = telebot.TeleBot(BOT_TOKEN)


def is_valid_url(url):
    instagram_regex = r"(?:https?:\/\/)?(?:www\.)?instagram\.com"
    return re.search(instagram_regex, url)


def download_video(url):
    ydl_opts = {
        "format": "best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
    }
    ydl_opts["http_headers"] = {"Cookie": f"sessionid={COOKIE_SESSION_ID}"}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
    except:
        raise Exception("This video link is age-restricted or from a private account.")


@bot.message_handler(commands=["start"])
def send_welcome(message):
    text = """Send me an Instagram link, and I'll download the video for you!"""
    bot.reply_to(message, text)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()
    # Log the message to the logger bot
    log_text = (
        f"👤 User: @{message.from_user.username or 'Unknown'}\n"
        f"🆔 User ID: #user_{message.from_user.id}\n"
        f"📛 Name: {message.from_user.first_name or ''} {message.from_user.last_name or ''}\n"
        f"🌐 Language: {message.from_user.language_code or 'Unknown'}\n"
        f"💬 Chat ID: {message.chat.id}\n"
        f"📩 Message: {url}"
    )
    if message.from_user.username != "Ilia_Abolhasani":
        bot.send_message(LOG_CHAT_ID, log_text, message_thread_id=LOG_TOPIC_ID)

    if not is_valid_url(url):
        bot.reply_to(message, "Please send a valid Instagram link.")
        return

    downloading_msg = bot.reply_to(message, "Downloading... Please wait.")
    try:
        video_path = download_video(url)
        with open(video_path, "rb") as video:
            sent_message = bot.send_video(message.chat.id, video)
            # Forward the video message to the logger topic
            if message.from_user.username != "Ilia_Abolhasani":
                bot.forward_message(
                    LOG_CHAT_ID,  # Group ID
                    sent_message.chat.id,  # User chat ID
                    sent_message.message_id,  # Message ID to forward
                    message_thread_id=LOG_TOPIC_ID,  # Forward to correct topic
                )

        os.remove(video_path)  # Clean up after sending
    except Exception as e:
        error_message = f"Error: {e}"
        bot.reply_to(message, error_message)
        bot.send_message(LOG_CHAT_ID, error_message, message_thread_id=LOG_TOPIC_ID)

    bot.delete_message(chat_id=message.chat.id, message_id=downloading_msg.message_id)


if __name__ == "__main__":
    bot.polling()

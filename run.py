import os
import re
import json
import random
import yt_dlp
import telebot
from dotenv import load_dotenv

load_dotenv()

# Replace with your actual Telegram bot token
BOT_TOKEN = os.getenv("bot_api_key")
LOG_CHAT_ID = os.getenv("log_chat_id")
LOG_SUCCESS_TOPIC_ID = int(os.getenv("log_success_topic_id"))
LOG_INVALID_TOPIC_ID = int(os.getenv("log_invalid_topic_id"))
LOG_ERROR_TOPIC_ID = int(os.getenv("log_error_topic_id"))
COOKIE_SESSION_ID = os.getenv("cookie_session_id")

ALLOWED_USER = ["Ilia_Abolhasani", "azsh74"]
bot = telebot.TeleBot(BOT_TOKEN)
USER_DATA_FILE = "users_data.json"


def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_user_data(data):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def update_user_stats(user_id, success=False, invalid=False, error=False):
    try:
        data = load_user_data()

        user_id = str(user_id)
        if user_id not in data:
            data[user_id] = {
                "message_count": 0,
                "success_count": 0,
                "invalid_count": 0,
                "error_count": 0,
            }

        data[user_id]["message_count"] += 1
        if success:
            data[user_id]["success_count"] += 1
        if invalid:
            data[user_id]["invalid_count"] += 1
        if error:
            data[user_id]["error_count"] += 1
        save_user_data(data)
    except:
        pass


def log_to_topic(message, text, topic_id):
    if message.from_user.username != "Ilia_Abolhasani":
        bot.send_message(LOG_CHAT_ID, text, message_thread_id=topic_id)


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
            if "playlist_count" in info and info["playlist_count"] > 1:
                output = []
                for item in info["entries"]:
                    output.append(ydl.prepare_filename(item))
                return output
            return [ydl.prepare_filename(info)]
    except:
        raise Exception("This video link is age-restricted or from a private account.")


@bot.message_handler(commands=["start"])
def send_welcome(message):
    if message.from_user.username not in ALLOWED_USER:
        return
    text = """Send me an Instagram link, and I'll download the video for you!"""
    bot.reply_to(message, text)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.chat.type != "private":
        msg = message.text.strip()
        if not msg.lower().startswith("download "):
            return  # Ignore unrelated messages in groups

    if message.from_user.username not in ALLOWED_USER:
        return
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

    if not is_valid_url(url):
        bot.reply_to(message, "Please send a valid Instagram link.")
        log_to_topic(message, log_text, LOG_INVALID_TOPIC_ID)
        update_user_stats(message.from_user.id, invalid=True)
        return

    msg_list = [
        " علی، تو زن داری؟ نامزد چی؟ پس تو چی داری ؟ یعنی تاحالا عاشق نشدی؟",
        "جای اینکه بری به سالن قارچ سر بزنی اومدی اینجا لینک بازی میکنی ؟",
        "سلام عشقای داداچ، پند امروز: باید از ناملایمتی ها گذشت و به شباهت ها توجه کرد. ناماستا قربه علی الله....",
        "دانلود را برای طبقه مستمند مجانی میکنیم.",
        "سلام عشقای داداچ، کاش وقت داشتم یه کم عشق و حال میکردیم ولی باید برم کلاس یوگا وینیاستا دارم، این دانلود هم خدمت شما. بایییییی",
        "اگر غیر اون بود که به جای مارشمالو جیگرتو میزدم به سیخ",
        "چطوری خط قرمز دوم هانیه",
        "چطوری قطر؟ همیشه میانجی گری کردی همیشه هم موشک خوردی!",
        "الان اون ضرر کرد یا من؟ اون خوشبخت شد یا من؟",
        "قرارمون یادت نره دیر نکنی منتظرم.",
        "جونمی ژون دختر",
        "دختر برکت خداست، هر چی اومد خدا رو شکر",
        "شما به عشق در نگاه اول ایمان داری؟",
    ]
    msg = random.choice(msg_list)
    # msg = "Downloading... Please wait."
    downloading_msg = bot.reply_to(message, msg)
    try:
        video_path_list = download_video(url)
        for i in range(len(video_path_list)):
            video_path = video_path_list[i]
            with open(video_path, "rb") as video:
                caption = ""
                if len(video_path_list) > 1:
                    caption = f"Part {i + 1}"
                sent_message = bot.send_video(message.chat.id, video, caption=caption)
                # Forward the video message to the logger topic
                log_to_topic(message, log_text, LOG_SUCCESS_TOPIC_ID)
                bot.forward_message(
                    LOG_CHAT_ID,  # Group ID
                    sent_message.chat.id,  # User chat ID
                    sent_message.message_id,  # Message ID to forward
                    message_thread_id=LOG_SUCCESS_TOPIC_ID,  # Forward to correct topic
                )
            os.remove(video_path)  # Clean up after sending
        update_user_stats(message.from_user.id, success=True)
    except Exception as e:
        log_error_message = f"{log_text}\n\nError: {e}"
        error_message = f"Error: {e}"
        bot.reply_to(message, error_message)
        log_to_topic(message, log_error_message, LOG_ERROR_TOPIC_ID)
        update_user_stats(message.from_user.id, error=True)

    # bot.delete_message(chat_id=message.chat.id, message_id=downloading_msg.message_id)


if __name__ == "__main__":
    bot.polling()

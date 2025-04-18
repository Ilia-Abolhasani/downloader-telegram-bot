
# 📥 Downloader Telegram Bot

A simple Telegram bot that downloads videos from public Instagram posts using `yt-dlp`. Built with Python and powered by the Telegram Bot API, this project is ideal for personal use or private bots.

## 🚀 Features

- ✅ Download videos from Instagram (public posts)
- 🔐 Session cookie support for private content (requires `sessionid`)
- 🧠 Smart URL validation
- 📝 Logs messages and video downloads to a Telegram group/topic
- 🗑️ Cleans up temporary video files after sending
- 🔄 Simple message forwarding for audit/logging

## 📁 Project Structure
- ├── downloads/# Temporary directory for downloaded videos
- ├── README.md # Project documentation
- ├── requirements.txt # Required Python packages
- ├── run.py # Main bot logic
- ├── send_message.py # Utility to send custom messages to users
- ├── .env.template # Template for environment variables 
- ├── .gitignore # Files and directories to be ignored by Git
- └── venv/ # Virtual environment (excluded via .gitignore)


## 🛠 Requirements

- Python 3.8+
- Telegram bot token
- Telegram group/topic for logging (optional)
- Instagram account with session cookie (for private videos)

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🔐 Environment Variables
Create a .env file in the root directory with the following values:
```
## bot_api_key
bot_api_key=YOUR_BOT_TOKEN
log_chat_id=YOUR_LOG_CHAT_ID
log_topic_id=YOUR_TOPIC_ID
cookie_session_id=YOUR_INSTAGRAM_SESSION_ID
```

## ▶️ Running the Bot
Start the bot with:
```
python run.py
```

## 📦 send_message.py
This utility script can send a message to a specific user or chat based on a message ID.
Useful for follow-ups, manual notifications, or bot administration.

## ⚠️ Disclaimer

- This bot is intended for educational and personal use only.
- Do not use this bot to download content from private accounts without explicit permission.
- You are responsible for complying with the laws and terms of service of any platforms used.
- Ensure compliance with Instagram's [Terms of Use](https://help.instagram.com/581066165581870) and [Community Guidelines](https://help.instagram.com/477434105621119).

## 🤝 Contributing

Contributions are welcome!  
If you have ideas, bug fixes, or improvements, feel free to fork the repo and open a pull request.

For major changes, please open an issue first to discuss the proposed changes.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.

&copy; [Ilia Abolhasani](https://github.com/Ilia-Abolhasani)

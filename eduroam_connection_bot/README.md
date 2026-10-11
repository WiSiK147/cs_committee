# École Polytechnique eduroam Support Bot

A Python-based Telegram bot designed to help new students at École Polytechnique seamlessly connect their devices to the **eduroam** Wi-Fi network. 

✨ **Note: This project is fully vibecoded.** ✨

The bot provides interactive, step-by-step configuration guides for all major operating systems, troubleshooting parameters, and an instant alert system to ping support staff for in-person help.

## Features

* **Interactive Device Menus:** Clear inline keyboards for easy navigation.
* **Platform-Specific Guides:** Tailored instructions and download links for:
  * iOS (iPhone / iPad) via Safari profiles
  * Android via the `geteduroam` app
  * Laptops (Windows / macOS) via `cat.eduroam.org`
* **BYOD & Guest Support:** Direct links to the MAC address registration portal for smart devices and instructions for temporary guest access.
* **Troubleshooting:** Quick access to manual connection parameters (SSID, EAP Method, Phase 2 Auth, etc.).
* **Live Helper Alert System:** A built-in SOS button that broadcasts an alert (including the student's name and username) to pre-registered IT helpers, calling them to the physical support desk.

## Prerequisites

* **Python 3.7+**
* A Telegram Bot API Token (obtained via [@BotFather](https://t.me/botfather) on Telegram)
* `pyTelegramBotAPI` library

## Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/YOUR-USERNAME/eduroam-support-bot.git
cd eduroam-support-bot
```

**2. Install dependencies**
Install the required pyTelegramBotAPI library:
```bash
pip install pyTelegramBotAPI
```

**3. Configure the Bot**
Open the main Python script (e.g., `bot.py`) and update the following variables at the top of the file:

* `API_TOKEN`: Insert your Bot API token from @BotFather.
* `HELPER_CHAT_IDS`: Add the numeric Telegram Chat IDs of your support team members. 
  * *Note: Helpers must have started a chat with the bot at least once before they can receive broadcasted alerts.*

```python
API_TOKEN = "YOUR_BOT_API_TOKEN_HERE"
HELPER_CHAT_IDS = [123456789, 987654321] # Replace with actual numeric IDs
```

**4. Run the Bot**
```bash
python bot.py
```
You should see `Bot is running...` in your terminal. Open Telegram and send `/start` to your bot to test it.

## Usage / Commands

* `/start` or `/help` - Initializes the bot, provides default credential formats, and opens the main device selection menu.

## Technologies Used

* [Python](https://www.python.org/)
* [pyTelegramBotAPI (Telebot)](https://github.com/eternnoir/pyTelegramBotAPI) - Python wrapper for the Telegram Bot API.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

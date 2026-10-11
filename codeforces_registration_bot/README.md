# Codeforces Registration Telegram Bot 🚀

**Note: This project is 100% vibe-coded!** 🧠✨ It was built entirely through AI/LLM interactions without writing the core logic manually. 

This repository contains two different Telegram bots designed to manage join requests for a Codeforces group. Codeforces does not provide an official API to accept group join requests, so these bots provide two different workarounds: a heavy automation approach and a lightweight manual-approval approach.

## 📦 The Two Versions

### Version 1: The Automation Juggernaut (SeleniumBase)
This version runs a permanent, headless-like Chrome browser session on your machine using `SeleniumBase`.
- **How it works:** Users send their `name.surname` and Codeforces handle to the bot. The bot adds them to a queue, physically navigates to your Codeforces group members page (bypassing Cloudflare protection), finds the specific user's row, and clicks "Accept" on your behalf.
- **Pros:** 100% automated. The admin doesn't need to do anything.
- **Cons:** Requires a machine that can run a Chrome browser (like a local laptop or a server with a virtual display/persistent profile). Heavy on resources.

### Version 2: The Lightweight Admin-Approval Bot (pyTelegramBotAPI)
This version drops the browser automation entirely and relies on Telegram's inline buttons.
- **How it works:** Users send their details to the bot. The bot instantly forwards the request to your private Telegram chat with two inline buttons: **✅ Accept** or **❌ Reject**. You go to Codeforces yourself, accept them, and then click the button in Telegram. The bot then updates the database and notifies the user of your decision.
- **Pros:** Extremely fast, lightweight, and can run on the cheapest Linux VPS or Raspberry Pi. Zero Cloudflare issues.
- **Cons:** Requires the admin to manually click "Accept" on the Codeforces website.

---

## 🛠️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/codeforces-registration-bot.git
   cd codeforces-registration-bot
   ```

2. **Install the dependencies:**
   ```bash
   pip install pyTelegramBotAPI python-dotenv
   # If using Version 1, also install seleniumbase:
   pip install seleniumbase
   ```

3. **Configure your Environment Variables:**
   Rename `.env.example` to `.env` and fill in your details:
   ```env
   # Shared Variables
   TELEGRAM_TOKEN=your_telegram_bot_token_here
   DB_FILE=users_db.json

   # Variables for Version 1 (Browser Automation)
   GROUP_ID=your_codeforces_group_id
   ADMIN_HANDLE=your_codeforces_bot_account_handle
   ADMIN_PASSWORD=your_codeforces_password

   # Variables for Version 2 (Admin Approval)
   ADMIN_CHAT_ID=123456789
   ```

4. **Run the bot:**
   ```bash
   # For the automated version:
   python3 version1_automation.py
   
   # OR for the lightweight version:
   python3 version2_lightweight.py
   ```

## 🗄️ Database
Both bots automatically generate a `users_db.json` file to keep track of accepted and failed/rejected users, preventing duplicates and spam.

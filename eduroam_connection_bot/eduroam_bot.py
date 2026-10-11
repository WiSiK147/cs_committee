import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Insert your Bot API Token from @BotFather here
API_TOKEN = "" #bot api token

# Add the Telegram CHAT_IDs (numeric integers) of all helpers.
# NOTE: Each helper MUST have started/messaged the bot at least once!
HELPER_CHAT_IDS = ['''helper's Chat ID''']

bot = telebot.TeleBot(API_TOKEN)

# --- KEYBOARD BUILDERS ---

def get_main_keyboard():
    """Builds the primary device selection menu."""
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("📱 iPhone / iPad", callback_data="device_ios"),
        InlineKeyboardButton("🤖 Android", callback_data="device_android"),
        InlineKeyboardButton("💻 Windows / Mac", callback_data="device_desktop"),
        InlineKeyboardButton("🎮 BYOD (Smart Devices)", callback_data="device_byod"),
        InlineKeyboardButton("🌐 Guest Wi-Fi", callback_data="device_guest"),
        InlineKeyboardButton("🛠️ Troubleshooting", callback_data="troubleshoot")
    )
    # Helptable button spans full width at the bottom
    markup.add(InlineKeyboardButton("📍 In-Person Help & Alert Team", callback_data="helptable"))
    return markup

def get_back_keyboard():
    """Builds a simple navigation back button."""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("« Back to Main Menu", callback_data="main_menu"))
    return markup


# --- COMMAND HANDLERS ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 **Welcome to the École Polytechnique Wi-Fi Support Bot!**\n\n"
        "I can help you connect your devices to **eduroam** quickly.\n\n"
        "🔑 **Your Default Credentials:**\n"
        "• **Username:** `firstname.lastname@polytechnique.fr`\n"
        "• **Password:** Your LDAP password *(Synapses/Moodle)*\n\n"
        "⚠️ *Make sure you have active mobile data or are connected to 'Wi-Fi Guest' first to download tools!*\n\n"
        "**Please select your device below:**"
    )
    bot.send_message(
        message.chat.id, 
        welcome_text, 
        parse_mode="Markdown", 
        reply_markup=get_main_keyboard()
    )


# --- CALLBACK QUERY HANDLER (BUTTON PRESSES) ---

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    user = call.from_user

    # 1. Main Menu
    if call.data == "main_menu":
        text = (
            "👋 **École Polytechnique Wi-Fi Support**\n\n"
            "Select your device or issue from the options below:"
        )
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=get_main_keyboard())

    # 2. iOS (iPhone / iPad)
    elif call.data == "device_ios":
        text = (
            "📱 **iPhone / iPad Setup Instructions:**\n\n"
            "1. Open **Safari** *(you MUST use Safari)* and visit: https://cat.eduroam.org/\n"
            "2. Tap **'Download your eduroam installer'** and choose **'École Polytechnique'**.\n"
            "3. Allow the profile download.\n"
            "4. Open your phone's **Settings** app → tap **Profile Downloaded** (near the top).\n"
            "5. Tap **Install**, enter your passcode, and input your credentials:\n"
            "   • `firstname.lastname@polytechnique.fr`\n"
            "   • LDAP Password\n"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔗 Open cat.eduroam.org", url="https://cat.eduroam.org/"))
        markup.add(InlineKeyboardButton("« Back to Main Menu", callback_data="main_menu"))
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # 3. Android
    elif call.data == "device_android":
        text = (
            "🤖 **Android Setup Instructions:**\n\n"
            "1. Install the **geteduroam** app from the Google Play Store.\n"
            "2. Open the app and search for **'École Polytechnique'**.\n"
            "3. Enter your full email: `firstname.lastname@polytechnique.fr`\n"
            "4. Enter your LDAP Password and tap **Connect**.\n"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔗 Download geteduroam (Play Store)", url="https://play.google.com/store/apps/details?id=app.eduroam.geteduroam"))
        markup.add(InlineKeyboardButton("« Back to Main Menu", callback_data="main_menu"))
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # 4. Laptops (Windows / macOS)
    elif call.data == "device_desktop":
        text = (
            "💻 **Windows & macOS Setup Instructions:**\n\n"
            "1. Open your browser and go to: https://cat.eduroam.org/\n"
            "2. Click **'Download your eduroam installer'**.\n"
            "3. Select **'École Polytechnique'** and download the installer.\n"
            "4. Run the downloaded file and enter your username (`firstname.lastname@polytechnique.fr`) and LDAP password when prompted."
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔗 Open cat.eduroam.org", url="https://cat.eduroam.org/"))
        markup.add(InlineKeyboardButton("« Back to Main Menu", callback_data="main_menu"))
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # 5. BYOD (Printers, Consoles, Smart TVs)
    elif call.data == "device_byod":
        text = (
            "🎮 **BYOD Network Registration:**\n\n"
            "⚠️ *Do NOT connect laptops or smartphones here.*\n\n"
            "1. Find your device's **MAC Address** in its network settings.\n"
            "2. Go to the registration portal.\n"
            "3. Log in with your LDAP credentials.\n"
            "4. Select your building and register the MAC address."
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔗 Open BYOD Portal", url="https://portail-wifi-byod.polytechnique.fr/deleg/"))
        markup.add(InlineKeyboardButton("« Back to Main Menu", callback_data="main_menu"))
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # 6. Guest Wi-Fi
    elif call.data == "device_guest":
        text = (
            "🌐 **Guest Wi-Fi (Temporary Access):**\n\n"
            "1. Connect to the SSID: `Wi-Fi Guest`\n"
            "2. The captive portal web page will open automatically.\n"
            "3. Log in with LinkedIn/Twitter **OR** click the red button to get credentials via email."
        )
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=get_back_keyboard())

    # 7. Troubleshooting & Manual Configuration
    elif call.data == "troubleshoot":
        text = (
            "🛠️ **Troubleshooting & Manual Settings:**\n\n"
            "**Common Checks:**\n"
            "✓ Did you append `@polytechnique.fr` to your username?\n"
            "✓ Did you 'Forget' old eduroam networks / delete old profiles?\n\n"
            "**Manual Connection Parameters:**\n"
            "• **SSID:** `eduroam`\n"
            "• **EAP Method:** `TTLS`\n"
            "• **Phase 2 Auth:** `PAP`\n"
            "• **Anonymous Identity:** `anonymous@polytechnique.fr`\n"
            "• **Servers (Win):** `nac-wifi1.polytechnique.fr;nac-wifi2.polytechnique.fr`\n"
            "• **Trusted Root CAs:** AAA Certificate Services & USERTrust RSA"
        )
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=get_back_keyboard())

    # 8. Helptable Location & Live Alert Menu
    elif call.data == "helptable":
        text = (
            "📍 **In-Person Wi-Fi Helptable:**\n\n"
            "We have a dedicated support desk located on the **Ground Floor** (Main Hall).\n\n"
            "If no helper is currently sitting at the desk, press the button below to **call a team member** to the helptable!"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🚨 Call Helper to Desk", callback_data="alert_helpers"))
        markup.add(InlineKeyboardButton("« Back to Main Menu", callback_data="main_menu"))
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # 9. Alert Helpers Callback
    elif call.data == "alert_helpers":
        # Format user info
        user_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        username_str = f"(@{user.username})" if user.username else "(No @username set)"
        
        alert_msg = (
            f"🚨 **HELPTABLE ALERT!**\n\n"
            f"A student needs assistance at the **Ground Floor Helptable**!\n\n"
            f"👤 **Student:** {user_name} {username_str}\n"
            f"🆔 **User ID:** `{user.id}`"
        )

        # Broadcast message to all registered helpers
        sent_count = 0
        for helper_id in HELPER_CHAT_IDS:
            try:
                bot.send_message(helper_id, alert_msg, parse_mode="Markdown")
                sent_count += 1
            except Exception as e:
                print(f"Failed to alert helper {helper_id}: {e}")

        # Pop up a brief alert overlay on user's screen
        bot.answer_callback_query(call.id, text="🔔 Alert sent to team members!", show_alert=True)

        # Update screen text
        confirm_text = (
            "✅ **Team Alerted!**\n\n"
            "A message has been sent to our Wi-Fi support team. Someone will meet you at the **Ground Floor Helptable** shortly!"
        )
        bot.edit_message_text(confirm_text, chat_id, message_id, parse_mode="Markdown", reply_markup=get_back_keyboard())


# --- START POLLING ---
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
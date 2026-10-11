import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# ================= CONFIGURATION =================
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
# Convert the admin ID from string to integer
ADMIN_CHAT_ID = int(os.getenv('ADMIN_CHAT_ID')) 
DB_FILE = os.getenv('DB_FILE', 'users_db.json')
# =================================================


bot = telebot.TeleBot(TELEGRAM_TOKEN)
user_data = {}

# ================= DATABASE =================
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            db = json.load(f)
            # Ensure all keys exist in case of old database versions
            if "pending" not in db: db["pending"] = {}
            if "rejected" not in db: db["rejected"] = {}
            return db
    return {"accepted": {}, "rejected": {}, "pending": {}}

def save_db(db):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=4, ensure_ascii=False)

# ================= USER REGISTRATION FLOW =================
@bot.message_handler(commands=['start', 'join'])
def send_welcome(message):
    msg = bot.reply_to(message, "Welcome! To join the Codeforces group, please enter your name and surname in the format: **name.surname**")
    bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name_surname = message.text.strip().lower()
        
        if "." not in name_surname or len(name_surname.split(".")) != 2:
            msg = bot.reply_to(message, "Invalid format. Please use strictly the **name.surname** format. Try again:")
            bot.register_next_step_handler(msg, process_name_step)
            return

        db = load_db()
        if name_surname in db["accepted"]:
            bot.reply_to(message, f"The user {name_surname} has already been successfully added to the group!")
            return

        user_data[chat_id] = {'name': name_surname}
        msg = bot.reply_to(message, f"Got it, {name_surname}. Now, please enter your exact **Codeforces handle**:")
        bot.register_next_step_handler(msg, process_cf_handle_step)
        
    except Exception as e:
        bot.reply_to(message, 'Something went wrong. Please type /start to try again.')

def process_cf_handle_step(message):
    try:
        chat_id = message.chat.id
        cf_handle = message.text.strip()
        name = user_data[chat_id]['name']
        
        db = load_db()
        # Check for duplicates by handle
        is_duplicate = any(
            (isinstance(v, dict) and v.get("handle") == cf_handle) or (isinstance(v, str) and v == cf_handle)
            for v in db["accepted"].values()
        )
        
        if is_duplicate:
            bot.send_message(chat_id, f"The account {cf_handle} is already in the group!")
            return

        # Create a unique request ID
        request_id = f"{chat_id}_{cf_handle}"
        
        # Save user info to pending database
        user_info = {
            "chat_id": chat_id,
            "name": name,
            "handle": cf_handle,
            "tg_username": message.from_user.username,
            "tg_id": message.from_user.id
        }
        db["pending"][request_id] = user_info
        save_db(db)

        # Notify the User
        bot.send_message(chat_id, f"✅ Your request for **{cf_handle}** has been sent to the administrator.\n\nPlease make sure you have clicked 'Join' on the Codeforces group page. You will receive a notification here once the admin processes your request.", parse_mode="Markdown")
        
        # Notify the Admin with Inline Buttons
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("✅ Accept", callback_data=f"accept_{request_id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{request_id}")
        )
        
        tg_mention = f"@{user_info['tg_username']}" if user_info['tg_username'] else f"ID: {user_info['tg_id']}"
        admin_text = (
            f"🆕 <b>New Join Request!</b>\n\n"
            f"👤 <b>Name:</b> {name}\n"
            f"💻 <b>CF Handle:</b> {cf_handle}\n"
            f"📱 <b>Telegram:</b> {tg_mention}\n\n"
            f"<i>Please accept/reject them on Codeforces, then click a button below to notify the user.</i>"
        )
        bot.send_message(ADMIN_CHAT_ID, admin_text, reply_markup=markup, parse_mode="HTML")
            
    except Exception as e:
        bot.reply_to(message, 'Something went wrong. Please type /start to try again.')

# ================= ADMIN BUTTON CALLBACKS =================
@bot.callback_query_handler(func=lambda call: call.data.startswith('accept_') or call.data.startswith('reject_'))
def handle_admin_decision(call):
    # Only the admin should be able to press these buttons
    if call.message.chat.id != ADMIN_CHAT_ID:
        return

    action, req_id = call.data.split('_', 1)
    db = load_db()
    
    if req_id not in db["pending"]:
        bot.answer_callback_query(call.id, "This request has already been processed or doesn't exist.")
        return
        
    req_data = db["pending"].pop(req_id)
    user_chat_id = req_data["chat_id"]
    name = req_data["name"]
    handle = req_data["handle"]
    
    if action == "accept":
        db["accepted"][name] = req_data
        # Update the admin's message so the buttons disappear
        bot.edit_message_text(f"✅ <b>Approved:</b> {name} ({handle})", call.message.chat.id, call.message.message_id, parse_mode="HTML")
        # Notify the user
        try:
            bot.send_message(user_chat_id, f"🎉 <b>Good news!</b> The administrator has accepted your request. You are now in the Codeforces group with the handle <b>{handle}</b>.", parse_mode="HTML")
        except:
            pass # Fails if user blocked the bot
            
    elif action == "reject":
        db["rejected"][name] = req_data
        bot.edit_message_text(f"❌ <b>Rejected:</b> {name} ({handle})", call.message.chat.id, call.message.message_id, parse_mode="HTML")
        try:
            bot.send_message(user_chat_id, f"❌ Your request to join with the handle <b>{handle}</b> was declined by the administrator. Please make sure you clicked 'Join' on the Codeforces page, or contact the admin.", parse_mode="HTML")
        except:
            pass
            
    save_db(db)
    bot.answer_callback_query(call.id, "Action saved!")

if __name__ == '__main__':
    print("Lightweight Telegram bot is running...")
    bot.polling(none_stop=True)

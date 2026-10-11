import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import telebot
import time
import json
import os
import threading
import queue
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# ================= CONFIGURATION =================
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GROUP_ID = os.getenv('GROUP_ID')             
ADMIN_HANDLE = os.getenv('ADMIN_HANDLE')       
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')   
DB_FILE = os.getenv('DB_FILE', 'users_db.json')
# =================================================


bot = telebot.TeleBot(TELEGRAM_TOKEN)
task_queue = queue.Queue() # Queue for browser tasks
user_data = {}

# ================= DATABASE =================
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"accepted": {}, "failed": {}}

def save_db(db):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=4, ensure_ascii=False)

# ================= TELEGRAM BOT =================
@bot.message_handler(commands=['start', 'join'])
def send_welcome(message):
    msg = bot.reply_to(message, "Welcome! To join the Codeforces group, please enter your name and surname in the format: **name.surname**")
    bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name_surname = message.text.strip().lower() # Convert to lowercase for consistency
        
        if "." not in name_surname or len(name_surname.split(".")) != 2:
            msg = bot.reply_to(message, "Invalid format. Please use strictly the **name.surname** format. Try again:")
            bot.register_next_step_handler(msg, process_name_step)
            return

        # Check for duplicates by name
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
        
        # Check for duplicates by handle (supports both old string format and new dict format)
        db = load_db()
        is_duplicate = any(
            (isinstance(v, dict) and v.get("handle") == cf_handle) or (isinstance(v, str) and v == cf_handle)
            for v in db["accepted"].values()
        )
        
        if is_duplicate:
            bot.send_message(chat_id, f"The account {cf_handle} is already in the group!")
            return

        bot.send_message(chat_id, f"Adding your request to the processing queue ({name}, CF: {cf_handle})...\nPlease make sure you have already clicked 'Join' on the Codeforces group page.")
        
        # Send task to the background browser queue WITH Telegram info
        task_queue.put({
            'chat_id': chat_id, 
            'name': name, 
            'handle': cf_handle,
            'tg_username': message.from_user.username,
            'tg_id': message.from_user.id
        })
            
    except Exception as e:
        bot.reply_to(message, 'Something went wrong. Please type /start to try again.')

# ================= BACKGROUND BROWSER (WORKER) =================
def browser_worker():
    print("Initializing browser...")
    driver = Driver(uc=True)
    
    try:
        print(f"Logging in as {ADMIN_HANDLE}...")
        driver.get("https://codeforces.com/enter?locale=en")
        
        print("Waiting for Cloudflare check...")
        time.sleep(10)
        
        if "enter" not in driver.current_url:
            print("Cloudflare redirected to the main page. Returning to the login page...")
            driver.get("https://codeforces.com/enter?locale=en")
        
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "handleOrEmail")))
        
        print("Form found, logging in...")
        time.sleep(2)
        
        handle_input = driver.find_element(By.ID, "handleOrEmail")
        handle_input.clear()
        for char in ADMIN_HANDLE:
            handle_input.send_keys(char)
            time.sleep(0.1)
            
        time.sleep(1)
        pass_input = driver.find_element(By.ID, "password")
        pass_input.clear()
        for char in ADMIN_PASSWORD:
            pass_input.send_keys(char)
            time.sleep(0.1)
            
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, "submit").click()
        
        try:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, f"//a[contains(@href, '/profile/{ADMIN_HANDLE}')]")))
            print("BROWSER READY: Login successful. Waiting for tasks...")
        except TimeoutException:
            print("CRITICAL ERROR: Failed to log into the account.")
            return # Stop the worker

        # Infinite loop waiting for Telegram requests
        while True:
            task = task_queue.get() # Script pauses here until a task appears
            chat_id = task['chat_id']
            name = task['name']
            target_user_handle = task['handle']
            tg_username = task.get('tg_username')
            tg_id = task.get('tg_id')
            
            print(f"Processing task: {name} ({target_user_handle})")
            db = load_db()
            success = False
            
            try:
                # Navigate to the members page
                members_url = f"https://codeforces.com/group/{GROUP_ID}/members?locale=en"
                driver.get(members_url)
                
                WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "datatable")))
                
                row_xpath = f"//tr[.//a[contains(@href, '/profile/{target_user_handle}')]]"
                
                try:
                    user_row = driver.find_element(By.XPATH, row_xpath)
                    accept_button = user_row.find_element(By.XPATH, ".//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept') or contains(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]")
                    accept_button.click()
                    print(f"✅ Successfully accepted: {target_user_handle}")
                    time.sleep(3)
                    success = True
                except NoSuchElementException:
                    print(f"❌ Could not find request from {target_user_handle} (Maybe they didn't click Join)")
                    
            except Exception as e:
                print(f"Error during browser execution: {e}")
            
            # Update database and send response to Telegram (UPDATED JSON STRUCTURE)
            user_info = {
                "handle": target_user_handle,
                "tg_username": tg_username,
                "tg_id": tg_id
            }
            
            if success:
                db["accepted"][name] = user_info
                # If they were in the failed list previously, remove them
                if name in db["failed"]:
                    del db["failed"][name]
                bot.send_message(chat_id, f"✅ Success! The account {target_user_handle} has been accepted into the Codeforces group.")
            else:
                db["failed"][name] = user_info
                bot.send_message(chat_id, f"❌ Failed to add {target_user_handle}. Are you sure you applied on the group page? Try again: /start")
                
            save_db(db)
            task_queue.task_done() # Notify the queue that the task is done

    except Exception as e:
        print(f"Global worker error: {e}")
    finally:
        driver.quit()

if __name__ == '__main__':
    print("Starting background browser...")
    # Start browser in a separate thread (daemon=True means it closes when script stops)
    worker_thread = threading.Thread(target=browser_worker, daemon=True)
    worker_thread.start()
    
    print("Starting Telegram bot...")
    bot.polling(none_stop=True)
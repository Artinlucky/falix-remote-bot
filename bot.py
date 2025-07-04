import os
import time
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, CallbackContext

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
FALIX_EMAIL = os.getenv('FALIX_EMAIL')
FALIX_PASSWORD = os.getenv('FALIX_PASSWORD')
PORT = int(os.environ.get('PORT', 10000))

bot = Bot(token=TELEGRAM_TOKEN)
app = Flask(__name__)

dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)

def start_falix_server():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://client.falixnodes.net/server/console")
        time.sleep(4)
        driver.find_element(By.ID, "email").send_keys(FALIX_EMAIL)
        driver.find_element(By.ID, "password").send_keys(FALIX_PASSWORD)
        driver.find_element(By.ID, "login-btn").click()
        time.sleep(7)
        driver.find_element(By.XPATH, "//button[contains(text(),'Start')]").click()
        time.sleep(5)
        driver.quit()
        return True
    except Exception as e:
        print("Error:", e)
        driver.quit()
        return False

def start_server(update: Update, context: CallbackContext):
    update.message.reply_text("Starting your FalixNodes server, please wait...")
    success = start_falix_server()
    if success:
        update.message.reply_text("✅ Server started successfully!")
    else:
        update.message.reply_text("❌ Failed to start server.")

dispatcher.add_handler(CommandHandler("startserver", start_server))

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def index():
    return "Bot is running."

if __name__ == "__main__":
    bot.set_webhook(url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TELEGRAM_TOKEN}")
    app.run(host="0.0.0.0", port=PORT)

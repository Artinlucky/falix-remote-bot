import time
import os
from flask import Flask, request
import telebot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
FALIX_EMAIL = os.environ['FALIX_EMAIL']
FALIX_PASSWORD = os.environ['FALIX_PASSWORD']

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['startserver'])
def handle_start(message):
    bot.reply_to(message, "🔄 Starting your FalixNodes server...")

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://client.falixnodes.net/login")
        time.sleep(3)
        driver.find_element(By.NAME, "email").send_keys(FALIX_EMAIL)
        driver.find_element(By.NAME, "password").send_keys(FALIX_PASSWORD)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(5)

        driver.get("https://client.falixnodes.net/server")
        time.sleep(5)
        start_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Start')]")
        start_button.click()
        time.sleep(2)
        bot.send_message(message.chat.id, "✅ Server started!")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {str(e)}")
    finally:
        driver.quit()

@app.route('/')
def home():
    return 'Bot running!'

@app.route('/' + TELEGRAM_TOKEN, methods=['POST'])
def receive_update():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return 'OK'

def start():
    bot.remove_webhook()
    bot.set_webhook(url=os.environ['RENDER_EXTERNAL_URL'] + TELEGRAM_TOKEN)
    app.run(host="0.0.0.0", port=10000)

if __name__ == '__main__':
    start()

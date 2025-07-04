import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
FALIX_EMAIL = os.getenv('FALIX_EMAIL')
FALIX_PASSWORD = os.getenv('FALIX_PASSWORD')

FALIX_CONSOLE_URL = 'https://client.falixnodes.net/server/console'

def start_falix_server():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")  # Needed for some Linux containers

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(FALIX_CONSOLE_URL)
        time.sleep(3)

        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-btn")

        email_input.send_keys(FALIX_EMAIL)
        password_input.send_keys(FALIX_PASSWORD)
        login_button.click()

        time.sleep(7)

        start_button = driver.find_element(By.XPATH, "//button[contains(text(),'Start')]")
        start_button.click()
        time.sleep(5)

        driver.quit()
        return True

    except Exception as e:
        print("Error starting server:", e)
        driver.quit()
        return False

def startserver(update: Update, context: CallbackContext):
    update.message.reply_text("Starting your FalixNodes server, please wait...")
    success = start_falix_server()
    if success:
        update.message.reply_text("Server started successfully!")
    else:
        update.message.reply_text("Failed to start the server. Check logs.")

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("startserver", startserver))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

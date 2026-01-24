import telebot
import re
import io
from telebot import types

# Your provided Token
API_TOKEN = '8513430754:AAHqlTk9dJa7zV-v4SWlgT1S016LbULhyU4'
bot = telebot.TeleBot(API_TOKEN)

# Temporary storage for multi-message support
user_data = {}

def get_action_markup():
    markup = types.InlineKeyboardMarkup()
    btn_done = types.InlineKeyboardButton("📥 GENERATE FILE", callback_data="generate_file")
    btn_clear = types.InlineKeyboardButton("🗑️ CLEAR LIST", callback_data="clear_data")
    markup.add(btn_done, btn_clear)
    return markup

# Handle /start and /help commands
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.from_user.id
    user_data[user_id] = [] # Reset data for user
    welcome_text = ("<b>🚀 Welcome To NUMBER EXTRACTOR BOT 🤖✨</b>\n\n"
                    "<b>💥 Bot Created By @Lohit_69 💎</b>\n\n"
                    "<b>📥 PLEASE SEND YOUR TEXT OR LIST 🔥</b>\n"
                    "<i>(You can send multiple messages. Click 'Generate' when done.)</i>")
    bot.reply_to(message, welcome_text, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    user_id = call.from_user.id
    
    if call.data == "generate_file":
        collected = user_data.get(user_id, [])
        if not collected:
            bot.answer_callback_query(call.id, "❌ No numbers collected yet!", show_alert=True)
            return

        # নম্বর থেকে ডুপ্লিকেট সরানো এবং সর্ট করা
        unique_numbers = sorted(list(set(collected)))
        
        # '+' এড করা
        formatted_list = [f"+{num}" for num in unique_numbers]
        total_count = len(formatted_list)

        # ফাইল কন্টেন্ট তৈরি
        file_content = "\n".join(formatted_list)

        # ইন-মেমোরি ফাইল তৈরি
        file_stream = io.BytesIO(file_content.encode('utf-8'))
        
        # SMART NAMING: LISTED_500_Numbers.txt
        file_stream.name = f"LISTED_{total_count}_Numbers.txt"

        # ফাইলটি ইউজারের কাছে পাঠানো
        bot.send_document(
            call.message.chat.id,
            file_stream,
            caption=
            ("<b>✅ EXTRACTION COMPLETE!</b>\n\n"
             f"<b>📊 Total Unique Numbers:</b> <code>{total_count}</code>\n"
             f"<b>📁 Filename:</b> <code>{file_stream.name}</code>\n\n"
             "<b>🔥 Powered By @Lohit_69</b>"),
            parse_mode='HTML')
        
        # Clear data after generation
        user_data[user_id] = []
        bot.answer_callback_query(call.id, "File Generated Successfully!")

    elif call.data == "clear_data":
        user_data[user_id] = []
        bot.answer_callback_query(call.id, "List Cleared!")
        bot.send_message(call.message.chat.id, "<b>🗑️ Your collection has been cleared.</b>", parse_mode='HTML')

# Handle all incoming text messages
@bot.message_handler(func=lambda message: True)
def process_numbers(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = []

    # Improved Regex: Extracts digits between 9 to 15 length
    found_numbers = re.findall(r'\d{9,15}', message.text)

    if not found_numbers:
        bot.reply_to(
            message,
            "<b>❌ NO VALID NUMBERS FOUND!</b>\n<i>Please send a text containing phone numbers.</i>",
            parse_mode='HTML')
        return

    # Add to the session pool
    user_data[user_id].extend(found_numbers)
    current_total = len(set(user_data[user_id]))

    bot.reply_to(
        message,
        f"<b>📥 Added {len(found_numbers)} numbers.</b>\n"
        f"<b>📊 Current Unique Pool:</b> <code>{current_total}</code>\n\n"
        "<i>Send more lists or click the button below to finish.</i>",
        parse_mode='HTML',
        reply_markup=get_action_markup())

if __name__ == "__main__":
    print("--- NUMBER SEPARATOR BOT IS ONLINE ---")
    bot.infinity_polling()

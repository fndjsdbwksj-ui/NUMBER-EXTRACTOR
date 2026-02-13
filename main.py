import telebot
import re
import io
import threading
from telebot import types

# Your provided Token
API_TOKEN = '8513430754:AAHqlTk9dJa7zV-v4SWlgT1S016LbULhyU4'
bot = telebot.TeleBot(API_TOKEN)

# Storage for collected numbers and timers
user_data = {}
user_timers = {}

def process_and_send_file(chat_id, user_id):
    """Processes the collected numbers and sends the file."""
    if user_id not in user_data or not user_data[user_id]:
        return

    collected = user_data[user_id]
    # Remove duplicates and sort
    unique_numbers = sorted(list(set(collected)))
    formatted_list = [f"+{num}" for num in unique_numbers]
    total_count = len(formatted_list)
    
    file_content = "\n".join(formatted_list)
    file_stream = io.BytesIO(file_content.encode('utf-8'))
    file_stream.name = f"EXTRACTED_{total_count}_Numbers.txt"

    bot.send_document(
        chat_id,
        file_stream,
        caption=(
            "<b>✅ EXTRACTION COMPLETE!</b>\n\n"
            f"<b>📊 Total Unique Numbers:</b> <code>{total_count}</code>\n"
            "<b>🔥 Powered By @Lohit_69</b>"
        ),
        parse_mode='HTML'
    )
    
    # Clear data for this session after sending
    user_data[user_id] = []
    if user_id in user_timers:
        del user_timers[user_id]

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = ("<b>🚀 Welcome To NUMBER EXTRACTOR BOT 🤖✨</b>\n\n"
                    "<b>💥 Bot Created By @Lohit_69 💎</b>\n\n"
                    "<b>📥 SEND YOUR TEXT OR LIST BELOW 🔥</b>\n"
                    "<i>(I will automatically combine and extract numbers!)</i>")
    bot.reply_to(message, welcome_text, parse_mode='HTML')

@bot.message_handler(func=lambda message: True)
def handle_incoming_text(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Extract numbers (9 to 15 digits)
    found_numbers = re.findall(r'\d{9,15}', message.text)

    if not found_numbers:
        bot.reply_to(message, "<b>❌ NO VALID NUMBERS FOUND!</b>", parse_mode='HTML')
        return

    # Initialize list if first time
    if user_id not in user_data:
        user_data[user_id] = []

    # Add new numbers to the pool
    user_data[user_id].extend(found_numbers)

    # --- Debouncing Logic ---
    # If a timer is already running for this user, cancel it
    if user_id in user_timers:
        user_timers[user_id].cancel()

    # Start a new timer (waits 3 seconds of silence before sending the file)
    # This allows users to send multiple messages/files at once
    t = threading.Timer(3.0, process_and_send_file, args=[chat_id, user_id])
    user_timers[user_id] = t
    t.start()

    bot.send_chat_action(chat_id, 'typing')

if __name__ == "__main__":
    print("--- AUTO-EXTRACTOR BOT IS ONLINE ---")
    bot.infinity_polling()

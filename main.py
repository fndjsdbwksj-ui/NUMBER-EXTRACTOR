import telebot
import re
import io

# Your provided Token
API_TOKEN = '8513430754:AAHqlTk9dJa7zV-v4SWlgT1S016LbULhyU4'
bot = telebot.TeleBot(API_TOKEN)


# Handle /start and /help commands
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = ("<b>🚀 Welcome To NUMBER EXTRACTOR BOT 🤖✨</b>\n\n"
                    "<b>💥 Bot Created By @Lohit_69 💎</b>\n\n"
                    "<b>📥 PLEASE SEND YOUR TEXT OR LIST 🔥</b>\n")
    bot.reply_to(message, welcome_text, parse_mode='HTML')


# Handle all incoming text messages
@bot.message_handler(func=lambda message: True)
def process_numbers(message):
    # Improved Regex: Extracts digits between 9 to 15 length
    found_numbers = re.findall(r'\d{9,15}', message.text)

    if not found_numbers:
        bot.reply_to(
            message,
            "<b>❌ NO VALID NUMBERS FOUND!</b>\n<i>Please send a text containing phone numbers.</i>",
            parse_mode='HTML')
        return

    # নম্বর থেকে ডুপ্লিকেট সরানো এবং সর্ট করা
    unique_numbers = sorted(list(set(found_numbers)))

    # '+' এড করা
    formatted_list = [f"+{num}" for num in unique_numbers]

    # ফাইল কন্টেন্ট তৈরি
    file_content = "\n".join(formatted_list)

    # ইন-মেমোরি ফাইল তৈরি
    file_stream = io.BytesIO(file_content.encode('utf-8'))
    file_stream.name = "Separated_Numbers.txt"

    # ফাইলটি ইউজারের কাছে পাঠানো
    bot.send_document(
        message.chat.id,
        file_stream,
        caption=
        ("<b>✅ EXTRACTION COMPLETE!</b>\n\n"
         f"<b>📊 Total Numbers Found:</b> <code>{len(formatted_list)}</code>\n"
         "<b>📁 Format:</b> <code>.txt (UTF-8)</code>\n\n"
         "<b>🔥 Powered By @Lohit_69</b>"),
        parse_mode='HTML')


if __name__ == "__main__":
    print("--- NUMBER SEPARATOR BOT IS ONLINE ---")
    bot.infinity_polling()

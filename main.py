import logging
import config
import database

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# handlers ফোল্ডার থেকে ফাংশন ইমপোর্ট করুন
from earn import generate_and_send_captcha, handle_earn_message
from account import show_account
from refer import show_refer
from withdraw import show_withdraw_menu
from support import show_support
from language import show_language

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

def get_main_keyboard():
    keyboard = [
        [KeyboardButton("💵 Earn"), KeyboardButton("👤 Account")],
        [KeyboardButton("💳 Withdraw"), KeyboardButton("🔗 Refer")],
        [KeyboardButton("🤝 Support"), KeyboardButton("🌐 Language")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    database.add_user(user.id, user.username, user.first_name)
    
    welcome_text = (
        f"👋 আসসালামু আলাইকুম {user.first_name}!\n"
        "আমাদের অফিশিয়াল ক্যাপচা আর্নিং প্ল্যাটফর্মে আপনাকে স্বাগতম! ❤️\n\n"
        "🚀 আপনি কি ঘরে বসে আপনার স্মার্টফোন দিয়ে প্রতিদিন নিশ্চিত পার্ট-টাইম আয় করতে চান? তাহলে আপনি একদম সঠিক জায়গায় এসেছেন! এটি বর্তমান সময়ের সবচেয়ে সহজ, বিশ্বস্ত এবং দ্রুত পেমেন্টকারী একটি রিয়েল আর্নিং বট।\n\n"
        "✨ এখানে আপনার কাজ কী?\n"
        "খুবই সহজ! ছবিতে দেওয়া ছোট ছোট ক্যাপচা কোডগুলো দেখে দেখে সঠিকভাবে টাইপ করবেন, আর প্রতি সঠিক উত্তরের জন্য সাথে সাথে টাকা আপনার অ্যাকাউন্টে যোগ হবে।\n\n"
        "💎 সততা ও নিষ্ঠার সাথে কাজ করে আমাদের শত শত ইউজার প্রতিদিন তাদের পকেট খরচ ও হাতখরচ অনায়াসেই তুলে নিচ্ছেন। "
        "দেরী না করে এখনই নিচের মেনু থেকে 💵 Earn বাটনে ক্লিক করে আপনার ইনকাম জার্নি শুরু করুন! আপনার জন্য শুভকামনা। 🌹"
    )
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # ১ম চেষ্টা: ক্যাপচা উত্তর চেক করা
    if await handle_earn_message(update, context):
        return

    # ২য় চেষ্টা: মেনু বাটন চেক করা
    if text == "💵 Earn":
        await generate_and_send_captcha(update, context)
    elif text == "👤 Account":
        await show_account(update, context)
    elif text == "🔗 Refer":
        await show_refer(update, context)
    elif text == "💳 Withdraw":
        await show_withdraw(update, context)
    elif text == "🤝 Support":
        await show_support(update, context)
    elif text == "🌐 Language":
        await show_language(update, context)

async def post_init(application: Application):
    await application.bot.set_my_commands([
        ("start", "Start the bot"),
        ("account", "Check Account"),
        ("earn", "Earn Money"),
        ("refer", "Referral Link"),
        ("withdraw", "Withdraw Funds"),
        ("support", "Support"),
        ("language", "Change Language")
    ])

def main():
    database.init_db() # ডেটাবেজ ইনিশিয়ালাইজ
    app = Application.builder().token(config.BOT_TOKEN).post_init(post_init).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("account", show_account))
    app.add_handler(CommandHandler("earn", generate_and_send_captcha))
    app.add_handler(CommandHandler("refer", show_refer))
    app.add_handler(CommandHandler("withdraw", show_withdraw))
    app.add_handler(CommandHandler("support", show_support))
    app.add_handler(CommandHandler("language", show_language))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Modular Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

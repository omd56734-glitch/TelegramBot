from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

def get_main_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton("💵 Earn"), KeyboardButton("👤 Account")],
        [KeyboardButton("💳 Withdraw"), KeyboardButton("🔗 Refer")],
        [KeyboardButton("🤝 Support"), KeyboardButton("🌐 Language")]
    ], resize_keyboard=True)

async def show_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌐 ভাষা পরিবর্তন অপশন। বর্তমানে বাংলা ভাষা সিলেক্ট করা আছে।", reply_markup=get_main_keyboard())

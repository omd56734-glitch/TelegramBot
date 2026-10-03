from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

def get_main_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton("💵 Earn"), KeyboardButton("👤 Account")],
        [KeyboardButton("💳 Withdraw"), KeyboardButton("🔗 Refer")],
        [KeyboardButton("🤝 Support"), KeyboardButton("🌐 Language")]
    ], resize_keyboard=True)

async def show_refer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bot_username = context.bot.username
    ref_link = f"https://t.me/{bot_username}?start={user_id}"
    text = f"🔗 **রেফারেল প্রোগ্রাম**\n\nআপনার বন্ধুদের সাথে এই লিংকটি শেয়ার করুন। প্রতি রেফারে বোনাস পান!\n\nআপনার রেফার লিংক:\n`{ref_link}`"
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=get_main_keyboard())

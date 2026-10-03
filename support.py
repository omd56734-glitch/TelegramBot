from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

def get_main_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton("💵 Earn"), KeyboardButton("👤 Account")],
        [KeyboardButton("💳 Withdraw"), KeyboardButton("🔗 Refer")],
        [KeyboardButton("🤝 Support"), KeyboardButton("🌐 Language")]
    ], resize_keyboard=True)

async def show_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # এখানে https://t.me/your_support_group এর জায়গায় আপনার আসল সাপোর্ট গ্রুপের লিংক বসিয়ে দিন
    group_link = "https://t.me/captcha890" 
    
    keyboard = [
        [InlineKeyboardButton("💬 আমাদের সাপোর্ট গ্রুপে জয়েন করুন", url=group_link)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "🤝 কোনো সমস্যা বা প্রশ্ন থাকলে নিচে দেওয়া লিংকে ক্লিক করে আমাদের অফিশিয়াল সাপোর্ট গ্রুপে যোগাযোগ করুন।"
    
    await update.message.reply_text(text, reply_markup=reply_markup)
    # মেইন কিবোর্ডটি টিক রাখার জন্য নিচে আরেকটি মেসেজ দিতে পারেন অথবা এখানেই শেষ করতে পারেন

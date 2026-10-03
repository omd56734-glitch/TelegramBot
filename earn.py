import random
import config
import database
from PIL import Image, ImageDraw, ImageFont
import io
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

def create_captcha_image(text):
    img = Image.new('RGB', (160, 60), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    for _ in range(5):
        d.line([random.randint(0, 160), random.randint(0, 60), random.randint(0, 160), random.randint(0, 60)], fill=(200, 200, 200), width=1)
        
    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except:
        font = ImageFont.load_default()
        
    d.text((25, 12), text, fill=(0, 0, 0), font=font)
    
    bio = io.BytesIO()
    bio.name = 'captcha.png'
    img.save(bio, 'PNG')
    bio.seek(0)
    return bio

async def generate_and_send_captcha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    captcha_text = str(random.randint(1000, 9999))
    database.set_pending_captcha(user.id, captcha_text)
    photo_bio = create_captcha_image(captcha_text)
    
    keyboard = [[InlineKeyboardButton("🔄 নতুন ক্যাপচা", callback_data="refresh_captcha")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.message.reply_photo(
            photo=photo_bio,
            caption="🖼️ উপরের ছবিতে থাকা ৪ ডিজিটের সংখ্যাটি টাইপ করে পাঠান:",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_photo(
            photo=photo_bio,
            caption="🖼️ উপরের ছবিতে থাকা ৪ ডিজিটের সংখ্যাটি টাইপ করে পাঠান:",
            reply_markup=reply_markup
        )

async def handle_earn_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text.strip()
    
    # মেনু বাটনগুলোর লিস্ট - এগুলো চাপা মাত্রই সব পেন্ডিং ক্যাপচা বাতিল হয়ে যাবে এবং মেনু কাজ করবে
    menu_buttons = ["💵 Earn", "👤 Account", "💳 Withdraw", "🔗 Refer", "🤝 Support", "🌐 Language"]
    if text in menu_buttons:
        database.clear_pending_captcha(user.id)  # মেনুতে গেলে ক্যাপচা মোড ক্লিয়ার হয়ে যাবে
        return False
    
    pending_captcha = database.get_pending_captcha(user.id)
    
    if pending_captcha:
        if text == pending_captcha:
            # সঠিক উত্তর হ্যান্ডেলিং
            database.clear_pending_captcha(user.id)
            balance = database.add_balance(user.id, 5)
            
            success_text = (
                "🎉 অভিনন্দন! আপনি সফল ও সঠিকভাবে ক্যাপচা কোডটি সাবমিট করেছেন। আপনার মেইন ব্যালেন্সে 5.00 টাকা যোগ করে দেওয়া হয়েছে। পরবর্তী কাজের জন্য আবার ক্লিক করুন。\n\n"
                f"💰 আপনার বর্তমান ব্যালেন্স : {balance} টাকা।"
            )
            await update.message.reply_text(success_text)
        else:
            await update.message.reply_text(
                "❌ ভুল ক্যাপচা! আবার সঠিক সংখ্যাটি লিখে পাঠান।"
            )

        return True
    
    return False

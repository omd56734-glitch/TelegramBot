import random
import io
from PIL import Image, ImageDraw, ImageFont
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

# --- কনফিগারেশন ---
SUPPORT_GROUP_LINK = "https://t.me/captcha890"
CHANNEL_LINK = "https://t.me/capthaearnofficial2371"

# আপনার আসল অ্যাডমিন আইডি
ADMIN_ID = 6987224465  

# গ্লোবাল ইউজার ডাটা ডিকশনারি
user_data_db = {}

def get_user(user_id):
    if user_id not in user_data_db:
        user_data_db[user_id] = {
            "balance": 0.0,
            "correct_caps": 0,
            "wrong_caps": 0,
            "referrals": 0,
            "ref_income": 0.0,
            "verified": False,
            "lang": "bn",
            "current_captcha": None,
            "withdraw_method": None
        }
    return user_data_db[user_id]

def main_reply_keyboard():
    keyboard = [
        [KeyboardButton("💵 Earn"), KeyboardButton("👤 Account")],
        [KeyboardButton("💳 Withdraw"), KeyboardButton("🔗 Refer")],
        [KeyboardButton("🤝 Support"), KeyboardButton("🌐 Language")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def generate_captcha_image(text):
    img_width, img_height = 180, 70
    image = Image.new('RGB', (img_width, img_height), color=(240, 240, 240))
    draw = ImageDraw.Draw(image)
    
    for _ in range(6):
        xy = (random.randint(0, img_width), random.randint(0, img_height), random.randint(0, img_width), random.randint(0, img_height))
        draw.line(xy, fill=(random.randint(120, 180), random.randint(120, 180), random.randint(120, 180)), width=2)
        
    try:
        font = ImageFont.load_default()
    except:
        font = None

    draw.text((40, 22), text, fill=(15, 15, 15), font=font)
    
    bio = io.BytesIO()
    bio.name = 'captcha.png'
    image.save(bio, 'PNG')
    bio.seek(0)
    return bio

# /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    u_data = get_user(user.id)
    
    args = context.args
    if args and args[0].startswith("ref_"):
        try:
            ref_by = int(args[0].split("_")[1])
            if ref_by != user.id and ref_by in user_data_db:
                user_data_db[ref_by]["referrals"] += 1
                user_data_db[ref_by]["ref_income"] += 40.0
                user_data_db[ref_by]["balance"] += 40.0
        except:
            pass

    welcome_text = (
        f"👋 আসসালামু আলাইকুম, {user.first_name}!\n\n"
        "👋 আমাদের অফিশিয়াল ক্যাপচা আর্নিং প্ল্যাটফর্মে আপনাকে স্বাগতম! ❤️\n\n"
        "🚀 ছবিতে দেওয়া ছোট ছোট ক্যাপচা কোডগুলো দেখে সঠিকভাবে টাইপ করুন, প্রতি সঠিক উত্তরের জন্য সাথে সাথে টাকা অ্যাকাউন্টে যোগ হবে। এখনই 💵 Earn এ ক্লিক করে ইনকাম শুরু করুন! 🌹"
    )
    await update.message.reply_text(welcome_text, reply_markup=main_reply_keyboard())

# অ্যাডমিন ভেরিফাই কমান্ড: /verify [user_id]
async def verify_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id != ADMIN_ID:
        await update.message.reply_text("❌ এই কমান্ডটি শুধুমাত্র অ্যাডমিনের জন্য!")
        return

    if not context.args:
        await update.message.reply_text("⚠️ ব্যবহারবিধি: `/verify ইউজার_আইডি`", parse_mode="Markdown")
        return

    try:
        target_id = int(context.args[0])
        t_data = get_user(target_id)
        t_data["verified"] = True
        
        await update.message.reply_text(f"✅ সফলভাবে ইউজার আইডি `{target_id}` এর অ্যাকাউন্ট ভেরিফাই করা হয়েছে!", parse_mode="Markdown")
        try:
            await context.bot.send_message(
                chat_id=target_id,
                text="🎉 অভিনন্দন! আপনার পেমেন্ট স্ক্রিনশট সফলভাবে চেক করা হয়েছে এবং আপনার অ্যাকাউন্ট সফলভাবে প্রিমিয়াম অ্যাক্টিভ (Verified) করা হয়েছে! 💵"
            )
        except:
            pass
    except Exception as e:
        await update.message.reply_text(f"❌ ভুল হয়েছে: {e}")

# অ্যাডমিন স্ট্যাটাস বা মোট ইউজারের সংখ্যা দেখার কমান্ড: /stats
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id != ADMIN_ID:
        await update.message.reply_text("❌ এই কমান্ডটি শুধুমাত্র অ্যাডমিনের জন্য!")
        return

    total_users = len(user_data_db)
    verified_users = sum(1 for u in user_data_db.values() if u.get("verified"))
    unverified_users = total_users - verified_users

    stats_text = (
        "📊 **বট স্ট্যাটিস্টিক্স ও ইউজার রিপোর্ট**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 মোট যুক্ত হওয়া ইউজার: `{total_users}` জন\n"
        f"✅ ভেরিফাইড ইউজার: `{verified_users}` জন\n"
        f"❌ আনভেরিফাইড ইউজার: `{unverified_users}` জন\n"
        "━━━━━━━━━━━━━━━━━━━━━━"
    )
    await update.message.reply_text(stats_text, parse_mode="Markdown")

# 📸 পেমেন্ট স্ক্রিনশট বা ছবি হ্যান্ডলার
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    u_data = get_user(user.id)
    
    if user.id == ADMIN_ID:
        await update.message.reply_text("🖼️ এটি আপনার পাঠানো ছবি।")
        return

    photo_file = await update.message.photo[-1].get_file()
    await update.message.reply_text("📥 আপনার পেমেন্ট স্ক্রিনশটটি সফলভাবে অ্যাডমিন প্যানেলে জমা হয়েছে! ৫-১০ মিনিটের মধ্যে চেক করে অ্যাকাউন্ট ভেরিফাই করে দেওয়া হবে। ধন্যবাদ! ❤️")

    caption_text = (
        "🔔 **নতুন পেমেন্ট ভেরিফিকেশন স্ক্রিনশট এসেছে!**\n\n"
        f"👤 নাম: {user.first_name}\n"
        f"🆔 ইউজার আইডি: `{user.id}`\n"
        f"🔗 ইউজারনেম: @{user.username if user.username else 'নেই'}\n"
        f"💰 বর্তমান ব্যালেন্স: {int(u_data['balance']) if u_data['balance'].is_integer() else u_data['balance']} টাকা\n"
        f"📊 স্ট্যাটাস: {'Verified ✅' if u_data['verified'] else 'Unverified ❌'}\n\n"
        "🛠️ **অ্যাকাউন্ট ভেরিফাই করতে নিচের কমান্ডে ক্লিক করুন বা কপি করুন:**\n"
        f"`/verify {user.id}`"
    )
    
    try:
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo_file.file_id,
            caption=caption_text,
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Error sending photo to admin: {e}")

# টেক্সট মেসেজ হ্যান্ডলার
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    u_data = get_user(user.id)

    if u_data.get("current_captcha"):
        expected = u_data["current_captcha"]
        if text.strip() == expected:
            u_data["balance"] += 5.0
            u_data["correct_caps"] += 1
            u_data["current_captcha"] = None
            await update.message.reply_text(
                f"🎉 অভিনন্দন! ক্যাপচা সফলভাবে সলভ হয়েছে। আপনার মেইন ব্যালেন্সে 5.00 টাকা যোগ করা হয়েছে।\n\n"
                f"💰 বর্তমান ব্যালেন্স: {int(u_data['balance']) if u_data['balance'].is_integer() else u_data['balance']} টাকা।"
            )
        else:
            u_data["wrong_caps"] += 1
            u_data["current_captcha"] = None
            await update.message.reply_text("❌ ভুল ক্যাপচা কোড! সঠিক কোড দিয়ে আবার চেষ্টা করুন।")
        return

    if text == "💵 Earn":
        captcha_code = str(random.randint(1000, 9999))
        u_data["current_captcha"] = captcha_code
        photo_bio = generate_captcha_image(captcha_code)
        await update.message.reply_photo(photo=photo_bio, caption="🔠 উপরে দেওয়া ইমেজ ক্যাপচাটি দেখে নিচের বক্সে হুবহু টাইপ করে পাঠান:")

    elif text == "👤 Account":
        profile_text = (
            "👤 আপনার পার্সোনাল প্রোফাইল ড্যাশবোর্ড\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 আইডি: {user.id}\n"
            f"👤 নাম: {user.first_name}\n"
            f"💰 ব্যালেন্স: {int(u_data['balance']) if u_data['balance'].is_integer() else u_data['balance']}.00 টাকা 💵\n"
            f"✅ সঠিক ক্যাপচা: {u_data['correct_caps']} টি\n"
            f"❌ ভুল ক্যাপচা: {u_data['wrong_caps']} টি\n"
            f"👥 সফল রেফারেল: {u_data['referrals']} জন\n"
            f"🎁 রেফারেল ইনকাম: {int(u_data['ref_income']) if u_data['ref_income'].is_integer() else u_data['ref_income']} টাকা\n"
            f"🔒 স্ট্যাটাস: {'Verified ✅' if u_data['verified'] else 'Unverified ❌'}\n"
            "━━━━━━━━━━━━━━━━━━━━━━"
        )
        await update.message.reply_text(profile_text)

    elif text == "💳 Withdraw":
        keyboard = [
            [InlineKeyboardButton("৳ বিকাশ (Bkash)", callback_data="wd_bkash"),
             InlineKeyboardButton("৳ নগদ (Nagad)", callback_data="wd_nagad")]
        ]
        await update.message.reply_text("💳 পেমেন্ট নেওয়ার জন্য আপনার পছন্দের মাধ্যমটি সিলেক্ট করুন:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif text == "🔗 Refer":
        refer_link = f"https://t.me/{context.bot.username}?start=ref_{user.id}"
        refer_text = (
            "🤝 **রেফার করে আনলিমিটেড ইনকাম করার দারুণ সুযোগ!**\n\n"
            "📢 আপনার রেফারেল লিংক দিয়ে জয়েন করলে আপনি পাবেন **৪০ টাকা** ফ্রি!\n\n"
            "✨ **আপনার ইউনিক রেফার লিংক:**\n"
            f"`{refer_link}`"
        )
        await update.message.reply_text(refer_text, parse_mode="Markdown")

    elif text == "🤝 Support":
        support_text = "🤝 আমাদের অফিশিয়াল সাপোর্ট ও হেল্প ডেস্কে যোগাযোগ করুন:"
        inline_kb = [
            [InlineKeyboardButton("📢 টেলিগ্রাম গ্রুপ", url=SUPPORT_GROUP_LINK)],
            [InlineKeyboardButton("🎬 কাজের ভিডিও", url=CHANNEL_LINK)]
        ]
        await update.message.reply_text(support_text, reply_markup=InlineKeyboardMarkup(inline_kb))

    elif text == "Language" or text == "🌐 Language":
        lang_kb = [
            [InlineKeyboardButton("বাংলা 🇧🇩", callback_data="lang_bn"),
             InlineKeyboardButton("English 🇺🇸", callback_data="lang_en")]
        ]
        await update.message.reply_text("🌐 ভাষা পরিবর্তন করুন:", reply_markup=InlineKeyboardMarkup(lang_kb))

# ইনলাইন বাটন হ্যান্ডলার
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    u_data = get_user(user.id)
    data = query.data

    if data.startswith("wd_") and not data.startswith("wd_amt_"):
        method = "বিকাশ (Bkash)" if "bkash" in data else "নগদ (Nagad)"
        u_data["withdraw_method"] = method
        
        amt_keyboard = [
            [InlineKeyboardButton("300 ৳", callback_data="wd_amt_300"),
             InlineKeyboardButton("400 ৳", callback_data="wd_amt_400"),
             InlineKeyboardButton("500 ৳", callback_data="wd_amt_500")],
            [InlineKeyboardButton("600 ৳", callback_data="wd_amt_600"),
             InlineKeyboardButton("700 ৳", callback_data="wd_amt_700"),
             InlineKeyboardButton("800 ৳", callback_data="wd_amt_800")]
        ]
        await query.message.edit_text(
            f"✅ আপনি **{method}** সিলেক্ট করেছেন।\n\n💵 এবার উইথড্র অ্যামাউন্ট সিলেক্ট করুন:",
            reply_markup=InlineKeyboardMarkup(amt_keyboard),
            parse_mode="Markdown"
        )

    elif data.startswith("wd_amt_"):
        req_amount = int(data.split("_")[2])
        method = u_data.get("withdraw_method", "বিকাশ")

        if u_data["balance"] < req_amount:
            await query.message.edit_text(
                f"❌ দুঃখিত! {req_amount} টাকা উইথড্র করার মতো পর্যাপ্ত ব্যালেন্স আপনার নেই।\n"
                f"💰 বর্তমান ব্যালেন্স: {int(u_data['balance']) if u_data['balance'].is_integer() else u_data['balance']} টাকা।"
            )
        elif not u_data["verified"]:
            verification_text = (
                f"✅ আপনি {method}-এর মাধ্যমে {req_amount} টাকা উইথড্র রিকোয়েস্ট দিয়েছেন!\n\n"
                "⚠️ **অ্যাকাউন্ট ভেরিফিকেশন স্ট্যাটাস:** ইন অ্যাক্টিভ (Unverified)\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "টাকা তুলতে হলে অ্যাকাউন্ট একবার প্রিমিয়াম অ্যাক্টিভ (Verified) করতে হবে।\n\n"
                "💵 ভেরিফিকেশন ফি: ১০০ টাকা\n"
                "📱 বিকাশ নম্বর: 01754703542\n"
                "📱 নগদ নম্বর: 01623082371\n\n"
                "⚠️ **করণীয়:**\n"
                "উপরের নম্বরে ১০০ টাকা Send Money করে সফল সেন্ড মানির পরিষ্কার স্ক্রিনশটটি এই চ্যাটে আপলোড করুন। টিম ৫ মিনিটে ভেরিফাই করে দেবে। ❤️"
            )
            await query.message.edit_text(verification_text, parse_mode="Markdown")
        else:
            await query.message.edit_text(f"✅ আপনার {req_amount} টাকার উইথড্র রিকোয়েস্ট সফলভাবে গ্রহণ করা হয়েছে!")

    elif data == "lang_bn":
        u_data["lang"] = "bn"
        await query.message.reply_text("✅ ভাষা সফলভাবে পরিবর্তন করা হয়েছে!")
    elif data == "lang_en":
        u_data["lang"] = "en"
        await query.message.reply_text("✅ Language changed successfully!")

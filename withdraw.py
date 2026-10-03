from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import database  # আপনার ডাটাবেজ মডিউল

# ১. উইথড্র মেনু দেখানোর ফাংশন (বিকাশ বা নগদ সিলেক্ট করার জন্য)
async def show_withdraw_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # টেক্সট মেসেজ বা কলব্যাক উভয় মাধ্যম থেকেই যেন কাজ করে তার চেক
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        target = query.message
    else:
        target = update.message
    
    keyboard = [
        [
            InlineKeyboardButton("📱 বিকাশ (Bkash)", callback_data="method_bkash"),
            InlineKeyboardButton("📱 নগদ (Nagad)", callback_data="method_nagad")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "💵 দয়া করে আপনার পেমেন্ট মাধ্যমটি সিলেক্ট করুন:"
    await target.reply_text(text, reply_markup=reply_markup)


# ২. উইথড্র এবং এমাউন্ট সংক্রান্ত কলব্যাক হ্যান্ডলার (অ্যাক্টিভেশন নোটিশ সহ)
async def withdraw_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # যদি ইউজার বিকাশ বা নগদ সিলেক্ট করে
    if query.data.startswith("method_"):
        method = query.data.split("_")[1] # bkash অথবা nagad
        context.user_data['withdraw_method'] = method

        keyboard = [
            [
                InlineKeyboardButton("৫০০ টাকা", callback_data="amount_500"),
                InlineKeyboardButton("৭০০ টাকা", callback_data="amount_700")
            ],
            [
                InlineKeyboardButton("১০০০ টাকা", callback_data="amount_1000"),
                InlineKeyboardButton("১৫০০ টাকা", callback_data="amount_1500")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = f"✅ আপনি **{method.upper()}** সিলেক্ট করেছেন।\n\nদয়া করে আপনার কাঙ্ক্ষিত এমাউন্টটি সিলেক্ট করুন:"
        await query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")
        return

    # যদি ইউজার এমাউন্টের কোনো বাটন সিলেক্ট করে
    if query.data.startswith("amount_"):
        selected_amount = float(query.data.split("_")[1])
        user_id = query.from_user.id
        
        try:
            user_balance = float(database.get_balance(user_id))
        except:
            user_balance = 0.0

        # লজিক ১: ব্যালেন্স কম থাকলে অপর্যাপ্ত টাকার মেসেজ দেখাবে
        if user_balance < selected_amount:
            insufficient_text = (
                "❌ দুঃখিত! পেমেন্ট রিকোয়েস্ট দেওয়ার জন্য আপনার মেইন ব্যালেন্সে পর্যাপ্ত পরিমাণ টাকা নেই। "
                "দয়া করে 💵 Earn অপশন থেকে আরও কিছু ক্যাপচা পূরণ করে ব্যালেন্স বাড়িয়ে নিন। 🌹"
            )
            await query.message.reply_text(insufficient_text)
            
        # লজিক ২: ব্যালেন্স পর্যাপ্ত থাকলে অ্যাকাউন্ট অ্যাক্টিভেশন নোটিশটি দেখাবে
        else:
            verification_text = (
                "অ্যাকাউন্ট ভেরিফিকেশন স্ট্যাটাস: ইন অ্যাক্টিভ (Unverified)\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "সম্মানিত গ্রাহক, আমাদের এই রিয়েল প্ল্যাটফর্ম থেকে টাকা তুলতে হলে আপনার অ্যাকাউন্টটি একবার প্রিমিয়াম অ্যাক্টিভ (Verified) করা বাধ্যতামূলক।\n\n"
                "💵 এককালীন ওয়ান-টাইম ভেরিফিকেশন ফি: 150 টাকা\n"
                "📱 নগদ নম্বর: 01623082371\n\n"
                "📱 বিকাশ নম্বর : 01742120640\n\n"
                "💬 কেন এই ভেরিফিকেশন ফি নেওয়া হচ্ছে?\n"
                "বাজারে অনেক অসৎ ইউজার আছেন যারা অটো-বট বা হ্যাকিং স্ক্রিপ্ট দিয়ে ফেক রেফারেল বোনাস নিয়ে সিস্টেম নষ্ট করার চেষ্টা করে। প্রকৃত এবং সৎ মেম্বারদের পেমেন্ট সিকিউরিটি নিশ্চিত করতে এবং ফেক আইডি সম্পূর্ণ দূর করতেই এই ওয়ান-টাইম 150 টাকা সিকিউরিটি ফি নেওয়া হচ্ছে। একবার ভেরিফাই হয়ে গেলে আপনি আজীবন আনলিমিটেড টাকা সরাসরি তুলতে পারবেন এবং পরবর্তী কোনো উইথড্রতে আর কোনো ফি লাগবে না। এটি ১০০% রিয়েল ও গ্যারান্টিড।\n\n"
                "⚠️⚠️ আপনার করণীয়:\n"
                "উপরে দেওয়া নম্বরে আপনার বিকাশ বা নগদ অ্যাপ থেকে 150 টাকা Send Money (সেন্ড মানি) করুন। টাকা পাঠানো সফল হলে সেন্ড মানি কনফার্মেশনের একটি পরিষ্কার স্ক্রিনশট (Screenshot) এই চ্যাটে আপলোড করে পাঠিয়ে দিন। আমাদের টিম ৫ মিনিটের মধ্যে আপনার অ্যাকাউন্টটি পার্মানেন্ট অ্যাক্টিভ করে দেবে। ধন্যবাদ! ❤️"
            )
            await query.message.reply_text(verification_text)

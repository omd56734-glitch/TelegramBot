from telegram import Update
from telegram.ext import ContextTypes
import database

async def show_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # ডেটাবেজে ইউজার নিশ্চিত করা
    database.add_user(user.id, user.username, user.first_name)
    
    # ব্যালেন্স নিয়ে আসা
    balance = database.get_balance(user.id)
    
    account_text = (
        f"👤 *আপনার অ্যাকাউন্ট ইনফো:*\n\n"
        f"🆔 আইডি: `{user.id}`\n"
        f"👤 নাম: {user.first_name}\n"
        f"💰 বর্তমান ব্যালেন্স: *{balance} টাকা*"
    )
    
    if update.callback_query:
        await update.callback_query.message.reply_text(account_text, parse_mode='Markdown')
    else:
        await update.message.reply_text(account_text, parse_mode='Markdown')

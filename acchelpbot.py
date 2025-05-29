import logging, uuid, random, string
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Bot token (already given)
BOT_TOKEN = '7819144274:AAGCil0Yt2GYO2s528IqIlEliRrlleB8kcA'

# Your Telegram channel link
CHANNEL_URL = 'https://t.me/+JNGo2Z6oKt0yOWQ1'  # Replace this

logging.basicConfig(level=logging.INFO)

# Start message
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey!👋 *Welcome to Password Reset Bot!*\n\n"
        "📩 Just send your Instagram *email* or *username* below, and send a reset link.(use mail-get links faster)",
        parse_mode="Markdown"
    )

# Handle input
async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = update.message.text.strip()

    if target.startswith("@"):
        await update.message.reply_text("⚠️ Please *remove the @* and try again.", parse_mode="Markdown")
        return

    is_email = "@" in target
    data = {
        "_csrftoken": "".join(random.choices(string.ascii_letters + string.digits, k=32)),
        "guid": str(uuid.uuid4()),
        "device_id": str(uuid.uuid4())
    }
    if is_email:
        data["user_email"] = target
    else:
        data["username"] = target

    headers = {
        "user-agent":
        f"Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440; "
        f"{''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}/"
        f"{''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; "
        f"{''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; "
        f"{''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; "
        f"{''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; en_GB;)"
    }

    try:
        res = requests.post(
            "https://i.instagram.com/api/v1/accounts/send_password_reset/",
            headers=headers,
            data=data
        )

        if "obfuscated_email" in res.text:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Join Channel", url=CHANNEL_URL)]
            ])
            msg = (
                "✅ *Reset link successfully sent!*\n\n"
                "_This bot is created by @twistens & @voxhi_"
            )
            await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=keyboard)
        else:
            await update.message.reply_text(
                "❌ *Reset link could not be sent.* Please check the username/email again.",
                parse_mode="Markdown"
            )
    except Exception as e:
        await update.message.reply_text(
            f"❌ *An error occurred:* `{str(e)}`",
            parse_mode="Markdown"
        )

# Set up the bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))

print("🚀 Acc Help Bot is now running...")
app.run_polling()

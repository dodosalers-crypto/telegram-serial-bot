import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("7638202361:AAHHflFyE1MxGnDp_T8XduCYc53UqLLdyag")
API_URL = "https://serial-register-api.yourname.workers.dev/api/register"

async def handle_serial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    serial = update.message.text.strip()

    # Basic length check
    if len(serial) < 5:
        await update.message.reply_text("❌ Invalid Serial Format")
        return

    try:
        response = requests.post(API_URL, json={"serial": serial})
        data = response.json()

        if data.get("success"):
            await update.message.reply_text(f"✅ {data.get('message')}")
        else:
            await update.message.reply_text("❌ Registration Failed")

    except:
        await update.message.reply_text("🚫 API DOWN")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_serial))

app.run_polling()

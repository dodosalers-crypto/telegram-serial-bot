from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import requests

BOT_TOKEN = "8097482357:AAHiX0sfa35AyVISPHlC9Xxa1CZlxAhYKjI"
WORKER_API = "https://toolserver.dodosalers.workers.dev/api/register"

async def handle_serial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    serial = update.message.text.strip()

    try:
        r = requests.post(
            WORKER_API,
            json={"serial": serial},
            timeout=10
        )

        if r.status_code == 200 and r.json().get("success"):
            await update.message.reply_text(f"✅ SERIAL REGISTERED\n\n{serial}")
        else:
            await update.message.reply_text("❌ FAILED TO REGISTER")

    except:
        await update.message.reply_text("❌ SERVER ERROR")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_serial))

print("🤖 Bot Running...")
app.run_polling()

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import requests

BOT_TOKEN = "8097482357:AAHiX0sfa35AyVISPHlC9Xxa1CZlxAhYKjI"
API_URL = "https://toolserver.dodosalers.workers.dev/api/register"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if len(text) < 5:
        await update.message.reply_text("❌ Invalid serial")
        return

    try:
        r = requests.post(
            API_URL,
            json={"serial": text},
            timeout=10
        )
        data = r.json()

        if data.get("success"):
            await update.message.reply_text(f"✅ SERIAL REGISTERED\n\n{text}")
        else:
            await update.message.reply_text(f"⚠️ {data.get('error','FAILED')}")

    except Exception as e:
        await update.message.reply_text("❌ Server error")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()

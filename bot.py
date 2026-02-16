import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("7638202361:AAHHflFyE1MxGnDp_T8XduCYc53UqLLdyag")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in Railway Variables")

# 🔗 Apna Worker API link yahan dalo
API_URL = "https://toolserver.dodosalers.workers.dev/api/register?serial="


# ===== START COMMAND =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send only serial number to register.\nExample:\nC39X69ZAKPHF"
    )


# ===== SERIAL HANDLER =====
async def handle_serial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    serial = update.message.text.strip()

    if len(serial) < 5:
        await update.message.reply_text("❌ Invalid Serial")
        return

    try:
        response = requests.get(API_URL + serial)
        result = response.text

        if "REGISTERED" in result or "success" in result.lower():
            await update.message.reply_text("✅ Serial Registered Successfully")
        else:
            await update.message.reply_text("⚠️ Server Response:\n" + result)

    except Exception as e:
        await update.message.reply_text("❌ Server Error")


# ===== MAIN APP =====
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_serial))

app.run_polling()

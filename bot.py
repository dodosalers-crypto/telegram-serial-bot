from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests

BOT_TOKEN = "8097482357:AAHiX0sfa35AyVISPHlC9Xxa1CZlxAhYKjI"
API_URL = "https://toolserver.dodosalers.workers.dev/api/register"

async def register(update, context):
    await update.message.reply_text("🚫 API DOWN. Registration temporarily disabled.")

# -------- GUIDE FOR WRONG COMMANDS --------
async def guide_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if text.startswith("/regis") or text.startswith("/register"):
        await update.message.reply_text(
            "❌ *Wrong format*\n\n"
            "✅ Correct usage:\n"
            "`/register SERIALNUMBER`\n\n"
            "Example:\n"
            "`/register C39X69ZAKPHF`",
            parse_mode="Markdown"
        )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # command
    app.add_handler(CommandHandler("register", register_cmd))

    # wrong format / help
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guide_message))

    app.run_polling()

if __name__ == "__main__":
    main()

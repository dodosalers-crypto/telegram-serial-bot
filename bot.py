from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests

BOT_TOKEN = "8097482357:AAHiX0sfa35AyVISPHlC9Xxa1CZlxAhYKjI"
API_URL = "https://toolserver.dodosalers.workers.dev/api/register"

# -------- /register COMMAND --------
async def register_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    # serial missing
    if len(context.args) != 1:
        await update.message.reply_text(
            "❌ *Wrong format*\n\n"
            "✅ Use:\n"
            "`/register SERIALNUMBER`\n\n"
            "Example:\n"
            "`/register C39X69ZAKPHF`",
            parse_mode="Markdown"
        )
        return

    serial = context.args[0].strip()

    # basic validation
    if len(serial) < 5:
        await update.message.reply_text("❌ Invalid serial format")
        return

    try:
        r = requests.post(
            API_URL,
            json={"serial": serial},
            timeout=10
        )
        data = r.json()

        if data.get("success"):
            await update.message.reply_text(
                f"✅ *SSTEAM A5 SUCCESSFULLY REGISTERED*\n\n`{serial}`",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(
                f"⚠️ {data.get('error', 'Already Registered')}"
            )

    except Exception:
        await update.message.reply_text("❌ Server error, try again later")

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

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests

BOT_TOKEN = "8097482357:AAHiX0sfa35AyVISPHlC9Xxa1CZlxAhYKjI"
API_URL = "https://toolserver.dodosalers.workers.dev/api/register"

async def register_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    # ❌ block private chat
    if chat.type == "private":
        await update.message.reply_text(
            "❌ *Registration not allowed in private chat*\n\n"
            "✅ Please use this command inside the official group.",
            parse_mode="Markdown"
        )
        return

    # ❌ wrong format
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

        # ✅ NEW
        if data.get("success") is True and data.get("message") == "ALREADY REGISTERED":
            await update.message.reply_text(
                f"⚠️ *Serial already registered*\n\n`{serial}`",
                parse_mode="Markdown"
            )
            return

        if data.get("success"):
            await update.message.reply_text(
                f"✅ *Serial Registered Successfully*\n\n`{serial}`",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(
                "❌ Registration failed"
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

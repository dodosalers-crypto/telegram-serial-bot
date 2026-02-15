import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

BOT_TOKEN = "8372696690:AAH9KM2gDUlRiDeHo8QVt9S_jO5QSUeshLE"
API_URL = "https://toolserver.dodosalers.workers.dev/api/register"

ADMIN_ID = 6374332180  # apna numeric telegram id

# 🔹 Check if user approved
def is_user_approved(user_id):
    r = requests.get(
        "https://toolserver.dodosalers.workers.dev/api/check_user",
        params={"id": user_id},
        timeout=10
    )
    try:
        return r.json().get("approved", False)
    except:
        return False

# 🔹 Approve command
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if len(context.args) != 1:
        await update.message.reply_text("Use: /approve USER_ID")
        return

    user_id = context.args[0]

    requests.post(
        "https://toolserver.dodosalers.workers.dev/api/approve_user",
        json={"id": user_id}
    )

    await update.message.reply_text(f"✅ User {user_id} Approved")


# 🔹 Auto Serial Detect
async def auto_register(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_chat.type == "private":
        return

    user_id = update.effective_user.id
    text = update.message.text.strip()

    if len(text) < 5 or " " in text:
        return

    # Check approval
    if not is_user_approved(user_id):
        await update.message.reply_text(
            "⏳ Waiting for admin approval.\n"
            f"Your ID: {user_id}"
        )
        return

    # Register serial
    try:
        r = requests.post(API_URL, json={"serial": text}, timeout=10)
        data = r.json()

        if data.get("message") == "ALREADY REGISTERED":
            await update.message.reply_text("⚠️ Already Registered")
            return

        if data.get("success"):
            await update.message.reply_text("✅ Registered Successfully")

            # Admin log
            await context.bot.send_message(
                ADMIN_ID,
                f"📝 New Registration\n\n"
                f"Serial: {text}\n"
                f"User ID: {user_id}"
            )
        else:
            await update.message.reply_text("❌ Failed")

    except:
        await update.message.reply_text("❌ Server Error")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("approve", approve))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), auto_register))

app.run_polling()

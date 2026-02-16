import os
from telegram.ext import ApplicationBuilder

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables")

app = ApplicationBuilder().token(BOT_TOKEN).build()


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

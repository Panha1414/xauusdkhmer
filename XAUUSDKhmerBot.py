from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, request
import os
import threading

# ================== CONFIG ==================
TOKEN = os.getenv("8991740281:AAG0cIFGLlmUql0wsDtDLoQpjDoYKZS0gP0")                    # ប្រើ Environment Variable
CHANNEL_ID = os.getenv("-1003762681312")              # ប្រើ Environment Variable
# ===========================================

app = Flask(__name__)
bot = None

@app.route('/webhook', methods=['POST'])
async def xauusd_webhook():
    global bot
    try:
        data = request.get_json()
        message = f"""🚨 **XAUUSD ALERT** 🚨

{data.get('message', 'New Signal')}
Symbol: **XAUUSD**
Price: **${data.get('price', 'N/A')}**
Time: {data.get('time', '')}

Strategy: {data.get('strategy', 'Price Action')}
        """
        if bot:
            await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')
        return "OK", 200
    except Exception as e:
        print(f"Error: {e}")
        return "ERROR", 500

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 **សួស្តី!**\n\n"
        "ខ្ញុំជា **Khmer XAUUSD Signals Bot** 🪙\n"
        "ខ្ញុំនឹងផ្ញើ alert តម្លៃមាស និង signals ជូន។\n\n"
        "/alerts - កំណត់តម្លៃដែលចង់តាមដាន"
    )

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    application = Application.builder().token(TOKEN).build()
    global bot
    bot = application.bot

    application.add_handler(CommandHandler("start", start))

    # Run Flask
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    print("✅ Bot is running...")
    application.run_polling()
    
    # Run Telegram bot
    application.run_polling()

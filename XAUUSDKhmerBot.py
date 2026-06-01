from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, request
import asyncio
import threading

# ================== CONFIG ==================
TOKEN = "8991740281:AAG0cIFGLlmUql0wsDtDLoQpjDoYKZS0gP0"          # ដាក់ Bot Token របស់អ្នក
CHANNEL_ID = "-1003762681312"          # ដាក់ Channel/Group ID (អវិជ្ជមានសម្រាប់ group)
# ===========================================

app = Flask(__name__)
bot = None  # នឹងកំណត់នៅពេល bot ដំណើរការ

@app.route('/webhook', methods=['POST'])
async def xauusd_webhook():
    global bot
    try:
        data = request.json
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
        "ខ្ញុំនឹងផ្ញើ alert តម្លៃមាស និង trading signals ជូន។\n\n"
        "/alerts - កំណត់តម្លៃដែលចង់តាមដាន\n"
        "/help - មើលព័ត៌មានបន្ថែម"
    )

def run_flask():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    # Create bot application
    application = Application.builder().token(TOKEN).build()
    global bot
    bot = application.bot

    # Add handlers
    application.add_handler(CommandHandler("start", start))

    # Run Flask in background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    print("✅ Bot កំពុងដំណើរការ... Webhook ត្រៀមទទួលពី TradingView")
    
    # Run Telegram bot
    application.run_polling()
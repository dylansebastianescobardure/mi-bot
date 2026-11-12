import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola! Pasame tu codigo: ROMA, TOKYO, etc")

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    chat = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "system", "content": "Sos un vendedor amable."}, {"role": "user", "content": texto}])
    await update.message.reply_text(chat.choices[0].message.content)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
app.run_polling()

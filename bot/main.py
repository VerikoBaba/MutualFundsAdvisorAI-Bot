from telegram import Update, Document
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
from ocr.paddle_ocr import extract_text_from_image, extract_text_from_pdf

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I'm your Mutual Fund Advisor AI 🤖\n\nSend me:\n📄 PDF of your portfolio\n🖼️ Image snapshot\n🗣️ Or type a mutual fund question!")

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    image_path = f"temp/image_{update.message.message_id}.jpg"
    await file.download_to_drive(image_path)

    extracted_text = extract_text_from_image(image_path)
    os.remove(image_path)

    await update.message.reply_text("📤 Extracted text:\n\n" + extracted_text[:3000])

async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document: Document = update.message.document
    if document.mime_type == "application/pdf":
        file = await document.get_file()
        pdf_path = f"temp/pdf_{update.message.message_id}.pdf"
        await file.download_to_drive(pdf_path)

        extracted_text = extract_text_from_pdf(pdf_path)
        os.remove(pdf_path)

        await update.message.reply_text("📤 Extracted text:\n\n" + extracted_text[:3000])

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text(f"🔍 You said: {user_message}\n\n(This will soon trigger fund analysis logic...)")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

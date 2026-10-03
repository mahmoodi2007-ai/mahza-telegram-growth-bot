import os
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes


# =========================
# تنظیمات
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_URL = "https://t.me/MahzaCollection"
WEBSITE_URL = "https://mahzacollection.ir"


# =========================
# لاگ
# =========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


# =========================
# دستور /start
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "🛍 ورود به سایت مهزا",
                url=WEBSITE_URL
            )
        ],
        [
            InlineKeyboardButton(
                "📢 عضویت در کانال مهزا",
                url=CHANNEL_URL
            )
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "سلام 🌷 به ربات Mahza Collection خوش آمدید.\n\n"
        "اینجا می‌توانید جدیدترین محصولات، تخفیف‌ها و "
        "پیشنهادهای مهزا کالکشن را دنبال کنید. 🛍✨\n\n"
        "برای ورود به سایت یا عضویت در کانال، یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=reply_markup,
    )


# =========================
# اجرای ربات
# =========================

def main():

    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN تنظیم نشده است.")

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(
        CommandHandler("start", start)
    )

    print("Mahza Collection Growth Bot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()

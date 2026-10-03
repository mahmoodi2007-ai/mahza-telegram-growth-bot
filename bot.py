import os
import logging
from datetime import datetime, timezone

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)


# ============================================================
# Configuration
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_USERNAME = "@MahzaCollection"
CHANNEL_URL = "https://t.me/MahzaCollection"
WEBSITE_URL = "https://mahzacollection.ir"


# ============================================================
# Logging
# ============================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# ============================================================
# /start
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    source = "direct"

    if context.args:
        source = context.args[0].strip().lower()

    username = user.username if user.username else "بدون_username"
    user_id = user.id

    now = datetime.now(timezone.utc).isoformat()

    logger.info(
        "NEW USER | user_id=%s | username=%s | source=%s | time=%s",
        user_id,
        username,
        source,
        now,
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "📢 عضویت در کانال مهزا",
                url=CHANNEL_URL,
            )
        ],
        [
            InlineKeyboardButton(
                "✅ عضو کانال شدم",
                callback_data="check_membership",
            )
        ],
        [
            InlineKeyboardButton(
                "🛍 مشاهده محصولات در سایت",
                url=WEBSITE_URL,
            )
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if source == "instagram":

        message = (
            "🌷 سلام و خوش آمدید به Mahza Collection\n\n"
            "🛍 مجموعه‌ای از محصولات زنانه، مردانه و کودک "
            "از برندهای منتخب را در مهزا کالکشن دنبال کنید.\n\n"
            "برای دیدن جدیدترین محصولات و اطلاع از "
            "موجودی‌های جدید، به کانال تلگرام مهزا بپیوندید. 💕\n\n"
            "1️⃣ ابتدا روی «📢 عضویت در کانال مهزا» بزنید.\n"
            "2️⃣ سپس روی «✅ عضو کانال شدم» بزنید."
        )

    elif source == "website":

        message = (
            "🌷 سلام و خوش آمدید به Mahza Collection\n\n"
            "از طریق سایت مهزا وارد ربات شده‌اید. 🛍️\n\n"
            "برای دنبال کردن جدیدترین محصولات و اطلاع از "
            "موجودی‌های جدید، به کانال تلگرام مهزا بپیوندید. 💕\n\n"
            "1️⃣ ابتدا روی «📢 عضویت در کانال مهزا» بزنید.\n"
            "2️⃣ سپس روی «✅ عضو کانال شدم» بزنید."
        )

    else:

        message = (
            "🌷 سلام و خوش آمدید به Mahza Collection\n\n"
            "🛍 جدیدترین محصولات زنانه، مردانه و کودک "
            "مهزا کالکشن را دنبال کنید.\n\n"
            "برای اطلاع از محصولات جدید و موجودی‌های تازه، "
            "به کانال تلگرام مهزا بپیوندید. 💕\n\n"
            "1️⃣ ابتدا وارد کانال شوید.\n"
            "2️⃣ سپس روی «✅ عضو کانال شدم» بزنید."
        )

    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
    )


# ============================================================
# Check Membership
# ============================================================

async def check_membership(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    user = query.from_user

    try:

        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user.id,
        )

        status = member.status

        if status in ["member", "administrator", "creator"]:

            await query.message.reply_text(
                "🎉 عضویت شما در کانال Mahza Collection تأیید شد.\n\n"
                "خوش آمدید 🌷\n"
                "از همراهی شما با مهزا کالکشن خوشحالیم. 🛍️"
            )

            logger.info(
                "MEMBERSHIP CONFIRMED | user_id=%s | username=%s",
                user.id,
                user.username,
            )

        else:

            await query.message.reply_text(
                "⚠️ هنوز عضویت شما در کانال تأیید نشده است.\n\n"
                "ابتدا وارد کانال شوید و عضو شوید، "
                "سپس دوباره روی «✅ عضو کانال شدم» بزنید."
            )

            logger.info(
                "MEMBERSHIP NOT CONFIRMED | user_id=%s | status=%s",
                user.id,
                status,
            )

    except Exception as error:

        logger.error(
            "MEMBERSHIP CHECK ERROR | user_id=%s | error=%s",
            user.id,
            error,
        )

        await query.message.reply_text(
            "⚠️ فعلاً نتوانستم عضویت شما را بررسی کنم.\n\n"
            "لطفاً مطمئن شوید ابتدا عضو کانال شده‌اید "
            "و دوباره تلاش کنید."
        )


# ============================================================
# Main
# ============================================================

def main():

    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN تنظیم نشده است.")

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CallbackQueryHandler(
            check_membership,
            pattern="^check_membership$",
        )
    )

    print("Mahza Collection Growth Bot is running...")

    application.run_polling()


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    main()

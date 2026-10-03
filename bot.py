import os
import json
import logging
import subprocess
from datetime import datetime, timezone
from pathlib import Path

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

STATS_FILE = Path("stats.json")


# ============================================================
# Logging
# ============================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# ============================================================
# Stats
# ============================================================

def load_stats():

    if not STATS_FILE.exists():

        return {
            "instagram": 0,
            "website": 0,
            "direct": 0,
            "members_confirmed": 0,
        }

    try:

        with open(STATS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception as error:

        logger.error(
            "STATS LOAD ERROR | error=%s",
            error,
        )

        return {
            "instagram": 0,
            "website": 0,
            "direct": 0,
            "members_confirmed": 0,
        }


def save_stats(stats):

    try:

        with open(STATS_FILE, "w", encoding="utf-8") as file:

            json.dump(
                stats,
                file,
                ensure_ascii=False,
                indent=2,
            )

        # ----------------------------------------------------
        # Save stats.json permanently in GitHub
        # ----------------------------------------------------

        subprocess.run(
            ["git", "config", "user.name", "Mahza Collection Bot"],
            check=True,
        )

        subprocess.run(
            [
                "git",
                "config",
                "user.email",
                "mahza-collection-bot@users.noreply.github.com",
            ],
            check=True,
        )

        subprocess.run(
            ["git", "add", "stats.json"],
            check=True,
        )

        result = subprocess.run(
            [
                "git",
                "commit",
                "-m",
                "Update stats [skip ci]",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:

            subprocess.run(
                ["git", "push"],
                check=True,
            )

            logger.info(
                "STATS SAVED TO GITHUB"
            )

        else:

            logger.info(
                "STATS COMMIT SKIPPED | %s",
                result.stdout.strip(),
            )

    except Exception as error:

        logger.error(
            "STATS GITHUB SAVE ERROR | error=%s",
            error,
        )


def increase_stat(stat_name):

    stats = load_stats()

    if stat_name not in stats:
        stats[stat_name] = 0

    stats[stat_name] += 1

    save_stats(stats)

    logger.info(
        "STAT UPDATED | %s=%s",
        stat_name,
        stats[stat_name],
    )


# ============================================================
# /start
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    source = "direct"

    if context.args:
        source = context.args[0].strip().lower()

    if source not in ["instagram", "website"]:
        source = "direct"

    increase_stat(source)

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
# /stats
# ============================================================

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    stats_data = load_stats()

    message = (
        "📊 آمار ربات Mahza Collection\n\n"
        f"📸 Instagram: {stats_data.get('instagram', 0)}\n"
        f"🌐 Website: {stats_data.get('website', 0)}\n"
        f"🔗 Direct: {stats_data.get('direct', 0)}\n"
        f"✅ Members confirmed: "
        f"{stats_data.get('members_confirmed', 0)}"
    )

    await update.message.reply_text(message)


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

            increase_stat("members_confirmed")

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

        raise ValueError(
            "BOT_TOKEN تنظیم نشده است."
        )

    application = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    application.add_handler(
        CommandHandler(
            "stats",
            stats,
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            check_membership,
            pattern="^check_membership$",
        )
    )

    print(
        "Mahza Collection Growth Bot is running..."
    )

    application.run_polling()


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    main()

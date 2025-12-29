# © [2024] Malith-Rukshan. All rights reserved.
# Repository: https://github.com/Malith-Rukshan/Suno-AI-BOT
# Modified for Russian Payment Integration by User

import asyncio
import logging
import os

from telegram.constants import ParseMode
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters
import suno

# ==========================================
# 👇 НАСТРОЙКИ (ВШИТЫ) 👇
# ==========================================

# 1. ТВОЙ ТОКЕН ОТ BOTFATHER
BOT_TOKEN = "8350338676:AAGNLXAkqmARQBpd9BqH65Jfygb_s1Ilk7c"

# 2. ТВОИ КУКИ ОТ SUNO (Чистая рабочая сессия)
# Я оставил только самое важное, чтобы библиотека не путалась
SUNO_COOKIE = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdW5vLmNvbS9jbGFpbXMvdXNlcl9pZCI6ImY3M2ExOTEyLThmODYtNGQ1MC05N2M0LWI1MGJlMzA1MGQ5OCIsImh0dHBzOi8vc3Vuby5haS9jbGFpbXMvY2xlcmtfaWQiOiJmNzNhMTkxMi04Zjg2LTRkNTAtOTdjNC1iNTBiZTMwNTBkOTgiLCJzdW5vLmNvbS9jbGFpbXMvdG9rZW5fdHlwZSI6ImFjY2VzcyIsImV4cCI6MTc2NzA0MzAxNiwiYXVkIjoic3Vuby1hcGkiLCJzdWIiOiJmNzNhMTkxMi04Zjg2LTRkNTAtOTdjNC1iNTBiZTMwNTBkOTgiLCJhenAiOiJodHRwczovL3N1bm8uY29tIiwiZnZhIjpbMCwtMV0sImlhdCI6MTc2NzAzOTQxNiwiaXNzIjoiaHR0cHM6Ly9hdXRoLnN1bm8uY29tIiwiaml0IjoiYzQxN2ZiZGMtMzNjMy00NGIxLWIzYTQtMzQ3OTY2NTY3MWFmIiwidml6IjpmYWxzZSwic2lkIjoic2Vzc2lvbl85Y2JjOGY1Zjk1OTc1N2U1NmRjMTRlIiwic3Vuby5jb20vY2xhaW1zL2VtYWlsIjoiemVwaHlyLm1pcnJvckBnbWFpbC5jb20iLCJodHRwczovL3N1bm8uYWkvY2xhaW1zL2VtYWlsIjoiemVwaHlyLm1pcnJvckBnbWFpbC5jb20ifQ.WDfnnovCKJclR9a63XPKozkRKksEuL6w08DZuYkhchR9gayj8PorQvBzUQLH6Zx5KbN7w8ZEFl3eWV-MdXG3rm037eGeQ3D_Y-H2aA-m9Wt-k0MjWYkFCcJ7Htnvl2wxa6KvwsJkjKqaErQ2hhERz3hCE8m2BWpMgpUe8XFGqhpOY0zwgb7VI_e8YmNa0H5W1b72ovJH4Q0O3iysv-5F1Igfyk4fCQ-kHdIREDnwfh4pa73AOUAyDUHmjB6LNtZSc6EUmaM1cq7Zzsi1t3lYRMjh8HJKtwURun-Hr7KZIJgu__G6kb9Cvq3xN4q3cfohcFZrlY4XodE4kw-C9Blt9A"

# 3. ДАННЫЕ ДЛЯ ОПЛАТЫ
PAYMENT_LINK = "https://tips.yandex.ru/guest/payment/3747309"
ADMIN_USERNAME = "@zephyr_murr"

# ==========================================

# Configure logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Suno AI Library
# Пытаемся передать куки напрямую как сессию
client = suno.Suno(cookie=SUNO_COOKIE)

# Store user session data
chat_states = {}

def get_base_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎨 Свой текст песни", callback_data="custom")],
        [InlineKeyboardButton("🏞️ Просто описание", callback_data="default")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = (
        "👋 Привет! Я бот для создания музыки через *Suno AI*! 🎶\n\n"
        "👉 Нажми /generate чтобы начать творить. 🚀\n"
        "👉 Нажми /credits чтобы проверить лимит генераций.\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "💎 **ПОПОЛНЕНИЕ БАЛАНСА / ДОСТУП**\n"
        "Чтобы поддержать работу бота и получить доступ к генерациям, оплатите по ссылке:\n\n"
        f"💳 [ОПЛАТИТЬ ЧЕРЕЗ YANDEX TIPS]({PAYMENT_LINK})\n\n"
        f"📩 После оплаты ОБЯЗАТЕЛЬНО отправь скриншот чека сюда: {ADMIN_USERNAME}\n"
        "━━━━━━━━━━━━━━━━━━"
    )
    await update.message.reply_markdown(welcome_message, disable_web_page_preview=True)

async def credits_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        credits = await asyncio.to_thread(client.get_credits)
        credit_info_message = (
            "*💰 Статистика кредитов*\n\n"
            f"ᗚ Доступно : {credits.credits_left}\n"
            f"ᗚ Использовано : {credits.monthly_usage}\n\n"
            "Нужно больше? Пиши админу: " + ADMIN_USERNAME
        )
        await update.message.reply_text(credit_info_message, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"⁉️ Ошибка получения баланса: {e}")

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Выбери режим: свой текст песни или просто описание темы? 🤔', reply_markup=get_base_keyboard())
    chat_states[update.effective_chat.id] = {}

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_states.pop(update.effective_chat.id, None)
    await update.message.reply_text('Генерация отменена. 🚫 Нажми /generate чтобы начать заново.')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id
    chat_states[chat_id]['mode'] = query.data
    if query.data == "custom":
        await query.message.reply_text("🎤 Отправь мне текст песни (куплеты, припев).")
    else:
        await query.message.reply_text("🎤 Опиши, о чем должна быть песня и в каком стиле.")

async def onMessage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id not in chat_states or 'mode' not in chat_states[chat_id]:
        return

    state = chat_states[chat_id]
    
    if 'lyrics' not in state:
        state['lyrics'] = update.message.text
        if state['mode'] == 'custom':
            await update.message.reply_text("🏷️ Теперь напиши стиль музыки (например: Rock, Pop, Russian Chanson).")
            return

    # Если дошли сюда, значит данные собраны
    await update.message.reply_text("🎵 Сочиняю музыку... подожди пару минут. ⏳")
    try:
        is_custom = (state['mode'] == 'custom')
        tags = update.message.text if is_custom else ""
        
        songs = await asyncio.to_thread(
            client.generate,
            prompt=state['lyrics'],
            tags=tags,
            is_custom=is_custom,
            wait_audio=True
        )

        for song in songs:
            file_path = await asyncio.to_thread(client.download, song=song)
            await context.bot.send_audio(chat_id=chat_id, audio=open(file_path, 'rb'))
            os.remove(file_path)
    except Exception as e:
        await update.message.reply_text(f"⁉️ Ошибка: {e}")
    finally:
        chat_states.pop(chat_id, None)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("generate", generate))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CommandHandler("credits", credits_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, onMessage))
    application.run_polling()

if __name__ == "__main__":
    main()

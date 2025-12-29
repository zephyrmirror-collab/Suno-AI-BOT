import asyncio
import logging
import os
from telegram.constants import ParseMode
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters
import suno

# ==========================================
# 👇 НАСТРОЙКИ 👇
# ==========================================

BOT_TOKEN = "8350338676:AAGNLXAkqmARQBpd9BqH65Jfygb_s1Ilk7c"

# Твоя рабочая сессия
SESSION_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdW5vLmNvbS9jbGFpbXMvdXNlcl9pZCI6ImY3M2ExOTEyLThmODYtNGQ1MC05N2M0LWI1MGJlMzA1MGQ5OCIsImh0dHBzOi8vc3Vuby5haS9jbGFpbXMvY2xlcmtfaWQiOiJmNzNhMTkxMi04Zjg2LTRkNTAtOTdjNC1iNTBiZTMwNTBkOTgiLCJzdW5vLmNvbS9jbGFpbXMvdG9rZW5fdHlwZSI6ImFjY2VzcyIsImV4cCI6MTc2NzA0MzAxNiwiYXVkIjoic3Vuby1hcGkiLCJzdWIiOiJmNzNhMTkxMi04Zjg2LTRkNTAtOTdjNC1iNTBiZTMwNTBkOTgiLCJhenAiOiJodHRwczovL3N1bm8uY29tIiwiZnZhIjpbMCwtMV0sImlhdCI6MTc2NzAzOTQxNiwiaXNzIjoiaHR0cHM6Ly9hdXRoLnN1bm8uY29tIiwiaml0IjoiYzQxN2ZiZGMtMzNjMy00NGIxLWIzYTQtMzQ3OTY2NTY3MWFmIiwidml6IjpmYWxzZSwic2lkIjoic2Vzc2lvbl85Y2JjOGY1Zjk1OTc1N2U1NmRjMTRlIiwic3Vuby5jb20vY2xhaW1zL2VtYWlsIjoiemVwaHlyLm1pcnJvckBnbWFpbC5jb20iLCJodHRwczovL3N1bm8uYWkvY2xhaW1zL2VtYWlsIjoiemVwaHlyLm1pcnJvckBnbWFpbC5jb20ifQ.WDfnnovCKJclR9a63XPKozkRKksEuL6w08DZuYkhchR9gayj8PorQvBzUQLH6Zx5KbN7w8ZEFl3eWV-MdXG3rm037eGeQ3D_Y-H2aA-m9Wt-k0MjWYkFCcJ7Htnvl2wxa6KvwsJkjKqaErQ2hhERz3hCE8m2BWpMgpUe8XFGqhpOY0zwgb7VI_e8YmNa0H5W1b72ovJH4Q0O3iysv-5F1Igfyk4fCQ-kHdIREDnwfh4pa73AOUAyDUHmjB6LNtZSc6EUmaM1cq7Zzsi1t3lYRMjh8HJKtwURun-Hr7KZIJgu__G6kb9Cvq3xN4q3cfohcFZrlY4XodE4kw-C9Blt9A"
SUNO_COOKIE = f"__session={SESSION_TOKEN}"

PAYMENT_LINK = "https://tips.yandex.ru/guest/payment/3747309"
ADMIN_USERNAME = "@zephyr_murr"

# ==========================================

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализируем клиент СРАЗУ в глобальной области
client = suno.Suno(cookie=SUNO_COOKIE)

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
        "👉 Нажми /credits чтобы проверить лимит.\n\n"
        f"💳 [ОПЛАТИТЬ ДОСТУП]({PAYMENT_LINK})\n"
        f"📩 Чек сюда: {ADMIN_USERNAME}"
    )
    await update.message.reply_markdown(welcome_message, disable_web_page_preview=True)

async def credits_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Используем глобальный клиент
        credits = await asyncio.to_thread(client.get_credits)
        await update.message.reply_text(f"💰 Доступно: {credits.credits_left}\nИспользовано: {credits.monthly_usage}")
    except Exception as e:
        await update.message.reply_text(f"⁉️ Ошибка баланса (проверьте куки): {e}")

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Выбери режим:', reply_markup=get_base_keyboard())
    chat_states[update.effective_chat.id] = {}

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id
    if chat_id not in chat_states: chat_states[chat_id] = {}
    chat_states[chat_id]['mode'] = query.data
    await query.message.reply_text("🎤 Теперь отправь текст песни или её описание:")

async def onMessage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id not in chat_states: return
    
    user_text = update.message.text
    mode = chat_states[chat_id].get('mode')
    
    await update.message.reply_text("🎵 Начинаю генерацию... это займет 1-2 минуты. ⏳")
    try:
        is_custom = (mode == 'custom')
        # Если кастомный режим, используем текст как prompt, а теги можно оставить пустыми или добавить дефолт
        songs = await asyncio.to_thread(
            client.generate,
            prompt=user_text,
            is_custom=is_custom,
            wait_audio=True
        )
        for song in songs:
            file_path = await asyncio.to_thread(client.download, song=song)
            await context.bot.send_audio(chat_id=chat_id, audio=open(file_path, 'rb'))
            if os.path.exists(file_path): os.remove(file_path)
    except Exception as e:
        await update.message.reply_text(f"⁉️ Ошибка: {e}")
    finally:
        chat_states.pop(chat_id, None)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate))
    app.add_handler(CommandHandler("credits", credits_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, onMessage))
    app.run_polling()

if __name__ == "__main__":
    main()

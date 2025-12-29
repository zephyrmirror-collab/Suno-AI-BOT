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

# Вставляем ПОЛНУЮ строку куки, которую ты присылал. 
# Библиотека сама выцепит из нее нужный Session ID.
SUNO_COOKIE = "__session=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdW5vLmNvbS9jbGFpbXMvdXNlcl9pZCI6ImY3M2ExOTEyLThmODYtNGQ1MC05N2M0LWI1MGJlMzA1MGQ5OCIsImh0dHBzOi8vc3Vuby5haS9jbGFpbXMvY2xlcmtfaWQiOiJmNzNhMTkxMi04Zjg2LTRkNTAtOTdjNC1iNTBiZTMwNTBkOTgiLCJzdW5vLmNvbS9jbGFpbXMvdG9rZW5fdHlwZSI6ImFjY2VzcyIsImV4cCI6MTc2NzA0MzAxNiwiYXVkIjoic3Vuby1hcGkiLCJzdWIiOiJmNzNhMTkxMi04Zjg2LTRkNTAtOTdjNC1iNTBiZTMwNTBkOTgiLCJhenAiOiJodHRwczovL3N1bm8uY29tIiwiZnZhIjpbMCwtMV0sImlhdCI6MTc2NzAzOTQxNiwiaXNzIjoiaHR0cHM6Ly9hdXRoLnN1bm8uY29tIiwiaml0IjoiYzQxN2ZiZGMtMzNjMy00NGIxLWIzYTQtMzQ3OTY2NTY3MWFmIiwidml6IjpmYWxzZSwic2lkIjoic2Vzc2lvbl85Y2JjOGY1Zjk1OTc1N2U1NmRjMTRlIiwic3Vuby5jb20vY2xhaW1zL2VtYWlsIjoiemVwaHlyLm1pcnJvckBnbWFpbC5jb20iLCJodHRwczovL3N1bm8uYWkvY2xhaW1zL2VtYWlsIjoiemVwaHlyLm1pcnJvckBnbWFpbC5jb20ifQ.WDfnnovCKJclR9a63XPKozkRKksEuL6w08DZuYkhchR9gayj8PorQvBzUQLH6Zx5KbN7w8ZEFl3eWV-MdXG3rm037eGeQ3D_Y-H2aA-m9Wt-k0MjWYkFCcJ7Htnvl2wxa6KvwsJkjKqaErQ2hhERz3hCE8m2BWpMgpUe8XFGqhpOY0zwgb7VI_e8YmNa0H5W1b72ovJH4Q0O3iysv-5F1Igfyk4fCQ-kHdIREDnwfh4pa73AOUAyDUHmjB6LNtZSc6EUmaM1cq7Zzsi1t3lYRMjh8HJKtwURun-Hr7KZIJgu__G6kb9Cvq3xN4q3cfohcFZrlY4XodE4kw-C9Blt9A;singular_device_id=44b0ec7a-88ed-4d32-8bcb-0e042b8d1aff;__session_Jnxw-muT=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdW5vLmNvbS9jbGFpbXMvdXNlcl9pZCI6ImY3M2ExOTEyLThmODYtNGQ1MC05N2M0LWI1MGJlMzA1MGQ5OCIsImh0dHBzOi8vc3Vuby5haS9jbGFpbXMvY2xlcmtfaWQiOiJmNzNhMTkxMi04Zjg2LTRkNTAtOTdjNC1iNTBiZTMwNTBkOTgiLCJzdW5vLmNvbS9jbGFpbXMvdG9rZW5fdHlwZSI6ImFjY2VzcyIsImV4cCI6MTc2NzA0MzAxNiwiYXVkIjoic3Vuby1hcGkiLCJzdWIiOiJmNzNhMTkxMi04Zjg2LTRkNTAtOTdjNC1iNTBiZTMwNTBkOTgiLCJhenAiOiJodHRwczovL3N1bm8uY29tIiwiZnZhIjpbMCwtMV0sImlhdCI6MTc2NzAzOTQxNiwiaXNzIjoiaHR0cHM6Ly9hdXRoLnN1bm8uY29tIiwiaml0IjoiYzQxN2ZiZGMtMzNjMy00NGIxLWIzYTQtMzQ3OTY2NTY3MWFmIiwidml6IjpmYWxzZSwic2lkIjoic2Vzc2lvbl85Y2JjOGY1Zjk1OTc1N2U1NmRjMTRlIiwic3Vuby5jb20vY2xhaW1zL2VtYWlsIjoiemVwaHlyLm1pcnJvckBnbWFpbC5jb20iLCJodHRwczovL3N1bm8uYWkvY2xhaW1zL2VtYWlsIjoiemVwaHlyLm1pcnJvckBnbWFpbC5jb20ifQ.WDfnnovCKJclR9a63XPKozkRKksEuL6w08DZuYkhchR9gayj8PorQvBzUQLH6Zx5KbN7w8ZEFl3eWV-MdXG3rm037eGeQ3D_Y-H2aA-m9Wt-k0MjWYkFCcJ7Htnvl2wxa6KvwsJkjKqaErQ2hhERz3hCE8m2BWpMgpUe8XFGqhpOY0zwgb7VI_e8YmNa0H5W1b72ovJH4Q0O3iysv-5F1Igfyk4fCQ-kHdIREDnwfh4pa73AOUAyDUHmjB6LNtZSc6EUmaM1cq7Zzsi1t3lYRMjh8HJKtwURun-Hr7KZIJgu__G6kb9Cvq3xN4q3cfohcFZrlY4XodE4kw-C9Blt9A"

PAYMENT_LINK = "https://tips.yandex.ru/guest/payment/3747309"
ADMIN_USERNAME = "@zephyr_murr"

# ==========================================

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Попытка инициализации Suno
try:
    client = suno.Suno(cookie=SUNO_COOKIE)
except Exception as e:
    logger.error(f"Suno Init Error: {e}")
    client = None

chat_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Убираем MarkdownV2, чтобы не было ошибок парсинга спецсимволов
    welcome_message = (
        f"👋 Привет! Я бот для создания музыки через Suno AI! 🎶\n\n"
        f"👉 Нажми /generate чтобы начать творить. 🚀\n"
        f"👉 Нажми /credits чтобы проверить лимит.\n\n"
        f"💳 Оплатить доступ: {PAYMENT_LINK}\n"
        f"📩 Чек присылать сюда: {ADMIN_USERNAME}"
    )
    await update.message.reply_text(welcome_message)

async def credits_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not client:
        return await update.message.reply_text("⁉️ Ошибка: Клиент Suno не инициализирован. Проверьте куки.")
    try:
        credits = await asyncio.to_thread(client.get_credits)
        await update.message.reply_text(f"💰 Доступно: {credits.credits_left}\nИспользовано: {credits.monthly_usage}")
    except Exception as e:
        await update.message.reply_text(f"⁉️ Ошибка баланса: {e}")

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎨 Свой текст", callback_data="custom")],
        [InlineKeyboardButton("🏞️ Описание", callback_data="default")]
    ])
    await update.message.reply_text('Выбери режим:', reply_markup=keyboard)
    chat_states[update.effective_chat.id] = {}

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id
    if chat_id not in chat_states: chat_states[chat_id] = {}
    chat_states[chat_id]['mode'] = query.data
    await query.message.reply_text("🎤 Отправь текст песни или описание темы:")

async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id not in chat_states or 'mode' not in chat_states[chat_id]: return
    
    text = update.message.text
    mode = chat_states[chat_id]['mode']
    await update.message.reply_text("🎵 Начинаю генерацию... это займет около минуты. ⏳")
    
    try:
        songs = await asyncio.to_thread(
            client.generate,
            prompt=text,
            is_custom=(mode == 'custom'),
            wait_audio=True
        )
        for song in songs:
            file_path = await asyncio.to_thread(client.download, song=song)
            await context.bot.send_audio(chat_id=chat_id, audio=open(file_path, 'rb'))
            if os.path.exists(file_path): os.remove(file_path)
    except Exception as e:
        await update.message.reply_text(f"⁉️ Ошибка генерации: {e}")
    finally:
        chat_states.pop(chat_id, None)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate))
    app.add_handler(CommandHandler("credits", credits_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
    app.run_polling()

if __name__ == "__main__":
    main()

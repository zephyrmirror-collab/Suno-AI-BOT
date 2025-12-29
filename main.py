import asyncio
import logging
import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters
import suno

# ==========================================
# 👇 НАСТРОЙКИ 👇
# ==========================================

BOT_TOKEN = "8350338676:AAGNLXAkqmARQBpd9BqH65Jfygb_s1Ilk7c"

# Твой JSON, который ты прислал
SUNO_COOKIE_JSON = """
[
    {
        "name": "__session",
        "value": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdW5vLmNvbS9jbGFpbXMvdXNlcl9pZCI6ImY3M2ExOTEyLThmODYtNGQ1MC05N2M0LWI1MGJlMzA1MGQ5OCIsImh0dHBzOi8vc3Vuby5haS9jbGFpbXMvY2xlcmtfaWQiOiJmNzNhMTkxMi04Zjg2LTRkNTAtOTdjNC1iNTBiZTMwNTBkOTgiLCJzdW5vLmNvbS9jbGFpbXMvdG9rZW5fdHlwZSI6ImFjY2VzcyIsImV4cCI6MTc2NzA0NDMzOSwiYXVkIjoic3Vuby1hcGkiLCJzdWIiOiJmNzNhMTkxMi04Zjg2LTRkNTAtOTdjNC1iNTBiZTMwNTBkOTgiLCJhenAiOiJodHRwczovL3N1bm8uY29tIiwiZnZhIjpbMCwtMV0sImlhdCI6MTc2NzA0MDczOSwiaXNzIjoiaHR0cHM6Ly9hdXRoLnN1bm8uY29tIiwiaml0IjoiMDdiNDk4NDktMmExNi00M2UxLWFmMDMtMGE1ZWNjYTAwMDk0Iiwidml6IjpmYWxzZSwic2lkIjoic2Vzc2lvbl85Y2JjOGY1Zjk1OTc1N2U1NmRjMTRlIiwic3Vuby5jb20vY2xhaW1zL2VtYWlsIjoiemVwaHlyLm1pcnJvckBnbWFpbC5jb20iLCJodHRwczovL3N1bm8uYWkvY2xhaW1zL2VtYWlsIjoiemVwaHlyLm1pcnJvckBnbWFpbC5jb20ifQ.Hc-Z4Yo8Yu3wklkKArFINBJ-4DhLIUy5sWCqJbt1ikwUguzfhij05f4xlrAOpWf8iTrceAY8bIE9-ZjW01nsIncq5sRhyl-W_6fDO_Rf8HmQCpFCVQMS3MYH9CXwfCWxwqb1TqBg1zdartIgIb86se9B3KqC8Jr6Q6y37UHZ9oPrg6GS3QPjmNrvHXCG5BEIIOqbu09q8J0WBh976vMJX73TVyuZ-QKv-OS4dzE-rCI8RrdQ43PFPSw0RQS7ODjv_Yy5d1Zv7bi639u7Lo6qlTuoH327187WaYrOqfM5zEmTRjP5sXB8qFWoGE7cEwOQF0d0cV6mnGXNL_CJlhbbjA"
    },
    {
        "name": "singular_device_id",
        "value": "44b0ec7a-88ed-4d32-8bcb-0e042b8d1aff"
    },
    {
        "name": "__session_Jnxw-muT",
        "value": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdW5vLmNvbS9jbGFpbXMvdXNlcl9pZCI6ImY3M2ExOTEyLThmODYtNGQ1MC05N2M0LWI1MGJlMzA1MGQ5OCIsImh0dHBzOi8vc3Vuby5haS9jbGFpbXMvY2xlcmtfaWQiOiJmNzNhMTkxMi04Zjg2LTRkNTAtOTdjNC1iNTBiZTMwNTBkOTgiLCJzdW5vLmNvbS9jbGFpbXMvdG9rZW5fdHlwZSI6ImFjY2VzcyIsImV4cCI6MTc2NzA0NDMzOSwiYXVkIjoic3Vuby1hcGkiLCJzdWIiOiJmNzNhMTkxMi04Zjg2LTRkNTAtOTdjNC1iNTBiZTMwNTBkOTgiLCJhenAiOiJodHRwczovL3N1bm8uY29tIiwiZnZhIjpbMCwtMV0sImlhdCI6MTc2NzA0MDczOSwiaXNzIjoiaHR0cHM6Ly9hdXRoLnN1bm8uY29tIiwiaml0IjoiMDdiNDk4NDktMmExNi00M2UxLWFmMDMtMGE1ZWNjYTAwMDk0Iiwidml6IjpmYWxzZSwic2lkIjoic2Vzc2lvbl85Y2JjOGY1Zjk1OTc1N2U1NmRjMTRlIiwic3Vuby5jb20vY2xhaW1zL2VtYWlsIjoiemVwaHlyLm1pcnJvckBnbWFpbC5jb20iLCJodHRwczovL3N1bm8uYWkvY2xhaW1zL2VtYWlsIjoiemVwaHlyLm1pcnJvckBnbWFpbC5jb20ifQ.Hc-Z4Yo8Yu3wklkKArFINBJ-4DhLIUy5sWCqJbt1ikwUguzfhij05f4xlrAOpWf8iTrceAY8bIE9-ZjW01nsIncq5sRhyl-W_6fDO_Rf8HmQCpFCVQMS3MYH9CXwfCWxwqb1TqBg1zdartIgIb86se9B3KqC8Jr6Q6y37UHZ9oPrg6GS3QPjmNrvHXCG5BEIIOqbu09q8J0WBh976vMJX73TVyuZ-QKv-OS4dzE-rCI8RrdQ43PFPSw0RQS7ODjv_Yy5d1Zv7bi639u7Lo6qlTuoH327187WaYrOqfM5zEmTRjP5sXB8qFWoGE7cEwOQF0d0cV6mnGXNL_CJlhbbjA"
    }
]
"""

PAYMENT_LINK = "https://tips.yandex.ru/guest/payment/3747309"
ADMIN_USERNAME = "@zephyr_murr"

# ==========================================

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

def get_cookie_string(json_data):
    try:
        cookies = json.loads(json_data)
        return "; ".join([f"{c['name']}={c['value']}" for c in cookies])
    except Exception as e:
        logger.error(f"Cookie parsing error: {e}")
        return ""

# Глобальный клиент
cookie_str = get_cookie_string(SUNO_COOKIE_JSON)
try:
    client = suno.Suno(cookie=cookie_str)
    logger.info("Suno client initialized")
except Exception as e:
    logger.error(f"Suno failed to start: {e}")
    client = None

chat_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = (
        f"👋 Привет! Я бот для создания музыки через Suno AI! 🎶\n\n"
        f"👉 Нажми /generate чтобы начать.\n"
        f"👉 Нажми /credits для проверки баланса.\n\n"
        f"💳 Оплатить: {PAYMENT_LINK}\n"
        f"📩 Админ: {ADMIN_USERNAME}"
    )
    await update.message.reply_text(welcome_message)

async def credits_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not client:
        return await update.message.reply_text("⁉️ Ошибка: Клиент не запущен. Проверьте логи.")
    try:
        credits = await asyncio.to_thread(client.get_credits)
        await update.message.reply_text(f"💰 Доступно: {credits.credits_left} кредитов.")
    except Exception as e:
        await update.message.reply_text(f"⁉️ Ошибка баланса: {e}")

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎨 Свой текст", callback_data="custom")],
        [InlineKeyboardButton("🏞️ Описание", callback_data="default")]
    ])
    await update.message.reply_text('Выбери режим создания:', reply_markup=keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    chat_states[update.effective_chat.id] = {'mode': query.data}
    await query.message.reply_text("🎤 Теперь пришли текст песни или описание стиля:")

async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id not in chat_states or 'mode' not in chat_states[chat_id]:
        return

    if not client:
        return await update.message.reply_text("⁉️ Клиент Suno не активен.")

    prompt_text = update.message.text
    mode = chat_states[chat_id]['mode']
    await update.message.reply_text("🎵 Начинаю магию... Жду готовности трека (около 1 минуты) ⏳")

    try:
        songs = await asyncio.to_thread(
            client.generate,
            prompt=prompt_text,
            is_custom=(mode == "custom"),
            wait_audio=True
        )
        for song in songs:
            file_path = await asyncio.to_thread(client.download, song=song)
            await context.bot.send_audio(chat_id=chat_id, audio=open(file_path, 'rb'), caption=f"✅ Готово: {song.title}")
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

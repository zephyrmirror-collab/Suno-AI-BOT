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

# 2. ТВОИ КУКИ ОТ SUNO (Вставлены твои свежие)
SUNO_COOKIE = "__session=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdW5vLmNvbS9jbGFpbXMvdXNlcl9pZCI6ImY3M2ExOTEyLThmODYtNGQ1MC05N2M0LWI1MGJlMzA1MGQ5OCIsImh0dHBzOi8vc3Vuby5haS9jbGFpbXMvY2xlcmtfaWQiOiJmNzNhMTkxMi04Zjg2LTRkNTAtOTdjNC1iNTBiZTMwNTBkOTgiLCJzdW5vLmNvbS9jbGFpbXMvdG9rZW5fdHlwZSI6ImFjY2VzcyIsImV4cCI6MTc2NzAzOTkzNiwiYXVkIjoic3Vuby1hcGkiLCJzdWIiOiJmNzNhMTkxMi04Zjg2LTRkNTAtOTdjNC1iNTBiZTMwNTBkOTgiLCJhenAiOiJodHRwczovL3N1bm8uY29tIiwiZnZhIjpbMCwtMV0sImlhdCI6MTc2NzAzNjMzNiwiaXNzIjoiaHR0cHM6Ly9hdXRoLnN1bm8uY29tIiwiaml0IjoiZDM1MzA5ZDUtN2QyNi00ZjgyLTllYjQtZDNmZTRiYmExZmFiIiwidml6IjpmYWxzZSwic2lkIjoic2Vzc2lvbl85Y2JjOGY1Zjk1OTc1N2U1NmRjMTRlIiwic3Vuby5jb20vY2xhaW1zL2VtYWlsIjoiemVwaHlyLm1pcnJvckBnbWFpbC5jb20iLCJodHRwczovL3N1bm8uYWkvY2xhaW1zL2VtYWlsIjoiemVwaHlyLm1pcnJvckBnbWFpbC5jb20ifQ.KCyhexXx-huBQLBWsfP3GGmGzXS46zYCT0t-J9MeFSgzE6IqhV3OJ8OM0MSZz2_fVBun0h43-a2o6mnECUGacNOV-ZJtSOYJYM9sdhcHba38ULDnqkeAbtaYTrD_TiDA7zvhp0UPEBbDqGY-IY289rdOJZtVAXSz_RY6Djhbzg1gV2oCUNaCsUizS757RnFJh8ewggygV5MMjtOf4WhWdzZ9Uza6sC32hSC1HclLbuxsAG00kd2OTcxr8E9Fhz8Om_Lm10OWy3HDscdutYa-vA0AEF2q21hCKuLcD9cy43ksEk-M4GHqPDm23imI4LbpW8yvZMhHjesnU3mgwUUPyw;singular_device_id=44b0ec7a-88ed-4d32-8bcb-0e042b8d1aff;__session_Jnxw-muT=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdW5vLmNvbS9jbGFpbXMvdXNlcl9pZCI6ImY3M2ExOTEyLThmODYtNGQ1MC05N2M0LWI1MGJlMzA1MGQ5OCIsImh0dHBzOi8vc3Vuby5haS9jbGFpbXMvY2xlcmtfaWQiOiJmNzNhMTkxMi04Zjg2LTRkNTAtOTdjNC1iNTBiZTMwNTBkOTgiLCJzdW5vLmNvbS9jbGFpbXMvdG9rZW5fdHlwZSI6ImFjY2VzcyIsImV4cCI6MTc2NzAzOTkzNiwiYXVkIjoic3Vuby1hcGkiLCJzdWIiOiJmNzNhMTkxMi04Zjg2LTRkNTAtOTdjNC1iNTBiZTMwNTBkOTgiLCJhenAiOiJodHRwczovL3N1bm8uY29tIiwiZnZhIjpbMCwtMV0sImlhdCI6MTc2NzAzNjMzNiwiaXNzIjoiaHR0cHM6Ly9hdXRoLnN1bm8uY29tIiwiaml0IjoiZDM1MzA5ZDUtN2QyNi00ZjgyLTllYjQtZDNmZTRiYmExZmFiIiwidml6IjpmYWxzZSwic2lkIjoic2Vzc2lvbl85Y2JjOGY1Zjk1OTc1N2U1NmRjMTRlIiwic3Vuby5jb20vY2xhaW1zL2VtYWlsIjoiemVwaHlyLm1pcnJvckBnbWFpbC5jb20iLCJodHRwczovL3N1bm8uYWkvY2xhaW1zL2VtYWlsIjoiemVwaHlyLm1pcnJvckBnbWFpbC5jb20ifQ.KCyhexXx-huBQLBWsfP3GGmGzXS46zYCT0t-J9MeFSgzE6IqhV3OJ8OM0MSZz2_fVBun0h43-a2o6mnECUGacNOV-ZJtSOYJYM9sdhcHba38ULDnqkeAbtaYTrD_TiDA7zvhp0UPEBbDqGY-IY289rdOJZtVAXSz_RY6Djhbzg1gV2oCUNaCsUizS757RnFJh8ewggygV5MMjtOf4WhWdzZ9Uza6sC32hSC1HclLbuxsAG00kd2OTcxr8E9Fhz8Om_Lm10OWy3HDscdutYa-vA0AEF2q21hCKuLcD9cy43ksEk-M4GHqPDm23imI4LbpW8yvZMhHjesnU3mgwUUPyw;_uetsid=7ffe7f60e4cb11f09281b5abd4755bc8|x1ez51|2|g29|0|2189;ax_visitor=%7B%22firstVisitTs%22%3A1767022304798%2C%22lastVisitTs%22%3A1767026682467%2C%22currentVisitStartTs%22%3A1767036338214%2C%22ts%22%3A1767036340611%2C%22visitCount%22%3A3%7D;has_logged_in_before=true;_clck=14zzdnb%5E2%5Eg29%5E0%5E2189;_uetvid=7ffe9980e4cb11f0bb7b2f1c65035a28|w9z1w8|1767036350056|2|1|bat.bing.com/p/conversions/c/q;__client_uat_Jnxw-muT=1767026886;_sctr=1%7C1766955600000;_ga_7B0KEDD7XP=GS2.1.s1767036284$o3$g1$t1767036341$j3$l0$h0$daP5IOb3F2YNUHW8A76aV__v2qJZ1BKawPw;__stripe_mid=eaba7af3-ec08-4ec6-a20f-3c557bf1caaf20bce4;ttcsid=1767036292547::1piTvjZSqhZmXmCzfg-r.3.1767036344990.0;__clerk_redirect_count=1;__client_uat=1767026886;__client_uat_U9tcbTPE=0;__stripe_sid=1a3d5348-bf25-4e03-a044-b347fcb37885fc8310;_axwrt=a9558528-e971-48b3-8f15-9db32d2d65e7;_clsk=17qf546%5E1767026793666%5E3%5E1%5Ee.clarity.ms%2Fcollect;_dd_s=aid=f47da03a-309c-4c7f-9e7a-07b75b5f03d7&rum=0&expire=1767037242203;_fbp=fb.1.1767036293924.914800788765310283;_ga=GA1.1.555738447.1767022300;_gcl_au=1.1.919499537.1767022300.955338219.1767036298.1767036297;_scid=hJXWFdlQRX6ysnEyqfXSo4mqkphASkyt;_scid_r=ghXWFdlQRX6ysnEyqfXSo4mqkphASkytZO3v5w;_sp_id.e685=4f8dad04-66bb-4a08-92bd-54098c84d911.1767026683.2.1767036338.1767026986.5beab935-67d6-4829-9587-2bd17af3ad5e.e633fbf8-7939-4c67-bedb-97b1464676e1.c721bcd2-dbbf-4f02-b328-0410fd8f4d7d.1767036285727.4;_sp_ses.e685=*;_tt_enable_cookie=1;_ttp=01KDNBSDXYRG7SNH75BB463DA3_.tt.1;ajs_anonymous_id=17ec7067-2248-43ff-bf7f-379cc131aa15;clerk_active_context=session_9cbc8f5f959757e56dc14e:;suno_auth=pk_live_YXV0aC5zdW5vLmNvbSQ;ttcsid_CT67HURC77UB52N3JFBG=1767036292546::q_3I6wHua8excgc-1Exn.3.1767036344990.1"

# 3. ДАННЫЕ ДЛЯ ОПЛАТЫ
PAYMENT_LINK = "https://tips.yandex.ru/guest/payment/3747309"
ADMIN_USERNAME = "@zephyr_murr"

# ==========================================

# Configure logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Initialize Suno AI Library
# Теперь используем переменную сверху, а не os.getenv
client = suno.Suno(cookie=SUNO_COOKIE)

# Store user session data
chat_states = {}

# Keyboard options for user selection
def get_base_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎨 Свой текст песни", callback_data="custom")],
        [InlineKeyboardButton("🏞️ Просто описание", callback_data="default")]
    ])

# Welcome message with Markdown
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

# Handler for the get credits
async def credits_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    credit_info_message = (
        "*💰 Статистика кредитов*\n\n"
        "ᗚ Доступно : {}\n"
        "ᗚ Использовано : {}\n\n"
        "Нужно больше? Пиши админу: " + ADMIN_USERNAME
    )
    try:
        credits = await asyncio.to_thread(client.get_credits)
    except Exception as e:
        return await update.message.reply_text(f"⁉️ Ошибка получения баланса (возможно, слетели куки): {e}")
    await update.message.reply_text(credit_info_message.format(credits.credits_left, credits.monthly_usage), parse_mode=ParseMode.MARKDOWN)

# Handler for the generate command
async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Выбери режим: свой текст песни или просто описание темы? 🤔', reply_markup=get_base_keyboard())
    chat_states[update.effective_chat.id] = {}

# Command to cancel and clear state
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id in chat_states:
        chat_states.pop(chat_id, None)
    await update.message.reply_text('Генерация отменена. 🚫 Нажми /generate чтобы начать заново.')

# Handler for button presses
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    chat_id = int(update.effective_chat.id)
    chat_states[chat_id]['mode'] = query.data

    if query.data == "custom":
        await query.message.reply_text("🎤 Отправь мне текст песни (куплеты, припев).")
    else:
        await query.message.reply_text("🎤 Опиши, о чем должна быть песня и в каком стиле.")
    return await context.application.bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        

async def onMessage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = int(update.effective_chat.id)
    # Collects lyrics from the user
    if chat_id in chat_states and 'mode' in chat_states[chat_id]:
        if not 'lyrics' in chat_states[chat_id]:
            chat_states[chat_id]['lyrics'] = update.message.text
        if chat_states[chat_id].get('mode') == 'custom':
            if not (chat_id in chat_states and 'tags' in chat_states[chat_id] and "Wait-for-tags" == chat_states[chat_id]['tags']):
                chat_states[chat_id]['tags'] = "Wait-for-tags"
                return await update.message.reply_text("🏷️ Теперь напиши стиль музыки (например: Rock, Pop, Russian Chanson).")
    
    # Collects tags (if custom) / generates music
    if chat_id in chat_states and 'lyrics' in chat_states[chat_id]:
        if chat_states[chat_id].get('mode') == 'custom':
            # Custom music generation logic
            chat_states[chat_id]['tags'] = update.message.text
            await update.message.reply_text("🎵 Сочиняю музыку... подожди пару минут. ⏳")
            try:
                prompt = f"{chat_states[chat_id]['lyrics']}"
                tags = f"{chat_states[chat_id]['tags']}"
                
                # Generate Custom Music
                songs = await asyncio.to_thread(
                    client.generate,
                    prompt=prompt,
                    tags=tags,
                    is_custom=True,
                    wait_audio=True)

                for song in songs:
                    file_path = await asyncio.to_thread(client.download, song=song)
                    await context.bot.send_audio(chat_id=chat_id, audio=open(file_path, 'rb'), thumbnail=open("thumb.jpg", 'rb'))
                    os.remove(file_path)
                if chat_id in chat_states:
                    chat_states.pop(chat_id, None)
            except Exception as e:
                await update.message.reply_text(f"⁉️ Ошибка генерации: {e}")
        else:
            # Default music generation logic
            await update.message.reply_text("🎵 Сочиняю музыку... подожди пару минут. ⏳")
            try:
                prompt = f"{chat_states[chat_id]['lyrics']}"

                # Generate Music by Description
                songs = await asyncio.to_thread(
                    client.generate,
                    prompt=prompt, 
                    is_custom=False,
                    wait_audio=True)
                
                for song in songs:
                    file_path = await asyncio.to_thread(client.download, song=song)
                    await context.bot.send_audio(chat_id=chat_id, audio=open(file_path, 'rb'), thumbnail=open("thumb.jpg", 'rb'))
                    os.remove(file_path)
                if chat_id in chat_states:
                    chat_states.pop(chat_id, None)
            except Exception as e:
                await update.message.reply_text(f"⁉️ Ошибка генерации: {e}")
        
        if chat_id in chat_states:
            chat_states.pop(chat_id, None)
    

def main():
    # Токен теперь берется из переменной в начале файла
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("generate", generate))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, onMessage))
    application.add_handler(CommandHandler("credits", credits_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

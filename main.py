# © [2024] Malith-Rukshan. All rights reserved.
# Repository: https://github.com/Malith-Rukshan/Suno-AI-BOT

import asyncio
import logging
import os

from telegram.constants import ParseMode
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters
import suno

# ==========================================
# 👇 YOUR SETTINGS 👇
# ==========================================

BOT_TOKEN = "8350338676:AAGNLXAkqmARQBpd9BqH65Jfygb_s1Ilk7c"

# Your fresh session cookies
SUNO_COOKIE = "__session=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdW5vLmNvbS9jbGFpbXMvdXNlcl9pZCI6ImY3M2ExOTEyLThmODYtNGQ1MC05N2M0LWI1MGJlMzA1MGQ5OCIsImh0dHBzOi8vc3Vuby5haS9jbGFpbXMvY2xlcmtfaWQiOiJmNzNhMTkxMi04Zjg2LTRkNTAtOTdjNC1iNTBiZTMwNTBkOTgiLCJzdW5vLmNvbS9jbGFpbXMvdG9rZW5fdHlwZSI6ImFjY2VzcyIsImV4cCI6MTc2NzA0NDk0MCwiYXVkIjoic3Vuby1hcGkiLCJzdWIiOiJmNzNhMTkxMi04Zjg2LTRkNTAtOTdjNC1iNTBiZTMwNTBkOTgiLCJhenAiOiJodHRwczovL3N1bm8uY29tIiwiZnZhIjpbMCwtMV0sImlhdCI6MTc2NzA0MTM0MCwiaXNzIjoiaHR0cHM6Ly9hdXRoLnN1bm8uY29tIiwiaml0IjoiOWM3NjFmNmMtZDA1Yy00MTBhLTk2ZGMtNTU0N2Q5OTVmZDE2Iiwidml6IjpmYWxzZSwic2lkIjoic2Vzc2lvbl85Y2JjOGY1Zjk1OTc1N2U1NmRjMTRlIiwic3Vuby5jb20vY2xhaW1zL2VtYWlsIjoiemVwaHlyLm1pcnJvckBnbWFpbC5jb20iLCJodHRwczovL3N1bm8uYWkvY2xhaW1zL2VtYWlsIjoiemVwaHlyLm1pcnJvckBnbWFpbC5jb20ifQ.moq8gvvwT4p_3fHJrC_Q0XBnqrrNIp2h_CdYZulqa6wgV548wYxXQ9e-4gIwgD9_SvY0YpkT31Y2PWyvMERjAoR4zpcrcpzKxKmz00yq2u8GUfcYqG31KztmTrNgYsso_ryPtpiThMuUDl9hMV05rrs3mTAZJTEQE2VW6j_smRaBnp3Bjs33clA4nuSr5iADiX-151W6s4VVR-nEjiwJAP0ARuSQ76FmhQkusFZ_APT5XQlNp4keT8W9EpBWYlT5NOfdJbHmiN4lKtEESV_byrP5mlyZClBOQh3P2A449hNVubJ2g5wHeA1ZZA8aIn2T1U2_u_ueuNVX3j-F1lVcZA;singular_device_id=44b0ec7a-88ed-4d32-8bcb-0e042b8d1aff;__session_Jnxw-muT=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdW5vLmNvbS9jbGFpbXMvdXNlcl9pZCI6ImY3M2ExOTEyLThmODYtNGQ1MC05N2M0LWI1MGJlMzA1MGQ5OCIsImh0dHBzOi8vc3Vuby5haS9jbGFpbXMvY2xlcmtfaWQiOiJmNzNhMTkxMi04Zjg2LTRkNTAtOTdjNC1iNTBiZTMwNTBkOTgiLCJzdW5vLmNvbS9jbGFpbXMvdG9rZW5fdHlwZSI6ImFjY2VzcyIsImV4cCI6MTc2NzA0NDk0MCwiYXVkIjoic3Vuby1hcGkiLCJzdWIiOiJmNzNhMTkxMi04Zjg2LTRkNTAtOTdjNC1iNTBiZTMwNTBkOTgiLCJhenAiOiJodHRwczovL3N1bm8uY29tIiwiZnZhIjpbMCwtMV0sImlhdCI6MTc2NzA0MTM0MCwiaXNzIjoiaHR0cHM6Ly9hdXRoLnN1bm8uY29tIiwiaml0IjoiOWM3NjFmNmMtZDA1Yy00MTBhLTk2ZGMtNTU0N2Q5OTVmZDE2Iiwidml6IjpmYWxzZSwic2lkIjoic2Vzc2lvbl85Y2JjOGY1Zjk1OTc1N2U1NmRjMTRlIiwic3Vuby5jb20vY2xhaW1zL2VtYWlsIjoiemVwaHlyLm1pcnJvckBnbWFpbC5jb20iLCJodHRwczovL3N1bm8uYWkvY2xhaW1zL2VtYWlsIjoiemVwaHlyLm1pcnJvckBnbWFpbC5jb20ifQ.moq8gvvwT4p_3fHJrC_Q0XBnqrrNIp2h_CdYZulqa6wgV548wYxXQ9e-4gIwgD9_SvY0YpkT31Y2PWyvMERjAoR4zpcrcpzKxKmz00yq2u8GUfcYqG31KztmTrNgYsso_ryPtpiThMuUDl9hMV05rrs3mTAZJTEQE2VW6j_smRaBnp3Bjs33clA4nuSr5iADiX-151W6s4VVR-nEjiwJAP0ARuSQ76FmhQkusFZ_APT5XQlNp4keT8W9EpBWYlT5NOfdJbHmiN4lKtEESV_byrP5mlyZClBOQh3P2A449hNVubJ2g5wHeA1ZZA8aIn2T1U2_u_ueuNVX3j-F1lVcZA;_uetsid=7ffe7f60e4cb11f09281b5abd4755bc8|x1ez51|2|g29|0|2189;ax_visitor=%7B%22firstVisitTs%22%3A1767022304798%2C%22lastVisitTs%22%3A1767026682467%2C%22currentVisitStartTs%22%3A1767036338214%2C%22ts%22%3A1767041340357%2C%22visitCount%22%3A3%7D;has_logged_in_before=true;_clck=14zzdnb%5E2%5Eg29%5E0%5E2189;_uetvid=7ffe9980e4cb11f0bb7b2f1c65035a28|1uivgj|1767041348150|2|1|bat.bing.com/p/conversions/c/q;__client_uat_Jnxw-muT=1767026886;_sctr=1%7C1766955600000;_ga_7B0KEDD7XP=GS2.1.s1767038705$o4$g1$t1767041342$j56$l0$h0$daP5IOb3F2YNUHW8A76aV__v2qJZ1BKawPw;__stripe_mid=eaba7af3-ec08-4ec6-a20f-3c557bf1caaf20bce4;ttcsid=1767038712094::vmIv2W-R-bBF8nmHAvyo.4.1767041346347.0;__clerk_redirect_count=1;__client_uat=1767026886;__client_uat_U9tcbTPE=0;__stripe_sid=8a15506f-bb71-4c24-a6be-37f99937975cb5f36f;_axwrt=a9558528-e971-48b3-8f15-9db32d2d65e7;_clsk=17qf546%5E1767026793666%5E3%5E1%5Ee.clarity.ms%2Fcollect;_dd_s=aid=f47da03a-309c-4c7f-9e7a-07b75b5f03d7&rum=0&expire=1767042239900;_fbp=fb.1.1767036293924.914800788765310283;_ga=GA1.1.555738447.1767022300;_gcl_au=1.1.919499537.1767022300.464245928.1767038707.1767038744;_scid=hJXWFdlQRX6ysnEyqfXSo4mqkphASkyt;_scid_r=lxXWFdlQRX6ysnEyqfXSo4mqkphASkytZO3v7A;_sp_id.e685=4f8dad04-66bb-4a08-92bd-54098c84d911.1767026683.3.1767041341.1767036338.77d58bfb-05f4-49c2-bb61-64313e043b84.5beab935-67d6-4829-9587-2bd17af3ad5e.42b981a7-aacc-4fda-a4e7-8585b05238b5.1767038707045.10;_sp_ses.e685=*;_tt_enable_cookie=1;_ttp=01KDNBSDXYRG7SNH75BB463DA3_.tt.1;ajs_anonymous_id=17ec7067-2248-43ff-bf7f-379cc131aa15;clerk_active_context=session_9cbc8f5f959757e56dc14e:;suno_auth=pk_live_YXV0aC5zdW5vLmNvbSQ;ttcsid_CT67HURC77UB52N3JFBG=1767038712093::BH5Nby2ZkG9Bo_1xwSkf.4.1767041346347.1"

PAYMENT_LINK = "https://tips.yandex.ru/guest/payment/3747309"
ADMIN_USERNAME = "@zephyr_murr"

# ==========================================

# Configure logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Initialize Suno AI Library
client = suno.Suno(cookie=SUNO_COOKIE)

# Store user session data
chat_states = {}

# Keyboard options for user selection
def get_base_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎨 Custom", callback_data="custom")],
        [InlineKeyboardButton("🏞️ Default", callback_data="default")]
    ])

# Welcome message with Markdown
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = (
        "👋 Hello! Welcome to the *Suno AI Music Generator Bot*! 🎶\n\n"
        "👉 Use /generate to start creating.\n"
        "👉 Use /credits to check balance.\n\n"
        f"💳 [PAY FOR ACCESS]({PAYMENT_LINK})\n"
        f"📩 Send receipt to: {ADMIN_USERNAME}"
    )
    await update.message.reply_markdown(welcome_message, disable_web_page_preview=True)

# Handler for the get credits
async def credits_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    credit_info_message = (
        "*💰Credits Stat*\n\n"
        "ᗚ Available : {}\n"
        "ᗚ Usage : {}"
    )
    try:
        credits = await asyncio.to_thread(client.get_credits)
        await update.message.reply_text(credit_info_message.format(credits.credits_left,credits.monthly_usage), parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"⁉️ Failed to get credits info: {e}")

# Handler for the generate command
async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Select mode: custom or not. 🤔', reply_markup=get_base_keyboard())
    chat_states[update.effective_chat.id] = {}

# Command to cancel and clear state
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id in chat_states:
        chat_states.pop(chat_id, None)
    await update.message.reply_text('Generation canceled. 🚫 You can start again with /generate.')

# Handler for button presses
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    chat_id = int(update.effective_chat.id)
    if chat_id not in chat_states: chat_states[chat_id] = {}
    chat_states[chat_id]['mode'] = query.data

    if query.data == "custom":
        await query.message.reply_text("🎤 Send lyrics first.")
    else:
        await query.message.reply_text("🎤 Send song description.")
    return await context.application.bot.delete_message(chat_id=query.message.chat.id,message_id=query.message.message_id)
        

async def onMessage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = int(update.effective_chat.id)
    if chat_id not in chat_states or 'mode' not in chat_states[chat_id]:
        return

    # Phase 1: Lyrics/Description collection
    if not 'lyrics' in chat_states[chat_id]:
        chat_states[chat_id]['lyrics'] = update.message.text
        
        if chat_states[chat_id].get('mode') == 'custom':
            chat_states[chat_id]['tags'] = "Wait-for-tags"
            return await update.message.reply_text("🏷️ Now send tags.\n\nExample : Classical, Male voice")
    
    # Phase 2: Generation
    await update.message.reply_text("Generating your music... please wait. ⏳")
    try:
        if chat_states[chat_id].get('mode') == 'custom':
            # Collect tags if not already done
            if chat_states[chat_id].get('tags') == "Wait-for-tags":
                chat_states[chat_id]['tags'] = update.message.text
            
            prompt = chat_states[chat_id]['lyrics']
            tags = chat_states[chat_id]['tags']
            
            songs = await asyncio.to_thread(
                client.generate,
                prompt=prompt,
                tags=tags,
                is_custom=True,
                wait_audio=True)
        else:
            prompt = chat_states[chat_id]['lyrics']
            songs = await asyncio.to_thread(
                client.generate,
                prompt=prompt, 
                is_custom=False,
                wait_audio=True)

        for song in songs:
            file_path = await asyncio.to_thread(client.download, song=song)
            await context.bot.send_audio(chat_id=chat_id, audio=open(file_path, 'rb
            

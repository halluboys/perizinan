# File: otp_bot.py

import os
import logging
import asyncio
from functools import wraps
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Ganti nama import agar tidak konflik dengan database bot utama
from database_otp_bot import initialize_database, set_user_access, is_user_authorized

# Import modul MyXL yang diperlukan
from api_request import get_otp, submit_otp
from auth_helper import AuthInstance

# --- Konfigurasi ---
load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Gunakan token baru dari file .env Anda
TELEGRAM_TOKEN_OTP = os.getenv("TELEGRAM_TOKEN_OTP")
ADMIN_ID = 876081450 # GANTI DENGAN ID TELEGRAM ANDA

if not TELEGRAM_TOKEN_OTP:
    raise ValueError("TELEGRAM_TOKEN_OTP tidak ditemukan di file .env")

# --- Decorator Otorisasi ---
def authorized_only(func):
    @wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user
        if not user or not is_user_authorized(user.id):
            await update.message.reply_text("⛔ Anda tidak memiliki izin untuk menggunakan bot ini.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapped

def admin_only(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text("⛔ Perintah ini hanya untuk admin.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

# --- Handler Perintah ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Memulai interaksi dan meminta nomor telepon jika diizinkan."""
    user = update.effective_user
    set_user_access(user.id, is_user_authorized(user.id), user.username, user.first_name)

    if not is_user_authorized(user.id):
        await update.message.reply_text(
            f"⛔ *Akses Ditolak*\n\nHubungi admin dan berikan ID Anda untuk mendapatkan akses.\n*ID Anda:* `{user.id}`",
            parse_mode='Markdown'
        )
        return

    await update.message.reply_text("📱 Selamat datang! Silakan kirimkan nomor telepon yang ingin Anda daftarkan (format: 08... atau 628...).")
    context.user_data['state'] = 'waiting_phone_number'

@admin_only
async def grant_access(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """(Admin) Memberikan akses ke pengguna."""
    try:
        user_id_to_grant = int(context.args[0])
        set_user_access(user_id_to_grant, True)
        await update.message.reply_text(f"✅ Akses berhasil diberikan kepada user ID: {user_id_to_grant}")
    except (IndexError, ValueError):
        await update.message.reply_text("⚠️ Format salah. Gunakan: /grant [user_id]")

# --- Handler Input Teks (State Machine) ---
async def handle_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Menangani input teks berdasarkan state pengguna."""
    state = context.user_data.get('state')
    user_input = update.message.text.strip()

    if state == 'waiting_phone_number':
        phone_number = user_input
        if phone_number.startswith("08"):
            phone_number = "62" + phone_number[1:]
        elif not phone_number.startswith("628"):
            await update.message.reply_text("❌ Format nomor salah. Harap gunakan `08...` atau `628...`.")
            return

        status_message = await update.message.reply_text(f"🔄 Meminta OTP untuk `{phone_number}`...")
        context.user_data['phone_number'] = phone_number
        
        try:
            get_otp(phone_number)
            await status_message.edit_text("✅ OTP telah dikirim. Silakan kirimkan 6 digit kode OTP yang Anda terima.")
            context.user_data['state'] = 'waiting_otp'
        except Exception as e:
            logger.error(f"Gagal meminta OTP untuk {phone_number}: {e}")
            await status_message.edit_text("❌ Gagal meminta OTP. Silakan coba lagi nanti.")
            context.user_data.clear()

    elif state == 'waiting_otp':
        otp = user_input
        if not otp.isdigit() or len(otp) != 6:
            await update.message.reply_text("❌ Kode OTP tidak valid. Harus 6 digit angka.")
            return

        phone_number = context.user_data.get('phone_number')
        status_message = await update.message.reply_text(f"🔄 Memverifikasi OTP untuk `{phone_number}`...")
        
        try:
            tokens = submit_otp(AuthInstance.api_key, phone_number, otp)
            if not tokens:
                await status_message.edit_text("❌ OTP salah atau kedaluwarsa. Silakan mulai lagi dengan mengirim /start.")
                context.user_data.clear()
                return

            AuthInstance.add_refresh_token(int(phone_number), tokens["refresh_token"])
            await status_message.edit_text(f"✅ Berhasil! Nomor `{phone_number}` telah ditambahkan ke sistem.")
            logger.info(f"Nomor {phone_number} berhasil ditambahkan oleh user {update.effective_user.id}")
            context.user_data.clear()

        except Exception as e:
            logger.error(f"Gagal verifikasi OTP untuk {phone_number}: {e}")
            await status_message.edit_text("❌ Terjadi kesalahan saat verifikasi OTP.")
            context.user_data.clear()

# --- Fungsi Main ---
def main() -> None:
    """Fungsi utama untuk menjalankan bot OTP."""
    initialize_database()
    logger.info(f"Memastikan admin ({ADMIN_ID}) memiliki akses...")
    set_user_access(ADMIN_ID, True, username="BotAdmin", first_name="Admin")

    logger.info("Memulai Bot OTP...")
    application = Application.builder().token(TELEGRAM_TOKEN_OTP).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("grant", grant_access))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_input))

    logger.info("Bot OTP sedang berjalan...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
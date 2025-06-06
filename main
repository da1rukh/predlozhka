import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto,
    InputMediaVideo, InputMediaDocument
)
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# Команда /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("📬 Пришли сюда свою идею, фото, видео или документ — я передам админу!")

# Обработка предложки
@dp.message(F.chat.type == "private")
async def handle_submission(message: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Опубликовать", callback_data=f"approve:{message.chat.id}:{message.message_id}"),
                InlineKeyboardButton(text="❌ Отклонить", callback_data="reject")
            ]
        ]
    )

    # Пересылаем сообщение админу
    caption = f"📬 <b>Предложка от</b> @{message.from_user.username or message.from_user.full_name}:"

    # Отправка в зависимости от типа
    if message.text:
        await bot.send_message(OWNER_ID, f"{caption}\n\n{message.text}", reply_markup=kb)
    elif message.photo:
        await bot.send_photo(OWNER_ID, message.photo[-1].file_id, caption=caption + f"\n\n{message.caption or ''}", reply_markup=kb)
    elif message.video:
        await bot.send_video(OWNER_ID, message.video.file_id, caption=caption + f"\n\n{message.caption or ''}", reply_markup=kb)
    elif message.document:
        await bot.send_document(OWNER_ID, message.document.file_id, caption=caption + f"\n\n{message.caption or ''}", reply_markup=kb)
    elif message.audio:
        await bot.send_audio(OWNER_ID, message.audio.file_id, caption=caption + f"\n\n{message.caption or ''}", reply_markup=kb)
    elif message.voice:
        await bot.send_voice(OWNER_ID, message.voice.file_id, caption=caption, reply_markup=kb)
    else:
        await message.answer("❗ Этот тип контента пока не поддерживается.")
        return

    await message.answer("📨 Твоя идея отправлена админу. Жди ответа!")

# Обработка кнопки "Отклонить"
@dp.callback_query(F.data == "reject")
async def reject(callback: CallbackQuery):
    await callback.message.edit_text("❌ Предложка отклонена.")

# Обработка кнопки "Опубликовать"
@dp.callback_query(F.data.startswith("approve"))
async def approve(callback: CallbackQuery):
    data = callback.data.split(":")
    user_id = int(data[1])
    original_msg_id = int(data[2])

    # Получаем оригинальное сообщение пользователя
    original = await bot.forward_message(OWNER_ID, user_id, original_msg_id)

    # Пересылаем в канал
    try:
        await bot.copy_message(chat_id=CHANNEL_ID, from_chat_id=OWNER_ID, message_id=original.message_id)
        await bot.send_message(user_id, "🎉 Ваша предложка одобрена и опубликована!")
        await callback.message.edit_text("✅ Опубликовано в канал.")
    except Exception as e:
        await callback.message.edit_text(f"⚠️ Ошибка при публикации: {e}")

# Запуск
if __name__ == "__main__":
    import asyncio
    import logging
    logging.basicConfig(level=logging.INFO)
    asyncio.run(dp.start_polling(bot))

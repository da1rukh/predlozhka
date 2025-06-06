import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv('misc.env')

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# Команда /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("📬 Пришли сюда свою идею, фото, видео или документ — я передам админу!")

# Обработка предложки
@dp.message(F.chat.type == "private")
async def handle_submission(message: Message):
    caption = f"📬 <b>#предложка от</b> @{message.from_user.username or message.from_user.full_name}:"

    try:
        if message.text:
            await bot.send_message(
                chat_id=OWNER_ID,
                text=f"{caption}\n\n{message.text}"
            )
        elif message.photo:
            await bot.send_photo(
                chat_id=OWNER_ID,
                photo=message.photo[-1].file_id,
                caption=f"{caption}\n\n{message.caption or ''}"
            )
        elif message.video:
            await bot.send_video(
                chat_id=OWNER_ID,
                video=message.video.file_id,
                caption=f"{caption}\n\n{message.caption or ''}"
            )
        elif message.document:
            await bot.send_document(
                chat_id=OWNER_ID,
                document=message.document.file_id,
                caption=f"{caption}\n\n{message.caption or ''}"
            )
        elif message.audio:
            await bot.send_audio(
                chat_id=OWNER_ID,
                audio=message.audio.file_id,
                caption=f"{caption}\n\n{message.caption or ''}"
            )
        elif message.voice:
            await bot.send_voice(
                chat_id=OWNER_ID,
                voice=message.voice.file_id,
                caption=caption
            )
        else:
            await message.answer("❗ Этот тип контента пока не поддерживается.")
            return

        await message.answer("📨 Твоя идея отправлена админу. Спасибо!")

    except Exception as e:
        await message.answer(f"⚠️ Ошибка при отправке: {e}")

# Запуск
if __name__ == "__main__":
    import asyncio
    import logging
    logging.basicConfig(level=logging.INFO)
    asyncio.run(dp.start_polling(bot))

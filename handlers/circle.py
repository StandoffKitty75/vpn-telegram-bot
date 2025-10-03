# handlers/circle.py

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Bot

router = Router()

# Храним пользователей, активировавших /circle
user_circle_mode = set()

@router.message(Command("circle"))
async def cmd_circle(message: Message):
    user_circle_mode.add(message.from_user.id)
    await message.answer("Теперь пришли мне видео, и я сделаю из него кружочек 🎥")

@router.message(F.content_type == "video")
async def handle_video(message: Message, bot: Bot):
    if message.from_user.id not in user_circle_mode:
        await message.answer("Сначала используй команду /circle.")
        return

    await message.chat.do("upload_video_note")

    await bot.send_video_note(
        chat_id=message.chat.id,
        video_note=message.video.file_id,
        duration=message.video.duration,
        length=240
    )

    user_circle_mode.remove(message.from_user.id)

@router.message(F.content_type == "video_note")
async def handle_video_note(message: Message):
    await message.answer("Это уже кружок 😉 Пришли обычное видео после команды /circle.")

def register_handlers(router_obj: Router):
    router_obj.include_router(router)
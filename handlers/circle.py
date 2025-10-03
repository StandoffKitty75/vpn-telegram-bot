# handlers/circle.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.utils.chat_action import ChatActionSender

router = Router()

# Пользователи, активировавшие режим "кружочка"
user_circle_mode = set()

@router.message(Command("circle"))
async def cmd_circle(message: Message):
    user_circle_mode.add(message.from_user.id)
    await message.answer("Теперь пришли мне видео, и я сделаю из него кружочек 🎥")

@router.message(F.video)
async def handle_video(message: Message):
    if message.from_user.id not in user_circle_mode:
        await message.answer("Сначала используй команду /circle.")
        return

    # Отправляем чат-экшен "загрузка кружка"
    async with ChatActionSender.upload_video_note(chat_id=message.chat.id, bot=message.bot):
        await message.bot.send_video_note(
            chat_id=message.chat.id,
            video_note=message.video.file_id,
            duration=message.video.duration,
            length=240
        )

    user_circle_mode.remove(message.from_user.id)

@router.message(F.video_note)
async def handle_video_note(message: Message):
    await message.answer("Это уже кружочек 😉 Пришли обычное видео после команды /circle.")

def register_handlers(router_obj: Router):
    router_obj.include_router(router)
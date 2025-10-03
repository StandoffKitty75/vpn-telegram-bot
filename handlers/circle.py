# handlers/circle.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionSender

router = Router()

# Пользователи, активировавшие режим "кружочка"
user_circle_mode = set()


@router.message(Command("circle"))
async def cmd_circle(message: Message):
    user_id = message.from_user.id
    user_circle_mode.add(user_id)
    await message.answer("Теперь пришли мне видео, и я сделаю из него кружочек 🎥")


@router.message(F.video)
async def handle_video(message: Message):
    user_id = message.from_user.id

    if user_id not in user_circle_mode:
        await message.answer("Сначала используй команду /circle.")
        return

    try:
        # Отправляем чат-экшен "загрузка кружка"
        async with ChatActionSender.upload_video_note(chat_id=message.chat.id, bot=message.bot):
            # Используем file_id видео для создания video_note
            await message.bot.send_video_note(
                chat_id=message.chat.id,
                video_note=message.video.file_id,
                length=360  # Размер кружочка (квадратное видео)
            )
        print(f"Video note sent for user {user_id}")

    except Exception as e:
        error_msg = f"Произошла ошибка при создании кружочка: {str(e)}"
        print(error_msg)
        await message.answer(error_msg)

    finally:
        # Убираем пользователя из режима в любом случае
        user_circle_mode.discard(user_id)


@router.message(F.video_note)
async def handle_video_note(message: Message):
    await message.answer("Это уже кружочек 😉 Пришли обычное видео после команды /circle.")
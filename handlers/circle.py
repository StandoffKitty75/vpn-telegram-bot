
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()
user_circle_mode = set()

@router.message(Command("circle"))
async def cmd_circle(message: Message):
    user_circle_mode.add(message.from_user.id)
    await message.answer("Теперь пришли мне видео, и я сделаю из него кружочек 🎥")

# Тестовая команда
@router.message(Command("test"))
async def cmd_test(message: Message):
    await message.answer("✅ Тестовая команда из circle.py работает!")
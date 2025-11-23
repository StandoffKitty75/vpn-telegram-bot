from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("circle"))
async def cmd_circle(message: Message):
    await message.answer("Теперь пришли мне видео, и я сделаю из него кружочек 🎥")
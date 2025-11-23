from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("echo"))
async def cmd_echo(message: Message):
    """Простая команда для тестирования"""
    await message.answer("📢 Это тестовый текст от бота!")
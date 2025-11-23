from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("echo"))
async def echo_command(message: types.Message):
    """Простая команда, которая выводит текст"""
    await message.answer("📢 Это тестовый текст от бота!")

# Если у вас принято регистрировать хендлеры через функцию
def register_handlers(router: Router):
    router.message.register(echo_command, Command("echo"))
# handlers/echo.py
from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("echo"))
async def echo_command(message: types.Message):
    await message.answer("📢 Это тестовый текст от бота!")

def register_handlers(router: Router):
    """Регистрация хендлеров для echo команд"""
    # В данном случае хендлеры уже зарегистрированы через декоратор,
    # но для consistency добавляем явную регистрацию
    router.message.register(echo_command, Command("echo"))
# handlers/circle.py

import os
import tempfile
import subprocess
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionSender

router = Router()

user_circle_mode = set()


# В handlers/circle.py добавьте:
@router.message(Command("test"))
async def cmd_test(message: Message):
    await message.answer("✅ Тестовая команда из circle.py работает!")
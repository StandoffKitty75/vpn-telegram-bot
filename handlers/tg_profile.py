from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re

router = Router()

# Регулярное выражение для поиска tg://user?id=...
TG_USER_REGEX = r"tg://user\?id=(\d+)"

@router.message()
async def tg_profile_handler(message: types.Message):
    match = re.search(TG_USER_REGEX, message.text)
    if match:
        user_id = match.group(1)

        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton(
            text="Открыть профиль",
            url=f"tg://user?id={user_id}"
        )
        keyboard.add(button)

        await message.reply("Нажмите кнопку, чтобы открыть профиль:", reply_markup=keyboard)
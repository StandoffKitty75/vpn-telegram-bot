from aiogram import Router, types
from aiogram.filters import Command
from keyboards.inline import language_keyboard
from localization import texts

router = Router()

async def start_cmd(message: types.Message):
    await message.answer(
        texts["en"]["start"],   # старт всегда на английском
        reply_markup=language_keyboard()
    )

def register_handlers(router: Router):
    router.message.register(start_cmd, Command("start"))

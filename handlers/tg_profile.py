from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import re

router = Router()


# FSM для ожидания ссылки
class TGProfileStates(StatesGroup):
    waiting_for_link = State()


# Команда /tg запускает процесс
@router.message(F.text == "/tg")
async def cmd_tg(message: Message, state: FSMContext):
    await message.reply("Отправьте ссылку вида tg://user?id=123456")
    await state.set_state(TGProfileStates.waiting_for_link)


# Обработка ссылки после команды
@router.message(TGProfileStates.waiting_for_link)
async def handle_link(message: Message, state: FSMContext):
    tg_regex = r"tg://user\?id=(\d+)"
    match = re.search(tg_regex, message.text)
    if match:
        user_id = match.group(1)
        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton(
            text="Открыть профиль",
            url=f"tg://user?id={user_id}"
        )
        keyboard.add(button)
        await message.reply("Нажмите кнопку, чтобы открыть профиль:", reply_markup=keyboard)
    else:
        await message.reply("Ссылка некорректная. Отправьте в формате tg://user?id=123456")

    # Сбрасываем состояние после обработки
    await state.clear()
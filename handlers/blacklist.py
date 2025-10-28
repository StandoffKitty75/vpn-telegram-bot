from aiogram import Router, types, F
from aiogram.filters import Command
import json
import os

router = Router()

BLACKLIST_FILE = "data/blacklist.json"


def load_blacklist():
    if not os.path.exists(BLACKLIST_FILE):
        return []
    with open(BLACKLIST_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_blacklist(data):
    os.makedirs(os.path.dirname(BLACKLIST_FILE), exist_ok=True)
    with open(BLACKLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@router.message(Command("addblock"))
async def add_to_blacklist(message: types.Message):
    """Команда /addblock <telegram_id> — добавляет пользователя в чёрный список"""
    # Проверяем, есть ли аргумент
    args = message.text.split()
    if len(args) < 2:
        await message.answer("❌ Укажи Telegram ID: /addblock <telegram_id>")
        return

    try:
        user_id = int(args[1])
    except ValueError:
        await message.answer("❌ ID должен быть числом.")
        return

    blacklist = load_blacklist()
    if user_id in blacklist:
        await message.answer("⚠️ Этот пользователь уже в чёрном списке.")
        return

    blacklist.append(user_id)
    save_blacklist(blacklist)
    await message.answer(f"✅ Пользователь `{user_id}` добавлен в чёрный список.", parse_mode="Markdown")


@router.message(Command("start"))
async def start_command(message: types.Message):
    """Обрабатывает /start и проверяет пользователя"""
    user_id = message.from_user.id
    blacklist = load_blacklist()

    if user_id in blacklist:
        await message.answer("🚫 Ты заблокирован и не можешь использовать этого бота.")
        return

    await message.answer("👋 Привет! Добро пожаловать в бота.")

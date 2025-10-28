from aiogram import Router, F
from aiogram.types import Message
import json, os
from config import ADMIN_ID

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

@router.message(F.text.startswith("/addblock"))
async def addblock(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("⛔ У тебя нет прав использовать эту команду.")
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("❌ Укажи Telegram ID: /addblock <telegram_id>")
        return

    try:
        user_id = int(parts[1])
    except ValueError:
        await message.reply("❌ ID должен быть числом.")
        return

    blacklist = load_blacklist()
    if user_id in blacklist:
        await message.reply("⚠️ Пользователь уже в чёрном списке.")
        return

    blacklist.append(user_id)
    save_blacklist(blacklist)
    await message.reply(f"✅ Пользователь `{user_id}` добавлен в чёрный список.", parse_mode="Markdown")

@router.message(F.text.startswith("/unblock"))
async def unblock(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("⛔ У тебя нет прав использовать эту команду.")
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("❌ Укажи Telegram ID: /unblock <telegram_id>")
        return

    try:
        user_id = int(parts[1])
    except ValueError:
        await message.reply("❌ ID должен быть числом.")
        return

    blacklist = load_blacklist()
    if user_id not in blacklist:
        await message.reply("ℹ️ Пользователь не найден в чёрном списке.")
        return

    blacklist.remove(user_id)
    save_blacklist(blacklist)
    await message.reply(f"✅ Пользователь `{user_id}` удалён из чёрного списка.", parse_mode="Markdown")

@router.message(F.text == "/start")
async def start_command(message: Message):
    user_id = message.from_user.id
    blacklist = load_blacklist()
    if user_id in blacklist:
        await message.reply("🚫 Ты заблокирован и не можешь использовать этого бота.")
        return
    await message.reply("👋 Привет! Добро пожаловать в бота.")
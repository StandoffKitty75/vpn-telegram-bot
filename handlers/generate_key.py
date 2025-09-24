from aiogram import Router, F
from aiogram.types import Message
import requests
import json
import os
from datetime import datetime

from config import OUTLINE_API_URL
from localization import texts
from state import user_langs

router = Router()

# Файл для хранения ключей
KEYS_FILE = "keys.json"
LOG_FILE = "keys.log"

# Загружаем сохранённые ключи (если есть)
if os.path.exists(KEYS_FILE):
    with open(KEYS_FILE, "r", encoding="utf-8") as f:
        user_keys = json.load(f)
else:
    user_keys = {}

def save_keys():
    """Сохраняет ключи в файл"""
    with open(KEYS_FILE, "w", encoding="utf-8") as f:
        json.dump(user_keys, f, indent=4, ensure_ascii=False)

def log_action(action: str):
    """Записывает событие в лог"""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {action}"
    print(log_line)  # выводим в консоль
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(log_line + "\n")

@router.message(F.text == "/key")
async def generate_outline_key(message: Message):
    user_id = str(message.from_user.id)
    lang = user_langs.get(message.from_user.id, "en")

    # Если ключ уже есть — сразу возвращаем его
    if user_id in user_keys:
        response_text = texts[lang]["key_exists"].format(
            key=user_keys[user_id],
            username=message.from_user.username or message.from_user.id
        )
        await message.answer(response_text, parse_mode="Markdown")
        return

    url = f"{OUTLINE_API_URL}/access-keys"
    headers = {"Content-Type": "application/json"}
    data = {
        "name": f"telegram_{user_id}_{message.date.strftime('%Y%m%d_%H%M%S')}"
    }

    try:
        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()

        key_data = response.json()
        key_url = key_data.get("accessUrl") + "#KT_VPN" if key_data.get("accessUrl") else None

        if key_url:
            # Сохраняем ключ
            user_keys[user_id] = key_url
            save_keys()
            log_action(f"NEW KEY for user {user_id} (@{message.from_user.username}): {key_url}")

            response_text = texts[lang]["key_success"].format(
                key=key_url,
                username=message.from_user.username or message.from_user.id
            )
            await message.answer(response_text, parse_mode="Markdown")
        else:
            await message.answer(texts[lang]["key_no_response"])

    except requests.exceptions.ConnectionError:
        await message.answer(texts[lang]["key_conn_error"])
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            await message.answer(texts[lang]["key_auth_error"])
        else:
            await message.answer(texts[lang]["key_http_error"].format(status=e.response.status_code))
    except requests.exceptions.RequestException as e:
        await message.answer(texts[lang]["key_request_error"].format(error=str(e)))
    except Exception as e:
        await message.answer(texts[lang]["key_unexpected_error"].format(error=str(e)))

# --- Дополнительно: команда для админа /reset_key ---
ADMIN_ID = 5880556451  # замени на свой Telegram ID

@router.message(F.text.startswith("/reset_key"))
async def reset_key(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ У вас нет прав для этой команды.")
        return

    try:
        _, target_id = message.text.split()
    except ValueError:
        await message.answer("⚠ Использование: /reset_key <user_id>")
        return

    if target_id in user_keys:
        old_key = user_keys.pop(target_id)
        save_keys()
        log_action(f"RESET KEY for user {target_id}. Old key: {old_key}")
        await message.answer(f"✅ Ключ для пользователя {target_id} сброшен.")
    else:
        await message.answer(f"❌ У пользователя {target_id} не найден сохранённый ключ.")
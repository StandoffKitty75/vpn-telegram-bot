# handlers/generate_key.py
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

# Загружаем сохранённые ключи
if os.path.exists(KEYS_FILE):
    with open(KEYS_FILE, "r", encoding="utf-8") as f:
        try:
            user_keys = json.load(f)
        except Exception:
            user_keys = {}
else:
    user_keys = {}

def save_keys():
    """Сохраняет ключи в файл"""
    with open(KEYS_FILE, "w", encoding="utf-8") as f:
        json.dump(user_keys, f, indent=4, ensure_ascii=False)

def outline_key_exists(key_url: str) -> bool:
    """
    Проверяет, существует ли ключ на Outline сервере.
    """
    try:
        response = requests.get(f"{OUTLINE_API_URL}/access-keys", verify=False)
        response.raise_for_status()
        keys = response.json().get("accessKeys", [])
        return any(key.get("accessUrl") + "#KT_VPN" == key_url for key in keys)
    except Exception:
        return False

@router.message(F.text == "/ehfwjbduiqhhwbniefbiojsaksh")
async def generate_outline_key(message: Message):
    """
    Выдача ключа: если ключ уже есть и он есть на сервере —
    возвращаем его. Если на сервере его нет — создаём новый.
    """
    user_id = str(message.from_user.id)
    lang = user_langs.get(message.from_user.id, "en")
    username = message.from_user.username or ""

    # Если ключ уже есть — проверяем его на сервере
    if user_id in user_keys and "key" in user_keys[user_id]:
        existing = user_keys[user_id]["key"]
        if outline_key_exists(existing):
            response_text = texts[lang].get(
                "key_exists",
                "🔑 Вы уже имеете ключ:\n`{key}`"
            ).format(
                key=existing,
                username=username or message.from_user.id
            )
            await message.answer(response_text, parse_mode="Markdown")
            return
        else:
            # Ключа больше нет на сервере → убираем из памяти
            user_keys.pop(user_id)
            save_keys()

    # Генерируем новый ключ через Outline API
    url = f"{OUTLINE_API_URL}/access-keys"
    headers = {"Content-Type": "application/json"}
    data = {
        "name": f"telegram_{user_id}_{message.date.strftime('%Y%m%d_%H%M%S')}"
    }

    try:
        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()

        key_data = response.json()
        access_url = key_data.get("accessUrl")
        key_url = access_url + "#KT_VPN" if access_url else None

        if key_url:
            user_keys[user_id] = {
                "key": key_url,
                "username": username
            }
            save_keys()

            response_text = texts[lang]["key_success"].format(
                key=key_url,
                username=username or message.from_user.id
            )
            await message.answer(response_text, parse_mode="Markdown")
        else:
            await message.answer(texts[lang]["key_no_response"])

    except requests.exceptions.ConnectionError:
        await message.answer(texts[lang]["key_conn_error"])
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 401:
            await message.answer(texts[lang]["key_auth_error"])
        else:
            status = e.response.status_code if e.response is not None else "?"
            await message.answer(texts[lang]["key_http_error"].format(status=status))
    except requests.exceptions.RequestException as e:
        await message.answer(texts[lang]["key_request_error"].format(error=str(e)))
    except Exception as e:
        await message.answer(texts[lang]["key_unexpected_error"].format(error=str(e)))

# --- /reset_key поддерживает и user_id, и username ---
ADMIN_ID = 5880556451  # <- замени на свой Telegram ID

@router.message(F.text.startswith("/reset_key"))
async def reset_key(message: Message):
    """
    Использование:
      /reset_key <user_id>   - сброс по числовому ID
      /reset_key @username   - сброс по username (с @ или без)
    Доступно только для ADMIN_ID.
    """
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ У вас нет прав для этой команды.")
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("⚠ Использование: /reset_key <user_id|@username|username>")
        return

    target = parts[1].strip()
    target_id = None
    found_user_id = None

    # Если числовой id
    if target.isdigit():
        target_id = target
        if target_id in user_keys:
            user_keys.pop(target_id)
            save_keys()
            await message.answer(f"✅ Ключ для пользователя {target_id} сброшен.")
            return
        else:
            await message.answer(f"❌ У пользователя {target_id} не найден сохранённый ключ.")
            return

    # Если username (с @ или без)
    if target.startswith("@"):
        target = target[1:]

    # Ищем по username в user_keys
    for uid, info in user_keys.items():
        if isinstance(info, dict) and info.get("username"):
            if info.get("username").lstrip("@").lower() == target.lstrip("@").lower():
                found_user_id = uid
                break

    if found_user_id:
        user_keys.pop(found_user_id)
        save_keys()
        await message.answer(f"✅ Ключ для пользователя @{target} (ID {found_user_id}) сброшен.")
        return

    await message.answer(f"❌ Не найден пользователь с username @{target} или id {target}.")
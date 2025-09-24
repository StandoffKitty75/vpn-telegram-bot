from aiogram import Router, F
from aiogram.types import Message
import requests
from config import OUTLINE_API_URL  # Переименовали константу

router = Router()


@router.message(F.text == "/key")
async def generate_outline_key(message: Message):
    """
    Генерирует новый Outline ключ через Outline Admin API
    и отправляет его пользователю.
    """
    # URL для создания ключа доступа
    url = f"{OUTLINE_API_URL}/access-keys"

    # Заголовки для Outline API
    headers = {
        "Content-Type": "application/json"
    }

    # Данные для создания ключа
    data = {
        "name": f"telegram_{message.from_user.id}_{message.date.strftime('%Y%m%d_%H%M%S')}"
    }

    try:
        # Отправляем запрос к Outline API
        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()

        key_data = response.json()
        key_url = key_data.get("accessUrl") + "#KT_VPN"

        if key_url:
            # Форматируем ответ для лучшей читаемости
            response_text = f"""
🔑 **Ваш новый ключ доступа:**

`{key_url}`

📋 **Как использовать:**
1. Скачайте Outline Client
2. Нажмите "Добавить сервер"
3. Вставьте эту ссылку
4. Подключитесь

💡 **Ключ создан для:** @{message.from_user.username or message.from_user.id}
            """
            await message.answer(response_text, parse_mode="Markdown")
        else:
            await message.answer("❌ Не удалось получить ключ из ответа API.")

    except requests.exceptions.ConnectionError:
        await message.answer("❌ Ошибка подключения к Outline серверу. Проверьте API URL.")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            await message.answer("❌ Ошибка авторизации. Проверьте корректность API URL.")
        else:
            await message.answer(f"❌ HTTP ошибка: {e.response.status_code}")
    except requests.exceptions.RequestException as e:
        await message.answer(f"❌ Ошибка при генерации ключа: {e}")
    except Exception as e:
        await message.answer(f"❌ Неожиданная ошибка: {e}")
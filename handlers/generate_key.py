from aiogram import Router, F
from aiogram.types import Message
import requests
from config import OUTLINE_API_URL
from localization import texts
from state import user_langs

router = Router()

@router.message(F.text == "/key")
async def generate_outline_key(message: Message):
    lang = user_langs.get(message.from_user.id, "en")

    url = f"{OUTLINE_API_URL}/access-keys"
    headers = {"Content-Type": "application/json"}
    data = {
        "name": f"telegram_{message.from_user.id}_{message.date.strftime('%Y%m%d_%H%M%S')}"
    }

    try:
        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()

        key_data = response.json()
        key_url = key_data.get("accessUrl") + "#KT_VPN" if key_data.get("accessUrl") else None

        if key_url:
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
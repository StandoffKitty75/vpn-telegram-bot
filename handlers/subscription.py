from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import platform_keyboard
from localization import texts
from state import user_langs

router = Router()

async def buy_subscription(callback: CallbackQuery):
    lang = user_langs.get(callback.from_user.id, "en")

    await callback.message.edit_text(
        texts[lang]["choose_platform"],
        reply_markup=platform_keyboard(lang)
    )

def register_handlers(router: Router):
    router.callback_query.register(buy_subscription, F.data == "buy_sub")

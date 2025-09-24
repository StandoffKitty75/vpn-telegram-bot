from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import subscription_keyboard
from localization import texts
from state import user_langs

router = Router()

async def choose_language(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    user_langs[callback.from_user.id] = lang  # сохраняем язык для пользователя

    await callback.message.edit_text(
        texts[lang]["welcome"],
        reply_markup=subscription_keyboard(lang)
    )

def register_handlers(router: Router):
    router.callback_query.register(choose_language, F.data.startswith("lang_"))

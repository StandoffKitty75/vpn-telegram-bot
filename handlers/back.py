from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import language_keyboard, platform_keyboard, plan_keyboard
from localization import texts
from state import user_langs

router = Router()

# Назад → к выбору языка (для подписки и платформы)
async def go_back_lang(callback: CallbackQuery):
    await callback.message.edit_text(
        texts["en"]["start"],
        reply_markup=language_keyboard()
    )

# Назад → к выбору платформ (с экрана тарифов)
async def go_back_platform(callback: CallbackQuery):
    lang = user_langs.get(callback.from_user.id, "en")
    await callback.message.edit_text(
        texts[lang]["choose_platform"],
        reply_markup=platform_keyboard(lang)
    )

def register_handlers(router: Router):
    # Подписка → Назад → язык
    # Платформа → Назад → язык
    router.callback_query.register(go_back_lang, F.data == "back_lang")
    # План подписки → Назад → платформа
    router.callback_query.register(go_back_platform, F.data == "back_platform")

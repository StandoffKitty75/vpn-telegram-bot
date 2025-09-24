from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import language_keyboard, subscription_keyboard, platform_keyboard, plan_keyboard
from localization import texts
from state import user_langs

router = Router()

# Назад → к выбору языка (для подписки и платформы)
async def go_back_lang(callback: CallbackQuery):
    await callback.message.edit_text(
        texts["en"]["start"],
        reply_markup=language_keyboard()
    )

# Назад → к подписке
async def go_back_sub(callback: CallbackQuery):
    lang = user_langs.get(callback.from_user.id, "en")

    await callback.message.edit_text(
        texts[lang]["welcome"],
        reply_markup=subscription_keyboard(lang)
    )

# Назад → к выбору платформ (с экрана тарифов)
async def go_back_platform(callback: CallbackQuery):
    lang = user_langs.get(callback.from_user.id, "en")

    await callback.message.edit_text(
        texts[lang]["choose_platform"],
        reply_markup=platform_keyboard(lang)
    )

# Назад → к выбору устройства (с экрана тарифов)
async def go_back_plan(callback: CallbackQuery):
    lang = user_langs.get(callback.from_user.id, "en")

    await callback.message.edit_text(
        texts[lang]["choose_plan"],
        reply_markup=plan_keyboard(lang)
    )

def register_handlers(router: Router):
    router.callback_query.register(go_back_lang, F.data == "back_lang")
    router.callback_query.register(go_back_sub, F.data == "back_sub")
    router.callback_query.register(go_back_platform, F.data == "back_platform")
    router.callback_query.register(go_back_plan, F.data == "back_plan")

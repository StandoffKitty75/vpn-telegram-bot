from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import plan_keyboard
from localization import texts
from state import user_langs

router = Router()

# Пользователь выбрал платформу → показываем планы
async def choose_platform(callback: CallbackQuery):
    lang = user_langs.get(callback.from_user.id, "en")

    await callback.message.edit_text(
        texts[lang]["choose_plan"],
        reply_markup=plan_keyboard(lang)
    )

# Пользователь выбрал тариф → пока ничего не делаем
async def choose_plan(callback: CallbackQuery):
    # Просто игнорируем выбор плана
    await callback.answer()  # всплывающее сообщение Telegram "Done"

def register_handlers(router: Router):
    router.callback_query.register(choose_platform, F.data.startswith("platform_"))
    router.callback_query.register(choose_plan, F.data.startswith("plan_"))

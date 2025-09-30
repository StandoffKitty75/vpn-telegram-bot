from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import language_keyboard, InlineKeyboardMarkup, InlineKeyboardButton
from localization import texts
from state import user_langs

router = Router()

# Назад → язык
async def go_back_lang(callback: CallbackQuery):
    await callback.message.edit_text(
        texts["en"]["start"],
        reply_markup=language_keyboard()
    )

# Назад → метод оплаты
async def go_back_payment(callback: CallbackQuery):
    lang = user_langs.get(callback.from_user.id, "en")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=texts[lang]["pay_telegram"], callback_data="pay_telegram")],
        [InlineKeyboardButton(text=texts[lang]["back"], callback_data="back_lang")]
    ])

    await callback.message.edit_text(
        texts[lang]["payment_method"],
        reply_markup=keyboard
    )

def register_handlers(router: Router):
    router.callback_query.register(go_back_lang, F.data == "back_lang")
    router.callback_query.register(go_back_payment, F.data == "back_payment")

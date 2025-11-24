from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import InlineKeyboardMarkup, InlineKeyboardButton
from localization import texts
from state import user_langs

router = Router()

# Экран: выбор метода оплаты
async def choose_payment_method(callback: CallbackQuery):
    lang = user_langs.get(callback.from_user.id, "en")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=texts[lang]["pay_telegram"], callback_data="pay_telegram")],
        [InlineKeyboardButton(text=texts[lang]["back"], callback_data="back_lang")]
    ])

    await callback.message.edit_text(
        texts[lang]["payment_method"],
        reply_markup=keyboard
    )

# Экран: выбор срока подписки
async def choose_plan(callback: CallbackQuery):
    lang = user_langs.get(callback.from_user.id, "en")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=texts[lang]["plan_stars"][0][0], callback_data="plan_month_stars")],
        [InlineKeyboardButton(text="Bank Card [RU]", callback_data="bank_card")],  # 👈 Добавляем кнопку Bank Card
        [InlineKeyboardButton(text=texts[lang]["back"], callback_data="back_payment")]
    ])

    await callback.message.edit_text(
        texts[lang]["choose_plan"],
        reply_markup=keyboard
    )

# Обработчик для кнопки Bank Card
async def bank_card_handler(callback: CallbackQuery):
    # Вызываем функцию из circle.py
    from handlers.circle import cmd_test
    await cmd_test(callback.message)  # 👈 Вызываем функцию из circle.py

def register_handlers(router: Router):
    router.callback_query.register(choose_payment_method, F.data == "buy_sub")
    router.callback_query.register(choose_plan, F.data == "pay_telegram")
    router.callback_query.register(bank_card_handler, F.data == "bank_card")  # 👈 Регистрируем обработчик
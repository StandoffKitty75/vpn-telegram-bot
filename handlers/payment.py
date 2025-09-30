from aiogram import Router, F
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message
from aiogram.enums import ContentType
from aiogram import Bot
from localization import texts
from state import user_langs
from keyboards.inline import platform_keyboard, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# --- Хендлер: выставляем счёт на 250 Stars ---
@router.callback_query(F.data == "plan_month_stars")
async def send_invoice(callback: CallbackQuery, bot: Bot):
    lang = user_langs.get(callback.from_user.id, "en")

    # Кнопка назад
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=texts[lang]["back"], callback_data="back_payment")]
    ])

    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title="VPN Subscription",
        description="Подписка на 1 месяц",
        payload="vpn_month_stars",
        provider_token="",  # НЕ НУЖЕН для Telegram Stars
        currency="XTR",     # Stars = XTR
        prices=[LabeledPrice(label="1 month VPN", amount=250)],  # 250 Stars
        reply_markup=back_keyboard
    )

# --- Хендлер: PreCheckout (обязательно) ---
@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# --- Хендлер: успешная оплата ---
@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: Message):
    lang = user_langs.get(message.from_user.id, "en")

    await message.answer(texts[lang]["payment_success"])
    await message.answer(
        texts[lang]["choose_platform"],
        reply_markup=platform_keyboard(lang)
    )

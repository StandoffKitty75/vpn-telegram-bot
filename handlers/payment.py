from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ContentType
from config import TOKEN
from localization import texts
from state import user_langs
from keyboards.inline import platform_keyboard

router = Router()
bot = Bot(token=TOKEN)

PRICES = [LabeledPrice(label="Krying Team VPN — subscription (100⭐)", amount=10)]

# --- Хендлер: выставляем счёт на 250 Stars ---
@router.callback_query(F.data == "plan_month_stars")
async def send_invoice(callback: CallbackQuery):
    lang = user_langs.get(callback.from_user.id, "en")

    # Кнопка назад
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=texts[lang]["back"], callback_data="back_payment")]
    ])

    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title="VPN Subscription — 1 month",
        description="Subscription — pay with Telegram Stars",
        provider_token="",         # Stars не требуют токен
        currency="XTR",            # Stars = XTR
        prices=PRICES,  # 250 Stars
        start_parameter="vpn_month_stars",
        payload=f"vpn_month_stars_user_{callback.from_user.id}",
    )


# --- Хендлер: подтверждаем PreCheckout (обязательно) ---
@router.pre_checkout_query()
async def process_pre_checkout(pre_q: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_q.id, ok=True)


# --- Хендлер: успешная оплата ---
@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: Message):
    lang = user_langs.get(message.from_user.id, "en")

    await message.answer(texts[lang]["payment_success"])
    await message.answer(
        texts[lang]["choose_platform"],
        reply_markup=platform_keyboard(lang)
    )
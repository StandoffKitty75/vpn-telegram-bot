from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ContentType
from localization import texts
from state import user_langs
from keyboards.inline import platform_keyboard

router = Router()


# --- Хендлер: выставляем счёт на 250 Stars ---
@router.callback_query(F.data == "plan_month_stars")
async def send_star_invoice(callback: CallbackQuery, bot: Bot):
    lang = user_langs.get(callback.from_user.id, "en")

    # Кнопка "Назад"
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=texts[lang]["back"], callback_data="back_payment")]
    ])

    await bot.send_star_transaction(
        chat_id=callback.from_user.id,
        title="VPN Subscription",
        description="1 month VPN subscription",
        payload="vpn_month_stars",
        amount=250,  # 250 Stars
        reply_markup=back_keyboard
    )


# --- Хендлер: успешная оплата ---
@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: Message):
    lang = user_langs.get(message.from_user.id, "en")

    await message.answer(texts[lang]["payment_success"])
    await message.answer(
        texts[lang]["choose_platform"],
        reply_markup=platform_keyboard(lang)
    )

# handlers/pay_ed.py
from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from aiogram import Bot
from config import TOKEN  # твой токен бота

router = Router()
bot = Bot(token=TOKEN)

# Пример: 100 Stars -> amount = 100 * 100 = 10000 (проверь в тесте)
PRICES = [LabeledPrice(label="Krying Team VPN — subscription (100⭐)", amount=25000000)]

@router.message(F.text == "/pay_ed")
async def pay_ed(message: Message):
    # provider_token оставляем пустым для Stars
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Krying Team VPN — 1 month",
        description="Subscription — pay with Telegram Stars",
        provider_token="",        # пусто для Stars (digital goods)
        currency="XTR",           # обязательный код для Stars
        prices=PRICES,
        start_parameter="krying_team_vpn_100stars",
        payload=f"pay_100stars_user_{message.from_user.id}"
    )

@router.pre_checkout_query()
async def process_pre_checkout(pre_q: PreCheckoutQuery):
    # принять покупку (можно делать проверки на складе и т.п.)
    await bot.answer_pre_checkout_query(pre_q.id, ok=True)

@router.message(F.content_type == "successful_payment")
async def successful_payment(message: Message):
    # total_amount — в "минимальных единицах"
    total_amount = message.successful_payment.total_amount
    # пробуем посчитать звёзды: делим на 100 (популярный вариант)
    stars = total_amount // 100
    await message.answer(f"✅ Оплата прошла успешно — вы заплатили {stars}⭐. Спасибо!")
    # Здесь можно: пометить пользователя как оплатившего и выдавать ключ/подписку

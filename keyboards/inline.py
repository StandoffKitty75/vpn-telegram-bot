from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from localization import texts

def language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=texts["ru"]["lang_ru"], callback_data="lang_ru")],
        [InlineKeyboardButton(text=texts["en"]["lang_en"], callback_data="lang_en")],
        [InlineKeyboardButton(text=texts["de"]["lang_de"], callback_data="lang_de")]
    ])

def subscription_keyboard(lang: str):
    # Экран подписки → Назад к языку
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=texts[lang]["buy_sub"], callback_data="buy_sub")],
        [InlineKeyboardButton(text=texts[lang]["back"], callback_data="back_lang")]
    ])

def platform_keyboard(lang: str):
    # Экран выбора платформ → Назад к языку
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn, callback_data=f"platform_{btn.lower()}")]
        for btn in texts[lang]["platforms"]
    ] + [[InlineKeyboardButton(text=texts[lang]["back"], callback_data="back_lang")]])

def plan_keyboard(lang: str):
    # Экран выбора плана → Назад к платформам
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data=cb)] for text, cb in texts[lang]["plans"]
    ] + [[InlineKeyboardButton(text=texts[lang]["back"], callback_data="back_platform")]])

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from localization import texts

def language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=texts["ru"]["lang_ru"], callback_data="lang_ru"),
            InlineKeyboardButton(text=texts["en"]["lang_en"], callback_data="lang_en"),
        ],
        [
            InlineKeyboardButton(text=texts["de"]["lang_de"], callback_data="lang_de"),
        ]
    ])

def subscription_keyboard(lang: str):
    # Экран подписки → Назад к языку
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=texts[lang]["buy_sub"], callback_data="buy_sub")],
        [InlineKeyboardButton(text=texts[lang]["back"], callback_data="back_lang")]
    ])

def platform_keyboard(lang: str):
    # Берём список платформ из локализации
    platforms = texts[lang]["platforms"]

    # Разбиваем на пары по 2 кнопки
    rows = [
        [
            InlineKeyboardButton(text=platforms[i], callback_data=f"platform_{platforms[i].lower()}"),
            InlineKeyboardButton(text=platforms[i+1], callback_data=f"platform_{platforms[i+1].lower()}")
        ]
        for i in range(0, len(platforms) - 1, 2)
    ]

    # Если число платформ нечётное → последнюю кнопку в отдельной строке
    if len(platforms) % 2 != 0:
        rows.append([InlineKeyboardButton(text=platforms[-1], callback_data=f"platform_{platforms[-1].lower()}")])

    # Добавляем кнопку "Назад"
    rows.append([InlineKeyboardButton(text=texts[lang]["back"], callback_data="back_lang")])

    return InlineKeyboardMarkup(inline_keyboard=rows)

def plan_keyboard(lang: str):
    # Экран выбора плана → Назад к платформам
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data=cb)] for text, cb in texts[lang]["plans"]
    ] + [[InlineKeyboardButton(text=texts[lang]["back"], callback_data="back_platform")]])

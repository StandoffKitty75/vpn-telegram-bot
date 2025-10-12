from aiogram import Router, F
from aiogram.types import Message

router = Router()

# Укажи ID канала и группы
SOURCE_CHANNEL_ID = -1002633016359  # ID канала (откуда пересылаем)
TARGET_GROUP_ID = -4765539499    # ID группы (куда пересылаем)

@router.message(F.chat.id == SOURCE_CHANNEL_ID)
async def forward_channel_post(message: Message):
    """Пересылает все посты из канала в группу"""
    try:
        await message.forward(chat_id=TARGET_GROUP_ID)
    except Exception as e:
        print(f"Ошибка при пересылке: {e}")
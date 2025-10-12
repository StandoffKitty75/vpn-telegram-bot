from aiogram import Router, F, Bot
from aiogram.types import Message

router = Router()

# 🎯 Настройки
SOURCE_CHANNEL_ID = -1002633016359
TARGET_GROUP_ID = -1003170930613
LOG_GROUP_ID = -1003170930613


async def forward_channel_post(message: Message, bot: Bot):
    """Пересылает пост из канала в группу (только обработка ошибок)."""
    try:
        # Просто пересылаем пост без каких-либо логов
        await message.forward(chat_id=TARGET_GROUP_ID)

    except Exception as e:
        # При ошибке отправляем лог в группу
        await bot.send_message(
            chat_id=LOG_GROUP_ID,
            text=f"❌ Ошибка при пересылке поста:\n`{e}`",
            parse_mode="Markdown"
        )


@router.channel_post()
@router.message()
async def handle_all_posts(message: Message, bot: Bot):
    """Обрабатывает все сообщения и посты"""

    # Если сообщение из нужного канала
    if message.chat.id == SOURCE_CHANNEL_ID:
        await forward_channel_post(message, bot)
from aiogram import Router, F, Bot
from aiogram.types import Message

router = Router()

# 🎯 Настройки
SOURCE_CHANNEL_ID = -1002633016359  # <-- ID канала, откуда брать посты
TARGET_GROUP_ID = -1003170930613    # <-- ID группы, куда пересылать посты
LOG_GROUP_ID = -1003170930613       # <-- ID группы/чата, куда писать логи (можно ту же)

@router.message(F.chat.id == SOURCE_CHANNEL_ID)
async def forward_channel_post(message: Message, bot: Bot):
    """Пересылает пост из канала в группу и пишет лог."""
    try:
        # Пересылаем пост
        forwarded = await message.forward(chat_id=TARGET_GROUP_ID)
        # Отправляем лог
        await bot.send_message(
            chat_id=LOG_GROUP_ID,
            text=(
                f"✅ Новый пост переслан!\n"
                f"• Из канала: `{SOURCE_CHANNEL_ID}`\n"
                f"• В группу: `{TARGET_GROUP_ID}`\n"
                f"• ID сообщения: `{forwarded.message_id}`"
            ),
            parse_mode="Markdown"
        )
    except Exception as e:
        # Если ошибка — отправляем лог об ошибке
        await bot.send_message(
            chat_id=LOG_GROUP_ID,
            text=f"❌ Ошибка при пересылке поста:\n`{e}`",
            parse_mode="Markdown"
        )

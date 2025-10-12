from aiogram import Router, F, Bot
from aiogram.types import Message

router = Router()

# 🎯 Настройки
SOURCE_CHANNEL_ID = -1002633016359
TARGET_GROUP_ID = -1003170930613
LOG_GROUP_ID = -1003170930613


async def forward_channel_post(message: Message, bot: Bot):
    """Пересылает пост из канала в группу и пишет лог."""
    try:
        print(f"Получено сообщение из канала: {message.message_id}")

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
        print(f"Ошибка: {e}")
        await bot.send_message(
            chat_id=LOG_GROUP_ID,
            text=f"❌ Ошибка при пересылке поста:\n`{e}`",
            parse_mode="Markdown"
        )


@router.channel_post()
@router.message()
async def handle_all_posts(message: Message, bot: Bot):
    """Обрабатывает все сообщения и посты"""

    # Логируем все входящие сообщения для дебага
    chat_info = f"Чат: {message.chat.id} (тип: {message.chat.type}, название: {getattr(message.chat, 'title', 'нет')})"
    message_type = "channel_post" if message.chat.type == "channel" else "message"
    print(f"Получено {message_type}: {chat_info}")
    print(f"ID сообщения: {message.message_id}")

    # Если сообщение из нужного канала
    if message.chat.id == SOURCE_CHANNEL_ID:
        print(f"Найдено сообщение из исходного канала! Пересылаем...")
        await forward_channel_post(message, bot)
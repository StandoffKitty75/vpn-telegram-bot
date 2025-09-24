import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import start, language, subscription, platform, back, generate_key

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Подключаем все роутеры
    dp.include_router(start.router)
    dp.include_router(language.router)
    dp.include_router(subscription.router)
    dp.include_router(platform.router)
    dp.include_router(back.router)   # подключили back
    dp.include_router(generate_key.router)  # Добавляем роутер для генерации ключей

    # Регистрируем хендлеры
    start.register_handlers(start.router)
    language.register_handlers(language.router)
    subscription.register_handlers(subscription.router)
    platform.register_handlers(platform.router)
    back.register_handlers(back.router)

    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

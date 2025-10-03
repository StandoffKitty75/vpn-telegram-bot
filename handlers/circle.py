# handlers/circle.py

import os
import tempfile
import subprocess
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionSender

router = Router()

user_circle_mode = set()


@router.message(Command("circle"))
async def cmd_circle(message: Message):
    user_circle_mode.add(message.from_user.id)
    await message.answer("Теперь пришли мне видео, и я сделаю из него кружочек 🎥")


@router.message(F.video)
async def handle_video(message: Message):
    user_id = message.from_user.id

    if user_id not in user_circle_mode:
        await message.answer("Сначала используй команду /circle.")
        return

    # Создаем временную папку для файлов
    with tempfile.TemporaryDirectory() as tmp_dir:
        try:
            # Получаем путь к файлу на серверах Telegram
            file = await message.bot.get_file(message.video.file_id)
            input_path = os.path.join(tmp_dir, "input.mp4")

            # Скачиваем файл локально
            await message.bot.download_file(file.file_path, destination=input_path)

            output_path = os.path.join(tmp_dir, "output.mp4")

            # Запускаем ffmpeg для конвертации в квадратное видео с нужными параметрами
            ffmpeg_cmd = [
                "ffmpeg",
                "-i", input_path,
                "-vf", "scale=640:640:force_original_aspect_ratio=decrease,pad=640:640:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
                "-c:v", "libx264",
                "-profile:v", "baseline",
                "-level", "3.0",
                #"-an",  # отключаем аудио
                "-movflags", "+faststart",
                output_path
            ]

            process = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)

            if process.returncode != 0:
                error_msg = f"Ошибка при обработке видео ffmpeg:\n{process.stderr}"
                await message.answer(error_msg)
                user_circle_mode.discard(user_id)
                return

            # Отправляем чат-экшен "загрузка кружка"
            async with ChatActionSender.upload_video_note(chat_id=message.chat.id, bot=message.bot):
                video_note_file = FSInputFile(output_path)
                await message.bot.send_video_note(
                    chat_id=message.chat.id,
                    video_note=video_note_file,
                    length=360
                )

            print(f"Video note sent for user {user_id}")

        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")

        finally:
            user_circle_mode.discard(user_id)


@router.message(F.video_note)
async def handle_video_note(message: Message):
    await message.answer("Это уже кружочек 😉 Пришли обычное видео после команды /circle.")
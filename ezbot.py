import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Инициализация бота и диспетчера
bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    await message.answer(
        'Привет! Я простой эхо-бот.\n'
        'Отправь мне команду /echo и текст, который нужно повторить.\n'
        'Или просто напиши мне что-нибудь, и я отвечу!'
    )

@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    await message.answer(
        'Доступные команды:\n'
        '/start - Начать работу\n'
        '/help - Показать справку\n'
        '/echo [текст] - Повторить текст\n\n'
        'Также я отвечаю на любые текстовые сообщения!'
    )

@dp.message(Command("echo"))
async def cmd_echo(message: Message):
    """Обработчик команды /echo"""
    # Получаем текст после команды /echo
    text = message.text.replace('/echo', '').strip()
    
    if text:
        await message.answer(f"Эхо: {text}")
    else:
        await message.answer(
            "Пожалуйста, укажите текст после команды /echo.\n"
            "Пример: /echo Привет, мир!"
        )

@dp.message(F.text)
async def handle_text(message: Message):
    """Обработчик текстовых сообщений"""
    # Получаем текст сообщения
    text = message.text
    
    # Отправляем ответ
    await message.answer(
        f"Вы написали: {text}\n\n"
        "Я получил ваше сообщение! Используйте /help для просмотра доступных команд."
    )

async def main():
    """Основная функция запуска бота"""
    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

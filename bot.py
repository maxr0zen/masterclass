import os
import logging
import json
import requests
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Конфигурация OpenRouter
AI_TOKEN = os.getenv('AI_TOKEN')
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "anthropic/claude-3-opus:beta"  # Можно изменить на другую модель
MAX_TOKENS = 500  # Ограничение на количество токенов

# Инициализация бота и диспетчера
bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
dp = Dispatcher()




@dp.message(F.text)
async def handle_message(message: Message):
    """Обработчик текстовых сообщений"""
    try:
        # Получаем сообщение от пользователя
        user_message = message.text
        
        # Отправляем запрос к OpenRouter
        headers = {
            "Authorization": f"Bearer {AI_TOKEN}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/your-repo",  # Замените на ваш репозиторий
            "X-Title": "Telegram Bot"  # Название вашего приложения
        }
        
        data = {
            "model": DEFAULT_MODEL,
            "messages": [
                {"role": "system", "content": "Вы - полезный ассистент."},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": MAX_TOKENS  # Ограничиваем количество токенов
        }
        
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            ai_response = response.json()['choices'][0]['message']['content']
            
            max_length = 4000
            for i in range(0, len(ai_response), max_length):
                chunk = ai_response[i:i + max_length]
                await message.answer(chunk)
                
        else:
            logging.error(f"Ошибка API: {response.status_code} - {response.text}")
            await message.answer(
                "Извините, произошла ошибка при обработке вашего сообщения."
            )
        
    except Exception as e:
        logging.error(f"Ошибка при обработке сообщения: {e}")
        await message.answer(
            "Извините, произошла ошибка при обработке вашего сообщения."
        )

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main()) 
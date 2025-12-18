import asyncio
import logging
import random
from datetime import datetime
from typing import Optional

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = 'BOT_TOKEN'

# Смайлики для команды "смайл"
SMILEYS = ['😀', '😂', '🤣', '😊', '😍', '🤔', '😎', '🥳', '🤖', '👾', '💀', '👻', '🎃', '💩', '👋', '🤘', '👍', '👏']

# Секретные пасхалки (бот не будет о них говорить)
SECRET_EASTER_EGGS = [
    "секретная пасхалка 1",
    "секретная пасхалка 2",
    "еще одна секретная пасхалка"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    await update.message.reply_text('Привет! Я бот для исправления ошибок.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка текстовых сообщений"""
    text = update.message.text
    
    # Проверка на секретные пасхалки (бот не будет о них говорить)
    if any(egg.lower() in text.lower() for egg in SECRET_EASTER_EGGS):
        return
    
    # Обработка разных команд
    text_lower = text.lower()
    
    if text_lower in ['mrvasya', 'mrvasyа'] or any(variant in text for variant in ['MrVasya', 'MrVaSyA']):
        await update.message.reply_text('согласен он топ')
    
    elif text == 'ABC1234':
        await animate_alphabet(update, context)
    
    elif text_lower == 'сочини':
        await write_story(update, context)
    
    elif text_lower == 'mrblock':
        await update.message.reply_text('кто это?')
    
    elif text_lower == 'ошибка':
        await animate_error(update, context)
    
    elif text_lower == 'тимер':
        await update.message.reply_text('тимер обыграл тебя в Rivals и построил лучше тебя в Build A Boat')
    
    elif text_lower == 'новые мемы':
        await update.message.reply_text('старые мемы: тролфейс, повар, ты кто такой, где моя сосиска')
    
    elif text_lower == 'timerruner' or text == 'TimerRuner':
        await update.message.reply_text('Вабщета правильно Boom Bim🤓👆')
    
    elif text_lower == 'смайл':
        smiley = random.choice(SMILEYS)
        await update.message.reply_text(smiley)

async def animate_alphabet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Анимация английского алфавита"""
    message = await update.message.reply_text('A')
    
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    for i in range(1, len(alphabet)):
        await asyncio.sleep(0.3)
        try:
            await message.edit_text(alphabet[:i+1])
        except Exception as e:
            logger.error(f"Ошибка при редактировании сообщения: {e}")
            break

async def animate_error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Анимация слова ERROR"""
    message = await update.message.reply_text('E')
    
    error_text = 'ERROR'
    
    for i in range(1, len(error_text)):
        await asyncio.sleep(0.5)
        try:
            await message.edit_text(error_text[:i+1])
        except Exception as e:
            logger.error(f"Ошибка при редактировании сообщения: {e}")
            break

async def write_story(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Сочинение рассказа"""
    stories = [
        "Жил-был в далеком королевстве мудрый дракон. Он не извергал пламя, а вместо этого рассказывал истории. "
        "Каждую ночь жители деревни собирались у его пещеры, чтобы послушать новые сказки. Однажды дракон рассказал "
        "историю о принце, который искал не сокровища, а знания. Принц путешествовал по миру, собирая мудрость "
        "у разных народов, и в конце концов стал самым мудрым правителем, которого когда-либо знало королевство.",
        
        "В маленьком городке, где каждый знал каждого, произошло нечто необычное: книги в библиотеке начали оживать. "
        "Персонажи выходили со страниц и помогали людям решать их проблемы. Шерлок Холмс раскрывал мелкие бытовые "
        "тайны, Д'Артаньян защищал слабых, а Алиса рассказывала детям о чудесах. Город превратился в место, "
        "где магия слов стала реальностью.",
        
        "Давным-давно существовал лес, где деревья могли говорить. Они рассказывали путникам истории о временах, "
        "когда мир был моложе. Одинокий путник по имени Элиас нашел этот лес и провел в нем целый год, записывая "
        "все услышанное. Его дневник стал самой ценной книгой в истории, содержащей мудрость тысячелетий."
    ]
    
    story = random.choice(stories)
    await update.message.reply_text(story)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка ошибок"""
    logger.error(f"Ошибка вызвана {update}: {context.error}")

def main() -> None:
    """Запуск бота"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Регистрируем обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    print("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

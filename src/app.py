from aiogram import Bot, Dispatcher

from config import settings

bot = Bot(settings.BOT_TOKEN)
dp = Dispatcher(bot=bot)
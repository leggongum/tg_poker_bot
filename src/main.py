from aiohttp import web

import asyncio

from config import settings
from app import bot


if __name__ == '__main__':
    from handler import dp
    asyncio.run(dp.start_polling(bot))

'''
#Insted of polling you may use webhook


WEBHOOK_PATH = f'/{settings.BOT_TOKEN}'
WEBHOOK_URL = f"{settings.WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0' 
WEBAPP_PORT = 8000


async def on_startup(dp):
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL)


if __name__ == '__main__':
    from handler import dp

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )

    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)

'''
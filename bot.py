from config import dp, logging, asyncio, bot, file_config
from handlers import routers
from middlewares import setup
import aioschedule as schedule
from apiozon.api import ozon_api
import traceback

async def start_api_bot():  

    while True:
        try:
            await ozon_api.cabinets()
            times = int(file_config['time_pars'])
            await asyncio.sleep(int(times))
        except Exception as ex:
            logging.error(traceback.format_exc())

async def main() -> None:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s" 
                        )
    
    
    dp.include_router(routers)
    task1 = asyncio.create_task(start_api_bot())
    setup(dp)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())
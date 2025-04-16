import asyncio
from bot import bot, dp

from modules import ALL_ROUTERS      

for router in ALL_ROUTERS:
    dp.include_router(router)
    
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

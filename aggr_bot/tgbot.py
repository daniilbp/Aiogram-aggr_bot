import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from driver import get_all_agg_data
from additions.addition import msg_error
from additions.p_conf import API_TOKEN

API_TOKEN = API_TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(msg_error[0])


@dp.message()
async def agg_static_data(message: types.Message):
    ans = await get_all_agg_data(message.text)
    await message.answer(ans)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

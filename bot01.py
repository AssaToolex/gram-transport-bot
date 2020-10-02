"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging

from aiogram import Bot, Dispatcher, executor, types
from bot_config import TELEGRAM_BOT_TOKENs

API_TOKEN = TELEGRAM_BOT_TOKENs["telegram_debug"][0]["token"]

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def get_users():
    """
    Return users list
    In this example returns some random ID's
    """
    yield from (61043901, 78238238, 78378343, 98765431, 12345678)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
    with open('data/cats.jpg', 'rb') as photo:
        '''
        # Old fashioned way:
        await bot.send_photo(
            message.chat.id,
            photo,
            caption='Cats are here 😺',
            reply_to_message_id=message.message_id,
        )
        '''

        await message.reply_photo(photo, caption='Cats are here 😺')


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


# checks specified chat
@dp.message_handler(is_chat_admin=-1001241113577)
async def handle_specified(msg: types.Message):
    await msg.answer("You are an admin of the specified chat!")


# checks multiple chats
@dp.message_handler(is_chat_admin=[-1001241113577, -320463906])
async def handle_multiple(msg: types.Message):
    await msg.answer("You are an admin of multiple chats!")


# checks current chat
@dp.message_handler(is_chat_admin=True)
async def handler3(msg: types.Message):
    await msg.answer("You are an admin of the current chat!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

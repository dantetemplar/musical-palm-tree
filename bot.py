import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.utils import executor

from my_token import TOKEN

# Настройа логгирования
logging.basicConfig(level=logging.INFO)

# Инициализировать бота и задать диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'], state="*")
async def _(message: Message, state: FSMContext):
    await state.update_data({"user_id": message.from_user.id})
    await message.answer("Привет! Напиши мне что-нибудь!")
    # то же самое что и
    # await bot.send_message(message.from_user.id, "Привет! Напиши мне что-нибудь!")
    await state.set_state("wait_for_message")


@dp.message_handler(state="wait_for_message")
async def _(message: Message, state: FSMContext):
    # await message.answer("Спасибо за сообщение!")
    # id_ = message.from_user.id # постоянный для аккаунта
    # message.from_user.username # пользователь может сменить его
    # text = f"@{message.from_user.username} написал(а):\n{message.text}"

    text = \
        f"<a href='tg://user?id={message.from_user.id}'>"\
        f"пользователь</a> написал(а):\n{message.text}"

    await message.answer(text, parse_mode="HTML")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

import logging
from typing import Iterable

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

all_users = set()


@dp.message_handler(commands=['start'], state="*")
async def _(message: Message, state: FSMContext):
    user_id = message.from_id

    # Запоминаем всех пользователей, что нажали /start
    if user_id not in all_users:
        all_users.add(user_id)
        await send_to_users(f"Всего пользователей: {len(all_users)}")

    await state.update_data({"user_id": user_id, "username": message.from_user.username})
    await message.answer("Привет! Напиши мне что-нибудь!")
    # то же самое что и
    # await bot.send_message(message.from_id, "Привет! Напиши мне что-нибудь!")
    await state.set_state("wait_for_message")


async def send_to_users(text, users: Iterable[int] = None, parse_mode=None):
    if users is None:
        users = tuple(all_users)
    else:
        users = tuple(users)

    for user_id in users:
        await bot.send_message(user_id, text, parse_mode=parse_mode)


@dp.message_handler(state="wait_for_message")
async def _(message: Message, state: FSMContext):
    # await message.answer("Спасибо за сообщение!")
    # id_ = message.from_id # постоянный для аккаунта
    # message.from_user.username # пользователь может сменить его
    # text = f"@{message.from_user.username} написал(а):\n{message.text}"

    text = \
        f"<a href='tg://user?id={message.from_id}'>" \
        f"пользователь</a> написал(а):\n{message.text}"
    all_except_me = all_users - {message.from_id}
    await send_to_users(text, users=all_except_me, parse_mode="HTML")

    # await message.answer(text, parse_mode="HTML")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

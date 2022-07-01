from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import BOT_TOKEN, MODERATOR_ID, LINK_TO_CHAT

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


class States(StatesGroup):
    user_input = State()
    reason = State()


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    requirements = ["1. Имя", "2. Сколько готовы уделять времени работе", "3. Ссылку на любую соц-сеть",
                    "4. Есть ли опыт в данной сфере"]

    await message.answer(f"Отправьте данные:\n" + "".join(
        [f"{r}\n" for r in requirements]) + "\n\n Эти данные будут отправлены нашим модератором на проверку")

    await States.user_input.set()


@dp.message_handler(state=States.user_input)
async def get_user_input(message: types.Message, state: FSMContext):
    await state.update_data(user_data=message.text)

    state_data = await state.get_data()
    user_data = state_data["user_data"]

    await message.answer("Заявка была отправлена на рассмотрение. Ожидайте...")

    moderator_keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [InlineKeyboardButton("Одобрить", callback_data=f"answer:approve:{message.from_user.id}:{message.from_user.username}")],
        [InlineKeyboardButton("Отклонить", callback_data=f"answer:decline:{message.from_user.id}:{message.from_user.username}")],
    ])
    await bot.send_message(chat_id=MODERATOR_ID,
                           text=f"@{message.from_user.username} [id: {message.from_user.id}]\n\n{user_data}",
                           reply_markup=moderator_keyboard)

    await state.finish()


@dp.callback_query_handler(text_contains="answer")
async def answer(callback_data: types.CallbackQuery):
    _, moderator_answer, user_id, username = callback_data.data.split(":")

    if moderator_answer == "approve":
        await bot.send_message(chat_id=user_id, text="Ваша заявка была одобрена!!!\nСсылка на чат: " + LINK_TO_CHAT)
        await callback_data.message.edit_text(f"Заявка была одобрена: {username} [id: {user_id}]")
    else:
        await bot.send_message(chat_id=user_id, text="Ваша заявка была отклонена :(")
        await callback_data.message.edit_text(f"Заявка была отклонена: {username} [id: {user_id}]")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

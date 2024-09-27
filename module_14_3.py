import asyncio
from config import TOKEN
from aiogram import Bot, Dispatcher, Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Рассчитать'),
                                    KeyboardButton(text='Информация'),
                                    KeyboardButton(text='Купить')]], resize_keyboard=True)
inl_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Рассчитать норму калорий',
                                                                     callback_data='calories'),
                                                InlineKeyboardButton(text='Формулы расчета',
                                                                     callback_data='formulas')]])
inl_kb2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='5w20',
                                                                      callback_data='product_buying'),
                                                InlineKeyboardButton(text='10w30',
                                                                     callback_data='product_buying'),
                                                InlineKeyboardButton(text='10w40_plus',
                                                                     callback_data='product_buying'),
                                                InlineKeyboardButton(text='lpg_10w40',
                                                                     callback_data='product_buying')]])


class UsesState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@router.message(CommandStart())
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@router.message(F.text == 'Информация')
async def info(message):
    await message.answer('Информация:\nЭто учебный бот университета Urban. Он помогает твоему'
                         'здоровью!')


@router.message(F.text == 'Купить')
async def get_buying_list(message):
    await message.answer('Название: 5w20 | Описание: maxima_5w20_5l | Цена: 100')
    await message.answer_photo(photo=FSInputFile("maxima_5w20_5l.jpg"))
    await message.answer('Название: 10w30 | Описание: maxima_10w30_5l | Цена: 200')
    await message.answer_photo(photo=FSInputFile("maxima_10w30_5l.jpg"))
    await message.answer('Название: 10w40_plus | Описание: maxima_10w40_plus_5l | Цена: 300')
    await message.answer_photo(photo=FSInputFile("maxima_10w40_plus_5l.jpg"))
    await message.answer('Название: auto_lpg_10w40 | Описание: maxima_auto_lpg_10w40_4l | Цена: 400')
    await message.answer_photo(photo=FSInputFile("maxima_auto_lpg_10w40_4l.jpg"))
    await message.answer('Выберите продукт для покупки:', reply_markup=inl_kb2)


@router.message(F.text == 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=inl_kb)


@router.callback_query(F.data == 'product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@router.callback_query(F.data == 'formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


@router.callback_query(F.data == 'calories')
async def set_age(call, state: FSMContext):
    await state.set_state(UsesState.age)
    await call.message.answer('Введите свой возраст:')
    await call.answer()


@router.message(UsesState.age)
async def set_growth(message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(UsesState.growth)
    await message.answer('Введите свой рост:')


@router.message(UsesState.growth)
async def set_weight(message, state: FSMContext):
    await state.update_data(growth=message.text)
    await state.set_state(UsesState.weight)
    await message.answer('Введите свой вес:')


@router.message(UsesState.weight)
async def send_calories(message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    a = int(data['age'])
    g = int(data['growth'])
    w = int(data['weight'])
    res = 10 * w + 6.25 * g - 5 * a + 5
    await message.answer(f'Ваша норма: {res} ккал/сутки')
    await state.clear()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')

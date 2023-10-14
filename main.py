import logging
import os

from aiogram import types, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import MediaGroup
from aiogram.utils.executor import start_webhook

from markups.inline_markups import *
from markups.reply_markups_start_and_back import *
from messages import *
from states import ProfileStatesGroup

storage = MemoryStorage()
TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)

dp = Dispatcher(bot,
                storage=storage)


CHANNEL_ID = -1001960789131

@dp.message_handler(commands=['start'], state='*')
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text="Саламатсызбы!\n\nСиз менен 'Dream_Card' командасы. Ар жыл сайын green card лотореясына катышууга жардам бере турган биринчи онлайн сервиси. Эгерде Сиз Америкага учууну кыялданып жатсаңыз жана дал ошол кыялыңыз орундалуусун каласаңыз, анда биз Сизге жардам беребиз.\n\nЭгерде Сиз даяр болсоңуз, жаныңызга керек документтериңизди алып, start баскычын басыңыз. Кеттик!\n\n"
                           "Здравствуйте!\n\nВас приветствует команда 'Dream_Card'. Первый онлайн помощник по заполнению заявки для участия в ежегодной лотерее green card. Если Вы желаете осуществить свою американскую мечту и наконец-то полететь в Америку, то мы с удовольствием поможем Вам в этом.\n\nЕсли вы готовы, то нажмите кнопку start и подготовьте заранее все необходимые документы. Поехали!\n\n"
                           "Salom!\n\n'Dream_Card' jamoasi sizni qo'llab-quvvatlaydi. Yillik 'Green Card' lotereyasida ishtirok etish va ariza to'ldirish uchun birinchi onlayn yordamchi. Agar siz orzuingizni ro'yobga chiqarmoqchi bo'lsangiz va nihoyat Amerikaga uchib ketmoqchi bo'lsangiz, biz sizga bu borada yordam berishdan xursand bo'lamiz.\n\nAgar tayyor bo'lsangiz, unda boshlash tugmasini bosing va barcha kerakli hujjatlarni oldindan tayyorlang."
                                ,
                           reply_markup=country_kb())
    await ProfileStatesGroup.country.set()



@dp.message_handler(content_types=[*types.ContentTypes.TEXT], state=ProfileStatesGroup.country)
async def load_it_info(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['country'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                        text="Выберите язык", reply_markup=lang_kb())
    await ProfileStatesGroup.language.set()


@dp.message_handler(content_types=[*types.ContentTypes.TEXT], state=ProfileStatesGroup.language)
async def load_it_info(message: types.Message, state: FSMContext) -> None:
    try:
        async with state.proxy() as data:
            data['lang'] = message.text
        await bot.send_message(chat_id=message.from_user.id,
                               text=lang_dict['passport'][data['lang']],
                               reply_markup=get_start_and_back_kb())
        await ProfileStatesGroup.passport1.set()
    except(KeyError):
        await bot.send_message(chat_id=message.from_user.id,
                               text="Выберите вариант кнопкой")



@dp.message_handler(content_types=types.ContentTypes.ANY, state=ProfileStatesGroup.passport1)
async def load_it_info(message: types.Message, state: FSMContext) -> None:
    if message.text == "🔙":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Выберите язык", reply_markup=lang_kb())
        await ProfileStatesGroup.language.set()

    if message.photo or message.document:
        file_info = message.document or message.photo
        async with state.proxy() as data:
            data['passport'] = file_info.file_id
        await bot.send_message(chat_id=message.from_user.id,
                               text=lang_dict['zagran'][data['lang']],
                               reply_markup=get_start_and_back_kb())
        await ProfileStatesGroup.zagran.set()



@dp.message_handler(content_types=['photo'], state=ProfileStatesGroup.zagran)
async def load_it_info(message: types.Message, state: FSMContext) -> None:
    if message.text == "🔙":
        async with state.proxy() as data:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['passport'][data['lang']], reply_markup=get_start_and_back_kb())
        await ProfileStatesGroup.passport1.set()
    if message.photo:
        async with state.proxy() as data:
            data['zagran'] = message.photo[0].file_id
        await bot.send_message(chat_id=message.from_user.id,
                               text=lang_dict['photo'][data['lang']],
                               reply_markup=get_start_and_back_kb())
        media = MediaGroup()
        media.attach_photo(types.InputFile('photo/Нигер1.jpg'))
        media.attach_photo(types.InputFile('photo/Нигер2.jpg'))
        media.attach_photo(types.InputFile('photo/Нигер3.jpg'))
        media.attach_photo(types.InputFile('photo/Белый1.jpg'))
        media.attach_photo(types.InputFile('photo/Белый2.jpg'))
        media.attach_photo(types.InputFile('photo/Белый3.jpg'))
        media.attach_photo(types.InputFile('photo/Жёлтый1.jpg'))
        media.attach_photo(types.InputFile('photo/Коричневый1.jpg'))
        await bot.send_media_group(chat_id=message.from_user.id, media=media)
        await ProfileStatesGroup.photo.set()


@dp.message_handler(content_types=['photo'], state=ProfileStatesGroup.photo)
async def load_it_info(message: types.Message, state: FSMContext) -> None:
    if message.text == "🔙":
        async with state.proxy() as data:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['zagran'][data['lang']], reply_markup=get_start_and_back_kb())
        await ProfileStatesGroup.zagran.set()
    if message.photo:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await bot.send_message(chat_id=message.from_user.id,
                               text=lang_dict['country'][data['lang']],
                               reply_markup=get_start_and_back_kb())
        await ProfileStatesGroup.contry_where_born.set()


@dp.message_handler(content_types=[*types.ContentTypes.TEXT], state=ProfileStatesGroup.contry_where_born)
async def load_it_info(message: types.Message, state: FSMContext) -> None:
    if message.text == "🔙":
        async with state.proxy() as data:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['photo'][data['lang']], reply_markup=get_start_and_back_kb())
        await ProfileStatesGroup.photo.set()
    else:
        async with state.proxy() as data:
            data['country_where_born'] = message.text

        await bot.send_message(chat_id=message.from_user.id,
                               text=lang_dict['town'][data['lang']],
                               reply_markup=get_start_and_back_kb())
        await ProfileStatesGroup.town_where_born.set()


@dp.message_handler(content_types=[*types.ContentTypes.TEXT], state=ProfileStatesGroup.town_where_born)
async def load_it_info(message: types.Message, state: FSMContext) -> None:
    if message.text == "🔙":
        async with state.proxy() as data:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['country'][data['lang']], reply_markup=get_start_and_back_kb())
        await ProfileStatesGroup.contry_where_born.set()
    else:
        async with state.proxy() as data:
            data['town_where_born'] = message.text

        await bot.send_message(chat_id=message.from_user.id,
                               text=lang_dict['green_country'][data['lang']],
                               reply_markup=get_start_and_back_kb())
        await ProfileStatesGroup.contry_where_green.set()


@dp.message_handler(content_types=[*types.ContentTypes.TEXT], state=ProfileStatesGroup.contry_where_green)
async def load_it_info(message: types.Message, state: FSMContext) -> None:
    if message.text == "🔙":
        async with state.proxy() as data:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['town'][data['lang']], reply_markup=get_start_and_back_kb())
        await ProfileStatesGroup.town_where_born.set()
    else:
        async with state.proxy() as data:
            data['country_where_green'] = message.text
        await bot.send_message(chat_id=message.from_user.id,
                               text=lang_dict['address'][data['lang']],
                               reply_markup=get_start_and_back_kb())
        await ProfileStatesGroup.address.set()


@dp.message_handler(content_types=[*types.ContentTypes.TEXT], state=ProfileStatesGroup.address)
async def load_it_info(message: types.Message, state: FSMContext) -> None:
    if message.text == "🔙":
        async with state.proxy() as data:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['green_country'][data['lang']], reply_markup=get_start_and_back_kb())
        await ProfileStatesGroup.contry_where_green.set()
    else:
        async with state.proxy() as data:
            data['address'] = message.text
        await bot.send_message(chat_id=message.from_user.id,
                               text=lang_dict['email'][data['lang']],
                               reply_markup=get_start_and_back_kb())
        await ProfileStatesGroup.email.set()

@dp.message_handler(content_types=[*types.ContentTypes.TEXT], state=ProfileStatesGroup.email)
async def load_it_info(message: types.Message, state: FSMContext) -> None:
    if message.text == "🔙":
        async with state.proxy() as data:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['address'][data['lang']], reply_markup=get_start_and_back_kb())
        await ProfileStatesGroup.address.set()
    else:
        async with state.proxy() as data:
            data['email'] = message.text
            def get_education_kb() -> InlineKeyboardMarkup:
                ked = InlineKeyboardMarkup(resize_keyboard=True)
                b1 = InlineKeyboardButton(text=lang_dict['begin_school'][data['lang']], callback_data='Начальная школа')
                b2 = InlineKeyboardButton(text=lang_dict['middle'][data['lang']],
                                          callback_data='Среднее')
                b3 = InlineKeyboardButton(text=lang_dict['middle_special'][data['lang']], callback_data='Среднее спец.')
                b4 = InlineKeyboardButton(text=lang_dict['incomplete_high'][data['lang']],
                                          callback_data='Бакалавр')
                b5 = InlineKeyboardButton(text=lang_dict['complete_high'][data['lang']],
                                          callback_data='Магистр')
                b6 = InlineKeyboardButton(text=lang_dict['doctor'][data['lang']],
                                          callback_data='Доктор')
                b7 = InlineKeyboardButton(text=lang_dict['back'][data['lang']], callback_data='Назад')
                ked.add(b1).add(b2).add(b3).add(b4).add(b5).add(b6).add(b7)
                return ked

        await bot.send_message(chat_id=message.from_user.id,
                               text=lang_dict['education_level'][data['lang']],
                               reply_markup=get_education_kb())
        await ProfileStatesGroup.education.set()


@dp.message_handler(content_types=[*types.ContentTypes.TEXT], state=ProfileStatesGroup.ch_number)
async def load_it_info(message: types.Message, state: FSMContext) -> None:
    if message.text == "🔙":
        async with state.proxy() as data:
            def get_fam_status_kb() -> InlineKeyboardMarkup:
                kst = InlineKeyboardMarkup(resize_keyboard=True)
                b1 = InlineKeyboardButton(text=lang_dict['unmarried'][data['lang']], callback_data='not married')
                b2 = InlineKeyboardButton(text=lang_dict['married_on_citizen'][data['lang']],
                                          callback_data='married(USA)')
                b3 = InlineKeyboardButton(text=lang_dict['married_not_on_citizen'][data['lang']], callback_data='married(not USA)')
                b4 = InlineKeyboardButton(text=lang_dict['divorced'][data['lang']],
                                          callback_data='Divorced')
                b5 = InlineKeyboardButton(text=lang_dict['widowed'][data['lang']],
                                          callback_data='Widowed')
                b6 = InlineKeyboardButton(text=lang_dict['back'][data['lang']], callback_data='Назад')
                kst.add(b1).add(b2).add(b3).add(b4).add(b5).add(b6)
                return kst

            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['family_status'][data['lang']], reply_markup=get_fam_status_kb())
        await ProfileStatesGroup.family_status.set()
    else:
        async with state.proxy() as data:
            data['ch_number'] = message.text

        offerta_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton(lang_dict['send_contact'][data['lang']], request_contact=True)
        offerta_menu.row(btn1)
        await bot.send_message(chat_id=message.from_user.id,
                               text=lang_dict['phone_number_text'][data['lang']],
                               reply_markup=offerta_menu)
        await ProfileStatesGroup.phone_number.set()


@dp.message_handler(content_types=['contact'], state=ProfileStatesGroup.phone_number)
async def load_it_info(message: types.Message, state: FSMContext) -> None:
    try:
        async with state.proxy() as data:
            if message.contact is not None:
                data['phone_number'] = message.contact.phone_number
                await bot.send_message(chat_id=message.from_user.id,
                                       text=lang_dict['thank_you'][data['lang']])
                await bot.send_message(chat_id=message.from_user.id,
                                       text=lang_dict['telegram'][data['lang']],
                                       reply_markup=get_start_kb())

                media = MediaGroup()
                #media.attach_photo(photo=data['passport'])
                media.attach_photo(photo=data['zagran'])
                media.attach_photo(photo=data['photo'], caption=f"Выбранный язык:{data['lang']}\n"
                                                                f"Выбранная страна: {data['country']}\n"
                                                                f"Страна где родился: {data['country_where_born']}\n"
                                                                f"Город где родился: {data['town_where_born']}\n"
                                                                f"Страна от которой подаётся гринкарта: {data['country_where_green']}\n"
                                                                f"Адрес: {data['address']}\n"
                                                                f"Email: {data['email']}\n"
                                                                f"Уровень образования: {data['edu']}\n"
                                                                f"Семейное положение: {data['fam_status']}\n"
                                                                f"Количество детей: {data['ch_number']}\n"
                                                                f"Номер телефона: {data['phone_number']}")
                await bot.send_media_group(CHANNEL_ID, media=media)
                await bot.send_document(chat_id=CHANNEL_ID,
                                        document=data['passport1'])
                await state.finish()
    except KeyError:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Выберите вариант кнопкой!")





@dp.callback_query_handler(state=ProfileStatesGroup.education)
async def edu_keyboard(callback_query: types.CallbackQuery, state: FSMContext):
    if (
            callback_query.data == 'Начальная школа' or callback_query.data == 'Среднее' or callback_query.data == 'Среднее спец.' or
            callback_query.data == 'Бакалавр' or callback_query.data == 'Магистр' or callback_query.data == 'Доктор'):
        async with state.proxy() as data:
            data['edu'] = callback_query.data

            def get_fam_status_kb() -> InlineKeyboardMarkup:
                kst = InlineKeyboardMarkup(resize_keyboard=True)
                b1 = InlineKeyboardButton(text=lang_dict['unmarried'][data['lang']], callback_data='not married')
                b2 = InlineKeyboardButton(text=lang_dict['married_on_citizen'][data['lang']],
                                          callback_data='married(USA)')
                b3 = InlineKeyboardButton(text=lang_dict['married_not_on_citizen'][data['lang']], callback_data='married(not USA)')
                b4 = InlineKeyboardButton(text=lang_dict['divorced'][data['lang']],
                                          callback_data='Divorced')
                b5 = InlineKeyboardButton(text=lang_dict['widowed'][data['lang']],
                                          callback_data='Widowed')
                b6 = InlineKeyboardButton(text=lang_dict['back'][data['lang']], callback_data='Назад')
                kst.add(b1).add(b2).add(b3).add(b4).add(b5).add(b6)
                return kst

        await callback_query.message.delete()
        await bot.send_message(chat_id=callback_query.message.chat.id,
                               text=callback_query.data)
        await bot.send_message(chat_id=callback_query.message.chat.id,
                               text=lang_dict['family_status'][data['lang']],
                               reply_markup=get_fam_status_kb())
        await ProfileStatesGroup.family_status.set()
    if callback_query.data == 'Назад':
        async with state.proxy() as data:
            await callback_query.message.delete()
            await bot.send_message(chat_id=callback_query.message.chat.id,
                                   text=lang_dict['email'][data['lang']],
                                   reply_markup=get_start_and_back_kb())
            await ProfileStatesGroup.email.set()


@dp.callback_query_handler(state=ProfileStatesGroup.family_status)
async def edu_keyboard(callback_query: types.CallbackQuery, state: FSMContext):
    if (
            callback_query.data == 'not married' or callback_query.data == 'married(USA)' or callback_query.data == 'married(not USA)' or
            callback_query.data == 'Divorced' or callback_query.data == 'Widowed'):
        async with state.proxy() as data:
            data['fam_status'] = callback_query.data
        await callback_query.message.delete()
        await bot.send_message(chat_id=callback_query.message.chat.id,
                               text=callback_query.data)
        await bot.send_message(chat_id=callback_query.message.chat.id,
                               text=lang_dict['ch_number'][data['lang']],
                               reply_markup=get_start_and_back_kb())
        await ProfileStatesGroup.ch_number.set()
    if callback_query.data == 'Назад':
        async with state.proxy() as data:
            def get_education_kb() -> InlineKeyboardMarkup:
                ked = InlineKeyboardMarkup(resize_keyboard=True)
                b1 = InlineKeyboardButton(text=lang_dict['begin_school'][data['lang']], callback_data='Начальная школа')
                b2 = InlineKeyboardButton(text=lang_dict['middle'][data['lang']],
                                          callback_data='Среднее')
                b3 = InlineKeyboardButton(text=lang_dict['middle_special'][data['lang']], callback_data='Среднее спец.')
                b4 = InlineKeyboardButton(text=lang_dict['incomplete_high'][data['lang']],
                                          callback_data='Бакалавр')
                b5 = InlineKeyboardButton(text=lang_dict['complete_high'][data['lang']],
                                          callback_data='Магистр')
                b6 = InlineKeyboardButton(text=lang_dict['doctor'][data['lang']],
                                          callback_data='Доктор')
                b7 = InlineKeyboardButton(text=lang_dict['back'][data['lang']], callback_data='Назад')
                ked.add(b1).add(b2).add(b3).add(b4).add(b5).add(b6).add(b7)
                return ked

            await callback_query.message.delete()
            await bot.send_message(chat_id=callback_query.message.chat.id,
                                   text=lang_dict['education_level'][data['lang']],
                                   reply_markup=get_education_kb())
            await ProfileStatesGroup.education.set()


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )

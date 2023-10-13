from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_birthday_kb() -> InlineKeyboardMarkup:
    kbirth = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton('День', callback_data='day')
    b2 = InlineKeyboardButton('Месяц', callback_data='month')
    b3 = InlineKeyboardButton('Год', callback_data='year')
    b4 = InlineKeyboardButton('Назад', callback_data='back_to_surname')
    b5 = InlineKeyboardButton('Отправить', callback_data='send_birth')
    kbirth.add(b1, b2, b3).add(b4, b5)
    return kbirth



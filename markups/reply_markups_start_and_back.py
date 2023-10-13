from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def country_kb() -> ReplyKeyboardMarkup:
    kcountry = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton('Узбекистан')
    b2 = KeyboardButton('Кыргызстан')
    b3 = KeyboardButton('Россия')
    b4 = KeyboardButton('Казахстан')
    kcountry.add(b1, b2).add(b3, b4)
    return kcountry


def lang_kb() -> ReplyKeyboardMarkup:
    lang = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton('Русский 🇷🇺')
    b2 = KeyboardButton('Узбекский 🇺🇿')
    b3 = KeyboardButton('Кыргызский 🇰🇬')
    lang.add(b1, b2, b3)
    return lang


def get_start_and_back_kb() -> ReplyKeyboardMarkup:
    kmain = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton('🔙')
    b2 = KeyboardButton('/start')
    kmain.add(b1, b2)
    return kmain


def get_start_kb() -> ReplyKeyboardMarkup:
    kmain2 = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton('/start')
    kmain2.add(b1)
    return kmain2
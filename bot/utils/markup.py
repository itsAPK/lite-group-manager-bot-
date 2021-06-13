from pyrogram.types import (KeyboardButton,
                            ReplyKeyboardMarkup,
                            InlineKeyboardButton,
                            InlineKeyboardMarkup,
                            ReplyKeyboardRemove)

from bot.database.models.settings_db import get_buttons


def back_markup():
    cancel = KeyboardButton('🚫 Cancel')
    markup = ReplyKeyboardMarkup([[cancel]], resize_keyboard=True)
    return markup

def empty_markup():
    return ReplyKeyboardRemove()

def promo_button_markup():
    buttons=get_buttons()
    button=[[InlineKeyboardButton(x.name,url=x.url),] for x in buttons]
    markup=InlineKeyboardMarkup(button)
    return markup  


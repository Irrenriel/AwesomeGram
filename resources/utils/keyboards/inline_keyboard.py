# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB


# Button Types
def Call(*args):
    return dict(zip(('text', 'callback_data'), args))


def Url(*args):
    return dict(zip(('text', 'url'), args))


# Custom Inline Keyboard Constructor
def InlineKeyboard(*args, row_width: int = 5):
    return IKM(row_width=row_width).add(*(IKB(**l) for l in args))
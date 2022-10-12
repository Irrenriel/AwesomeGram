# -*- coding: utf-8 -*-
from aiogram.types import ReplyKeyboardMarkup as RKM


def ReplyKeyboard(*args: str, resize_keyboard: bool = True, selective: bool = True, row_width: int = 3):
    return RKM(resize_keyboard=resize_keyboard, selective=selective, row_width=row_width).add(*args)

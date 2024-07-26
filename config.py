from aiogram import Bot, Dispatcher, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.types.input_file import FSInputFile
from aiogram.types import FSInputFile
from aiogram.types import (
    KeyboardButton,
    Message,
    Update,
    CallbackQuery,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
import time
import asyncio
from aiogram import types
from aiogram.filters import Filter
import logging
import datetime
import json

bot_config_path = 'config_bot.json'


with open(bot_config_path, 'r+') as file:
    file_config = json.load(file)
    
# TOKEN = '6319367359:AAEgT-4e4esNWcMpQUaCbiCCDbH-uRo7BXI' # ТОКЕН БОТА

CHAT_ID_OZON_SUCCESS = -1002066055266
CHAT_ID_OZON_ERROR = -1002002201784

CHAT_ID_OZON_SUCCESS_4_5 = -1002102697905
CHAT_ID_OZON_ERROR_4_5 = -1002006040996

CHAT_ID_OZON_SUCCESS_1_2_3 = -1002072216527
CHAT_ID_OZON_ERROR_1_2_3 = -1002010052035





dp = Dispatcher(storage=MemoryStorage())
bot = Bot(file_config['bot_token'], parse_mode="html")





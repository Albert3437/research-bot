import time
from modules.config import *
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from modules.logger import logger
from modules.core import start
import asyncio
from modules.collect_data import update_data
from second_part import run

    


class Telegram:
    def __init__(self):
        self.bot = telebot.TeleBot(TELE_TOKEN)
        self.chat_id = TELE_USER_ID
        self.is_run = True

    @logger.catch
    def stop_bot(self):
        self.is_run = False


    @logger.catch
    def send_message(self, message):
        self.bot.send_message(self.chat_id, message)


    @logger.catch
    def handle_messages(self, message):
        text = message.text

        if text == '/start':
            # Создаем клавиатуру с двумя кнопками
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = KeyboardButton(text="Скачать все данные")
            button2 = KeyboardButton(text="Скачать готовый результат")
            button3 = KeyboardButton(text="Обновить данные для анализа")
            button4 = KeyboardButton(text="Второй этап!")
            button5 = KeyboardButton(text="Скачать логгер")
            button6 = KeyboardButton(text="Скачать базу данных")
            keyboard.add(button1, button2, button3, button4, button5, button6)

            # Отправляем сообщение с клавиатурой
            self.bot.send_message(self.chat_id, "Дорова бро, нажав одну кнопочку, через пару суток ты узнаешь о самых эффективных торговых инструментах", reply_markup=keyboard)
        if text == 'Скачать все данные':
            for token in TOKEN_LIST:
                excel_file = open(f'ready_data/{token}.xlsx', 'rb')
                self.bot.send_document(self.chat_id, excel_file)
        if text == 'Скачать готовый результат':
            excel_file = open('analized.xlsx', 'rb')  # Замените на путь к вашему Excel файлу
            self.bot.send_document(self.chat_id, excel_file)
        if text == 'Обновить данные для анализа':
            update_data()
            self.send_message('Данные обновлены!')
        if text == 'Второй этап!':
            run()
            self.send_message('Обработано')
        if text == 'Скачать базу данных':
            excel_file = open('data.db', 'rb')
            self.bot.send_document(self.chat_id, excel_file)
        if text == 'Скачать логгер':
            excel_file = open('debug.log', 'rb')
            self.bot.send_document(self.chat_id, excel_file)
        

    @logger.catch
    def run_bot(self):
        self.bot.message_handler()(self.handle_messages)
        while self.is_run:
            try:
                self.bot.polling(non_stop=True)
            except:
                time.sleep(3)
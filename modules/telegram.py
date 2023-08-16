import time
from modules.config import *
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from modules.logger import logger
from modules.core import start
import asyncio
from modules.collect_data import update_data


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
            button1 = KeyboardButton(text="ЗАПУСТИТЬ!")
            button2 = KeyboardButton(text="Скачать готовый результат")
            button3 = KeyboardButton(text="Обновить данные для анализа")
            keyboard.add(button1, button2, button3)

            # Отправляем сообщение с клавиатурой
            self.bot.send_message(self.chat_id, "Дорова бро, нажав одну кнопочку, через пару суток ты узнаешь о самых эффективных торговых инструментах", reply_markup=keyboard)
        if text == 'ЗАПУСТИТЬ!':
            asyncio.run(start())
            self.send_message('ПОЗДРАВЛЯЮ, спустя несколько суток, это говно наконец-то выполнено')
        if text == 'Скачать готовый результат':
            excel_file = open('analized.xlsx', 'rb')  # Замените на путь к вашему Excel файлу
            self.bot.send_document(self.chat_id, excel_file)
        if text == 'Обновить данные для анализа':
            update_data()
        

    @logger.catch
    def run_bot(self):
        self.bot.message_handler()(self.handle_messages)
        while self.is_run:
            try:
                self.bot.polling(non_stop=True)
            except:
                time.sleep(3)
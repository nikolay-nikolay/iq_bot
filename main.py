import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message
from questions import test_questions
from rooms import Rooms

bot = telebot.TeleBot('5526150854:AAErUO40Bor5vKFdAaDdhyLeVaQeSlcJxKw')
rooms = Rooms()

hello_text = 'Привет, я умный IQ-тестбот.\nХочешь пройти тест и узнать свой уровень IQ?'
another_test = 'Хочешь пройти тестирование?'

@bot.message_handler(commands=['start'])
def hello(message: Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton('Начать тестирование'))

    bot.send_message(message.chat.id, hello_text, reply_markup=markup, parse_mode='HTML')

@bot.message_handler(func=lambda message: message.text == 'Начать тестирование')
def start_test(message: Message):
    global bot
    rooms.create(bot, message.chat.id, test_questions)

@bot.message_handler(func=lambda message: message.text == 'Завершить тестирование')
def stop_test(message: Message):
    rooms.remove(message.chat.id)

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton('Начать тестирование'))

    bot.send_message(message.chat.id, another_test, reply_markup=markup, parse_mode='HTML')

@bot.message_handler(func=lambda message: True)
def on_message(message: Message):
    global bot
    result = rooms.on_message(bot, message)

    if not result:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton('Начать тестирование'))

        bot.send_message(message.chat.id, another_test, reply_markup=markup, parse_mode='HTML')

bot.infinity_polling()
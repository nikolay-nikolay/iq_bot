from os import path
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message
from random import sample, shuffle

incorrect_answer = 'Выберите вариант ответа <u>из приведенных вариантов</u> или завершите тестирование.'
iq_result = 'Поздравляю, ты успешно прошел тестирование!\n<b>Твой IQ составляет {0}</b>.'

class Room:
    def __init__(self, chatid: int, questions=[]):
        self.chatid = chatid
        self.iq = 100
        self.question = 0
        self.questions = []

        for i in sample(range(0, len(questions)), 10):
            self.questions.append(questions[i])

        shuffle(self.questions)

    def send_question(self, bot: TeleBot):
        question = self.questions[self.question]
        text = 'Вопрос {0} из {1}.\n\n'.format(self.question + 1, 10)

        if 'text' in question:
            text += question['text']

        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        for answer in question['answers']:
            markup.add(KeyboardButton(answer))

        markup.add(KeyboardButton('Завершить тестирование'))

        if 'image' in question:
            file = open(path.dirname(path.realpath(__file__)) + '/' + question['image'], 'rb')
            bot.send_photo(self.chatid, file, caption=text, reply_markup=markup, parse_mode='HTML')
            return

        bot.send_message(self.chatid, text, reply_markup=markup, parse_mode='HTML')

    def on_message(self, bot: TeleBot, message: Message):
        question = self.questions[self.question]
        text = message.text

        if not text in question['answers'].keys():
            bot.send_message(self.chatid, incorrect_answer, parse_mode='HTML')
            return

        self.iq += question['answers'][text]
        self.question += 1

        if self.question >= len(self.questions):
            bot.send_message(self.chatid, iq_result.format(self.iq), parse_mode='HTML')
            return

        self.send_question(bot)

class Rooms:
    created = {}

    def has(self, chatid: int):
        return chatid in self.created

    def get(self, chatid: int):
        if not chatid in self.created:
            return None

        return self.created[chatid]

    def create(self, bot: TeleBot, chatid: int, questions=[]):
        if self.has(chatid):
            return False

        self.created[chatid] = Room(chatid, questions)
        self.created[chatid].send_question(bot)

        return True

    def remove(self, chatid: int):
        if not self.has(chatid):
            return False

        self.created.pop(chatid, None)

        return True

    def on_message(self, bot: TeleBot, message: Message):
        chatid = message.chat.id

        if not self.has(chatid):
            return False

        room = self.get(chatid)
        room.on_message(bot, message)

        if room.question >= len(room.questions):
            self.remove(chatid)
            return False

        return True







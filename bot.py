import datetime

import pytz
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, PicklePersistence
import telegram.error
import os


def status_reminders_are_running(context: CallbackContext):
    with open('/home/udin76/chat_list/chat_list.txt', 'r', encoding='utf8') as f:
        chat_list = f.readlines()
        for chat_id in chat_list:
            try:
                context.bot.send_message(chat_id=chat_id,
                                         text='Напоминания о статусах запущены')
            except telegram.error.BadRequest:
                pass


def remind_about_status(context: CallbackContext):
    with open('/home/udin76/chat_list/chat_list.txt', 'r', encoding='utf8') as f:
        chat_list = f.readlines()
        for chat_id in chat_list:
            try:
                context.bot.send_message(chat_id=chat_id, text='Не забудьте написать о выполненных задачах')
            except telegram.error.BadRequest:
                pass


def add_chat_id_in_chat_list(update: Update, context: CallbackContext):
    with open(f'/home/udin76/chat_list/chat_list.txt', 'a+', encoding='utf8') as f:
        pass

    with open('/home/udin76/chat_list/chat_list.txt', 'r', encoding='utf8') as f:
        chat_list = []
        for chat_id in f:
            chat_list.append(int(chat_id.strip()))

    if update.message.chat_id not in chat_list:
        with open('/home/udin76/chat_list/chat_list.txt', 'a', encoding='utf8') as f:
            print(update.message.chat_id, file=f)


def get_chat_members(update: Update, context: CallbackContext):
    with open(f'/home/udin76/chat_members/chat_members{update.message.chat_id}.txt', 'a+',
            encoding='utf8') as f:
        pass

    with open(f'/home/udin76/chat_members/chat_members{update.message.chat_id}.txt', 'r',
                encoding='utf8') as f:
        chat_members = []
        for user_name in f:
            chat_members.append(str(user_name.strip()))

    if update.effective_user.name not in chat_members:
        with open(f'/home/udin76/chat_members/chat_members{update.message.chat_id}.txt', 'a',
                encoding='utf8') as f:
            print(update.effective_user.name, file=f)


def get_responded_members(update: Update, context: CallbackContext):
    with open(f'/home/udin76/responded_members/responded_members{update.message.chat_id}.txt', 'a+',
            encoding='utf8') as f:
        pass

    with open(f'/home/udin76/responded_members/responded_members{update.message.chat_id}.txt', 'r',
                encoding='utf8') as f:
        responded_members = []
        for user_name in f:
            responded_members.append(str(user_name.strip()))

    if update.effective_user.name not in responded_members:
        with open(f'/home/udin76/responded_members/responded_members{update.message.chat_id}.txt', 'a',
                    encoding='utf8') as f:
            print(update.effective_user.name, file=f)

    def send_praise_to_chat(context: CallbackContext):
        with open(f'/home/udin76/responded_members/responded_members{update.message.chat_id}.txt', 'r', encoding='utf8') as f:
            responded_members = []
            for user_name in f:
                responded_members.append(user_name.strip())
        number_of_responded_members = len(list(filter(None, responded_members)))

        with open(f'/home/udin76/chat_members/chat_members{update.message.chat_id}.txt', 'r', encoding='utf8') as f:
            chat_members = []
            for user_name in f:
                chat_members.append(user_name.strip())
        number_of_chat_members = len(list(filter(None, chat_members)))

        if number_of_responded_members == number_of_chat_members:
            context.bot.send_message(chat_id=update.message.chat_id,
                                         text='Все ответили! Молодцы!')

    context.job_queue.run_daily(send_praise_to_chat, time=datetime.time(17, 56,
                                                                            tzinfo=pytz.timezone('Europe/Moscow')),
                                    days=tuple(range(0, 5)))

    def remind_about_missed_persons(context: CallbackContext):
        with open(f'/home/udin76/responded_members/responded_members{update.message.chat_id}.txt', 'r',
                  encoding='utf8') as f:
            responded_members = f.readlines()

        with open(f'/home/udin76/chat_members/chat_members{update.message.chat_id}.txt', 'r',
                  encoding='utf8') as f:
            chat_members = f.readlines()

        for user_name in chat_members:
            if user_name not in responded_members:
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=f'Не направлен стaтус от {user_name}')
    context.job_queue.run_daily(remind_about_missed_persons, time=datetime.time(13, 25,
                                tzinfo=pytz.timezone('Europe/Moscow')), days=tuple(range(0, 5)))


persistence = PicklePersistence(filename='persistent_storage.pkl')

updater = Updater('2115574444:AAHL5eyZCEjkQRn4FILqYdXvhR4UJp76Ih0', persistence=persistence, use_context=True)

updater.dispatcher.add_handler(CommandHandler('register', add_chat_id_in_chat_list))

updater.dispatcher.add_handler(CommandHandler('run', get_chat_members))
updater.dispatcher.add_handler(MessageHandler(Filters.text, get_responded_members))


updater.job_queue.run_daily(status_reminders_are_running, time=datetime.time(9, 0, tzinfo=pytz.timezone('Europe/Moscow')),
                            days=tuple(range(0, 5)))
updater.job_queue.run_daily(remind_about_status, time=datetime.time(10, 0, tzinfo=pytz.timezone('Europe/Moscow')),
                            days=tuple(range(0, 5)))

updater.start_polling()
updater.idle()

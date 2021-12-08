import datetime

import pytz
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, PicklePersistence
import telegram.error
import os


def status_reminders_are_running(context: CallbackContext):
    with open('flow_daily_bot/chat_list.txt', 'r', encoding='utf8') as f:
        chat_list = f.readlines()
        for chat_id in chat_list:
            try:
                context.bot.send_message(chat_id=chat_id,
                                         text='Напоминания о статусах запущены')
            except telegram.error.BadRequest:
                pass


def remind_about_status(context: CallbackContext):
    with open('flow_daily_bot/chat_list.txt', 'r', encoding='utf8') as f:
        chat_list = f.readlines()
        for chat_id in chat_list:
            try:
                context.bot.send_message(chat_id=chat_id, text='Не забудьте написать о выполненных задачах')
            except telegram.error.BadRequest:
                pass


def add_chat_id_in_chat_list(update: Update, context: CallbackContext):
    with open('flow_daily_bot/chat_list.txt', 'r', encoding='utf8') as f:
        current_chat = update.message.chat_id
        chat_list = []
        for chat_id in f:
            chat_list.append(int(chat_id.strip()))
    if current_chat not in chat_list:
        with open('flow_daily_bot/chat_list.txt', 'a', encoding='utf8') as f:
            print(current_chat, file=f)


def get_chat_members(update: Update, context: CallbackContext):
    with open(f'flow_daily_bot/chat_members/chat_members{update.message.chat_id}.txt', 'a+', encoding='utf8') as f:
        print(update.effective_user.name, file=f)


def get_responded_members(update: Update, context: CallbackContext):
    with open(f'flow_daily_bot/responded_members/responded_members{update.message.chat_id}.txt', 'a+',
              encoding='utf8') as f:
        print(update.effective_user.name, file=f)

    def remind_about_missed_persons(context: CallbackContext):
        with open(f'flow_daily_bot/responded_members/responded_members{update.message.chat_id}.txt', 'r',
                  encoding='utf8') as f:
            respond_list = f.readlines()

        with open(f'flow_daily_bot/chat_members/chat_members{update.message.chat_id}.txt', 'r',
                  encoding='utf8') as f:
            chat_list = f.readlines()

        for user in chat_list:
            if user not in respond_list:
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=f'Не направлен стaтус от {user}')
    context.job_queue.run_daily(remind_about_missed_persons, time=datetime.time(12, 0,
                                tzinfo=pytz.timezone('Europe/Moscow')), days=tuple(range(0, 5)))


persistence = PicklePersistence(filename='persistent_storage.pkl')

updater = Updater(os.getenv('TOKEN1'), persistence=persistence, use_context=True)

updater.dispatcher.add_handler(CommandHandler('register', add_chat_id_in_chat_list))

updater.dispatcher.add_handler(CommandHandler('run', get_chat_members))
updater.dispatcher.add_handler(MessageHandler(Filters.text, get_responded_members))

updater.job_queue.run_daily(status_reminders_are_running, time=datetime.time(13, 20, tzinfo=pytz.timezone('Europe/Moscow')),
                            days=tuple(range(0, 5)))
updater.job_queue.run_daily(remind_about_status, time=datetime.time(10, 0, tzinfo=pytz.timezone('Europe/Moscow')),
                            days=tuple(range(0, 5)))

updater.start_polling()
updater.idle()

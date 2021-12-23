import datetime

import pytz
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, PicklePersistence
import telegram.error
import os
from object_storage import ObjectStorage


def hello(update: Update, context: CallbackContext):
    update.message.reply_text(f'Hello {update.effective_user.first_name}')


def remind_about_status(context: CallbackContext):
    chat_list = obj_storage.get('chat_list.txt', 'r')
    for chat_id in chat_list:
        try:
            context.bot.send_message(chat_id=chat_id, text='Не забудьте написать о выполненных задачах')
        except telegram.error.BadRequest:
            pass


def add_chat_id_in_chat_list(update: Update, context: CallbackContext):
    try:
        chat_list = obj_storage.get('chat_list.txt', 'r')
        if str(update.message.chat_id) not in chat_list:
            obj_storage.set('chat_list.txt', 'a', value=update.message.chat_id)

    except FileNotFoundError:
        with open(f'/home/udin76/storage/chat_list.txt', 'a+', encoding='utf8') as f:
            print(update.message.chat_id, file=f)


def get_chat_members(update: Update, context: CallbackContext):
    try:
        chat_members = obj_storage.get(f'chat_members{update.message.chat_id}.txt', 'r')
        if str(update.effective_user.name) not in chat_members:
            obj_storage.set(f'chat_members{update.message.chat_id}.txt', 'a',
                            value=update.effective_user.name)

    except FileNotFoundError:
        with open(f'/home/udin76/storage/chat_members{update.message.chat_id}.txt', 'a+',
                  encoding='utf8') as f:
            print(update.effective_user.name, file=f)


def get_responded_members(update: Update, context: CallbackContext):
    try:
        responded_members = obj_storage_responded_members.get(f'responded_members{update.message.chat_id}.txt', 'r')
        if str(update.effective_user.name) not in responded_members:
            obj_storage_responded_members.set(f'responded_members{update.message.chat_id}.txt', 'a',
                                              value=update.effective_user.name)

    except FileNotFoundError:
        with open(f'/home/udin76/responded_members/responded_members{update.message.chat_id}.txt', 'a+',
                  encoding='utf8') as f:
            print(update.effective_user.name, file=f)

    def send_feedback_to_chat(context: CallbackContext):
        responded_members = obj_storage_responded_members.get(f'responded_members{update.message.chat_id}.txt', 'r')
        number_of_responded_members = len(list(filter(None, responded_members)))

        chat_members = obj_storage.get(f'chat_members{update.message.chat_id}.txt', 'r')
        number_of_chat_members = len(list(filter(None, chat_members)))

        if number_of_responded_members == number_of_chat_members:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text='Все ответили! Молодцы!')
        else:
            for user_name in chat_members:
                if user_name not in responded_members:
                    context.bot.send_message(chat_id=update.message.chat_id,
                                             text=f'Не направлен стaтус от {user_name}')

    context.job_queue.run_daily(send_feedback_to_chat, time=datetime.time(12, 0,
                                                                          tzinfo=pytz.timezone('Europe/Moscow')),
                                days=tuple(range(0, 5)))


def create_list_of_responding_chats(context: CallbackContext):
    with open('/home/udin76/responded_members/responding_chats.txt', 'a+', encoding='utf8') as f:
        pass


def add_chat_id_in_list_of_responding_chats(update: Update, context: CallbackContext):
    try:
        responding_chats = obj_storage_responded_members.get('responding_chats.txt', 'r')

        if str(update.message.chat_id) not in responding_chats:
            obj_storage_responded_members.set('responding_chats.txt', 'a', value=update.message.chat_id)

    except FileNotFoundError:
        with open(f'/home/udin76/responded_members/responding_chats.txt', 'a+', encoding='utf8') as f:
            print(update.message.chat_id, file=f)


def send_message_no_one_write_to_chat(context: CallbackContext):
    responding_chats = obj_storage_responded_members.get('responding_chats.txt', 'r')
    chat_list = obj_storage.get('chat_list.txt', 'r')

    for chat_id in chat_list:
        try:
            if chat_id not in responding_chats:
                context.bot.send_message(chat_id=chat_id, text='Сегодня никто не направил отчет!')
        except telegram.error.BadRequest:
            pass


obj_storage = ObjectStorage('/home/udin76/storage')
obj_storage_responded_members = ObjectStorage('/home/udin76/responded_members')

persistence = PicklePersistence(filename='persistent_storage.pkl')

with open('/home/udin76/token.txt', 'r', encoding='utf8') as f:
    token = f.readline().strip()

updater = Updater(token, persistence=persistence, use_context=True)

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('register', add_chat_id_in_chat_list))
updater.dispatcher.add_handler(CommandHandler('run', get_chat_members))
updater.dispatcher.add_handler(MessageHandler(Filters.text, get_responded_members))
updater.dispatcher.add_handler(MessageHandler(Filters.text, add_chat_id_in_list_of_responding_chats))

updater.job_queue.run_daily(remind_about_status, time=datetime.time(10, 0, tzinfo=pytz.timezone('Europe/Moscow')),
                            days=tuple(range(0, 5)))

updater.job_queue.run_daily(create_list_of_responding_chats, time=datetime.time(5, 0,
                            tzinfo=pytz.timezone('Europe/Moscow')), days=tuple(range(0, 5)))

updater.job_queue.run_daily(send_message_no_one_write_to_chat, time=datetime.time(12, 2,
                            tzinfo=pytz.timezone('Europe/Moscow')), days=tuple(range(0, 5)))

updater.start_polling()
updater.idle()

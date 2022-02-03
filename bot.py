import datetime

import pytz
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, PicklePersistence
import telegram.error
import os
from objectstorage import ObjectStorage


def start(update: Update, context: CallbackContext):
    update.message.reply_text(f'Добрый день, {update.effective_user.first_name}. '
                              f'Я - flow_daily_bot. Я помогу вам в дальнейшей работе в данном чате.')


def help(update: Update, context):
    help_text = obj_storage['help']
    update.message.reply_text('\n'.join(help_text))


def remind_about_status(context: CallbackContext):
    chat_list = obj_storage['chat_list']
    for chat_id in chat_list:
        try:
            context.bot.send_message(chat_id=chat_id, text='Не забудьте написать о выполненных задачах')
        except telegram.error.BadRequest:
            pass


def add_chat_id_in_chat_list(update: Update, context: CallbackContext):
    chat_list = obj_storage['chat_list']
    if str(update.message.chat_id) not in chat_list:
        obj_storage.set('chat_list', value=update.message.chat_id)


def get_chat_members(update: Update, context: CallbackContext):
    chat_members = obj_storage[f'chat_members{update.message.chat_id}']
    if str(update.effective_user.name) not in chat_members:
        obj_storage.set(f'chat_members{update.message.chat_id}', value=update.effective_user.name)


def text_handler(update: Update, context: CallbackContext):
    get_responded_members(update, context)
    add_chat_id_in_list_of_responding_chats(update, context)


def get_responded_members(update: Update, context: CallbackContext):
    responded_members = obj_storage[f'responded_members{update.message.chat_id}']
    if str(update.effective_user.name) not in responded_members:
        obj_storage.set(f'responded_members{update.message.chat_id}', value=update.effective_user.name)


def send_feedback_to_chat(context: CallbackContext):
    chat_id = context.job.context
    responded_members = obj_storage[f'responded_members{chat_id}']
    number_of_responded_members = len(list(filter(None, responded_members)))

    chat_members = obj_storage[f'chat_members{chat_id}']
    number_of_chat_members = len(list(filter(None, chat_members)))

    try:
        if number_of_responded_members == number_of_chat_members:
            context.bot.send_message(chat_id=chat_id, text='Все ответили! Молодцы!')
        else:
            for user_name in chat_members:
                if user_name not in responded_members:
                    context.bot.send_message(chat_id=chat_id, text=f'Не направлен стaтус от {user_name}')
    except (telegram.error.Unauthorized, telegram.error.BadRequest):
        pass


def add_chat_id_in_list_of_responding_chats(update: Update, context: CallbackContext):
    responding_chats = obj_storage['responding_chats']
    if str(update.message.chat_id) not in responding_chats:
        obj_storage.set('responding_chats', value=update.message.chat_id)


def send_message_no_one_write_to_chat(context: CallbackContext):
    responding_chats = obj_storage['responding_chats']
    chat_list = obj_storage['chat_list']

    for chat_id in chat_list:
        try:
            if chat_id not in responding_chats:
                context.bot.send_message(chat_id=chat_id, text='Сегодня никто не направил отчет!')
        except (telegram.error.Unauthorized, telegram.error.BadRequest):
            pass


obj_storage = ObjectStorage('/home/udin76')

persistence = PicklePersistence(filename='persistent_storage.pkl')

with open('/home/udin76/token.txt', 'r', encoding='utf8') as f:
    token = f.readline().strip()

updater = Updater(token, persistence=persistence, use_context=True)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('register', add_chat_id_in_chat_list))
updater.dispatcher.add_handler(CommandHandler('run', get_chat_members))
updater.dispatcher.add_handler(MessageHandler(Filters.text, text_handler))

updater.job_queue.run_daily(
    remind_about_status,
    time=datetime.time(10, 0, tzinfo=pytz.timezone('Europe/Moscow')),
    days=tuple(range(0, 5))
)

updater.job_queue.run_daily(
    send_message_no_one_write_to_chat,
    time=datetime.time(12, 0, tzinfo=pytz.timezone('Europe/Moscow')),
    days=tuple(range(0, 5))
)

for chat_id in obj_storage['chat_list']:
    updater.job_queue.run_daily(
        send_feedback_to_chat,
        time=datetime.time(12, 1, tzinfo=pytz.timezone('Europe/Moscow')),
        days=tuple(range(0, 5)),
        context=chat_id
    )

updater.start_polling()
updater.idle()

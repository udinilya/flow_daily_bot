from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import datetime
import pytz


def daily_message(context: CallbackContext):
    context.bot.send_message(chat_id=x,
                             text='Не забудьте написать о выполненных задачах')


def register_callback(update: Update, context: CallbackContext):
    global x
    context.bot.send_message(chat_id=update.message.chat_id,
                             text='Напоминания о статусах запущены')
    context.job_queue.run_daily(daily_message, time=datetime.time(10, 0, tzinfo=pytz.timezone('Europe/Moscow')), days=tuple(range(0, 5)))
    x = update.message.chat_id


updater = Updater('2115574444:AAHL5eyZCEjkQRn4FILqYdXvhR4UJp76Ih0')

register_handler = CommandHandler('register', register_callback)
updater.dispatcher.add_handler(register_handler)

updater.start_polling()
updater.idle()

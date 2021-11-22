from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import datetime
import pytz


def callback_daily(context: CallbackContext):
    context.bot.send_message(chat_id=-693040330,
                             text=' Необходимо направить задания')


updater = Updater('2115574444:AAHL5eyZCEjkQRn4FILqYdXvhR4UJp76Ih0')


j = updater.job_queue
job_daily = j.run_daily(callback_daily, time=datetime.time(10, 0, tzinfo=pytz.timezone('Europe/Moscow')), days=tuple(range(0, 5)))

updater.start_polling()
updater.idle()

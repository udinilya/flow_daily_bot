from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import datetime
import pytz


def hello(update: Update, context: CallbackContext):
    update.message.reply_text(f'Hello{update.effective_user.first_name}')


def callback_daily(context: CallbackContext):
    context.bot.send_message(chat_id=-693040330,
                             text=' Необходимо направить задания')


updater = Updater('2115574444:AAHL5eyZCEjkQRn4FILqYdXvhR4UJp76Ih0')
updater.dispatcher.add_handler(CommandHandler('hello', hello))

j = updater.job_queue
job_daily = j.run_daily(callback_daily, time=datetime.time(10, 0, tzinfo=pytz.timezone('Europe/Moscow')), days=tuple(range(0, 4)))

updater.start_polling()
updater.idle()

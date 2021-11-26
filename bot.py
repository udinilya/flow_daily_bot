from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, PicklePersistence
import datetime
import pytz


def register_callback(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text='Напоминания о статусах запущены')

    def daily_message(context: CallbackContext):
         context.bot.send_message(chat_id=update.message.chat_id,
                                  text='Не забудьте написать о выполненных задачах')

    def daily_message_repeat(context: CallbackContext):
        with open('user.txt', 'r', encoding='utf8') as infile:
            line = infile.readlines()

        with open('user_list.txt', 'r', encoding='utf8') as myfile:
            list = myfile.readlines()

        for _ in list:
            if _ not in line:
                context.bot.send_message(chat_id=update.message.chat_id,
                                        text=f'Не направлен стaтус от...{_}')

    context.job_queue.run_daily(daily_message, time=datetime.time(10, 0, tzinfo=pytz.timezone('Europe/Moscow')),
                                days=tuple(range(0, 5)))
    context.job_queue.run_daily(daily_message_repeat, time=datetime.time(12, 0, tzinfo=pytz.timezone('Europe/Moscow')),
                                days=tuple(range(0, 5)))


def user_name(update: Update, context: CallbackContext):
    outfile = open('user.txt', 'a+', encoding='utf8')
    print(update.effective_user.name, file=outfile)
    outfile.close()


def user_list(update: Update, context: CallbackContext):
    outfile = open('user_list.txt', 'a+', encoding='utf8')
    print(update.effective_user.name, file=outfile)
    outfile.close()


my_persistence = PicklePersistence(filename='persistent_storage.pkl')

updater = Updater('2115574444:AAHL5eyZCEjkQRn4FILqYdXvhR4UJp76Ih0', persistence=my_persistence, use_context=True)

register_handler = CommandHandler('register', register_callback)
updater.dispatcher.add_handler(register_handler)

user_handler = MessageHandler(Filters.text, user_name)
updater.dispatcher.add_handler(user_handler)

updater.dispatcher.add_handler(CommandHandler('run', user_list))


updater.start_polling()
updater.idle()

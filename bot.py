from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, PicklePersistence
import datetime
import pytz


def register_callback(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text='Напоминания о статусах запущены')

    def remind_about_status(context: CallbackContext):
         context.bot.send_message(chat_id=update.message.chat_id,
                                  text='Не забудьте написать о выполненных задачах')

    def remind_about_missed_persons(context: CallbackContext):
        with open('user_respond_list.txt', 'r', encoding='utf8') as infile:
            respond_list = infile.readlines()

        with open('chat_user_list.txt', 'r', encoding='utf8') as myfile:
            chat_list = myfile.readlines()

        for user in chat_list:
            if user not in respond_list:
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=f'Не направлен стaтус от...{user}')

    context.job_queue.run_daily(remind_about_status, time=datetime.time(16, 37, tzinfo=pytz.timezone('Europe/Moscow')),
                                days=tuple(range(0, 5)))
    context.job_queue.run_daily(remind_about_missed_persons, time=datetime.time(16, 38, tzinfo=pytz.timezone('Europe/Moscow')),
                                days=tuple(range(0, 5)))


def user_respond_list(update: Update):
    outfile = open('user_respond_list.txt', 'a+', encoding='utf8')
    print(update.effective_user.name, file=outfile)
    outfile.close()


def user_in_chat_list(update: Update):
    outfile = open('chat_user_list.txt', 'a+', encoding='utf8')
    print(update.effective_user.name, file=outfile)
    outfile.close()


my_persistence = PicklePersistence(filename='persistent_storage.pkl')

updater = Updater('2115574444:AAHL5eyZCEjkQRn4FILqYdXvhR4UJp76Ih0', persistence=my_persistence, use_context=True)

register_handler = CommandHandler('register', register_callback)
updater.dispatcher.add_handler(register_handler)

user_handler = MessageHandler(Filters.text, user_respond_list)
updater.dispatcher.add_handler(user_handler)

updater.dispatcher.add_handler(CommandHandler('run', user_in_chat_list))


updater.start_polling()
updater.idle()

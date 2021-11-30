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
        with open(f'flow_daily_bot/responded_members/responded_members{update.message.chat_id}.txt', 'r', encoding='utf8') as f:
            respond_list = f.readlines()

        with open(f'flow_daily_bot/chat_members/chat_members{update.message.chat_id}.txt', 'r', encoding='utf8') as f:
            chat_list = f.readlines()

        for user in chat_list:
            if user not in respond_list:
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=f'Не направлен стaтус от...{user}')

    context.job_queue.run_daily(remind_about_status, time=datetime.time(10, 0,
                                tzinfo=pytz.timezone('Europe/Moscow')), days=tuple(range(0, 5)))
    context.job_queue.run_daily(remind_about_missed_persons, time=datetime.time(12, 0,
                                tzinfo=pytz.timezone('Europe/Moscow')), days=tuple(range(0, 5)))


def get_responded_members(update: Update, context: CallbackContext):
    f = open(f'flow_daily_bot/responded_members/responded_members{update.message.chat_id}.txt', 'a+', encoding='utf8')
    print(update.effective_user.name, file=f)
    f.close()


def get_chat_members(update: Update, context: CallbackContext):
    f = open(f'flow_daily_bot/chat_members/chat_members{update.message.chat_id}.txt', 'a+', encoding='utf8')
    print(update.effective_user.name, file=f)
    f.close()


persistence = PicklePersistence(filename='persistent_storage.pkl')

updater = Updater('2115574444:AAHL5eyZCEjkQRn4FILqYdXvhR4UJp76Ih0', persistence=persistence, use_context=True)

updater.dispatcher.add_handler(CommandHandler('run', get_chat_members))
updater.dispatcher.add_handler(CommandHandler('register', register_callback))
updater.dispatcher.add_handler(MessageHandler(Filters.text, get_responded_members))


updater.start_polling()
updater.idle()

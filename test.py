from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters


def hello(update: Update, context: CallbackContext):
    update.message.reply_text(f'Hello{update.effective_user.first_name}')



def sayhi(context):
    context.bot.send_message(chat_id=context.job.context, text="Направьте список задач")


def time(update, context):
    job = context.job_queue.run_repeating(sayhi, 5, context=update)


updater = Updater('2115574444:AAHL5eyZCEjkQRn4FILqYdXvhR4UJp76Ih0')


updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(MessageHandler(Filters.text, time, pass_job_queue=True))

updater.start_polling()
updater.idle()

import datetime

import pytz
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, PicklePersistence
import telegram.error
import os


def add_chat_id_in_chat_list(update: Update, context: CallbackContext):
    try:
        with open('/home/udin76/chat_list/chat_list.txt', 'r', encoding='utf8') as f:
            chat_list = []
            for chat_id in f:
                chat_list.append(int(chat_id.strip()))

        if update.message.chat_id not in chat_list:
            with open('/home/udin76/chat_list/chat_list.txt', 'a', encoding='utf8') as f:
                print(update.message.chat_id, file=f)

    except FileNotFoundError:
        with open(f'/home/udin76/chat_list/chat_list.txt', 'a+', encoding='utf8') as f:
            print(update.message.chat_id, file=f)


def get_chat_members(update: Update, context: CallbackContext):
    try:
        with open(f'/home/udin76/chat_members/chat_members{update.message.chat_id}.txt', 'r',
                  encoding='utf8') as f:
            chat_members = []
            for user_name in f:
                chat_members.append(str(user_name.strip()))

        if update.effective_user.name not in chat_members:
            with open(f'/home/udin76/chat_members/chat_members{update.message.chat_id}.txt', 'a',
                      encoding='utf8') as f:
                print(update.effective_user.name, file=f)

    except FileNotFoundError:
        with open(f'/home/udin76/chat_members/chat_members{update.message.chat_id}.txt', 'a+',
                  encoding='utf8') as f:
            print(update.effective_user.name, file=f)


def create_list_of_responding_chats(context: CallbackContext):
    with open('/home/udin76/responded_members/responding_chats.txt', 'a+', encoding='utf8') as f:
        pass


def add_chat_id_in_list_of_responding_chats(update: Update, context: CallbackContext):
    try:
        with open('/home/udin76/responded_members/responding_chats.txt', 'r', encoding='utf8') as f:
            responding_chats = []
            for chat_id in f:
                responding_chats.append(int(chat_id.strip()))

        if update.message.chat_id not in responding_chats:
            with open('/home/udin76/responded_members/responding_chats.txt', 'a', encoding='utf8') as f:
                print(update.message.chat_id, file=f)

    except FileNotFoundError:
        with open(f'/home/udin76/responded_members/responding_chats.txt', 'a+', encoding='utf8') as f:
            print(update.message.chat_id, file=f)

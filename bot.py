# -*- coding: utf-8 -*-
import telebot
import config
import datetime
import pytz
import json
import traceback
from utils import serialize_table, get_back_keyboard, getHTML, get_defi_keyboard
from backend import get_user_transactions, get_user_balances, set_user_address, get_user_address

# P_TIMEZONE = pytz.timezone(config.TIMEZONE)
# TIMEZONE_COMMON_NAME = config.TIMEZONE_COMMON_NAME

bot = telebot.TeleBot('1499578916:AAFwURdauecl6wUFLSeTy34eYj2kTGqIBn0')
print(bot)

@bot.message_handler(commands=['start'])
def start_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton(
            'Home 🏠', callback_data='home'
        )
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton(
            'Get Help ❓', callback_data='home'
        )
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton(
            'Powered by Covalent', callback_data='a'
        )
    )
    bot.send_message(
        message.chat.id,
        'Greetings! Manange Your whole Wallet Right From Telegram 📳\n' +
        'To Start Send /home 🏠\n' +
        'To Get Help Send /help ❓',
        reply_markup=keyboard
    )

@bot.message_handler(commands=['help'])
def help_command(message):
   keyboard = telebot.types.InlineKeyboardMarkup()
   keyboard.add(
       telebot.types.InlineKeyboardButton(
           'Message the developer 💻', url='telegram.me/man_jain'
       )
   )
   bot.send_message(
       message.chat.id,
       '1) To Manage Your Wallet Type /home 🏠\n' +
       '2) Click on the action you are interested in ➡\n',
       reply_markup=keyboard
   )

@bot.message_handler(commands=['home'])
def exchange_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
      telebot.types.InlineKeyboardButton('Balances 💵', callback_data='bal')
    )
    keyboard.row(
    telebot.types.InlineKeyboardButton('Last 10 Transactions 📃', callback_data='trans'),
    telebot.types.InlineKeyboardButton('Manage Defi 💰', callback_data='defi')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('Register/Update Address 👜', callback_data='setAddress')
    )

    bot.send_message(message.chat.id, 'What Do You Want to Do: ❔', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def set_user_address_handler(message):  # THIS FUNCTION
    sent = bot.send_message(message.chat.id, 'Please Send You Ethereum Address')
    def set_address(msg):
        # print('message', json.dumps(message))
        print(msg.from_user.id, msg.text)
        if msg.text[0:2] == '0x' and len(msg.text) == 42:
            set_user_address(msg.from_user.id, msg.text)
            bot.send_message(msg.chat.id, 'Your Address Has been Registered')
        else:
            bot.send_message(msg.chat.id, 'Not a Correct Address. Please restart process and Enter Correct One')
    bot.register_next_step_handler(sent, set_address)

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data
    if data == 'bal':
        items = get_user_balances(query)
        bot.answer_callback_query(query.id)
        bot.send_chat_action(query.message.chat.id, 'typing')
        bot.send_message(
            query.message.chat.id, getHTML('balances', items),
            reply_markup=get_back_keyboard("bal"),
            parse_mode='HTML'
        )
    elif data == 'trans':
        items = get_user_transactions(query)
        bot.answer_callback_query(query.id)
        bot.send_chat_action(query.message.chat.id, 'typing')
        print(getHTML('transactions', items))
        bot.send_message(
            query.message.chat.id, getHTML('transactions', items),
            reply_markup=get_back_keyboard("trans"),
            parse_mode='HTML'
        )
    elif data == 'defi':
        # items = get_user_transactions(query)
        bot.answer_callback_query(query.id)
        bot.send_chat_action(query.message.chat.id, 'typing')
        bot.send_message(
            query.message.chat.id, "Choose a Defi Platform",
            reply_markup=get_defi_keyboard("send"),
            parse_mode='HTML'
        )

    elif data == 'setAddress':
        bot.answer_callback_query(query.id)
        bot.send_chat_action(query.message.chat.id, 'typing')
        set_user_address_handler(query.message)

    elif data == "home":
        bot.answer_callback_query(query.id)
        bot.send_chat_action(query.message.chat.id, 'typing')
        exchange_command(query.message)

    elif data == "refreshbal":
        items = get_user_balances(query)
        bot.answer_callback_query(query.id)
        bot.send_chat_action(query.message.chat.id, 'typing')
        bot.send_message(
            query.message.chat.id, getHTML('balances', items),
            reply_markup=get_back_keyboard("bal"),
            parse_mode='HTML'
        )

    elif data == "refreshtrans":
        items = get_user_transactions(query)
        bot.answer_callback_query(query.id)
        bot.send_chat_action(query.message.chat.id, 'typing')
        print(getHTML('transactions', items))
        bot.send_message(
            query.message.chat.id, getHTML('transactions', items),
            reply_markup=get_back_keyboard("trans"),
            parse_mode='HTML'
        )


bot.polling(none_stop=True)

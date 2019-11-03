#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

import logging, time, sys
from data import Data
from telegram import Bot  
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from w1thermsensor import W1ThermSensor

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

sensor = W1ThermSensor()
extemp = Data("extemp", sensor.get_temperature)



# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def now(update, context):
    update.message.reply_text("{:.1f} °C \n{:.2f} °C/min \n{:.1f} °C/h"
    .format(extemp.now, extemp.delta_short(), extemp.delta_long()))

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

alert = False

def check_alert(bot):
    global alert
    lowtemp = extemp.now < 45
    if lowtemp != alert:
        if lowtemp:
            alert = True
            for i in subscribers:
                bot.bot.send_message(chat_id=i, text="lämpötilahälytys!!")
        else:
            alert = False

def update_subs():
    with open('subs.txt', 'w') as the_file:
        for i in subscribers:
            the_file.write(str(i)+"\n")

def read_subs():
    subs=[]
    try:
        with open('subs.txt', 'r') as the_file:
            for i in the_file:
                subs.append(int(i))
    except FileNotFoundError:
        open('subs.txt', 'a').close()
    return subs

subscribers = read_subs()

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def subscribe(update, context):
    id = update.effective_message.chat_id
    if(id in subscribers):
        update.message.reply_text("Tilaus jo olemassa")
    else:
        subscribers.append(id)
        update.message.reply_text("Tilaus lisätty")

def unsubscribe(update, context):
    id = update.effective_message.chat_id
    if(id in subscribers):
        subscribers.remove(id)
        update.message.reply_text("Tilaus poistettu")
    else:
        update.message.reply_text("Ei tilausta")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def read_token():
    file = open(".token","r")
    return file.readline()

def main():

    """Start the bot."""

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(read_token(), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("nyt", now))
    dp.add_handler(CommandHandler("now", now))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    dp.add_handler(CommandHandler("tilaa", subscribe))
    dp.add_handler(CommandHandler("poista", unsubscribe))
    dp.add_handler(CommandHandler("remove", unsubscribe))
    dp.add_handler(CommandHandler("unsubscribe", unsubscribe))
    dp.add_handler(CommandHandler("stop", unsubscribe))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    #updater.idle()
    print("Bot running...")
    try:
        while(True):
            extemp.update()
            check_alert(updater)
            time.sleep(60)
            if time.localtime().tm_min == 0:
                update_subs()
                extemp.save()
    except (KeyboardInterrupt, SystemExit):
        print("Saving and quitting")
        extemp.save()
        updater.stop()
        update_subs()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

if __name__ == '__main__':
    main()
# https://algorithmia.com/blog/create-a-chatbot-telegram-python-summarize-text
# https://t.me/botfather
# https://algorithmia.com/signup?invite=summarizer
# pip install algorithmia python-telegram-bot==5.0.0

from telegram.ext import Updater
import logging
import Algorithmia
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
# Set up basic logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
updater = Updater(token='-')
dispatcher = updater.dispatcher
# You can find your Algorithmia token by going to My Profile > Credentials
client = Algorithmia.client('-')
# The algorithm we'll be using
algo = client.algo('nlp/Summarizer/0.1.3')
def summarize(bot, update):
    try:
        # Get the text the user sent
        text = update.message.text
        # Run it through the summarizer
        summary = algo.pipe(text)
        print(summary.result)
        # Send back the result
        bot.sendMessage(chat_id=update.message.chat_id, 
        text=summary.result)
    except UnicodeEncodeError:
        bot.sendMessage(chat_id=update.message.chat_id, 
        text="Sorry, but I can't summarise your text.")
        # This enables the '/start' command
       
def start(bot, update):
    print(bot, update)
    # Your bot will send this message when users first talk to it, or when they use the /start command
    bot.sendMessage(chat_id=update.message.chat_id, 
    text="Hi. Send me any English text and I'll summarize it for you.")
   # This enables the '/start' command

def bx():
    start_handler = CommandHandler('start', start)
    # Summarize all the messages sent to the bot, but only if they contain text
    summarize_handler = MessageHandler([Filters.text], summarize)
    # dispatcher.add_handler(summarize_handler)
    dispatcher.add_handler(start_handler)
    updater.start_polling()
    start_handler = CommandHandler('start', start)
    # Summarize all the messages sent to the bot, but only if they contain text
    summarize_handler = MessageHandler([Filters.text], summarize)
    dispatcher.add_handler(summarize_handler)
    dispatcher.add_handler(start_handler)
    updater.start_polling()

bx()

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings

logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename = 'bot.log'
                    )
def greet_user(update, context):
    text = 'Вызван /start'
    logging.info = text
    update.message.reply_text(text)

def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text) 
    update.message.reply_text(user_text) 


def main(): 
    mybot = Updater(settings.API_KEY, use_context=True) 

    logging.info = 'Бот запускается.'
 
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
 

    mybot.start_polling() 
    mybot.idle() 

main() 
from telegram.ext import Updater , CommandHandler, MessageHandler , Filters , InlineQueryHandler
from telegram import InlineQueryResultArticle , InputTextMessageContent
import pyshorteners
import requests
import datetime

print('Bot Running...')


#Fill this section with your own API-KEYs
apitoken = '' 
bitlytoken = ''
updater = Updater(token=apitoken)

#Emojis
raising_hands = u'\U0001F64C' #raising hands
robot = u'\U0001F916' #robot
check_mark_button = u'\U00002705' #check mark button
e_mail = u'\U0001F4E7' #e-mail
alien_monster = u'\U0001F47E' #alien_monster
satellite_antenna = u'\U0001F4E1' #satellite antenna
gear = u'\U00002699' #gear
cross_mark = u'\U0000274C' #cross_mark
coffee = u'\U00002615' #coffee
open_book = u'\U0001F4D6' #open book
chain = u'\U0001F517' #chain

def start(update , context):
    context.bot.send_message(chat_id=update.effective_chat.id, text= raising_hands + ' Welcome to Relinked!\n' + coffee + ' Hope You Are Enjoying Your Day!\n\n' + open_book + ' Use /help if you need help')
updater.dispatcher.add_handler(CommandHandler('start' , start))

def about(update , context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=satellite_antenna + ' Early Version - Under Development\n'+gear+' Beta V2.0\n\n'+robot+' Developed By:\n@Kaonashi4 & @mac_mr\n\n'+e_mail+' relinkedsupport@solarunited.net')
updater.dispatcher.add_handler(CommandHandler('about' , about))

def help(update , context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=robot + ' How about a usage tutorial?\n\n' + check_mark_button + ' All you have to do is send us a link. Example:\nhttps://docs.python.org/3/tutorial/index.html\n\n' + alien_monster + ' And we will reply with a shortened link:\nhttps://bit.ly/35wBtuA\n\n' + chain + ' Another way of using this bot would be by inline commands\nSo open a chat... and type in @relinkedbot. then put your name directly into the line...\n\n' + check_mark_button + " So if you type in like this and tap 'Shorten Link' button:\n@relinkedbot https://docs.python.org/3/tutorial/index.html\n\n" + alien_monster + ' We will turn your message into a shortened link:\nhttps://bit.ly/35wBtuA')
updater.dispatcher.add_handler(CommandHandler('help' , help))

def check_message(update , context):
    try:
        request = requests.get(update.message.text)
        if request.status_code == 200:
            shortened_link = pyshorteners.Shortener(api_key=bitlytoken).bitly.short(update.message.text)
            context.bot.send_message(chat_id=update.effective_chat.id, text=check_mark_button + ' Done! Shortened Link: ' + shortened_link)
            file = open('data.csv' , 'a')
            file.write(str(update.effective_chat.id) + ',' + str(shortened_link) + ',' + str(datetime.datetime.today()) + '\n')
            file.close()
            return True
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=cross_mark + ' Invalid link! use /help for tutorial')
            return False
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text=cross_mark + ' Invalid link! use /help for tutorial')
        return False

updater.dispatcher.add_handler(MessageHandler(Filters.text , check_message))

def inline_link(update, context):
    query = update.inline_query.query
    file = open('data.csv' , 'a')
    if not query:
        return
    try:
        inlinerequest = requests.get(query)
        if inlinerequest.status_code == 200:
            shortened_link = pyshorteners.Shortener(api_key=bitlytoken).bitly.short(query)
            file.write(str(update.inline_query.id) + ',' + str(shortened_link) + ',' + str(datetime.datetime.today()) + '\n')
            file.close()
            results = list()
            results.append(
                InlineQueryResultArticle(
                    id='inlinelinkshorten',
                    title=check_mark_button + ' Send Shortened Link',
                    input_message_content=InputTextMessageContent(shortened_link)
                )
            )
            context.bot.answer_inline_query(update.inline_query.id, results)
            return True
        else:
            return False
    except:
            return False
    

updater.dispatcher.add_handler(InlineQueryHandler(inline_link))

updater.start_polling()
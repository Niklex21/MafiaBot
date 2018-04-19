from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import time

# --- GLOBALS --- #
game_state = False  # True - currently going, false - passive
registration_state = False  # Same here
players = dict()
quantity = 0

# --- CONSTANTS --- #
BOT_TOKEN = ""  # Insert here your bot Token (can be received from @BotFather)
REGISTRATION_TIME = 60  # In seconds

updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher


def registration():
    global registration_state

    bot.send_message('Registration is active. To try your fortune, please send "/imin" command')
    registration_state = True


def start_game():
    bot.send_message(chat_id=update.message.chat_id, text='Game is started. And may the strongest win.')


# Starts on '/game'
def game_command(bot, update):
    global game_state
    global quantity
    global registration_state
    global players

    if not game_state:
        bot.send_message(chat_id=update.message.chat_id, text='And may the odds be ever in your favor')
        game_state = True
        registration_state = True

        bot.send_message(chat_id=update.message.chat_id, text='Registration started. Call "/imin" to try your fortune')
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Currently running')


# On '/stop'
def stop_command(bot, update):
    global game_state
    global registration_state
    global quantity
    global players

    if game_state:
        bot.send_message(chat_id=update.message.chat_id, text='¡Sí, señor!')
        game_state = False
        registration_state = False

        quantity = 0
        players.clear()

        bot.send_message(chat_id=update.message.chat_id, text='Game aborted successfully.')
    else:
        bot.send_message(chat_id=update.message.chat_id, text='There is no active game to stop :(')


# On '/imin'
def reg_command(bot, update):
    global registration_state
    global quantity

    if registration_state:
        new_user = update.message.from_user

        players[new_user.id] = new_user
        quantity += 1

        print(players[new_user.id].username)
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Registration is not active right now. Please call "/game" to start registration')


# On '/start'
def start_command(bot, update):
    global quantity
    global registration_state
    global game_state

    if game_state:
        if registration_state:
            if quantity > 4:
                bot.send_message(chat_id=update.message.chat_id,
                                 text='Registration was successful! Game is starting...')
                start_game()
            else:
                bot.send_message(chat_id=update.message.chat_id,
                                 text='\n'.join(['Too small amount of players :(',
                                                 'Current amount of players: {}'.format(quantity),
                                                 'Amount of players required: 5.']))
        else:
            bot.send_message(chat_id=update.message.chat_id, text='Please call "/game" to begin the registration.')
    else:
        bot.send_message(chat_id=update.message.chat_id, text='No game is currently active :(')


game_command_handler = CommandHandler('game', game_command)
stop_command_handler = CommandHandler('stop', stop_command)
reg_command_handler = CommandHandler('imin', reg_command)
start_command_handler = CommandHandler('start', start_command)

dispatcher.add_handler(game_command_handler)
dispatcher.add_handler(stop_command_handler)
dispatcher.add_handler(reg_command_handler)
dispatcher.add_handler(start_command_handler)

updater.start_polling(clean=True)

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import time

# --- GLOBALS --- #
game_state = False  # True - currently going, false - passive
registration_state = False  # Same here
players = dict()
quantity = 0
used = []

# --- CONSTANTS --- #
BOT_TOKEN = "416682801:AAHygzvxHclVevhrwIufoUuNCAgJueh2GpI"
REGISTRATION_TIME = 60  # In seconds
REQUIRED_PLAYERS = 1
CARDS = ['mafia', 'innocent', 'detective', 'doctor']

updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher


class Player:
    def __init__(self, user):
        self.ID = user.id
        self.name = user.first_name + ' ' + user.last_name
        self.nick = user.username
        self.card = None
        self.is_alive = True
        self.able_to_play_round = True


# Main
def game(chat_id):
    global game_state

    game_state = True
    bot.send_message(chat_id=chat_id, text='Game is started. And may the strongest win.')


# Starts on '/game'
def registration_command(bot, update):
    global game_state
    global quantity
    global registration_state
    global players

    if not (game_state or registration_state):
        bot.send_message(chat_id=update.message.chat_id, text='And may the odds be ever in your favor')
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

    if game_state or registration_state:
        bot.send_message(chat_id=update.message.chat_id, text='¡Sí, señor!')

        game_state = False
        registration_state = False

        quantity = 0
        players.clear()
        used.clear()

        bot.send_message(chat_id=update.message.chat_id, text='Game aborted successfully.')
    else:
        bot.send_message(chat_id=update.message.chat_id, text='There is no active game to stop :(')


# On '/imin'
def reg_player_command(bot, update):
    global registration_state
    global quantity

    if registration_state:
        new_user = Player(update.message.from_user)

        if new_user.ID in used:
            bot.send_message(chat_id=update.message.chat_id,
                             text='You are already registered. Please wait for other players :)')
            return

        players[new_user.ID] = new_user
        quantity += 1

        print(players[new_user.ID].name)
        used.append(new_user.ID)
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Registration is not active right now. Please call "/game" to start registration')


# On '/start'
def start_command(bot, update):
    global quantity
    global registration_state
    global game_state

    if game_state:
        bot.send_message(chat_id=update.message.chat_id, text='Game is already running!')
        return

    if registration_state:
        if quantity >= REQUIRED_PLAYERS:
            bot.send_message(chat_id=update.message.chat_id,
                             text='Registration was successful! Game is starting...')
            registration_state = False
            game(update.message.chat_id)
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text='\n'.join(['Too small amount of players :(',
                                             'Current amount of players: {}'.format(quantity),
                                             'Amount of players required: {}.'.format(REQUIRED_PLAYERS)]))
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Please call "/game" to begin the registration.')


game_command_handler = CommandHandler('game', registration_command)
stop_command_handler = CommandHandler('stop', stop_command)
reg_command_handler = CommandHandler('imin', reg_player_command)
start_command_handler = CommandHandler('start', start_command)

dispatcher.add_handler(game_command_handler)
dispatcher.add_handler(stop_command_handler)
dispatcher.add_handler(reg_command_handler)
dispatcher.add_handler(start_command_handler)

updater.start_polling(clean=True)

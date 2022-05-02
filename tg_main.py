import os

import telebot
from dotenv import load_dotenv
from telebot.types import Message

import service
from data import Player, START_RANK
from db import BeerPongDao

load_dotenv()
TG_API_KEY = os.getenv('TG_API_KEY')

bot = telebot.TeleBot(TG_API_KEY)
db = BeerPongDao()
s = service.BeerPongService()


def get_player_handle(message: Message):
    try:
        return message.from_user.username or \
               f"{message.from_user.first_name} {message.from_user.last_name}"
    except AttributeError:
        return


@bot.message_handler(commands=['start'])
def send_welcome(message: Message) -> None:
    player_handle = get_player_handle(message)
    if not player_handle:
        bot.reply_to(message, "I couldn't get your username, please do something about it")
    new_player_handle = Player(name=player_handle)
    new_player_handle = db.add_player(new_player_handle)
    if new_player_handle:
        bot.reply_to(message, f"Hi, {new_player_handle}! You are now a part of beerpong community! Your starting ELO is"
                              f" {START_RANK} feel free to record your beerpong matches with our bot!")
    else:
        elo = db.elo_by_name(player_handle)
        bot.reply_to(message, f"Hi, {player_handle}! Your current elo is {elo['rank']}. Go play some beerpong!")


@bot.message_handler(commands=['save_solo_match'])
def save_solo_match(message: Message) -> None:
    ERROR_MSG = f"Please write in format\n" \
                f"/save_match OPPONENT_NAME CUPS_YOU_SCORED CUPS_HE_SCORED\n" \
                f"like this:\n" \
                f"/save_solo_match ABOBA 10 5"
    player1_handle = get_player_handle(message)
    text = message.text
    args = text.split(' ')[1:]
    if len(args) != 3:
        bot.reply_to(message, ERROR_MSG)
        return
    try:
        args[1] = int(args[1])
        args[2] = int(args[2])
    except ValueError:
        bot.reply_to(message, ERROR_MSG)
        return
    player2_handle = args[0]
    player1_score = args[1]
    player2_score = args[2]
    try:
        s.add_match([player1_handle], [player2_handle], player1_score, player2_score)
    except Exception as e:
        bot.reply_to(message, f'could not add match because {e}')
        return
    bot.reply_to(message, f"Nice game! Your new elo is {db.elo_by_name(player1_handle)['rank']}! {player2_handle}'s elo is now {db.elo_by_name(player2_handle)['rank']}")


if __name__ == '__main__':
    bot.infinity_polling()

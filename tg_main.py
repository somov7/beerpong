import os

import telebot
from dotenv import load_dotenv
from telebot.types import Message

import service
from data import Player, START_RANK, SIP_VOLUME

load_dotenv()
IS_DEV = os.getenv('TG_API_KEY_DEV')
TG_API_KEY = os.getenv('TG_API_KEY') if not IS_DEV else os.getenv('TG_API_KEY_DEV')

bot = telebot.TeleBot(TG_API_KEY)
s = service.BeerPongService()


def get_player_handle(message: Message):
    try:
        return message.from_user.username or \
               f"{message.from_user.first_name} {message.from_user.last_name}"
    except AttributeError:
        return


def parse_name(message: Message):
    text = message.text
    args = text.split(' ')[1:]
    if len(args) == 0:
        player_handle = get_player_handle(message)
    elif len(args) == 1:
        player_handle = args[0]
    else:
        raise Exception('You should provide either 0 or 1 argument')
    player = s.find_player(player_handle)
    if not player:
        raise Exception('No player with handle {player_handle} exists')
    return player_handle


@bot.message_handler(commands=['start'])
def send_welcome(message: Message) -> None:
    player_handle = get_player_handle(message)
    if not player_handle:
        bot.reply_to(message, "I couldn't get your username, please do something about it")
    new_player = s.add_player(player_handle)
    if new_player:
        bot.reply_to(message, f"Hi, {new_player.name}! You are now a part of beerpong community! Your starting ELO is"
                              f" {START_RANK} feel free to record your beerpong matches with our bot!")
    else:
        player = s.find_player(player_handle)
        bot.reply_to(message, f"Hi, {player_handle}! Your current elo is {player.rank}. Go play some beerpong!")


@bot.message_handler(commands=['save_solo_match'])
def save_solo_match(message: Message) -> None:
    ERROR_MSG = f"Please write in format\n" \
                f"/save_solo_match OPPONENT_NAME CUPS_YOU_SCORED CUPS_HE_SCORED\n" \
                f"like this:\n" \
                f"/save_solo_match ABOBA 10 5"
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

    player1_handle = get_player_handle(message)
    player2_handle = args[0]
    player1_score = args[1]
    player2_score = args[2]
    try:
        s.add_match([player1_handle], [player2_handle], player1_score, player2_score)
    except Exception as e:
        bot.reply_to(message, f'could not add match because {e}')
        return
    bot.reply_to(message,
                 f"Nice game! Your new elo is {s.find_player(player1_handle)['rank']}! {player2_handle}'s elo is now {s.find_player(player2_handle)['rank']}")


@bot.message_handler(commands=['leaderboards'])
def leaderboards(message: Message):
    response_message = [f'#{i}. {x.name} - {x.rank}' for i, x in enumerate(s.get_players(), start=1)]
    bot.reply_to(message, '\n'.join(response_message))


@bot.message_handler(commands=['matches'])
def matches(message: Message):
    try:
        player_handle = parse_name(message)
    except Exception as e:
        bot.reply_to(message, e)
    response_message = []
    for match in s.find_matches_by_player_name(player_handle):
        if player_handle in match.team1:
            response_message.append(
                f'{match.team1} {match.score1} - {match.score2} {match.team2}, {match.time.strftime("%d %b %Y %H:%M")} ({match.delta:+d})')
        else:
            response_message.append(
                f'{match.team2} {match.score2} - {match.score1} {match.team1}, {match.time.strftime("%d %b %Y %H:%M")} ({-match.delta:+d})')
    bot.reply_to(message, '\n'.join(response_message))


@bot.message_handler(commands=['stats'])
def stats(message: Message):
    try:
        player_handle = parse_name(message)
    except Exception as e:
        bot.reply_to(message, e)
    stats = s.get_stats(player_handle)
    if stats.total == 0:
        bot.reply_to(message, f'Player {stats.name} has not played any matches yet. Go play some beerpong!')
        return
    bot.reply_to(message,
                 f'Player\' {stats.name} current rank is {stats.rank}. He has played a total of {stats.total} matches\n'
                 f'{stats.wins} of them were wins, {stats.draws} of them where draws and {stats.loses} of them were '
                 f'loses ({stats.wins * 100 / stats.total:.2f}% winrate)\n '
                 f'There were total of {stats.scored + stats.conceded} cup hits in those games, {stats.scored} by {stats.name} and his teammates and {stats.conceded} by his opponents.\n '
                 f'If you drunk three sips of beer after each conceded throw, you woulde\'ve approximately consumed {stats.conceded * SIP_VOLUME:.1f} liters of beer! '
                 )


if __name__ == '__main__':
    bot.infinity_polling()

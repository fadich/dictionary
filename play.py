import sys
import time
import game


MESSAGE_INVALID_NUMBER = """! Sorry, this value is not valid. Please, type unsigned integer number."""
MESSAGE_INVALID_NAME = """! Sorry, this is not valid name."""
MESSAGE_NAME_EXISTS = """! Sorry, this name is already taken."""

MESSAGE_GAME_START = """The game has been started!"""
MESSAGE_GAME_TURN_SUCCESS = """Great! Next turn!"""
MESSAGE_GAME_TURN_FAULT = """Sorry, try again..."""

print """
// The game greeting
"""


def clear():
    print '\n' * 20


players = list()

while 1:
    number = raw_input('Insert the number of players: ')
    try:
        number = int(number)
        if number < 1:
            raise ValueError
    except ValueError:
        print MESSAGE_INVALID_NUMBER
        continue
    break

for i in range(number):
    while 1:
        name = raw_input('Please, tell me nickname of player #%d: ' % (i + 1,))
        if len(name) == 0:
            print MESSAGE_INVALID_NAME
            continue
        if players.count(name):
            print MESSAGE_NAME_EXISTS
            continue

        players.append(name)
        break

presenter = game.Presenter(set(players))

print MESSAGE_GAME_START + '\n'

while 1:
    print
    cp = presenter.get_current_player()
    word = raw_input(
        '%s\'s (%.2f) turn, your option is: ' % (
            cp.get('name'),
            round(cp.get('score'), 2)
        )
     )

    if len(word) and presenter.turn(word):
        print MESSAGE_GAME_TURN_SUCCESS
    else:
        print MESSAGE_GAME_TURN_FAULT

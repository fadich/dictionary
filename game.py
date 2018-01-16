import sys
import time
import Presenter


MESSAGE_INVALID_NUMBER = """! Sorry, this number is not valid. Please, try again"""
MESSAGE_INVALID_NAME = """! Sorry, this name is not valid. Please, try again"""

print """
// The game greeting
"""

players = list

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

            # TODO: check for unique...

        break

while 1:
    print '\r%f' % time.time(),
    time.sleep(1)

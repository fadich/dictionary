import repository
import sys
import time


reload(sys)
sys.setdefaultencoding('utf-8')

# if __name__ == '__main__':
#     arg = ''
#     try:
#         arg = sys.argv[1]
#     except IndexError as err:
#         print('{}'.format(err))
#         print('Please, set the query argument')
#         exit()
#
#     words = repository.search(arg, order='ASC')
#
#     index = len(words)
#     for word in words:
#         print "%s - %s\t\t%s" % (index, word.get('Word'), word.get('Score'))
#         index -= 1
#
#     exit()

debug = False

while 1:
    query = raw_input('Query: ')

    if query == "\q":
        break
    if query == "\d":
        debug = True
        print("Debug enabled")
        continue

    if debug:
        started = time.time()

    words = repository.search(query.decode('utf-8'), order='ASC')

    index = len(words)

    if not index:
        print("< No results... >")

    for word in words:
        print "%s - %s\t\t%s" % (index, word.get('Word'), word.get('Score'))
        index -= 1

    if debug:
        ended = time.time()
        print "Request time: %ss" % (ended - started)

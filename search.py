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
fully = False

while 1:
    query = raw_input('Query: ')

    if query == "\q":
        break
    if query == "\d":
        debug = not debug
        print("Debug enabled" if debug else "Debug disabled")
        continue
    if query == "\\f":
        fully = not fully
        print("Results will be displayed fully" if fully else "Only best results will be displayed")
        continue

    if debug:
        started = time.time()

    words = repository.search(query.decode('utf-8'), order='ASC')

    index = len(words) if (words and len(words)) else 0

    if not index:
        print("< No results... >")
    else:
        maxScore = words[-1].get('Score')
        dScore = maxScore / 100 * 60    # display only best 40%

        for word in words:
            if word.get('Score') < dScore and not fully:
                continue

            print "%s - %s" % (word.get('Score'), word.get('Word'))

    if debug:
        ended = time.time()
        print "Request time: %ss" % (ended - started)

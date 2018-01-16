import repository
import sys
import time


reload(sys)
sys.setdefaultencoding('utf-8')

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

    words = repository.search(query.decode('utf-8'))
    # ended = time.time()

    index = len(words) if (words and len(words)) else 0

    if not index:
        print("< No results... >")
    else:
        maxScore = words[-1].get('_score')
        dScore = maxScore / 100 * 40    # display only best 20%

        for word in words:
            if word.get('_score') < dScore and not fully:
                continue

            print "%s - %s" % (word.get('_score'), word.get('word'))

    if debug:
        ended = time.time()
        print "Request time: %ss" % (ended - started)

import repository
import sys


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

while 1:
    arg = raw_input('Query: ')

    if arg == "\q":
        exit()

    words = repository.search(arg, order='ASC')

    index = len(words)

    if not index:
        print("< No results... >")

    for word in words:
        print "%s - %s\t\t%s" % (index, word.get('Word'), word.get('Score'))
        index -= 1
